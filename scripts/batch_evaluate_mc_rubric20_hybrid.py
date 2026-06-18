#!/usr/bin/env python3
"""
Hybrid Model Card Rubric20 Batch Evaluator

20-question / 84-point hybrid evaluator. Uses YAML parsing + quality heuristics
(no LLM calls) to score Model Card YAML files against the rubric defined in
`.claude/agents/mc-rubric20.md`. Sibling to `batch_evaluate_mc_rubric10_hybrid.py`.

Categories:
    1. Structural Completeness     (Q1–Q5, max 21)
    2. Metadata Quality & Content  (Q6–Q10, max 21)
    3. Technical Documentation     (Q11–Q15, max 25)
    4. Performance & FAIRness      (Q16–Q20, max 17)

Question scoring is a mix of pass/fail (0/1) and numeric (0-5) as specified in
the rubric.

Usage:
    poetry run python scripts/batch_evaluate_mc_rubric20_hybrid.py \\
        --input-glob 'src/data/examples/extended/*.yaml' \\
        --output-dir data/evaluation/rubric20
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
# Helpers
# ---------------------------------------------------------------------------
SPDX_LICENSES = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "GPL-2.0", "GPL-3.0",
    "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0",
    "CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "OpenRAIL", "OpenRAIL-M", "LLAMA2", "Gemma",
    "Unlicense", "ISC", "AGPL-3.0",
}
DOI_RE = re.compile(r"(?:https?://(?:dx\.)?doi\.org/|doi:)?10\.\d{4,9}/\S+", re.IGNORECASE)
HF_HUB_RE = re.compile(r"https?://(?:hf\.co|huggingface\.co)/[^/\s]+/[^/\s]+")
SEMVER_RE = re.compile(r"^v?\d+\.\d+(?:\.\d+)?(?:[-+][\w.]+)?$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GRANT_RE = re.compile(r"\b(?:DE-[A-Z0-9-]+|[A-Z]{1,3}\d{2}[A-Z]{1,3}\d{4,}|[A-Z]+-\d{6,}|R01[A-Z0-9]+)\b")


def get_nested(data: Any, path: str) -> Any:
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


def stringify(value: Any) -> str:
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


# ---------------------------------------------------------------------------
# Per-question scorers
# ---------------------------------------------------------------------------
# Each returns (score, max_score, label, evidence)
def _all_datasets(d: dict) -> list:
    """Collect datasets across both base (model_parameters.data) and harmonized
    (model_parameters.training_datasets + evaluation_datasets) layouts."""
    base = get_nested(d, "model_parameters.data") or []
    train = get_nested(d, "model_parameters.training_datasets") or []
    ev = get_nested(d, "model_parameters.evaluation_datasets") or []
    out = []
    for src in (base, train, ev):
        if isinstance(src, list):
            out.extend(src)
        elif src:
            out.append(src)
    return out


# ---------------------------------------------------------------------------
# Semantic rules — deterministic checks lifted from the rubric20-semantic LLM
# evaluator. Currently cover:
#   Q18 (train/eval data leakage)
#   Q19 (bias declared without a matching fairness tradeoff)
# Caps reflect the consistent 5->3 (or 4->3) drop the semantic agent applies.
# ---------------------------------------------------------------------------
SEMANTIC_CAP = 3

# Tradeoff text is considered to acknowledge bias/fairness if it mentions any
# of these stems. Kept loose on purpose — the goal is to flag tradeoffs that
# are purely operational (size vs latency, accuracy vs cost) when the card has
# concrete bias_model / bias_output disclosures.
BIAS_TRADEOFF_RE = re.compile(
    r"\b(fair(?:ness)?|bias(?:es|ed)?|demographic|equit|disparit|"
    r"under[-\s]?represent|subgroup|protected[-\s]?(?:class|attribute|group)|"
    r"calibration|harm(?:ful|s)?|discriminat)\b",
    re.I,
)

_VERSION_TAIL_RE = re.compile(r"\s*(?:v\d+(?:\.\d+)*|version\s+\d+(?:\.\d+)*)\s*$", re.I)
_PARENS_RE = re.compile(r"\(([^()]*)\)")


def _normalize_dataset_name(name: Any) -> str:
    """Lowercase + collapse whitespace + drop trailing version marker.

    Leaves parenthetical content in place — the variant extractor uses parens
    as alias boundaries instead.
    """
    s = stringify(name).strip()
    s = _VERSION_TAIL_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def _dataset_name_variants(name: Any) -> list[str]:
    """Yield normalized variants of `name` for overlap matching.

    Returns the normalized full string, the parens-stripped variant, and each
    parenthetical's inner content normalized. This captures cases like
    'Test set (E3SM v2)' sharing 'e3sm v2' with 'E3SM v2 High-Resolution'.
    """
    raw = stringify(name)
    out: list[str] = []
    seen: set[str] = set()

    def _add(v: str) -> None:
        if v and v not in seen:
            seen.add(v)
            out.append(v)

    _add(_normalize_dataset_name(raw))
    paren_stripped = _PARENS_RE.sub("", raw)
    _add(_normalize_dataset_name(paren_stripped))
    for m in _PARENS_RE.finditer(raw):
        _add(_normalize_dataset_name(m.group(1)))
    return out


def _dataset_names_from(items: Any) -> list[str]:
    """Pull plausible dataset-name strings out of a list/dict/scalar source."""
    if not items:
        return []
    if isinstance(items, dict):
        items = [items]
    out: list[str] = []
    if isinstance(items, list):
        for it in items:
            if isinstance(it, dict):
                nm = it.get("name") or it.get("dataset") or it.get("id")
                if nm:
                    out.append(stringify(nm))
            elif isinstance(it, str):
                out.append(it)
    return out


def _training_dataset_names(d: dict) -> list[str]:
    return (
        _dataset_names_from(get_nested(d, "model_parameters.data"))
        + _dataset_names_from(get_nested(d, "model_parameters.training_datasets"))
    )


def _benchmark_dataset_names(d: dict) -> list[str]:
    names: list[str] = []
    names.extend(_dataset_names_from(get_nested(d, "model_parameters.evaluation_datasets")))
    metrics = get_nested(d, "quantitative_analysis.performance_metrics") or []
    if isinstance(metrics, list):
        for m in metrics:
            if isinstance(m, dict) and m.get("slice"):
                names.append(stringify(m["slice"]))
    mi = d.get("model_index") or []
    if isinstance(mi, list):
        for entry in mi:
            if not isinstance(entry, dict):
                continue
            for r in entry.get("results") or []:
                if not isinstance(r, dict):
                    continue
                ds = r.get("dataset")
                if isinstance(ds, dict):
                    nm = ds.get("name") or ds.get("id")
                    if nm:
                        names.append(stringify(nm))
                elif isinstance(ds, str):
                    names.append(ds)
    top_ds = d.get("datasets")
    if isinstance(top_ds, list):
        names.extend(stringify(x) for x in top_ds if x)
    return names


def detect_train_eval_leakage(d: dict) -> tuple[bool, str]:
    """True if a benchmark/eval dataset name matches a training dataset name.

    Matches the rubric20-semantic 'benchmark dataset <-> training data' rule.
    Comparison is case-insensitive after stripping version tails ('v2', '1.0')
    and parenthetical qualifiers, and uses substring containment so 'ImageNet-1k'
    matches 'ImageNet-1k validation'.
    """
    train_raw = _training_dataset_names(d)
    bench_raw = _benchmark_dataset_names(d)
    if not train_raw or not bench_raw:
        return False, ""
    train_variants = [(orig, _dataset_name_variants(orig)) for orig in train_raw]
    bench_variants = [(orig, _dataset_name_variants(orig)) for orig in bench_raw]
    overlaps: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for t_orig, t_vars in train_variants:
        for b_orig, b_vars in bench_variants:
            matched = False
            for t in t_vars:
                if not t:
                    continue
                for b in b_vars:
                    if not b:
                        continue
                    if t == b or (len(t) >= 4 and t in b) or (len(b) >= 4 and b in t):
                        matched = True
                        break
                if matched:
                    break
            if matched:
                key = (t_orig, b_orig)
                if key not in seen:
                    seen.add(key)
                    overlaps.append(key)
    if not overlaps:
        return False, ""
    examples = ", ".join(f"'{t}' ~ '{b}'" for t, b in overlaps[:3])
    return True, f"Training/benchmark dataset overlap: {examples}"


def detect_bias_tradeoff_gap(d: dict) -> tuple[bool, str]:
    """True if bias_model or bias_output is populated but tradeoffs[] mentions
    no fairness-adjacent concept.

    Mirrors the rubric20-semantic 'bias disclosure -> tradeoffs' consistency
    rule. Skips when tradeoffs is empty so we don't double-flag the existing
    base presence rule.
    """
    bias_declared = has_content(d.get("bias_model")) or has_content(d.get("bias_output"))
    if not bias_declared:
        return False, ""
    tradeoffs = get_nested(d, "considerations.tradeoffs") or []
    if not has_content(tradeoffs):
        return False, ""
    blob = stringify(tradeoffs)
    if BIAS_TRADEOFF_RE.search(blob):
        return False, ""
    snippet = blob[:120] + ("…" if len(blob) > 120 else "")
    return True, (
        "bias_model/bias_output populated but considerations.tradeoffs omits "
        f"fairness/bias dimension — tradeoffs read: {snippet!r}"
    )


def compute_semantic_caps(d: dict) -> dict[str, dict]:
    """Return {'Q18'|'Q19': {rule, reason}} for any deterministic semantic rule
    that fires against this card. Empty if none fire."""
    out: dict[str, dict] = {}
    leak, leak_reason = detect_train_eval_leakage(d)
    if leak:
        out["Q18"] = {"rule": "train_eval_leakage", "reason": leak_reason}
    gap, gap_reason = detect_bias_tradeoff_gap(d)
    if gap:
        out["Q19"] = {"rule": "bias_tradeoff_gap", "reason": gap_reason}
    return out


def q1_field_completeness(d: dict) -> tuple[int, int, str, str]:
    required = [
        ("model_details.name", get_nested(d, "model_details.name")),
        ("model_details.overview", get_nested(d, "model_details.overview")),
        ("model_details.licenses", get_nested(d, "model_details.licenses")),
        ("model_details.version", get_nested(d, "model_details.version")),
        ("model_parameters.model_architecture", get_nested(d, "model_parameters.model_architecture")),
    ]
    populated = [name for name, v in required if has_content(v)]
    n = len(populated)
    if n >= 5:
        return 5, 5, "All 5 required fields populated", f"populated={populated}"
    if n == 4:
        return 4, 5, "4 of 5 required fields populated", f"populated={populated}"
    if n == 3:
        return 3, 5, "3 of 5 required fields populated", f"populated={populated}"
    if n == 2:
        return 2, 5, "2 of 5 required fields populated", f"populated={populated}"
    if n == 1:
        return 1, 5, "1 of 5 required fields populated", f"populated={populated}"
    return 0, 5, "No required fields populated", "populated=[]"


def q2_overview_length(d: dict) -> tuple[int, int, str, str]:
    overview = stringify(get_nested(d, "model_details.overview"))
    doc = stringify(get_nested(d, "model_details.documentation"))
    short = stringify(get_nested(d, "model_details.short_description"))
    total = len(overview) + len(doc) + len(short)
    if total > 500:
        return 5, 5, ">500 chars across narrative fields", f"overview={len(overview)}, doc={len(doc)}, short={len(short)}"
    if total >= 50:
        return 3, 5, "50–500 chars combined", f"overview={len(overview)}, doc={len(doc)}, short={len(short)}"
    return 0, 5, "<50 chars combined", f"total={total}"


def q3_tag_diversity(d: dict) -> tuple[int, int, str, str]:
    tags = d.get("tags") or []
    if not isinstance(tags, list):
        tags = [tags]
    pipe = d.get("pipeline_tag")
    cat = d.get("model_category")
    lang = d.get("language")
    n_tags = len(tags)
    has_extra = bool(lang or cat)
    if n_tags >= 4 and pipe and has_extra:
        return 5, 5, "≥4 tags + pipeline_tag + (language or model_category)", f"{n_tags} tags, pipeline={pipe}, lang={lang}, cat={cat}"
    if (n_tags >= 1 and (pipe or has_extra)) or (pipe and not n_tags):
        return 3, 5, "Some tags or pipeline tag only", f"{n_tags} tags, pipeline={pipe}, lang={lang}, cat={cat}"
    return 0, 5, "No tags / pipeline tag", "no tags or pipeline"


def q4_io_specification(d: dict) -> tuple[int, int, str, str]:
    in_fmt = get_nested(d, "model_parameters.input_format")
    out_fmt = get_nested(d, "model_parameters.output_format")
    in_map = get_nested(d, "model_parameters.input_format_map")
    out_map = get_nested(d, "model_parameters.output_format_map")
    has_prose = has_content(in_fmt) and has_content(out_fmt)
    has_map = has_content(in_map) or has_content(out_map)
    if has_prose and has_map:
        return 5, 5, "Both I/O specified with format_map populated", "prose + structured map"
    if has_prose:
        return 3, 5, "Input AND output described in prose only", "prose only"
    if has_content(in_fmt) or has_content(out_fmt):
        return 1, 5, "Only one of input/output described", "partial"
    return 0, 5, "No I/O spec", "missing both"


def q5_schema_version(d: dict) -> tuple[int, int, str, str]:
    sv = d.get("schema_version")
    if has_content(sv):
        return 1, 1, "schema_version populated", f"schema_version={sv}"
    return 0, 1, "schema_version missing", "absent"


def q6_persistent_identifier(d: dict) -> tuple[int, int, str, str]:
    refs = get_nested(d, "model_details.references") or []
    ref_strs = [stringify(r) for r in refs] if isinstance(refs, list) else [stringify(refs)]
    path = stringify(get_nested(d, "model_details.path"))
    base = stringify(d.get("base_model"))
    blob = " ".join(ref_strs + [path, base])
    if DOI_RE.search(blob) or HF_HUB_RE.search(blob):
        return 1, 1, "Resolvable persistent identifier", "DOI or HF Hub URL present"
    if any(ref_strs):
        return 0, 1, "Only generic URLs, no DOI/HF Hub", f"refs={ref_strs[:2]}"
    return 0, 1, "No identifier", "absent"


def q7_funding_completeness(d: dict) -> tuple[int, int, str, str]:
    contribs = get_nested(d, "model_details.contributors") or []
    creator_refs = get_nested(d, "model_details.creator_references") or []  # harmonized
    # In the harmonized schema, funding_grants is a slot on MissionRelevance.
    funding_grants = get_nested(d, "mission_relevance.funding_grants") or []  # harmonized
    affils = [stringify(c.get("affiliation")) for c in contribs if isinstance(c, dict)]
    creator_text = [stringify(c) for c in creator_refs]
    grant_text = [stringify(g) for g in funding_grants]
    mission = stringify(d.get("mission_relevance"))
    blob = " ".join(affils + creator_text + grant_text + [mission])
    has_agency = bool(re.search(r"\b(NIH|NSF|DOE|DARPA|NASA|EU|European Commission|Horizon|ERC|BMBF)\b", blob, re.I))
    has_grant = bool(GRANT_RE.search(blob)) or bool(funding_grants)
    has_facility = bool(re.search(r"\b(NERSC|ALCF|OLCF|Perlmutter|Frontier|Summit|Aurora)\b", blob, re.I)) \
        or has_content(get_nested(d, "model_parameters.compute_infrastructure"))
    if has_agency and has_grant and has_facility:
        return 5, 5, "Agency + grant ID + facility/acknowledgement", "all three present"
    if has_agency:
        return 3, 5, "Funding agency mentioned, no grant number", "partial"
    return 0, 5, "No funding info detected", "absent"


def q8_ethical_responsible_ai(d: dict) -> tuple[int, int, str, str]:
    ethics = get_nested(d, "considerations.ethical_considerations") or []
    bias_m = d.get("bias_model")
    bias_o = d.get("bias_output")
    bias_i = d.get("bias_input")
    oos = get_nested(d, "considerations.out_of_scope_uses") or []
    has_ethics = bool(ethics)
    has_bias = any(has_content(x) for x in (bias_m, bias_o, bias_i))
    has_oos = bool(oos)
    if has_ethics and has_bias and has_oos:
        return 5, 5, "ethics + bias + out_of_scope all populated", "comprehensive"
    if has_ethics and (has_oos or has_bias):
        return 3, 5, "Ethics present but missing bias or out_of_scope", "partial"
    if has_ethics:
        return 2, 5, "Only ethical_considerations populated", "minimal"
    return 0, 5, "No ethics fields populated", "absent"


def q9_license_clarity(d: dict) -> tuple[int, int, str, str]:
    licenses = get_nested(d, "model_details.licenses") or []
    if not isinstance(licenses, list):
        licenses = [licenses]
    if not licenses:
        return 0, 5, "No license", "absent"
    spdx_ids = []
    has_restrictions = False
    for lic in licenses:
        if isinstance(lic, dict):
            ident = lic.get("identifier") or ""
            if ident in SPDX_LICENSES:
                spdx_ids.append(ident)
            if has_content(lic.get("custom_text")):
                has_restrictions = True
        elif isinstance(lic, str) and lic in SPDX_LICENSES:
            spdx_ids.append(lic)
    # Permissive SPDX licenses (MIT, Apache-2.0, BSD-*, CC-BY-*) need no
    # additional restrictions to clear the 5/5 bar — restrictions only
    # matter for non-permissive identifiers (OpenRAIL-M, LLAMA2, etc.).
    PERMISSIVE_SPDX = {
        "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
        "Unlicense", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0", "MPL-2.0",
    }
    has_permissive = any(s in PERMISSIVE_SPDX for s in spdx_ids)
    if spdx_ids and (has_restrictions or has_permissive):
        note = "SPDX + restrictions stated" if has_restrictions else "SPDX permissive license (no additional restrictions needed)"
        return 5, 5, note, f"spdx={spdx_ids}"
    if spdx_ids:
        return 4, 5, "SPDX identifier, no explicit restrictions text", f"spdx={spdx_ids}"
    return 3, 5, "License present but non-SPDX", f"identifiers={[l.get('identifier') if isinstance(l, dict) else l for l in licenses]}"


def q10_framework_standardization(d: dict) -> tuple[int, int, str, str]:
    fw = d.get("framework")
    fwv = d.get("framework_version")
    lib = d.get("library_name")
    mi = d.get("model_index")
    has_mi = bool(mi)
    if fw and fwv and lib and has_mi:
        return 5, 5, "Framework + version + library + model_index", f"{fw} {fwv}, lib={lib}, model_index present"
    if fw and fwv and lib:
        return 4, 5, "Framework + version + library, no model_index", f"{fw} {fwv}, lib={lib}"
    if fw and fwv:
        return 4, 5, "Framework + version pinned", f"{fw} {fwv}"
    if fw or lib:
        return 3, 5, "Framework or library declared, no version pin", f"fw={fw}, lib={lib}"
    return 0, 5, "No framework info", "absent"


def q11_software_transparency(d: dict) -> tuple[int, int, str, str]:
    fwv = d.get("framework_version")
    tp = get_nested(d, "model_parameters.training_procedure") or {}
    ci = get_nested(d, "model_parameters.compute_infrastructure") or {}
    code_examples = get_nested(d, "usage_documentation.code_examples") or []
    deps = stringify(ci.get("software_dependencies") if isinstance(ci, dict) else "")
    has_docker = "docker" in stringify(get_nested(d, "usage_documentation")).lower() or \
        "container" in stringify(get_nested(d, "usage_documentation")).lower()
    if fwv and (deps or has_docker) and code_examples:
        return 5, 5, "Comprehensive: framework_version + deps/container + examples", "exemplary"
    if fwv and code_examples:
        return 4, 5, "Framework version + code examples", "good"
    if fwv or code_examples:
        return 3, 5, "Some tool/library named", "partial"
    return 0, 5, "No software tools listed", "absent"


def q12_training_procedure(d: dict) -> tuple[int, int, str, str]:
    tp = get_nested(d, "model_parameters.training_procedure") or {}
    if not isinstance(tp, dict):
        if has_content(tp):
            return 3, 5, "Training procedure as string only", "prose only"
        return 0, 5, "No training procedure", "absent"
    hp = tp.get("reproducibility_info", {}).get("hyperparameters") if isinstance(tp.get("reproducibility_info"), dict) else None
    if not has_content(hp):
        hp = tp.get("hyperparameters")
    if not isinstance(hp, dict):
        hp = {}
    # str() guard handles non-string YAML keys (ints / floats / bools)
    keys = {str(k).lower() for k in hp.keys()}
    must_have = {"optimizer", "learning_rate"}
    # Each nice-to-have category groups synonyms so multiple keys hitting
    # the same category only count once (e.g. "epochs" and "training_epochs"
    # are the same concept).
    nice_to_have_groups = [
        {"batch_size"},
        {"epochs", "training_epochs", "num_epochs"},
        {"training_steps", "max_steps"},
        {"schedule", "lr_schedule", "scheduler", "warmup"},
        {"weight_decay", "dropout", "regularization"},
    ]
    have_must = sum(1 for m in must_have if any(m in k for k in keys))
    have_nice = sum(
        1 for group in nice_to_have_groups
        if any(any(member in k for k in keys) for member in group)
    )
    if have_must >= 2 and have_nice >= 3:
        return 5, 5, "Optimizer + LR + batch + epochs + schedule + regularization", "comprehensive hyperparameters"
    if have_must >= 1 and have_nice >= 2:
        return 4, 5, "Most hyperparameters present", "good"
    if has_content(tp):
        return 3, 5, "Training described, hyperparameters incomplete", f"have {have_must + have_nice} key(s)"
    return 0, 5, "No training procedure", "absent"


def q13_version_history(d: dict) -> tuple[int, int, str, str]:
    name = stringify(get_nested(d, "model_details.version.name"))
    date = stringify(get_nested(d, "model_details.version.date"))
    diff = stringify(get_nested(d, "model_details.version.diff"))
    is_semver = bool(name and SEMVER_RE.match(name))
    is_iso = bool(date and ISO_DATE_RE.match(date))
    has_diff = bool(diff and len(diff) >= 30)
    if is_semver and is_iso and has_diff:
        return 5, 5, "Semver + ISO date + non-trivial diff", f"version={name}, date={date}, diff={len(diff)} chars"
    if name and date:
        return 4, 5, "Version name + date present", f"version={name}, date={date}"
    if name or date:
        return 3, 5, "Version name or date present", f"name={name}, date={date}"
    return 0, 5, "No version info", "absent"


def q14_citations_references(d: dict) -> tuple[int, int, str, str]:
    citations = get_nested(d, "model_details.citations") or []
    references = get_nested(d, "model_details.references") or []
    n_cit = len(citations) if isinstance(citations, list) else (1 if has_content(citations) else 0)
    n_ref = len(references) if isinstance(references, list) else (1 if has_content(references) else 0)
    # check for DOIs in refs
    ref_strs = [stringify(r) for r in references] if isinstance(references, list) else [stringify(references)]
    has_doi = any(DOI_RE.search(s) for s in ref_strs)
    if n_cit >= 2 and n_ref >= 2 and has_doi:
        return 5, 5, "Multiple citations + multiple references with DOIs", f"{n_cit} cites, {n_ref} refs, DOIs present"
    if n_cit >= 1 and n_ref >= 1:
        return 4, 5, "Citation(s) + reference(s), DOIs missing", f"{n_cit} cites, {n_ref} refs"
    if n_cit + n_ref >= 1:
        return 3, 5, "One citation OR one reference", f"{n_cit} cites, {n_ref} refs"
    return 0, 5, "No citations or references", "absent"


def q15_compute_infra_energy(d: dict) -> tuple[int, int, str, str]:
    ci = get_nested(d, "model_parameters.compute_infrastructure")
    if not has_content(ci):
        return 0, 5, "No compute_infrastructure", "absent"
    s = stringify(ci).lower()
    hw = bool(re.search(r"\b(gpu|tpu|a100|h100|v100|cpu|node|cluster|nersc|alcf|olcf)\b", s))
    sw = bool(re.search(r"\b(pytorch|tensorflow|jax|cuda|cudnn|conda|docker)\b", s))
    compute = bool(re.search(r"\b(gpu-hours|tpu-hours|gpu-days|flops|petaflops|exaflops|wall-clock|hours)\b", s))
    energy = bool(re.search(r"\b(kwh|mwh|co2|carbon|kgco2)\b", s))
    if hw and sw and compute and energy:
        return 5, 5, "Hardware + software + compute + energy", "complete"
    if hw and sw and compute:
        return 4, 5, "Hardware + software + total compute", "no energy estimate"
    if hw or sw:
        return 3, 5, "Hardware or software listed", "partial"
    return 1, 5, "Compute infra present but ambiguous", "vague"


def q16_findability(d: dict) -> tuple[int, int, str, str]:
    refs = get_nested(d, "model_details.references") or []
    ref_strs = [stringify(r) for r in refs] if isinstance(refs, list) else [stringify(refs)]
    if any(re.search(r"^https?://", s) for s in ref_strs):
        return 1, 1, "At least one resolvable URL", f"{len(ref_strs)} refs"
    path = stringify(get_nested(d, "model_details.path"))
    if path and re.search(r"^https?://", path):
        return 1, 1, "model_details.path is a URL", path[:80]
    return 0, 1, "No external URLs", "absent"


def q17_accessibility_inference(d: dict) -> tuple[int, int, str, str]:
    code = get_nested(d, "usage_documentation.code_examples") or []
    in_fmt = get_nested(d, "model_parameters.input_format")
    out_fmt = get_nested(d, "model_parameters.output_format")
    n_examples = len(code) if isinstance(code, list) else (1 if has_content(code) else 0)
    has_io = has_content(in_fmt) and has_content(out_fmt)
    if n_examples >= 1 and has_io:
        return 5, 5, "Runnable code example(s) + I/O specs", f"{n_examples} example(s)"
    if n_examples >= 1 or has_io:
        return 3, 5, "Partial usage docs", f"examples={n_examples}, io={has_io}"
    return 0, 5, "No usage path documented", "absent"


def q18_metrics_slices_ci(d: dict) -> tuple[int, int, str, str]:
    metrics = get_nested(d, "quantitative_analysis.performance_metrics") or []
    if not isinstance(metrics, list):
        metrics = []
    with_values = [m for m in metrics if isinstance(m, dict) and m.get("value") not in (None, "")]
    slices = {m.get("slice") for m in metrics if isinstance(m, dict) and m.get("slice")}
    has_ci = any(
        isinstance(m, dict) and (m.get("confidence_interval") or m.get("value_error"))
        for m in metrics
    )
    if len(with_values) >= 2 and len(slices) >= 2 and has_ci:
        return 5, 5, "≥2 metrics, ≥2 slices, CI on ≥1", f"{len(with_values)} metrics, {len(slices)} slices, CI={has_ci}"
    if len(with_values) >= 1 and len(slices) >= 2:
        return 4, 5, "Metrics across multiple slices, no CI", f"{len(with_values)} metrics, {len(slices)} slices"
    if len(with_values) >= 1:
        return 3, 5, "Metrics with values, no slices", f"{len(with_values)} metric(s)"
    if metrics:
        return 0, 5, "Metrics declared without values", "no numeric values"
    return 0, 5, "No metrics", "absent"


def q19_oos_limitations_tradeoffs(d: dict) -> tuple[int, int, str, str]:
    lim = get_nested(d, "considerations.limitations") or []
    to = get_nested(d, "considerations.tradeoffs") or []
    oos = get_nested(d, "considerations.out_of_scope_uses") or []

    # Count only fields populated as non-empty LISTS — bare strings like
    # "None known" don't count as enumerated items even though has_content()
    # accepts them.
    def _is_item_list(x):
        return isinstance(x, list) and len(x) >= 1

    populated = sum(1 for x in (lim, to, oos) if has_content(x))
    list_populated = sum(1 for x in (lim, to, oos) if _is_item_list(x))

    if populated == 3 and list_populated == 3:
        return 5, 5, "All three populated with concrete enumerated items", \
            f"lim={len(lim)}, tradeoffs={len(to)}, oos={len(oos)}"
    if populated == 3:
        # All present, but at least one is a bare string instead of a list — cap at 4
        return 4, 5, "All three populated, some as prose rather than enumerated lists", \
            f"populated={populated}, lists={list_populated}"
    if populated >= 1:
        return 3, 5, f"{populated} of 3 populated", f"populated={populated}, lists={list_populated}"
    return 0, 5, "None populated", "absent"


def q20_cross_platform(d: dict) -> tuple[int, int, str, str]:
    mi = d.get("model_index") or []
    has_benchmark = False
    if isinstance(mi, list):
        for entry in mi:
            if isinstance(entry, dict) and entry.get("results"):
                has_benchmark = True
                break
    base = stringify(d.get("base_model"))
    refs = get_nested(d, "model_details.references") or []
    ref_strs = [stringify(r) for r in refs] if isinstance(refs, list) else [stringify(refs)]
    has_doi = any(DOI_RE.search(s) for s in ref_strs)
    # Use the file-local _all_datasets helper so harmonized
    # training_datasets / evaluation_datasets entries also count.
    datasets = _all_datasets(d)
    has_dataset_link = any(
        isinstance(ds, dict) and (ds.get("link") or ds.get("url")) for ds in datasets
    )
    if has_benchmark or has_doi or (base and re.search(r"https?://", base)) or has_dataset_link:
        return 1, 1, "Cross-platform reference present", f"benchmark={has_benchmark}, doi={has_doi}, dataset_link={has_dataset_link}"
    return 0, 1, "Only model's homepage referenced", "no cross-refs"


CATEGORIES = [
    {
        "name": "Structural Completeness",
        "max": 21,
        "questions": [
            ("1", "Required Field Completeness", q1_field_completeness),
            ("2", "Overview Length Adequacy", q2_overview_length),
            ("3", "Tag / Keyword Diversity", q3_tag_diversity),
            ("4", "Input / Output Specification", q4_io_specification),
            ("5", "Schema Version Declared", q5_schema_version),
        ],
    },
    {
        "name": "Metadata Quality & Content",
        "max": 21,
        "questions": [
            ("6", "Persistent Identifier Present", q6_persistent_identifier),
            ("7", "Funding & Acknowledgements Completeness", q7_funding_completeness),
            ("8", "Ethical & Responsible-AI Documentation", q8_ethical_responsible_ai),
            ("9", "License Clarity & SPDX Compliance", q9_license_clarity),
            ("10", "Framework / Library Standardization", q10_framework_standardization),
        ],
    },
    {
        "name": "Technical Documentation",
        "max": 25,
        "questions": [
            ("11", "Tool & Software Transparency", q11_software_transparency),
            ("12", "Training Procedure Clarity", q12_training_procedure),
            ("13", "Version History Documentation", q13_version_history),
            ("14", "Citations & References", q14_citations_references),
            ("15", "Compute Infrastructure & Energy", q15_compute_infra_energy),
        ],
    },
    {
        "name": "Performance & FAIRness",
        "max": 17,
        "questions": [
            ("16", "Findability (Persistent Landing)", q16_findability),
            ("17", "Accessibility & Inference Path", q17_accessibility_inference),
            ("18", "Performance Metrics with Slices & CI", q18_metrics_slices_ci),
            ("19", "Out-of-Scope Uses, Limitations & Tradeoffs", q19_oos_limitations_tradeoffs),
            ("20", "Cross-Platform Interlinks", q20_cross_platform),
        ],
    },
]
MAX_POINTS = 84


# ---------------------------------------------------------------------------
# Core eval
# ---------------------------------------------------------------------------
def evaluate_one(path: Path) -> dict[str, Any]:
    # Read once: hash and parse from the same buffer.
    try:
        raw = path.read_bytes()
    except Exception as e:
        return {"error": f"Failed to read file: {e}", "model_card_file": str(path)}
    try:
        data = yaml.safe_load(raw)
    except Exception as e:
        return {"error": f"Failed to load YAML: {e}", "model_card_file": str(path)}

    if not isinstance(data, dict):
        return {"error": "Top-level YAML is not a mapping", "model_card_file": str(path)}

    result: dict[str, Any] = {
        "rubric": "mc_rubric20",
        "version": "1.0",
        "model_card_file": str(path),
        "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
        "evaluator": {
            "name": "hybrid-heuristic-evaluator",
            "temperature": "N/A",
            "evaluation_type": "rule_based_with_quality_heuristics",
        },
        "categories": [],
        "overall_score": {},
        "assessment": {"strengths": [], "weaknesses": [], "recommendations": []},
        "metadata": {
            "evaluator_id": "batch-hybrid-rubric20",
            "model_card_hash": hashlib.sha256(raw).hexdigest(),
        },
    }

    semantic_caps = compute_semantic_caps(data)
    semantic_deductions: list[dict[str, Any]] = []

    total = 0
    for cat in CATEGORIES:
        cat_score = 0
        cat_questions = []
        for qid, qname, scorer in cat["questions"]:
            score, qmax, label, evidence = scorer(data)
            cap = semantic_caps.get(f"Q{qid}")
            if cap and score > SEMANTIC_CAP:
                raw = score
                score = SEMANTIC_CAP
                label = f"[capped {raw}->{score} by {cap['rule']}] {label}"
                evidence = f"{evidence}; semantic_rule={cap['rule']}: {cap['reason']}"
                semantic_deductions.append({
                    "question": f"Q{qid}",
                    "rule": cap["rule"],
                    "raw_score": raw,
                    "capped_score": score,
                    "reason": cap["reason"],
                })
            score_type = "pass_fail" if qmax == 1 else "numeric"
            cat_questions.append({
                "id": int(qid),
                "name": qname,
                "score_type": score_type,
                "score": score,
                "max_score": qmax,
                "score_label": label,
                "evidence": evidence,
                "quality_note": label,
            })
            cat_score += score
        result["categories"].append({
            "name": cat["name"],
            "category_score": cat_score,
            "category_max": cat["max"],
            "questions": cat_questions,
        })
        total += cat_score

    result["overall_score"] = {
        "total_points": total,
        "max_points": MAX_POINTS,
        "percentage": round(total / MAX_POINTS * 100, 1),
        "semantic_deductions": semantic_deductions,
    }

    for cat in result["categories"]:
        ratio = cat["category_score"] / cat["category_max"]
        if ratio >= 0.85:
            result["assessment"]["strengths"].append(
                f"Strong {cat['name']} ({cat['category_score']}/{cat['category_max']})"
            )
        elif ratio < 0.5:
            result["assessment"]["weaknesses"].append(
                f"Weak {cat['name']} ({cat['category_score']}/{cat['category_max']})"
            )

    return result


# ---------------------------------------------------------------------------
# Batch + summary outputs
# ---------------------------------------------------------------------------
def write_csv(results: list[dict], out_path: Path) -> None:
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "model_card_file", "total_score", "max_score", "percentage",
            "structural", "metadata", "technical", "fairness",
        ] + [f"q{i}_score" for i in range(1, 21)])
        for r in results:
            if "error" in r:
                writer.writerow([r.get("model_card_file"), "ERROR", "", "", *[""] * (4 + 20)])
                continue
            cats = r["categories"]
            cat_scores = [c["category_score"] for c in cats]
            qscores = [q["score"] for c in cats for q in c["questions"]]
            row = [
                r["model_card_file"],
                r["overall_score"]["total_points"],
                r["overall_score"]["max_points"],
                r["overall_score"]["percentage"],
                *cat_scores,
                *qscores,
            ]
            writer.writerow(row)


def write_markdown(results: list[dict], out_path: Path) -> None:
    lines = [
        "# Model Card Rubric20 Batch Summary",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}  ",
        f"Files evaluated: {len(results)}",
        "",
        "| File | Score | % | Structural | Metadata | Technical | FAIRness |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['model_card_file']} | ERROR | | {r['error']} | | | |")
            continue
        cats = r["categories"]
        scores = [f"{c['category_score']}/{c['category_max']}" for c in cats]
        lines.append(
            f"| `{r['model_card_file']}` | "
            f"{r['overall_score']['total_points']}/{r['overall_score']['max_points']} | "
            f"{r['overall_score']['percentage']}% | "
            f"{scores[0]} | {scores[1]} | {scores[2]} | {scores[3]} |"
        )
    out_path.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", type=Path, help="Single Model Card YAML")
    g.add_argument("--input-glob", help="Glob (e.g. 'src/data/examples/extended/*.yaml')")
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args(argv)

    paths = [args.input] if args.input else sorted(Path(p) for p in glob.glob(args.input_glob, recursive=True))
    if not paths:
        print("No input files matched.", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    for path in paths:
        print(f"Evaluating: {path}")
        r = evaluate_one(path)
        results.append(r)

        out_file = args.output_dir / f"{path.stem}_rubric20_evaluation.json"
        out_file.write_text(json.dumps(r, indent=2))

        if "error" in r:
            print(f"  ERROR: {r['error']}")
        else:
            s = r["overall_score"]
            cat_summary = ", ".join(
                f"{c['name'].split()[0]}={c['category_score']}/{c['category_max']}"
                for c in r["categories"]
            )
            print(f"  {s['total_points']}/{s['max_points']} ({s['percentage']}%) — {cat_summary}")

    write_csv(results, args.output_dir / "all_scores.csv")
    write_markdown(results, args.output_dir / "summary_report.md")
    print(f"\nWrote {len(results)} evaluations to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
