#!/usr/bin/env python3
"""
Hybrid Model Card Rubric10 Batch Evaluator

Uses YAML parsing + quality heuristics (no LLM calls) to score Model Card YAML files
against the 10-element rubric defined in `.claude/agents/mc-rubric10.md`. Faster and
cheaper than LLM-based evaluation; complements but does not replace the LLM rubric
agents (which assess semantic quality).

Usage:
    poetry run python scripts/batch_evaluate_mc_rubric10_hybrid.py \\
        --input-glob 'src/data/examples/extended/*.yaml' \\
        --output-dir data/evaluation/rubric10

    # Or single file
    poetry run python scripts/batch_evaluate_mc_rubric10_hybrid.py \\
        --input src/data/examples/extended/climate-model-extended.yaml \\
        --output-dir data/evaluation/rubric10

Output:
    - {output-dir}/<basename>_evaluation.json (one per input)
    - {output-dir}/all_scores.csv  (summary across the batch)
    - {output-dir}/summary_report.md
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Rubric10 element specification (mirrors .claude/agents/mc-rubric10.md)
# ---------------------------------------------------------------------------
RUBRIC10_ELEMENTS: dict[int, dict[str, Any]] = {
    1: {
        "name": "Model Discovery and Identification",
        "description": "Can a user or system discover and uniquely identify this model?",
        "sub_elements": [
            {"name": "Persistent Identifier",
             "fields": ["model_details.references", "model_details.path", "base_model"]},
            {"name": "Model Name and Description Completeness",
             "fields": ["model_details.name", "model_details.short_description",
                        "model_details.overview"]},
            {"name": "Tags / Pipeline Tag for Searchability",
             "fields": ["tags", "pipeline_tag", "model_category"]},
            {"name": "Landing Page or Repository URL",
             "fields": ["model_details.references", "model_details.documentation"]},
            {"name": "Library / Framework Identification",
             "fields": ["library_name", "framework", "framework_version"]},
        ],
    },
    2: {
        "name": "Model Access and Distribution",
        "description": "Can model weights, code, and inference pipeline be located and used?",
        "sub_elements": [
            {"name": "Weight Distribution Mechanism Defined",
             "fields": ["model_details.references", "model_details.path"]},
            {"name": "Code Repository Available",
             "fields": ["model_details.references", "usage_documentation.code_examples"]},
            {"name": "Inference / Usage Example Provided",
             "fields": ["usage_documentation.code_examples",
                        "model_parameters.input_format",
                        "model_parameters.output_format"]},
            {"name": "Input / Output Specification",
             "fields": ["model_parameters.input_format",
                        "model_parameters.output_format",
                        "model_parameters.input_format_map",
                        "model_parameters.output_format_map"]},
            {"name": "Model File Format Specified",
             "fields": ["model_details.path", "library_name"]},
        ],
    },
    3: {
        "name": "Model Reuse and Interoperability",
        "description": "Is sufficient information provided to reuse and integrate this model?",
        "sub_elements": [
            {"name": "License Terms Allow Reuse",
             "fields": ["model_details.licenses", "model_details.licenses.identifier"]},
            {"name": "Standard Framework / Format Used",
             "fields": ["framework", "framework_version", "library_name"]},
            {"name": "Base Model or Foundation Lineage Stated",
             "fields": ["base_model", "model_details.references"]},
            {"name": "Supported Tasks Declared",
             "fields": ["pipeline_tag", "model_index", "considerations.use_cases"]},
            {"name": "Reproducibility Artifacts Provided",
             "fields": ["model_parameters.training_procedure",
                        "mission_relevance",
                        "usage_documentation"]},
        ],
    },
    4: {
        "name": "Ethical Use and Responsible AI",
        "description": "Does the card document risks, bias, and ethical oversight?",
        "sub_elements": [
            {"name": "Ethical Considerations Documented",
             "fields": ["considerations.ethical_considerations"]},
            {"name": "Known Model / Output Bias Disclosed",
             "fields": ["bias_model", "bias_output", "bias_input"]},
            {"name": "Out-of-Scope / Discouraged Uses",
             "fields": ["considerations.out_of_scope_uses", "considerations.limitations"]},
            {"name": "Sensitive Data Use Disclosed",
             "fields": ["model_parameters.data"]},  # special heuristic checks .sensitive
            {"name": "Intended Users and Stakeholder Tradeoffs",
             "fields": ["considerations.users", "considerations.tradeoffs"]},
        ],
    },
    5: {
        "name": "Model Architecture and Training Composition",
        "description": "Can the architecture and training composition be understood?",
        "sub_elements": [
            {"name": "Architecture Described in Detail",
             "fields": ["model_parameters.model_architecture"]},
            {"name": "Training Data Documented",
             "fields": ["model_parameters.data",
                        "model_parameters.training_datasets",  # harmonized
                        "model_parameters.evaluation_datasets"]},
            {"name": "Hyperparameters Reported",
             "fields": ["model_parameters.training_procedure"]},
            {"name": "Compute Infrastructure Reported (Extended)",
             "fields": ["model_parameters.compute_infrastructure"]},
            {"name": "Training / Evaluation Split Defined",
             "fields": ["model_parameters.data",
                        "model_parameters.training_datasets",  # harmonized
                        "model_parameters.evaluation_datasets",  # harmonized
                        "model_index"]},
        ],
    },
    6: {
        "name": "Model Provenance and Versioning",
        "description": "Can a user determine versions, owners, citations?",
        "sub_elements": [
            {"name": "Version Number Provided",
             "fields": ["model_details.version.name", "model_details.version"]},
            {"name": "Version Date Documented",
             "fields": ["model_details.version.date"]},
            {"name": "Change Description for This Version",
             "fields": ["model_details.version.diff"]},
            {"name": "Owners / Contributors Identified",
             "fields": ["model_details.owners",
                        "model_details.contributors",
                        "model_details.creator_references"]},  # harmonized
            {"name": "Citation Provided",
             "fields": ["model_details.citations"]},
        ],
    },
    7: {
        "name": "Scientific Motivation and Funding Transparency",
        "description": "Does the metadata state why the model exists and who funded it?",
        "sub_elements": [
            {"name": "Motivation / Use Case Rationale",
             "fields": ["model_details.overview", "considerations.use_cases"]},
            {"name": "Primary Intended Use Articulated",
             "fields": ["considerations.use_cases", "pipeline_tag"]},
            {"name": "Mission Relevance Stated (Extended)",
             "fields": ["mission_relevance"]},
            {"name": "Funding Source / Grant Agency Listed",
             "fields": ["model_details.contributors",
                        "mission_relevance",
                        "funding_grants"]},  # harmonized
            {"name": "Compute / Platform Acknowledgement",
             "fields": ["model_parameters.compute_infrastructure", "model_details.overview"]},
        ],
    },
    8: {
        "name": "Training and Evaluation Transparency",
        "description": "Can training and evaluation procedures be replicated or understood?",
        "sub_elements": [
            {"name": "Training Procedure Documented",
             "fields": ["model_parameters.training_procedure"]},
            {"name": "Evaluation Procedure Documented",
             "fields": ["model_parameters.training_procedure",
                        "quantitative_analysis"]},
            {"name": "Reproducibility Information (Extended)",
             "fields": ["mission_relevance", "usage_documentation"]},
            {"name": "Open-Source Code Linked",
             "fields": ["model_details.references", "usage_documentation.code_examples"]},
            {"name": "External Standards or References Cited",
             "fields": ["model_details.references", "model_details.citations"]},
        ],
    },
    9: {
        "name": "Performance Evaluation and Limitations Disclosure",
        "description": "Does the metadata communicate performance and limitations?",
        "sub_elements": [
            {"name": "Quantitative Performance Metrics Reported",
             "fields": ["quantitative_analysis.performance_metrics"]},
            {"name": "Performance Across Slices / Subpopulations",
             "fields": ["quantitative_analysis.performance_metrics"]},  # heuristic checks slice
            {"name": "Confidence Intervals or Error Bars",
             "fields": ["quantitative_analysis.performance_metrics"]},  # heuristic checks CI
            {"name": "Limitations Section Present",
             "fields": ["considerations.limitations"]},
            {"name": "Tradeoffs / Risks Acknowledged",
             "fields": ["considerations.tradeoffs", "considerations.ethical_considerations"]},
        ],
    },
    10: {
        "name": "Cross-Platform and Community Integration",
        "description": "Does the card connect to wider model ecosystems and standards?",
        "sub_elements": [
            {"name": "Published on a Recognized Platform",
             "fields": ["model_details.references", "library_name", "model_details.path"]},
            {"name": "Cross-referenced DOIs or Related Model Links",
             "fields": ["model_details.references", "base_model"]},
            {"name": "Benchmark Results (Papers with Code)",
             "fields": ["model_index"]},
            {"name": "Standards / Schema Conformance Stated",
             "fields": ["schema_version", "model_category"]},
            {"name": "Datasets Linked",
             "fields": ["model_parameters.data", "datasets", "model_index"]},
        ],
    },
}

MAX_POINTS = 50  # 10 elements x 5 sub-elements

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def get_nested(data: Any, path: str) -> Any:
    """Resolve dot-paths through dicts. Lists short-circuit to the list itself
    (heuristics handle list element inspection separately)."""
    if data is None:
        return None
    cur = data
    for key in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(key)
        else:
            return None
        if cur is None:
            return None
    return cur


def has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return False
    return True


def short_evidence(field: str, value: Any) -> str:
    if isinstance(value, str):
        s = value.strip()
        return f"{field}: {s[:120]}…" if len(s) > 120 else f"{field}: {s}"
    if isinstance(value, list):
        return f"{field}: list({len(value)})"
    if isinstance(value, dict):
        return f"{field}: dict(keys={list(value.keys())[:5]})"
    return f"{field}: {value}"


def first_present(data: Any, fields: list[str]) -> tuple[bool, str]:
    for f in fields:
        v = get_nested(data, f)
        if has_content(v):
            return True, short_evidence(f, v)
    return False, f"Missing all of: {', '.join(fields)}"


# ---------------------------------------------------------------------------
# Quality heuristics (per element + sub-element index)
# ---------------------------------------------------------------------------
SPDX_LICENSES = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "GPL-2.0", "GPL-3.0",
    "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0",
    "CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "OpenRAIL", "OpenRAIL-M", "LLAMA2", "Gemma",
    "Unlicense", "ISC", "AGPL-3.0",
}

HF_HUB_RE = re.compile(r"^https?://(?:hf\.co|huggingface\.co)/[^/]+/[^/]+")
DOI_RE = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)?10\.\d{4,9}/[^\s]+", re.IGNORECASE)
SEMVER_RE = re.compile(r"^v?\d+\.\d+(?:\.\d+)?(?:[-+][\w.]+)?$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _string_of(value: Any) -> str:
    """Best-effort flatten to a string for regex matching."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for v in value:
            if isinstance(v, dict):
                parts.extend(str(x) for x in v.values() if isinstance(x, (str, int, float)))
            else:
                parts.append(str(v))
        return " ".join(parts)
    if isinstance(value, dict):
        return " ".join(str(x) for x in value.values() if isinstance(x, (str, int, float)))
    return str(value) if value is not None else ""


def heuristic_score(data: dict, element_id: int, sub_idx: int) -> tuple[int, str]:
    spec = RUBRIC10_ELEMENTS[element_id]["sub_elements"][sub_idx]
    present, evidence = first_present(data, spec["fields"])
    if not present:
        return 0, evidence

    # Element 1
    if element_id == 1:
        if sub_idx == 0:  # Persistent ID — look for DOI or HF Hub URL
            refs = get_nested(data, "model_details.references") or []
            ref_strings = [_string_of(r) for r in refs] if isinstance(refs, list) else [_string_of(refs)]
            path = _string_of(get_nested(data, "model_details.path"))
            base = _string_of(data.get("base_model"))
            combined = " ".join(ref_strings + [path, base])
            if DOI_RE.search(combined) or HF_HUB_RE.search(combined):
                return 1, f"Resolvable identifier present ({evidence})"
            return 1, f"Identifier-like field present but unverified: {evidence}"
        if sub_idx == 1:  # Name + description completeness
            name = _string_of(get_nested(data, "model_details.name"))
            short = _string_of(get_nested(data, "model_details.short_description"))
            overview = _string_of(get_nested(data, "model_details.overview"))
            doc = _string_of(get_nested(data, "model_details.documentation"))
            if name and (len(overview) >= 200 or len(doc) >= 200):
                return 1, f"Name + comprehensive overview ({len(overview)} chars)"
            if name and (short or overview):
                return 1, f"Name + brief description (overview={len(overview)} chars)"
            return 0, "Name present but no meaningful description"
        if sub_idx == 2:  # Tags / pipeline_tag
            tags = data.get("tags") or []
            pipe = data.get("pipeline_tag")
            cat = data.get("model_category")
            n_tags = len(tags) if isinstance(tags, list) else (1 if tags else 0)
            if (pipe or cat) and n_tags >= 3:
                return 1, f"{n_tags} tags + pipeline_tag/category"
            if pipe or cat or n_tags > 0:
                return 1, f"Some tags ({n_tags}) or pipeline tag present"
        if sub_idx == 4:  # framework + version
            fw = data.get("framework")
            fwv = data.get("framework_version")
            lib = data.get("library_name")
            if fw and fwv:
                return 1, f"Framework {fw} pinned to version {fwv}"
            if fw or lib:
                return 1, f"Framework/library declared but version not pinned"

    # Element 3 — license (sub 0) SPDX check
    if element_id == 3 and sub_idx == 0:
        licenses = get_nested(data, "model_details.licenses") or []
        if isinstance(licenses, list):
            ids = []
            for lic in licenses:
                if isinstance(lic, dict):
                    ids.append(lic.get("identifier") or "")
                else:
                    ids.append(str(lic))
            if any(i in SPDX_LICENSES for i in ids):
                return 1, f"SPDX license identified: {[i for i in ids if i in SPDX_LICENSES]}"
            if any(ids):
                return 1, f"License present but non-SPDX: {ids}"

    # Element 4 — sensitive data sub-element
    if element_id == 4 and sub_idx == 3:
        datasets = get_nested(data, "model_parameters.data") or []
        if isinstance(datasets, list):
            for ds in datasets:
                if isinstance(ds, dict):
                    s = ds.get("sensitive") or {}
                    if isinstance(s, dict) and (
                        s.get("sensitive_data_used") is not None
                        or has_content(s.get("sensitive_data"))
                    ):
                        return 1, "Sensitive-data disclosure present on at least one dataset"
            return 0, "No sensitive-data disclosure on any dataset"

    # Element 5 — training data, training/eval split
    if element_id == 5:
        if sub_idx == 1:  # training data documented
            datasets = get_nested(data, "model_parameters.data") or []
            train_ds = get_nested(data, "model_parameters.training_datasets") or []  # harmonized
            eval_ds = get_nested(data, "model_parameters.evaluation_datasets") or []  # harmonized
            all_datasets = list(datasets) + list(train_ds) + list(eval_ds)
            if all_datasets:
                with_links = sum(
                    1 for d in all_datasets
                    if isinstance(d, dict) and (d.get("link") or d.get("url"))
                )
                if with_links >= 1:
                    return 1, f"{len(all_datasets)} dataset(s), {with_links} with links/URIs"
                return 1, f"{len(all_datasets)} dataset(s) declared"
        if sub_idx == 4:  # train/eval split
            datasets = get_nested(data, "model_parameters.data") or []
            train_ds = get_nested(data, "model_parameters.training_datasets") or []
            eval_ds = get_nested(data, "model_parameters.evaluation_datasets") or []
            mi = data.get("model_index") or []
            harmonized_split = bool(train_ds) and bool(eval_ds)
            if harmonized_split:
                return 1, "Distinct training_datasets and evaluation_datasets declared"
            if (isinstance(datasets, list) and len(datasets) >= 2) or has_content(mi):
                return 1, "Multiple dataset entries or model_index present"
            return 0, "Single or no dataset; no benchmark split"

    # Element 6 — version, date, owners
    if element_id == 6:
        if sub_idx == 0:
            v = _string_of(get_nested(data, "model_details.version.name"))
            if v and SEMVER_RE.match(v):
                return 1, f"Semver-shaped version: {v}"
            if v:
                return 1, f"Version present but non-semver: {v}"
        if sub_idx == 1:
            d = _string_of(get_nested(data, "model_details.version.date"))
            if d and ISO_DATE_RE.match(d):
                return 1, f"ISO date: {d}"
            if d:
                return 1, f"Date present but non-ISO: {d}"
        if sub_idx == 3:  # owners/contributors with roles
            owners = get_nested(data, "model_details.owners") or []
            contribs = get_nested(data, "model_details.contributors") or []
            roled = [c for c in contribs if isinstance(c, dict) and c.get("role")]
            if roled:
                return 1, f"{len(roled)} contributor(s) with role"
            if owners or contribs:
                return 1, f"{len(owners) + len(contribs)} owner/contributor(s) (roles missing)"

    # Element 7 — funding heuristic
    if element_id == 7 and sub_idx == 3:
        contribs = get_nested(data, "model_details.contributors") or []
        affils = [c.get("affiliation", "") for c in contribs if isinstance(c, dict)]
        mission = _string_of(data.get("mission_relevance"))
        combined = " ".join(affils + [mission])
        if re.search(r"\b(NIH|NSF|DOE|DARPA|NASA|EU|European Commission|Horizon)\b", combined, re.I):
            return 1, "Funding agency mentioned in affiliations or mission_relevance"
        if affils:
            return 1, "Affiliations present (funding agency unclear)"

    # Element 9 — metrics, slices, CI, limitations
    if element_id == 9:
        metrics = get_nested(data, "quantitative_analysis.performance_metrics") or []
        if sub_idx == 0:
            num_with_value = sum(
                1 for m in metrics
                if isinstance(m, dict) and m.get("value") not in (None, "")
            )
            if num_with_value >= 1:
                return 1, f"{num_with_value} metric(s) with numeric value"
            return 0, "Metrics declared but no numeric values"
        if sub_idx == 1:  # slice coverage
            slices = {m.get("slice") for m in metrics if isinstance(m, dict) and m.get("slice")}
            if len(slices) >= 2:
                return 1, f"{len(slices)} distinct slice(s) reported"
            if slices:
                return 1, f"Single slice reported: {slices}"
            return 0, "No slice/factor breakdown"
        if sub_idx == 2:  # CI
            ci_present = any(
                isinstance(m, dict) and (m.get("confidence_interval") or m.get("value_error"))
                for m in metrics
            )
            if ci_present:
                return 1, "Confidence interval or value_error present"
            return 0, "No confidence intervals or error bars"

    # Element 10 — benchmarks + datasets
    if element_id == 10:
        if sub_idx == 2:
            mi = data.get("model_index") or []
            results = []
            if isinstance(mi, list):
                for entry in mi:
                    if isinstance(entry, dict):
                        results.extend(entry.get("results") or [])
            if results:
                return 1, f"{len(results)} benchmark result(s)"
            return 0, "No model_index benchmark results"
        if sub_idx == 4:
            datasets = get_nested(data, "model_parameters.data") or []
            named_with_links = sum(
                1 for d in datasets
                if isinstance(d, dict) and d.get("name") and d.get("link")
            )
            if named_with_links >= 1:
                return 1, f"{named_with_links} dataset(s) with name+link"
            top_ds = data.get("datasets")
            if has_content(top_ds):
                return 1, "Top-level datasets field populated"

    # Default: presence + non-trivial content = 1
    return 1, evidence


# ---------------------------------------------------------------------------
# Core eval
# ---------------------------------------------------------------------------
def evaluate_one(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as e:
        return {"error": f"Failed to load YAML: {e}", "model_card_file": str(path)}

    if not isinstance(data, dict):
        return {"error": "Top-level YAML is not a mapping", "model_card_file": str(path)}

    result: dict[str, Any] = {
        "rubric": "mc_rubric10",
        "version": "1.0",
        "model_card_file": str(path),
        "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
        "evaluator": {
            "name": "hybrid-heuristic-evaluator",
            "temperature": "N/A",
            "evaluation_type": "rule_based_with_quality_heuristics",
        },
        "elements": [],
        "overall_score": {},
        "assessment": {"strengths": [], "weaknesses": [], "recommendations": []},
        "metadata": {
            "evaluator_id": "batch-hybrid-evaluator",
            "model_card_hash": hashlib.sha256(path.read_bytes()).hexdigest(),
        },
    }

    total = 0
    for eid, spec in RUBRIC10_ELEMENTS.items():
        elem = {
            "id": eid,
            "name": spec["name"],
            "description": spec["description"],
            "sub_elements": [],
            "element_score": 0,
            "element_max": 5,
        }
        for idx, se in enumerate(spec["sub_elements"]):
            score, note = heuristic_score(data, eid, idx)
            elem["sub_elements"].append({
                "name": se["name"],
                "score": score,
                "evidence": note,
                "quality_note": note,
            })
            elem["element_score"] += score
        total += elem["element_score"]
        result["elements"].append(elem)

    result["overall_score"] = {
        "total_points": total,
        "max_points": MAX_POINTS,
        "percentage": round(total / MAX_POINTS * 100, 1),
    }

    for elem in result["elements"]:
        if elem["element_score"] >= 4:
            result["assessment"]["strengths"].append(
                f"Strong {elem['name']} ({elem['element_score']}/5)"
            )
        elif elem["element_score"] <= 1:
            result["assessment"]["weaknesses"].append(
                f"Weak {elem['name']} ({elem['element_score']}/5)"
            )

    return result


# ---------------------------------------------------------------------------
# Batch + summary
# ---------------------------------------------------------------------------
def write_csv(results: list[dict], out_path: Path) -> None:
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "model_card_file", "total_score", "max_score", "percentage",
            "elements_passing_3_of_5",
        ] + [f"element_{i}_score" for i in range(1, 11)])
        for r in results:
            if "error" in r:
                writer.writerow([r.get("model_card_file"), "ERROR", "", "", "", *[""] * 10])
                continue
            elems = r["elements"]
            passing = sum(1 for e in elems if e["element_score"] >= 3)
            row = [
                r["model_card_file"],
                r["overall_score"]["total_points"],
                r["overall_score"]["max_points"],
                r["overall_score"]["percentage"],
                passing,
            ] + [e["element_score"] for e in elems]
            writer.writerow(row)


def write_markdown(results: list[dict], out_path: Path) -> None:
    lines = [
        "# Model Card Rubric10 Batch Summary",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}  ",
        f"Files evaluated: {len(results)}",
        "",
        "| File | Score | % | Strongest element | Weakest element |",
        "|---|---:|---:|---|---|",
    ]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['model_card_file']} | ERROR | | {r['error']} | |")
            continue
        elems = r["elements"]
        best = max(elems, key=lambda e: e["element_score"])
        worst = min(elems, key=lambda e: e["element_score"])
        lines.append(
            f"| `{r['model_card_file']}` | "
            f"{r['overall_score']['total_points']}/{r['overall_score']['max_points']} | "
            f"{r['overall_score']['percentage']}% | "
            f"{best['name']} ({best['element_score']}/5) | "
            f"{worst['name']} ({worst['element_score']}/5) |"
        )
    out_path.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", type=Path, help="Single Model Card YAML")
    g.add_argument("--input-glob", help="Glob (e.g. 'src/data/examples/extended/*.yaml')")
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args(argv)

    if args.input:
        paths = [args.input]
    else:
        paths = sorted(Path(p) for p in glob.glob(args.input_glob, recursive=True))

    if not paths:
        print(f"No input files matched.", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    for path in paths:
        print(f"Evaluating: {path}")
        r = evaluate_one(path)
        results.append(r)

        out_file = args.output_dir / f"{path.stem}_evaluation.json"
        out_file.write_text(json.dumps(r, indent=2))

        if "error" in r:
            print(f"  ERROR: {r['error']}")
        else:
            s = r["overall_score"]
            print(f"  {s['total_points']}/{s['max_points']} ({s['percentage']}%)")

    write_csv(results, args.output_dir / "all_scores.csv")
    write_markdown(results, args.output_dir / "summary_report.md")
    print(f"\nWrote {len(results)} evaluations to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
