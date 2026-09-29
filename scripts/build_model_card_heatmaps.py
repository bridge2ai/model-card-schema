#!/usr/bin/env python3
"""Render detailed, current model-card heatmaps with reproducible provenance.

Run from any directory. Outputs editable SVG, vector PDF, 180-dpi PNG and
machine-readable companion data. Requires matplotlib and PyYAML.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import Rectangle, Circle
import yaml

# Every label position assumes Arial's advance widths. Matplotlib reads only the regular
# face of macOS's Helvetica Neue .ttc, which silently rendered bold labels as regular.
METRIC_FONTS = ["Arial", "Liberation Sans", "Arimo"]

STEMS = ["densenet121_tv_in1k", "subcell_saprot_650m"]
NAMES = ["DenseNet-121", "SubCell 650M"]
SHORT = ["DenseNet\n121", "SubCell\n650M"]
SCRIPT = "scripts/build_model_card_heatmaps.py"
# Shared with render_model_card_poster.py: section fractions get the same fill in both figures.
RAMP_STOPS = ["#f0efec", "#9ec5f4", "#2874d0", "#104281"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_remote(url):
    """Keep a remote URL only if it is a network location, without any credentials."""
    if not url:
        return None
    parts = urlsplit(url)
    if parts.scheme in ("http", "https", "ssh", "git"):
        return urlunsplit(parts._replace(netloc=parts.hostname + (f":{parts.port}" if parts.port else "")))
    if not parts.scheme and ":" in url and not url.startswith(("/", ".")):
        return url.split("@", 1)[-1]  # scp-style git@host:owner/repo carries only a user name
    return None


def evaluation_payload(report):
    """Compare every scoring/evidence field while allowing timestamp/path changes."""
    return {key: report.get(key) for key in ("rubric", "version", "evaluator", "elements", "categories", "overall_score", "assessment")}


def select_evaluation(repo, card_path, rubric):
    """Select current-card hybrid results, rejecting malformed or conflicting ties.

    Path.rglob includes ignored/hidden entries and does not invoke gitignore rules.
    Exact basename searches are limited to the repository evaluation directory.
    """
    actual_hash = sha256(card_path)
    candidates = []
    for path in sorted((repo / "data/evaluation").rglob(f"{card_path.stem}*.json")):
        report = json.loads(path.read_text())
        if report.get("rubric") != "mc_" + rubric:
            continue
        evaluator = report.get("evaluator") or {}
        if evaluator.get("name") != "hybrid-heuristic-evaluator" or evaluator.get("evaluation_type") != "rule_based_with_quality_heuristics":
            continue
        declared = str((report.get("metadata") or {}).get("model_card_hash", "")).lower().removeprefix("sha256:")
        if declared != actual_hash:
            continue
        declared_file = Path(report.get("model_card_file") or "")
        if declared_file.name != card_path.name:
            raise ValueError(f"Card hash matches but report names another card: {path}")
        try:
            timestamp = datetime.fromisoformat(report["evaluation_timestamp"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Current report has invalid timestamp: {path}") from error
        if timestamp.tzinfo is None:
            raise ValueError(f"Current report timestamp lacks timezone: {path}")
        candidates.append((timestamp, path, report))
    if not candidates:
        raise ValueError(f"No hash-matching deterministic {rubric} result for {card_path}; rerun the evaluator.")
    newest = max(item[0] for item in candidates)
    tied = [item for item in candidates if item[0] == newest]
    if any(evaluation_payload(item[2]) != evaluation_payload(tied[0][2]) for item in tied[1:]):
        raise ValueError(f"Conflicting current {rubric} reports at {newest.isoformat()}: {[str(item[1]) for item in tied]}")
    _, path, report = tied[0]
    return report, {
        "path": str(path.relative_to(repo)),
        "sha256": sha256(path),
        "model_card_sha256": actual_hash,
        "evaluation_timestamp": report["evaluation_timestamp"],
        "matching_candidates": len(candidates),
        "same_timestamp_identical_reports": [str(item[1].relative_to(repo)) for item in tied],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, help="Default: <repo>/data/poster_assets/model-card-heatmaps")
    parser.add_argument("--allow-uncommitted", action="store_true",
                        help="Write into the repository's figure folder even if an input is untracked or modified.")
    args = parser.parse_args(argv)
    REPO = args.repo.resolve()
    IN_REPO_OUT = REPO / "data/poster_assets/model-card-heatmaps"
    OUT = (args.output_dir or IN_REPO_OUT).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCES = {}
    generated_at = datetime.now(timezone.utc).isoformat()

    def git(*command):
        try:
            # Only the trailing newline: leading spaces are significant in `git status` output.
            return subprocess.check_output(["git", "-C", str(REPO), *command], text=True, stderr=subprocess.DEVNULL).rstrip("\n")
        except (OSError, subprocess.CalledProcessError):
            return None

    # Only trust git when --repo is itself the working tree's top level, not a folder
    # copied into some other repository.
    toplevel = git("rev-parse", "--show-toplevel")
    in_git = toplevel is not None and Path(toplevel).resolve() == REPO

    def read(relative, kind):
        path = REPO / relative
        raw = path.read_bytes()
        SOURCES[relative] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        return yaml.safe_load(raw) if kind == "yaml" else json.loads(raw)

    SCHEMA_PATH = "src/model_card_schema/schema/model_card_schema.yaml"
    schema = read(SCHEMA_PATH, "yaml")
    card_paths = [REPO / f"data/model_cards_assistant/{stem}_model_card.yaml" for stem in STEMS]
    cards = [read(str(path.relative_to(REPO)), "yaml") for path in card_paths]
    selections = {"rubric10": [], "rubric20": []}
    ratings = {"rubric10": [], "rubric20": []}
    for rubric in ratings:
        evaluator_path = REPO / f"scripts/batch_evaluate_mc_{rubric}_hybrid.py"
        SOURCES[str(evaluator_path.relative_to(REPO))] = {"sha256": sha256(evaluator_path), "bytes": evaluator_path.stat().st_size}
        spec = importlib.util.spec_from_file_location("heatmap_" + rubric, evaluator_path)
        evaluator_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator_module)
        for card_path in card_paths:
            report, selection = select_evaluation(REPO, card_path, rubric)
            regenerated = evaluator_module.evaluate_one(card_path)
            if evaluation_payload(report) != evaluation_payload(regenerated):
                raise ValueError(f"Current evaluator does not reproduce selected result: {selection['path']}")
            ratings[rubric].append(report)
            selections[rubric].append(selection)
            read(selection["path"], "json")
    # Always keyed by its repository path; a copy run from elsewhere (for example the
    # slide-assets build_heatmap.py) is named by file name only, never by absolute path.
    script_path = Path(__file__).resolve()
    SOURCES[SCRIPT] = {"sha256": sha256(script_path), "bytes": script_path.stat().st_size}
    if script_path != REPO / SCRIPT:
        SOURCES[SCRIPT]["run_from_copy"] = script_path.name
    if in_git:
        tracked = set(git("ls-files", "-z", "--", *SOURCES).split("\0"))
        changed = {entry[3:] for entry in git("status", "--porcelain=v1", "-z", "--untracked-files=all", "--", *SOURCES).split("\0") if entry}
        for relative, info in SOURCES.items():
            info["committed"] = relative in tracked and relative not in changed
        uncommitted = [relative for relative, info in SOURCES.items() if not info["committed"]]
        if uncommitted and OUT == IN_REPO_OUT.resolve() and not args.allow_uncommitted:
            raise SystemExit("Inputs are untracked or modified, so the published provenance would cite files that are "
                             f"not on GitHub: {uncommitted}. Commit them first, write elsewhere with --output-dir, "
                             "or pass --allow-uncommitted.")
    ratings10, ratings20 = ratings["rubric10"], ratings["rubric20"]

    def slots(class_name):
        c = schema["classes"][class_name]
        assert not c.get("is_a") and not c.get("mixins"), "Handle inherited slots before using a new schema."
        return [(s, {**schema["slots"][s], **c.get("slot_usage", {}).get(s, {})}) for s in c.get("slots", [])]


    def leaf_paths(class_name, prefix=(), ancestors=()):
        assert class_name not in ancestors, "Recursive class needs an explicit traversal boundary."
        paths = []
        for name, spec in slots(class_name):
            p = prefix + (name,)
            if spec.get("range") in schema["classes"]:
                paths.extend(leaf_paths(spec["range"], p, ancestors + (class_name,)))
            else:
                paths.append(p)
        return paths


    def populated(obj, path):
        if isinstance(obj, list):
            return any(populated(value, path) for value in obj)
        if not path:
            if obj is None:
                return False
            if isinstance(obj, str):
                return bool(obj.strip())
            if isinstance(obj, dict):
                return any(populated(v, ()) for v in obj.values())
            return True  # Zero and False are real values.
        return isinstance(obj, dict) and path[0] in obj and populated(obj[path[0]], path[1:])


    def validate_card(obj, class_name, prefix=()):
        if isinstance(obj, list):
            for v in obj:
                validate_card(v, class_name, prefix)
            return
        assert isinstance(obj, dict), (prefix, type(obj))
        declared = dict(slots(class_name))
        assert not set(obj) - set(declared), f"Undeclared fields at {prefix}: {set(obj) - set(declared)}"
        for k, v in obj.items():
            rng = declared[k].get("range")
            if rng in schema["classes"] and v is not None:
                validate_card(v, rng, prefix + (k,))


    paths = leaf_paths("modelCard")
    assert len(paths) == 126 and len(set(paths)) == 126
    for card in cards:
        validate_card(card, "modelCard")
    presence = {p: [int(populated(c, p)) for c in cards] for p in paths}
    presence_totals = [sum(v[i] for v in presence.values()) for i in range(2)]



    def flatten10(r):
        return [(e["id"], i + 1, e["name"], s) for e in r["elements"] for i, s in enumerate(e["sub_elements"])]


    def flatten20(r):
        return [(c["name"], q) for c in r["categories"] for q in c["questions"]]


    r10 = [flatten10(r) for r in ratings10]
    r20 = [flatten20(r) for r in ratings20]
    # The short row labels below are positional; fail if the evaluators reorder or renumber items.
    assert [(e, s) for e, s, _, _ in r10[0]] == [(e, s) for e in range(1, 11) for s in range(1, 6)], "rubric10 item order changed"
    assert [q["id"] for _, q in r20[0]] == list(range(1, 21)), "rubric20 question order changed"
    assert [(a, b, c, d["name"]) for a, b, c, d in r10[0]] == [(a, b, c, d["name"]) for a, b, c, d in r10[1]]
    assert [(c, q["id"], q["name"], q["max_score"], q["score_type"]) for c, q in r20[0]] == [(c, q["id"], q["name"], q["max_score"], q["score_type"]) for c, q in r20[1]]
    for i in range(2):
        assert len(r10[i]) == 50 and len(r20[i]) == 20
        assert all(s["score"] in (0, 1) for _, _, _, s in r10[i])
        assert all(0 <= q["score"] <= q["max_score"] for _, q in r20[i])
        assert sum(s["score"] for _, _, _, s in r10[i]) == ratings10[i]["overall_score"]["total_points"]
        assert sum(q["score"] for _, q in r20[i]) == ratings20[i]["overall_score"]["total_points"]
        assert sum(q["max_score"] for _, q in r20[i]) == 84

    root_scalars = [p for p in paths if len(p) == 1]
    left_groups = [
        ("Core metadata", "", root_scalars),
        ("Model details", "model_details.", [p for p in paths if p[0] == "model_details"]),
        ("Architecture, data and I/O", "model_parameters.", [p for p in paths if p[0] == "model_parameters" and p[1] not in ("compute_infrastructure", "training_procedure")]),
        ("Compute infrastructure", "model_parameters.compute_infrastructure.", [p for p in paths if p[:2] == ("model_parameters", "compute_infrastructure")]),
    ]
    right_groups = [
        ("Training procedure", "model_parameters.training_procedure.", [p for p in paths if p[:2] == ("model_parameters", "training_procedure")]),
        ("Quantitative analysis", "quantitative_analysis.", [p for p in paths if p[0] == "quantitative_analysis"]),
        ("Considerations", "considerations.", [p for p in paths if p[0] == "considerations"]),
        ("Benchmark index", "model_index.", [p for p in paths if p[0] == "model_index"]),
        ("Mission relevance", "mission_relevance.", [p for p in paths if p[0] == "mission_relevance"]),
        ("Usage documentation", "usage_documentation.", [p for p in paths if p[0] == "usage_documentation"]),
    ]
    ordered_paths = [p for _, _, ps in left_groups + right_groups for p in ps]
    assert len(ordered_paths) == len(paths) and set(ordered_paths) == set(paths)

    section_specs = [("Core metadata", root_scalars)] + [
        (label, [p for p in paths if p[0] == key]) for key, label in [
            ("model_details", "Model details"), ("model_parameters", "Model parameters"),
            ("quantitative_analysis", "Quantitative analysis"), ("considerations", "Considerations"),
            ("model_index", "Benchmark index"), ("mission_relevance", "Mission relevance"),
            ("usage_documentation", "Usage documentation"),
        ]
    ]

    # Shared visual language from data-sheets-schema/scripts/figures/_style.py.
    INK = "#0b0b0b"
    SECONDARY = "#52514e"
    MUTED = "#898781"
    GRID = "#e1e0d9"
    SURFACE = "#fcfcfb"
    EMPTY = "#f0efec"
    BLUE = "#2a78d6"
    NAVY = "#184f95"
    SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
    SCORE_COLORS = [SEQ[i] for i in [3, 4, 6, 8, 10, 12]]
    ramp = LinearSegmentedColormap.from_list("documentation_blue", RAMP_STOPS)
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": METRIC_FONTS, "svg.fonttype": "none",
                         "svg.hashsalt": "model-card-heatmaps", "pdf.fonttype": 42, "axes.unicode_minus": False})
    # Two installs of one font tie in findfont and the font cache's order is random; sorting
    # by path keeps the embedded PDF font stable.
    font_manager.fontManager.ttflist.sort(key=lambda entry: entry.fname)
    fonts = {}
    for weight in ("normal", "bold"):
        font_path = Path(font_manager.findfont(font_manager.FontProperties(family="sans-serif", weight=weight)))
        font = font_manager.get_font(font_path)
        if font.family_name not in METRIC_FONTS or (weight == "bold") != ("Bold" in font.style_name):
            raise SystemExit(f"Heatmap layout needs {' or '.join(METRIC_FONTS)} in regular and bold; "
                             f"found {font.family_name} {font.style_name}. If you just installed one, delete "
                             f"Matplotlib's font cache ({matplotlib.get_cachedir()}/fontlist-*.json) and rerun.")
        fonts[weight] = {"file": font_path.name, "sha256": sha256(font_path)}
    W, H = 2400, 1470
    fig = plt.figure(figsize=(W / 72, H / 72), facecolor=SURFACE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(H, 0))
    ax.axis("off")
    texts = []
    tooltips = {}


    def label(x, y, text, size=12, color=INK, weight="normal", ha="left", va="center", **kwargs):
        t = ax.text(x, y, text, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, linespacing=1.35, **kwargs)
        texts.append(t)
        return t


    def on_fill(color):
        """White or black text, whichever contrasts more with the fill; one always reaches 4.58:1."""
        linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in to_rgb(color)]
        luminance = sum(w * v for w, v in zip((0.2126, 0.7152, 0.0722), linear))
        return "white" if 1.05 / (luminance + 0.05) > (luminance + 0.05) / 0.05 else "black"


    def rect(x, y, w, h, fill, edge="none", lw=0.5, gid=None, tip=None):
        p = Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, linewidth=lw)
        if gid:
            p.set_gid(gid)
            tooltips[gid] = tip
        ax.add_patch(p)
        return p


    def line(x1, y1, x2, y2, color=GRID, lw=0.7):
        ax.plot([x1, x2], [y1, y2], color=color, lw=lw)


    def panel(x, y, letter, title, subtitle):
        label(x, y, letter, 20, BLUE, "bold")
        label(x + 30, y, title, 21, INK, "bold")
        label(x, y + 29, subtitle, 12, SECONDARY)


    def top_bars(cell_x, cw, totals, maximum, names=True):
        top, bottom = 233, 288
        for j, n in enumerate(totals):
            cx = cell_x + j * cw
            if names:
                label(cx + cw / 2, 205, SHORT[j], 10, SECONDARY, "bold", ha="center")
            rect(cx + 15, top, cw - 30, bottom - top, EMPTY)
            h = (bottom - top) * n / maximum
            rect(cx + 15, bottom - h, cw - 30, h, BLUE)
            label(cx + cw / 2, bottom + 13, f"{n / maximum:.1%}", 10.5, NAVY, "bold", ha="center")
            label(cx + cw / 2, bottom + 29, f"{n:g}/{maximum}", 9, SECONDARY, ha="center")
        line(cell_x + 6, bottom, cell_x + cw * 2 - 6, bottom)


    label(48, 51, "Model cards: structured field presence and documentation checks", 31, weight="bold")
    model_ids = [c["model_details"]["path"].removeprefix("https://huggingface.co/").split("/tree/")[0] for c in cards]
    label(48, 91, f"{NAMES[0]} ({model_ids[0]})   |   {NAMES[1]} ({model_ids[1]})", 14, SECONDARY)
    line(48, 119, W - 48, 119, lw=1.5)

    AX, BX, CX = 48, 1140, 1756
    AW, BW, CW = 1056, 580, 596
    panel(AX, 153, "A", "Field-value presence", "Non-empty values at all 126 terminal schema paths; list indices collapsed")
    panel(BX, 153, "B", "rubric10 · hybrid", "50 binary subitems in 10 elements")
    panel(CX, 153, "C", "rubric20 · hybrid", "20 questions: 16 graded 0–5; 4 pass/fail (maximum 84)")
    line(1122, 147, 1122, 1334)
    line(1738, 147, 1738, 1334)

    # Field legends and marginal coverage totals.
    rect(AX, 222, 17, 12, NAVY)
    label(AX + 25, 228, "Populated (non-empty)", 11, SECONDARY)
    rect(AX, 247, 17, 12, EMPTY, GRID)
    label(AX + 25, 253, "Empty or absent", 11, SECONDARY)
    label(AX, 281, "Presence counts structure, not accuracy.", 11, SECONDARY)
    label(AX + 540, 234, "Full field paths are available in the CSV.", 10.5, SECONDARY)
    label(AX + 540, 256, "Labels omit each group’s shared prefix.", 10.5, SECONDARY)
    label(AX + 540, 278, "The same two cards appear in both blocks.", 10.5, SECONDARY)


    def draw_presence(groups, x, width, block):
        cell_x, cw = x + width - 132, 66
        if block == 0:
            top_bars(cell_x, cw, presence_totals, 126)
        else:
            for j in range(2):
                label(cell_x + (j + 0.5) * cw, 306, SHORT[j], 10, SECONDARY, "bold", ha="center")
        y = 339
        for g, prefix, ps in groups:
            rect(x, y, width, 22, "#f2f5f9")
            label(x + 5, y + 11, g, 11, weight="bold")
            for j in range(2):
                total = sum(presence[p][j] for p in ps)
                label(cell_x + (j + 0.5) * cw, y + 11, f"{total}/{len(ps)}", 9, SECONDARY, ha="center")
            y += 25
            for p in ps:
                path = ".".join(p)
                shown = path[len(prefix):] if prefix and path.startswith(prefix) else path
                label(x + 5, y + 6, shown, 8.6, SECONDARY)
                for j in range(2):
                    present = presence[p][j]
                    rect(cell_x + j * cw + 1, y, cw - 2, 11, NAVY if present else EMPTY,
                         gid=f"field_{paths.index(p)}_{j}", tip=f"{NAMES[j]} | {path}: {'populated' if present else 'empty or absent'}")
                y += 12
            y += 5
        return y


    presence_bottom_left = draw_presence(left_groups, AX, 516, 0)
    presence_bottom_right = draw_presence(right_groups, AX + 540, 516, 1)

    note_y = presence_bottom_left + 23
    rect(AX, note_y, 516, 115, "#eef4fb")
    label(AX + 15, note_y + 20, "How to read presence", 12, NAVY, "bold")
    label(AX + 15, note_y + 47, "A path is filled if any list entry has a non-empty value.", 10.5, SECONDARY)
    label(AX + 15, note_y + 68, "Prose elsewhere does not fill a structured field.", 10.5, SECONDARY)
    label(AX + 15, note_y + 89, "Optional fields are retained; no applicability filter is used.", 10.5, SECONDARY)

    # Binary documentation checks from hash-matching deterministic evaluations.
    for k, (color, caption) in enumerate([(SCORE_COLORS[0], "0 · criterion not met"), (NAVY, "1 · criterion met")]):
        rect(BX, 222 + k * 27, 18, 15, color)
        label(BX + 27, 230 + k * 27, caption, 11, SECONDARY)
    label(BX, 286, "Deterministic documentation checks", 10.5, SECONDARY)
    B_CELL, B_CW = BX + BW - 132, 66
    top_bars(B_CELL, B_CW, [r["overall_score"]["total_points"] for r in ratings10], 50)
    groups10 = [
        "Discovery and identification", "Access and distribution", "Reuse and interoperability",
        "Ethics and responsible AI", "Architecture and training composition", "Provenance and versioning",
        "Motivation and funding", "Training and evaluation transparency", "Performance and limitations",
        "Platforms and community integration",
    ]
    labels10 = [
        "Persistent identifier", "Model name and description", "Tags / task discoverability", "Landing page / repository URL", "Library / framework identification",
        "Weight distribution", "Code repository", "Inference API / usage example", "Input / output specification", "Model file format",
        "License permits reuse", "Standard framework / format", "Base-model lineage", "Supported tasks", "Reproducibility artifacts",
        "Ethical considerations", "Model / output bias", "Out-of-scope / discouraged uses", "Sensitive data disclosure", "Intended users / stakeholder impact",
        "Architecture details", "Training data", "Hyperparameters", "Compute infrastructure", "Training / evaluation split",
        "Version number", "Version date", "Version change description", "Owners / contributors", "Citation / BibTeX",
        "Motivation / use-case rationale", "Primary intended use", "Mission relevance", "Funding source / grant agency", "Compute / platform acknowledgements",
        "Training procedure", "Evaluation procedure", "Reproducibility information", "Open-source code", "External standards / references",
        "Quantitative performance metrics", "Performance across slices", "Confidence intervals / error bars", "Limitations", "Tradeoffs / risks",
        "Recognized hosting platform", "Related DOIs / model links", "Structured benchmark results", "Standards / schema conformance", "Dataset / datasheet / D4D links",
    ]
    y = 339
    for group_i, group_name in enumerate(groups10):
        rect(BX, y, BW, 22, "#f2f5f9")
        label(BX + 5, y + 11, f"E{group_i + 1}  {group_name}", 11, weight="bold")
        y += 25
        for sub_i in range(5):
            idx = group_i * 5 + sub_i
            label(BX + 5, y + 7.2, f"{group_i + 1}.{sub_i + 1}  {labels10[idx]}", 10.2, SECONDARY)
            for j in range(2):
                item = r10[j][idx][3]
                value = int(item["score"])
                fill = NAVY if value else SCORE_COLORS[0]
                rect(B_CELL + j * B_CW + 1, y, B_CW - 2, 13.4, fill,
                     gid=f"r10_{idx}_{j}", tip=f"{NAMES[j]} | E{group_i + 1}.{sub_i + 1} {item['name']}: {value}/1\nEvaluation evidence: {item.get('evidence', '')}")
                label(B_CELL + (j + 0.5) * B_CW, y + 6.7, str(value), 9, on_fill(fill), ha="center")
            y += 14.4
        y += 4
    rubric10_bottom = y

    # Graded scores retain their native denominators; rings denote pass/fail.
    label(CX, 218, "Graded score", 10.5, SECONDARY)
    for value, color in enumerate(SCORE_COLORS):
        rect(CX + value * 30, 235, 28, 19, color)
        label(CX + value * 30 + 14, 244.5, str(value), 10, on_fill(color), ha="center")
    ax.add_patch(Circle((CX + 6, 280), radius=4, fill=False, edgecolor=SECONDARY, lw=1))
    label(CX + 20, 280, "Pass/fail: shown as 0/1 or 1/1", 11, SECONDARY)
    C_CELL, C_CW = CX + CW - 144, 72
    top_bars(C_CELL, C_CW, [r["overall_score"]["total_points"] for r in ratings20], 84)
    labels20 = [
        "Required field completeness", "Overview length", "Tag / keyword diversity", "Input / output specification", "Schema version",
        "Persistent identifier", "Funding / acknowledgements", "Ethics / responsible AI", "License / SPDX compliance", "Framework / library standards",
        "Tools / software transparency", "Training procedure", "Version history", "Citations / references", "Compute / energy",
        "Findability / persistent landing", "Access / inference path", "Performance, slices and uncertainty", "Out-of-scope uses / limits / tradeoffs", "Cross-platform links",
    ]
    y = 339
    idx = 0
    for cat in ratings20[0]["categories"]:
        rect(CX, y, CW, 22, "#f2f5f9")
        label(CX + 5, y + 11, cat["name"], 11.5, weight="bold")
        y += 27
        for _ in cat["questions"]:
            label(CX + 5, y + 10.5, f"Q{idx + 1}  {labels20[idx]}", 11, SECONDARY)
            for j in range(2):
                q = r20[j][idx][1]
                value, cap = int(q["score"]), int(q["max_score"])
                fill = SCORE_COLORS[value] if cap == 5 else SCORE_COLORS[-1 if value else 0]
                rect(C_CELL + j * C_CW + 1, y, C_CW - 2, 20, fill,
                     gid=f"r20_{idx}_{j}", tip=f"{NAMES[j]} | Q{q['id']} {q['name']}: {value}/{cap}\nEvaluation evidence: {q.get('evidence', '')}")
                text_color = on_fill(fill)
                label(C_CELL + (j + 0.5) * C_CW, y + 10, f"{value}/{cap}" if cap == 1 else str(value), 10, text_color, ha="center")
                if cap == 1:
                    ax.add_patch(Circle((C_CELL + j * C_CW + 10, y + 10), radius=3.2, fill=False, edgecolor=text_color, lw=0.8))
            y += 21
            idx += 1
        y += 5
    rubric20_bottom = y

    # D4D-style section-level coverage summary.
    dy = rubric20_bottom + 46
    panel(CX, dy, "D", "Field presence by section", "Fraction populated, with counts; same 126-path denominator as A")
    y = dy + 83
    for j in range(2):
        label(C_CELL + (j + 0.5) * C_CW, y - 27, SHORT[j], 10, SECONDARY, "bold", ha="center")
    for label_text, ps in section_specs:
        label(CX + 5, y + 14, label_text, 11.5, SECONDARY)
        for j in range(2):
            n = sum(presence[p][j] for p in ps)
            color = ramp(n / len(ps))
            rect(C_CELL + j * C_CW + 1, y, C_CW - 2, 27, color)
            label(C_CELL + (j + 0.5) * C_CW, y + 13.5, f"{n}/{len(ps)}", 10, on_fill(color), ha="center")
        y += 28
    summary_bottom = y
    training_paths = [p for p in paths if p[:2] == ("model_parameters", "training_procedure")]
    training_counts = [sum(presence[p][j] for p in training_paths) for j in range(2)]
    label(CX, y + 30, f"Training fields: {training_counts[0]}/{len(training_paths)} vs {training_counts[1]}/{len(training_paths)}.", 12, NAVY, "bold")
    compute_paths = [p for p in paths if p[:2] == ("model_parameters", "compute_infrastructure")]
    compute_counts = [sum(presence[p][j] for p in compute_paths) for j in range(2)]
    label(CX, y + 53, f"Compute fields: {compute_counts[0]}/{len(compute_paths)} vs {compute_counts[1]}/{len(compute_paths)}. Original-run records remain unavailable.", 11, SECONDARY)

    line(48, 1372, W - 48, 1372, lw=1.3)
    label(48, 1397, "Presence ≠ documentation quality or model performance. Optional and extension fields are included; absent values are not necessarily defects.", 12, SECONDARY)
    label(48, 1420, "Sources: current YAML + SHA-256-matched hybrid results; current evaluators reproduce every item score. Automated documentation checks, not model performance.", 11, SECONDARY)
    label(48, 1443, "Blue visual language adapted from D4D figures 3 and 5. Editable vector text; full paths, evidence, result hashes and evaluator hashes accompany this figure.", 10.5, SECONDARY)

    # Detect canvas clipping and colliding labels; preserve SVG text rather than rasterizing it.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    outside = []
    for t in texts:
        bounds = t.get_window_extent(renderer).transformed(ax.transData.inverted())
        if bounds.x0 < 0 or bounds.x1 > W or min(bounds.y0, bounds.y1) < 0 or max(bounds.y0, bounds.y1) > H:
            outside.append(t.get_text())
    assert not outside, f"Text outside canvas: {outside}"
    extents = [t.get_window_extent(renderer) for t in texts]
    overlapping = [(texts[a].get_text(), texts[b].get_text()) for a in range(len(texts)) for b in range(a + 1, len(texts))
                   if extents[a].overlaps(extents[b])]
    assert not overlapping, f"Overlapping text: {overlapping[:5]}"
    assert max(presence_bottom_right, rubric10_bottom, summary_bottom + 53) < 1360

    svg_path = OUT / "model_cards_scores_and_field_presence.svg"
    description = "DenseNet-121 and SaProtHub SubCell 650M. Field presence across 126 schema terminal paths; rubric10 and rubric20 deterministic hybrid documentation checks selected by the current YAML SHA-256. These scores do not measure model performance."
    fig.savefig(svg_path, facecolor=SURFACE, metadata={"Title": "Model cards: structured field presence and documentation checks", "Description": description, "Date": None})
    fig.savefig(OUT / "model_cards_scores_and_field_presence.png", dpi=180, facecolor=SURFACE, metadata={"Description": description})
    fig.savefig(OUT / "model_cards_scores_and_field_presence.pdf", facecolor=SURFACE, metadata={"Title": "Model-card field presence and documentation checks", "Subject": description, "CreationDate": None})

    # Add native SVG tooltips, including full rubric item names and stored evidence.
    NS = "http://www.w3.org/2000/svg"
    ET.register_namespace("", NS)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    tree = ET.parse(svg_path)
    root = tree.getroot()
    for node in root.iter():
        gid = node.get("id")
        if gid in tooltips:
            ET.SubElement(node, f"{{{NS}}}title").text = tooltips[gid]
    assert not list(root.iter(f"{{{NS}}}image")), "Expected pure vector output."
    tree.write(svg_path, encoding="utf-8", xml_declaration=True)

    with (OUT / "field_presence.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["schema_path", *STEMS])
        writer.writerows([".".join(p), *presence[p]] for p in ordered_paths)
    with (OUT / "scores.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rubric", "group", "item_id", "item_name", "max_score", *STEMS])
        for idx, (e, s, group, item) in enumerate(r10[0]):
            writer.writerow(["rubric10_hybrid", group, f"E{e}.{s}", item["name"], 1, *[r10[j][idx][3]["score"] for j in range(2)]])
        for idx, (group, q) in enumerate(r20[0]):
            writer.writerow(["rubric20_hybrid", group, f"Q{q['id']}", q["name"], q["max_score"], *[r20[j][idx][1]["score"] for j in range(2)]])


    def coverage(group_paths):
        return [sum(presence[p][j] for p in group_paths) for j in range(2)]

    figure_data = {
        "generated_at": generated_at,
        "method": "Current YAML field presence and hash-matching deterministic hybrid documentation checks",
        "models": [
            {
                "stem": stem,
                "label": NAMES[j],
                "repository_id": model_ids[j],
                "yaml_sha256": SOURCES[f"data/model_cards_assistant/{stem}_model_card.yaml"]["sha256"],
                "presence": {"count": presence_totals[j], "total": len(paths)},
                "rubrics": {
                    rubric: {
                        "score": reports[j]["overall_score"]["total_points"],
                        "max_score": reports[j]["overall_score"]["max_points"],
                        "result_path": selections[rubric][j]["path"],
                        "result_sha256": selections[rubric][j]["sha256"],
                    }
                    for rubric, reports in [("rubric10", ratings10), ("rubric20", ratings20)]
                },
            }
            for j, stem in enumerate(STEMS)
        ],
        "sections": [
            {"key": "core_metadata" if i == 0 else ps[0][0], "label": name, "total": len(ps), "counts": coverage(ps)}
            for i, (name, ps) in enumerate(section_specs)
        ],
        "display_groups": [
            {"key": name.lower().replace(",", "").replace("/", "").replace(" ", "_"), "label": name, "total": len(ps), "counts": coverage(ps)}
            for name, _, ps in left_groups + right_groups
        ],
        "caveats": [
            "Prose in another field does not populate a missing structured field; any non-empty value counts.",
            "All optional and extension fields are included without applicability filtering.",
            "Hybrid scores are automated documentation checks, not model capability or an independent semantic review.",
        ],
    }
    provenance = {
        "generated_at": generated_at,
        # The configured remote (read without insteadOf expansion, credentials removed), never
        # the local checkout path, which would publish a home directory.
        "source_repository": public_remote(git("config", "--get", "remote.origin.url")) if in_git else None,
        "checkout_commit": git("rev-parse", "HEAD") if in_git else None,
        "source_revision_note": "Input file SHA-256 values identify the actual workspace bytes; each input's committed flag says whether it was tracked and unmodified at the checkout commit.",
        "matplotlib_version": matplotlib.__version__,
        "fonts": fonts,
        "files": SOURCES,
        "selection": selections,
        "selection_policy": "Only exact current-card SHA-256 matches from deterministic hybrid evaluators; choose latest timestamp and reject conflicting tied results.",
        "evaluator_verification": "Current evaluator scripts were re-executed locally; all item/category scores, evidence, overall scores and assessments match the selected reports. No historical evaluator hash is inferred.",
        "presence_definition": "Traverse all terminal field paths from modelCard; collapse list indices; any nonempty resolved value fills a path. Whitespace, null and empty collections are absent. Zero and false are values. No prose inference or applicability filtering.",
        "schema_terminal_path_count": len(paths),
        "presence_counts": dict(zip(STEMS, presence_totals)),
        "root_slot_counts": dict(zip(STEMS, [sum(populated(c, (s,)) for s, _ in slots('modelCard')) for c in cards])),
        "root_slot_denominator": len(slots('modelCard')),
        "limitations": figure_data["caveats"],
        # Reports are embedded whole, except that model_card_file is made repository-relative.
        "rubric10": [{**report, "model_card_file": f"data/model_cards_assistant/{stem}_model_card.yaml"} for stem, report in zip(STEMS, ratings10)],
        "rubric20": [{**report, "model_card_file": f"data/model_cards_assistant/{stem}_model_card.yaml"} for stem, report in zip(STEMS, ratings20)],
        "validation": {
            "all_selected_card_hashes_match": True,
            "all_selected_results_reproduced": True,
            "all_text_within_canvas": not outside,
            "svg_contains_raster_images": False,
            "png_dpi": 180,
            "panel_bottoms": [presence_bottom_left, presence_bottom_right, rubric10_bottom, rubric20_bottom, summary_bottom],
        },
    }
    for name, document in (("provenance.json", provenance), ("figure_data.json", figure_data)):
        if str(Path.home()) in json.dumps(document):
            raise SystemExit(f"{name} would publish a home-directory path; not writing it.")
    (OUT / "figure_data.json").write_text(json.dumps(figure_data, indent=2) + "\n")
    (OUT / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    plt.close(fig)
    print(json.dumps({"output_dir": str(OUT), "presence": presence_totals, "rubric10": [r['overall_score']['total_points'] for r in ratings10], "rubric20": [r['overall_score']['total_points'] for r in ratings20], "selected_results": selections}, indent=2))


if __name__ == "__main__":
    main()
