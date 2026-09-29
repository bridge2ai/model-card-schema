#!/usr/bin/env python3
"""
Model Card Completeness Validator

Quality gate used by the @mcassistant GitHub Action workflow. Decides whether
a generated Model Card has enough substance to open a PR. Distinct from LinkML
schema validation (which only checks structure / types).

Quality levels (tunable via `--block-threshold`):
    comprehensive: 8+ sections, 80+ slots, 200+ lines → PASS
    acceptable:    5+ sections, 50+ slots, 150+ lines → PASS
    minimal:       3+ sections, 25+ slots,  80+ lines → PASS (warn)
    insufficient:  below minimal                      → FAIL

Usage:
    python src/github/validate_mc_completeness.py <model_card.yaml>
    python src/github/validate_mc_completeness.py <file.yaml> --block-threshold acceptable

Exit codes:
    0 — quality >= block threshold (proceed with PR)
    1 — below threshold (block PR)
    2 — validation error (bad YAML, missing required fields, etc.)
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# Top-level sections we count for "section coverage".
# Mirrors the modelCard root slots in model_card_schema.yaml.
COUNTABLE_SECTIONS = [
    "model_details",
    "model_parameters",
    "quantitative_analysis",
    "considerations",
    "model_category",
    "bias_model",
    "bias_output",
    "framework",
    "library_name",
    "pipeline_tag",
    "base_model",
    "tags",
    "datasets",
    "model_index",
    "mission_relevance",
    "usage_documentation",
]

REQUIRED_FIELDS = [
    ("model_details", "name"),
]

QUALITY_THRESHOLDS = {
    "comprehensive": {"sections": 8, "slots": 80, "lines": 200},
    "acceptable":    {"sections": 5, "slots": 50, "lines": 150},
    "minimal":       {"sections": 3, "slots": 25, "lines": 80},
}

QUALITY_ORDER = ["insufficient", "minimal", "acceptable", "comprehensive"]


@dataclass
class CompletenessReport:
    file: Path
    quality: str  # one of QUALITY_ORDER
    sections_populated: list[str]
    slots_populated: int
    non_empty_lines: int
    missing_required: list[str]

    @property
    def n_sections(self) -> int:
        return len(self.sections_populated)

    def passes(self, block_threshold: str) -> bool:
        if self.missing_required:
            return False
        return QUALITY_ORDER.index(self.quality) >= QUALITY_ORDER.index(block_threshold)


def has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return False
    return True


def count_populated_slots(node: Any) -> int:
    """Count non-empty leaf slots in the YAML tree (deep)."""
    if isinstance(node, dict):
        total = 0
        for k, v in node.items():
            if has_content(v):
                if isinstance(v, (dict, list)):
                    total += count_populated_slots(v)
                else:
                    total += 1
        return total
    if isinstance(node, list):
        total = 0
        for item in node:
            if isinstance(item, (dict, list)):
                total += count_populated_slots(item)
            elif has_content(item):
                total += 1
        return total
    return 1 if has_content(node) else 0


def assess(file: Path) -> CompletenessReport:
    raw = file.read_text()
    non_empty_lines = sum(
        1 for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")
    )

    try:
        data = yaml.safe_load(raw)
    except Exception as e:
        raise SystemExit(f"Failed to parse YAML: {e}") from e

    if not isinstance(data, dict):
        raise SystemExit("Top-level YAML must be a mapping (modelCard root)")

    sections = [s for s in COUNTABLE_SECTIONS if has_content(data.get(s))]
    slots = count_populated_slots(data)

    missing = []
    for parent, child in REQUIRED_FIELDS:
        v = data.get(parent)
        if not isinstance(v, dict) or not has_content(v.get(child)):
            missing.append(f"{parent}.{child}")

    quality = "insufficient"
    for level in ("comprehensive", "acceptable", "minimal"):
        t = QUALITY_THRESHOLDS[level]
        if len(sections) >= t["sections"] and slots >= t["slots"] and non_empty_lines >= t["lines"]:
            quality = level
            break

    return CompletenessReport(
        file=file,
        quality=quality,
        sections_populated=sections,
        slots_populated=slots,
        non_empty_lines=non_empty_lines,
        missing_required=missing,
    )


def render(report: CompletenessReport, block_threshold: str) -> str:
    lines = [
        "🌟 Model Card Completeness Report",
        "=" * 60,
        "",
        f"File: {report.file}",
        f"Quality Level: {report.quality.upper()}",
        "",
        "📊 Metrics:",
        f"   Sections: {report.n_sections}/{len(COUNTABLE_SECTIONS)} populated",
        f"   Slots: {report.slots_populated} populated",
        f"   Lines: {report.non_empty_lines} non-empty",
        "",
        f"🎯 Thresholds (Block threshold: {block_threshold}):",
    ]
    for level in ("comprehensive", "acceptable", "minimal"):
        t = QUALITY_THRESHOLDS[level]
        arrow = " → " if level == block_threshold else "   "
        lines.append(
            f"  {arrow}{level.capitalize()}: {t['sections']} sections, "
            f"{t['slots']} slots, {t['lines']} lines"
        )

    lines += ["", "📋 Populated Sections:"]
    for s in report.sections_populated:
        lines.append(f"   ✓ {s}")

    if report.missing_required:
        lines += ["", "❌ Missing required fields:"]
        for f in report.missing_required:
            lines.append(f"   ✗ {f}")

    passing = report.passes(block_threshold)
    lines += [
        "",
        ("✅ QUALITY CHECK PASSED" if passing else "❌ QUALITY CHECK FAILED"),
    ]
    if passing:
        lines.append(
            f"   Quality level '{report.quality}' meets threshold '{block_threshold}'"
        )
        lines.append("   PR creation is allowed.")
    else:
        if report.missing_required:
            lines.append("   Required fields missing — PR creation BLOCKED.")
        else:
            lines.append(
                f"   Quality level '{report.quality}' < threshold '{block_threshold}' — PR creation BLOCKED."
            )

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", type=Path, help="Model Card YAML file")
    p.add_argument(
        "--block-threshold",
        choices=("comprehensive", "acceptable", "minimal"),
        default="minimal",
        help="Quality level required to PASS (exit 0)",
    )
    args = p.parse_args(argv)

    if not args.file.exists():
        print(f"File not found: {args.file}", file=sys.stderr)
        return 2

    report = assess(args.file)
    print(render(report, args.block_threshold))
    return 0 if report.passes(args.block_threshold) else 1


if __name__ == "__main__":
    raise SystemExit(main())
