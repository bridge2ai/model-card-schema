#!/usr/bin/env python3
"""Compare revised cards with the supplied heatmap's immutable baseline.

Recomputes field presence and the existing deterministic hybrid rubrics on both
revisions. Archived semantic ratings are not reassigned to the revised cards.
Run from the repository root. No network access or model inference is needed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import yaml

STEMS = ("densenet121_tv_in1k", "subcell_saprot_650m")
NAMES = ("DenseNet-121", "SubCell / SaProt 650M")
SECTIONS = {
    "core": "Core metadata",
    "model_details": "Model details",
    "model_parameters": "Model parameters",
    "quantitative_analysis": "Quantitative analysis",
    "considerations": "Considerations",
    "model_index": "Benchmark index",
    "mission_relevance": "Mission relevance",
    "usage_documentation": "Usage documentation",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def leaf_paths(schema, class_name="modelCard", prefix=(), ancestors=()):
    """Use the supplied figure's traversal and fail on unsupported inheritance."""
    cls = schema["classes"][class_name]
    if cls.get("is_a") or cls.get("mixins") or class_name in ancestors:
        raise ValueError("Schema inheritance/recursion requires an explicit traversal policy")
    paths = []
    for name in cls.get("slots", []):
        spec = {**schema["slots"][name], **cls.get("slot_usage", {}).get(name, {})}
        path = prefix + (name,)
        if spec.get("range") in schema["classes"]:
            paths.extend(leaf_paths(schema, spec["range"], path, ancestors + (class_name,)))
        else:
            paths.append(path)
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
            return any(populated(value, ()) for value in obj.values())
        return True  # Numeric zero and boolean false are populated values.
    return isinstance(obj, dict) and path[0] in obj and populated(obj[path[0]], path[1:])


def validate_declared_fields(schema, obj, class_name="modelCard", prefix=()):
    if isinstance(obj, list):
        for value in obj:
            validate_declared_fields(schema, value, class_name, prefix)
        return
    if not isinstance(obj, dict):
        raise ValueError(f"Expected structured object at {prefix}")
    cls = schema["classes"][class_name]
    unknown = set(obj) - set(cls.get("slots", []))
    if unknown:
        raise ValueError(f"Undeclared fields at {prefix}: {sorted(unknown)}")
    for name, value in obj.items():
        spec = {**schema["slots"][name], **cls.get("slot_usage", {}).get(name, {})}
        if value is not None and spec.get("range") in schema["classes"]:
            validate_declared_fields(schema, value, spec["range"], prefix + (name,))


def load_evaluator(rubric):
    path = Path(f"scripts/batch_evaluate_mc_{rubric}_hybrid.py")
    spec = importlib.util.spec_from_file_location(rubric, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def plot_presence(summary, output):
    os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/model-card-remediation-matplotlib")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    plt.rcParams["svg.fonttype"] = "none"
    cmap = LinearSegmentedColormap.from_list("presence", ["#f0efec", "#2a78d6", "#104281"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 7), layout="constrained")
    for axis, name, stem in zip(axes, NAMES, STEMS):
        card = summary["cards"][stem]
        groups = list(card["sections"].values())
        grid = [[group[state] / group["total"] for state in ("before", "after")] for group in groups]
        axis.imshow(grid, vmin=0, vmax=1, cmap=cmap, aspect="auto")
        axis.set_xticks([0, 1], ["Before", "After"])
        axis.xaxis.tick_top()
        axis.set_yticks(range(len(groups)), SECTIONS.values())
        axis.tick_params(length=0)
        for row, group in enumerate(groups):
            for col, state in enumerate(("before", "after")):
                axis.text(col, row, f"{group[state]}/{group['total']}", ha="center", va="center",
                          color="white" if grid[row][col] > 0.5 else "#111111")
        presence = card["presence"]
        axis.set_title(f"{name}\n{presence['before']}/{presence['total']} → {presence['after']}/{presence['total']} fields", pad=16)
        for spine in axis.spines.values():
            spine.set_visible(False)
    fig.suptitle("Model-card documentation: populated schema fields", fontsize=16)
    fig.supxlabel("Optional fields remain in the denominator. Presence is not evidence quality or model performance.\nNo new semantic ratings are shown.", fontsize=10)
    fig.savefig(output / "field_presence_comparison.svg")
    fig.savefig(output / "field_presence_comparison.png", dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-dir", type=Path, default=Path("notes/model_card_remediation/baseline"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/evaluation/remediation/2026-09-28"))
    args = parser.parse_args()
    baseline = json.loads((args.baseline_dir / "provenance.json").read_text())
    schema_path = Path(baseline["schema_path"])
    if sha256(schema_path) != baseline["schema_sha256"]:
        raise ValueError("Schema differs from supplied figure; reconcile denominators first")
    for name, record in baseline["files"].items():
        if sha256(args.baseline_dir / name) != record["sha256"]:
            raise ValueError(f"Baseline input changed: {name}")
    schema = yaml.safe_load(schema_path.read_bytes())
    paths = leaf_paths(schema)
    with (args.baseline_dir / "field_presence.csv").open(newline="") as stream:
        original_presence = {row["schema_path"]: row for row in csv.DictReader(stream)}
    if {".".join(path) for path in paths} != set(original_presence):
        raise ValueError("Schema paths differ from supplied figure")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_commit": baseline["source_commit"],
        "schema_sha256": sha256(schema_path),
        "analysis_script_sha256": sha256(Path(__file__)),
        "method": "Field presence plus paired deterministic hybrid evaluations; no new semantic/LLM evaluation",
        "cards": {},
    }
    rows = {path: {"schema_path": ".".join(path)} for path in paths}
    for stem in STEMS:
        before_path = args.baseline_dir / f"{stem}_model_card.yaml"
        after_path = Path("data/model_cards_assistant") / before_path.name
        before_raw, after_raw = before_path.read_bytes(), after_path.read_bytes()
        before = yaml.safe_load(before_raw)
        after = yaml.safe_load(after_raw)
        validate_declared_fields(schema, before)
        validate_declared_fields(schema, after)
        groups = {key: {"before": 0, "after": 0, "total": 0} for key in SECTIONS}
        for path in paths:
            old, new = int(populated(before, path)), int(populated(after, path))
            if old != int(original_presence[".".join(path)][stem]):
                raise ValueError(f"Baseline presence does not reproduce figure: {stem}, {path}")
            rows[path].update({f"{stem}_before": old, f"{stem}_after": new})
            group = groups["core" if len(path) == 1 else path[0]]
            group["before"] += old
            group["after"] += new
            group["total"] += 1
        card = {
            "before_path": str(before_path), "after_path": str(after_path),
            "before_sha256": hashlib.sha256(before_raw).hexdigest(),
            "after_sha256": hashlib.sha256(after_raw).hexdigest(),
            "presence": {state: sum(group[state] for group in groups.values()) for state in ("before", "after", "total")},
            "sections": groups, "hybrid": {},
        }
        for rubric in ("rubric10", "rubric20"):
            evaluator, evaluator_path = load_evaluator(rubric)
            scores = {}
            for state, card_path in (("before", before_path), ("after", after_path)):
                result = evaluator.evaluate_one(card_path)
                if "error" in result:
                    raise ValueError(result["error"])
                if result["metadata"]["model_card_hash"] != card[f"{state}_sha256"]:
                    raise ValueError(f"Card changed during analysis; retry after edits finish: {card_path}")
                result["metadata"].update({"evaluator_sha256": sha256(evaluator_path), "schema_sha256": sha256(schema_path)})
                folder = args.output_dir / state / rubric
                folder.mkdir(parents=True, exist_ok=True)
                suffix = "_evaluation.json" if rubric == "rubric10" else "_rubric20_evaluation.json"
                target = folder / (card_path.stem + suffix)
                target.write_text(json.dumps(result, indent=2) + "\n")
                scores[state] = {**{key: result["overall_score"][key] for key in ("total_points", "max_points", "percentage")}, "evaluation": str(target)}
            card["hybrid"][rubric] = scores
        summary["cards"][stem] = card
    with (args.output_dir / "field_presence.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(next(iter(rows.values()))))
        writer.writeheader()
        writer.writerows(rows.values())
    (args.output_dir / "comparison.json").write_text(json.dumps(summary, indent=2) + "\n")
    plot_presence(summary, args.output_dir)
    for name, stem in zip(NAMES, STEMS):
        card = summary["cards"][stem]
        print(f"{name}: presence {card['presence']}; hybrid scores {card['hybrid']}")


if __name__ == "__main__":
    main()
