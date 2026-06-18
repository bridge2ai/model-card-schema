#!/usr/bin/env python3
"""Aggregate semantic_findings across portfolio rubric10/20-semantic JSONs.

Scans data/evaluation/**/rubric{10,20}_semantic/*evaluation.json, extracts
format / consistency / plausibility failures plus capped deductions, ranks
findings by how many cards they affect, and writes a markdown report.

The report's job is to surface which semantic findings recur often enough to
be worth encoding as deterministic hybrid rules (see Q18/Q19 already encoded
in scripts/batch_evaluate_mc_rubric20_hybrid.py).

Usage:
    poetry run python scripts/build_rubric_report.py \\
        --root data/evaluation \\
        --output data/evaluation/all/common_issues.md
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Rules already encoded in the hybrid evaluator. Lower-case, stem-style keys —
# we match findings against these via substring on a normalized rule string.
ENCODED_HYBRID_RULES: dict[str, str] = {
    "bias_tradeoff_gap": (
        "bias disclosure tradeoffs"  # matches both r10 and r20 wordings
    ),
    "train_eval_leakage": (
        "benchmark dataset training data"
    ),
}


def normalize(s: str) -> str:
    """Lowercase, collapse runs of non-word chars to single spaces, strip."""
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


@dataclass
class Finding:
    category: str           # "format" | "consistency" | "plausibility"
    rubric: str             # "rubric10" | "rubric20"
    rule_or_field: str      # rule (consistency/plausibility) or field (format)
    issue: str
    questions_impacted: list[str] = field(default_factory=list)
    card: str = ""
    source_file: str = ""


@dataclass
class Deduction:
    rubric: str
    question: str
    raw_score: int
    capped_score: int
    reason: str
    card: str
    source_file: str


def card_name_from(path: Path) -> str:
    stem = path.stem
    # Drop suffixes like '_llm_evaluation', '_llm_rubric20_evaluation'
    for suf in ("_llm_rubric20_evaluation", "_llm_evaluation", "_rubric20_evaluation", "_evaluation"):
        if stem.endswith(suf):
            stem = stem[: -len(suf)]
            break
    return stem


def collect_findings(paths: list[Path]) -> tuple[list[Finding], list[Deduction]]:
    findings: list[Finding] = []
    deductions: list[Deduction] = []
    for path in paths:
        try:
            doc = json.loads(path.read_text())
        except Exception as e:
            print(f"  warn: could not parse {path}: {e}", file=sys.stderr)
            continue
        rubric = "rubric20" if "rubric20" in str(path) else "rubric10"
        card = card_name_from(path)
        sf = doc.get("semantic_findings") or {}
        for cat_key, fcat in (
            ("format_failures", "format"),
            ("consistency_failures", "consistency"),
            ("plausibility_failures", "plausibility"),
        ):
            for entry in sf.get(cat_key) or []:
                if not isinstance(entry, dict):
                    continue
                rule_or_field = entry.get("rule") or entry.get("field") or "(unspecified)"
                findings.append(Finding(
                    category=fcat,
                    rubric=rubric,
                    rule_or_field=str(rule_or_field),
                    issue=str(entry.get("issue") or ""),
                    questions_impacted=list(entry.get("questions_impacted") or []),
                    card=card,
                    source_file=str(path),
                ))
        for entry in doc.get("overall_score", {}).get("semantic_deductions") or []:
            if not isinstance(entry, dict):
                continue
            deductions.append(Deduction(
                rubric=rubric,
                question=str(entry.get("question") or ""),
                raw_score=int(entry.get("raw_score") or 0),
                capped_score=int(entry.get("capped_score") or 0),
                reason=str(entry.get("reason") or ""),
                card=card,
                source_file=str(path),
            ))
    return findings, deductions


@dataclass
class Group:
    category: str
    rubric: str
    rule_or_field: str
    examples: list[Finding] = field(default_factory=list)

    @property
    def cards(self) -> set[str]:
        return {f.card for f in self.examples}


def group_findings(findings: list[Finding]) -> list[Group]:
    """Group by (category, rubric, normalized rule_or_field)."""
    buckets: dict[tuple[str, str, str], Group] = {}
    for f in findings:
        key = (f.category, f.rubric, normalize(f.rule_or_field))
        if key not in buckets:
            buckets[key] = Group(
                category=f.category,
                rubric=f.rubric,
                rule_or_field=f.rule_or_field,
            )
        buckets[key].examples.append(f)
    # Sort by cards-affected desc, then total occurrences, then alphabetic
    return sorted(
        buckets.values(),
        key=lambda g: (-len(g.cards), -len(g.examples), g.rule_or_field.lower()),
    )


def hybrid_coverage(group: Group) -> str | None:
    """Return the encoded rule name if this group is already covered, else None."""
    blob = normalize(group.rule_or_field + " " + (group.examples[0].issue if group.examples else ""))
    for rule_name, marker in ENCODED_HYBRID_RULES.items():
        marker_norm = normalize(marker)
        # Check all words of the marker appear in the finding's text
        if all(w in blob for w in marker_norm.split()):
            return rule_name
    return None


def render_markdown(
    groups: list[Group],
    deductions: list[Deduction],
    n_cards: int,
    n_files: int,
) -> str:
    out: list[str] = []
    out.append("# Common Semantic Findings — Portfolio Report")
    out.append("")
    out.append(
        f"Aggregated from {n_files} semantic evaluation file(s) covering "
        f"{n_cards} card(s).  "
        "Ranked by number of distinct cards affected. Findings already encoded "
        "as deterministic hybrid rules are marked with a coverage tag — these "
        "no longer need an LLM to flag them. Uncovered findings near the top "
        "are the next candidates to encode."
    )
    out.append("")
    out.append("## Top findings (ranked by card coverage)")
    out.append("")
    out.append("| # | Cards | Category | Rubric | Rule / Field | Hybrid coverage |")
    out.append("|---|---:|---|---|---|---|")
    for i, g in enumerate(groups, 1):
        cov = hybrid_coverage(g)
        cov_label = f"✅ `{cov}`" if cov else "—"
        out.append(
            f"| {i} | {len(g.cards)} | {g.category} | {g.rubric} | "
            f"{g.rule_or_field} | {cov_label} |"
        )
    out.append("")

    out.append("## Details (top 15)")
    out.append("")
    for i, g in enumerate(groups[:15], 1):
        cov = hybrid_coverage(g)
        out.append(f"### {i}. [{g.category} / {g.rubric}] {g.rule_or_field}")
        out.append("")
        out.append(f"- Cards affected ({len(g.cards)}): " + ", ".join(sorted(g.cards)))
        if cov:
            out.append(f"- Hybrid coverage: ✅ `{cov}`")
        else:
            out.append("- Hybrid coverage: — (candidate to encode)")
        qs = sorted({q for f in g.examples for q in f.questions_impacted})
        if qs:
            out.append(f"- Questions impacted: {', '.join(qs)}")
        out.append(f"- Example issue: {g.examples[0].issue}")
        out.append("")

    if deductions:
        out.append("## Capped deductions surfaced")
        out.append("")
        out.append("| Card | Rubric | Question | Raw → Capped | Reason |")
        out.append("|---|---|---|---|---|")
        for d in sorted(deductions, key=lambda x: (x.card, x.rubric, x.question)):
            reason = d.reason.replace("\n", " ").replace("|", "\\|")
            if len(reason) > 200:
                reason = reason[:200] + "…"
            out.append(
                f"| {d.card} | {d.rubric} | {d.question} | "
                f"{d.raw_score} → {d.capped_score} | {reason} |"
            )
        out.append("")

    out.append("## Encoded hybrid rules")
    out.append("")
    out.append("These rules already fire in `scripts/batch_evaluate_mc_rubric20_hybrid.py`:")
    out.append("")
    for name, marker in ENCODED_HYBRID_RULES.items():
        out.append(f"- `{name}` — matches findings containing: _{marker}_")
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--root",
        type=Path,
        default=Path("data/evaluation"),
        help="Root directory to scan for semantic evaluation JSONs (default: data/evaluation)",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path("data/evaluation/all/common_issues.md"),
        help="Output markdown path (default: data/evaluation/all/common_issues.md)",
    )
    args = p.parse_args(argv)

    pattern = str(args.root / "**" / "rubric*_semantic" / "*evaluation.json")
    paths = sorted(Path(p) for p in glob.glob(pattern, recursive=True))
    if not paths:
        print(f"No semantic evaluation JSONs found under {args.root}", file=sys.stderr)
        return 1

    findings, deductions = collect_findings(paths)
    groups = group_findings(findings)
    n_cards = len({f.card for f in findings} | {d.card for d in deductions})

    md = render_markdown(groups, deductions, n_cards=n_cards, n_files=len(paths))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md)
    print(
        f"Wrote {args.output} — {len(groups)} grouped finding(s), "
        f"{len(deductions)} capped deduction(s), across {n_cards} card(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
