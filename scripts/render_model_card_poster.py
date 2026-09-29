#!/usr/bin/env python3
"""Render a compact poster figure from the detailed heatmap's verified data.

The upstream builder performs card/schema/evaluation checks. This renderer keeps
the same measurements while replacing individual fields with section totals.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/model-card-heatmap-matplotlib")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import Rectangle

# Colors from the Bridge2AI Standards Portfolio poster. BACKGROUND is the Model Cards
# panel (#EEF7FD at 11% opacity) composited over the page gradient behind this figure.
BACKGROUND = "#2f719a"
INK = "#eef7fd"
MUTED = "#b3d0e2"
GRID = "#4e85ad"
CELL_INK = "#061f3a"
# Lighter = higher: dark blues vanish on this mid-tone teal. Stops are spaced by OKLCH
# lightness; the lowest keeps 2.1:1 contrast with BACKGROUND.
SCALE = [(0.0, "#6da7ec"), (0.185, "#86b6ef"), (0.374, "#9ec5f4"), (0.555, "#b7d3f6"), (0.740, "#cde2fb"), (1.0, "#eef7fd")]
W, H = 1600, 1080

SHORT_LABELS = {
    "Core metadata": "Core metadata",
    "Model details": "Model identity",
    "Architecture, data and I/O": "Architecture & data",
    "Compute infrastructure": "Compute",
    "Training procedure": "Training",
    "Quantitative analysis": "Evaluation",
    "Considerations": "Use & risks",
    "Benchmark index": "Benchmark results",
    "Mission relevance": "Mission context",
    "Usage documentation": "Usage",
}


def contrast_color(rgb):
    """Choose light or dark ink by actual relative-luminance contrast."""
    def luminance(color):
        linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in color[:3]]
        return sum(weight * value for weight, value in zip((0.2126, 0.7152, 0.0722), linear))

    def contrast(ink):
        pair = (luminance(rgb), luminance(to_rgb(ink)))
        return (max(pair) + 0.05) / (min(pair) + 0.05)

    return max((INK, CELL_INK), key=contrast)


def render(input_path, output_dir):
    data_bytes = input_path.read_bytes()
    data = json.loads(data_bytes)
    models = data["models"]
    groups = data["display_groups"]
    if len(models) != 2 or len(groups) != 10:
        raise ValueError("This layout requires two models and ten field groups")
    for col, model in enumerate(models):
        if sum(group["total"] for group in groups) != model["presence"]["total"]:
            raise ValueError("Poster groups do not partition the field denominator")
        if sum(group["counts"][col] for group in groups) != model["presence"]["count"]:
            raise ValueError("Poster group counts disagree with the detailed figure")
        for rubric in model["rubrics"].values():
            if not 0 <= rubric["score"] <= rubric["max_score"]:
                raise ValueError("Invalid rubric total")
    for group in groups:
        if group["label"] not in SHORT_LABELS or any(not 0 <= count <= group["total"] for count in group["counts"]):
            raise ValueError("Unexpected section or count")

    # Arial first: Matplotlib reads only the regular face of macOS's Helvetica Neue .ttc,
    # which silently rendered every bold label as regular.
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica Neue", "DejaVu Sans"],
        "svg.fonttype": "none", "pdf.fonttype": 42, "axes.unicode_minus": False,
    })
    fig = plt.figure(figsize=(16, 10.8), facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(H, 0))
    ax.axis("off")
    texts, tips = [], {}
    cmap = LinearSegmentedColormap.from_list("documentation_blue", SCALE)

    def label(x, y, text, size=19, color=INK, weight="normal", ha="left", va="center"):
        item = ax.text(x, y, text, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, linespacing=1.25)
        texts.append(item)
        return item

    def cell(x, y, width, height, fraction, gid, tip):
        patch = Rectangle((x, y), width, height, facecolor=cmap(fraction), edgecolor=BACKGROUND, linewidth=2)
        patch.set_gid(gid)
        ax.add_patch(patch)
        tips[gid] = tip
        return contrast_color(cmap(fraction))

    label(58, 60, "Model-card documentation", 34, weight="bold")
    label(58, 111, "Current cards · automated rubric checks", 18, MUTED)
    ax.plot([58, 1542], [150, 150], color=GRID, linewidth=1.2)

    label(58, 198, "Field coverage", 26, weight="bold")
    label(978, 198, "Evaluating the quality of content", 26, weight="bold")
    label(58, 258, "Model Card Modules", 18, weight="bold")
    model_labels = ["DenseNet-121", "SubCell 650M"]
    for col, name in enumerate(model_labels):
        label(480 + 195 * col, 258, name, 18, weight="bold", ha="center")
        label(1122 + 226 * col, 258, name, 18, weight="bold", ha="center")

    row_y, row_h = 300, 49
    for index, group in enumerate(groups):
        y = row_y + index * row_h
        label(58, y + row_h / 2, SHORT_LABELS[group["label"]], 19)
        for col, count in enumerate(group["counts"]):
            x = 385 + 195 * col
            fraction = count / group["total"]
            color = cell(x, y, 190, row_h, fraction, f"section-{index}-{col}",
                         f"{model_labels[col]} — {group['label']}: {count}/{group['total']} populated terminal schema paths")
            label(x + 95, y + row_h / 2, f"{count}/{group['total']}", 20, color, "bold", ha="center")

    # Totals retain the same denominator as the detailed field-level figure.
    label(58, 826, "All fields", 20, weight="bold")
    for col, model in enumerate(models):
        coverage = model["presence"]
        center = 480 + 195 * col
        label(center, 822, f"{coverage['count'] / coverage['total']:.0%}", 29, weight="bold", ha="center")
        label(center, 862, f"{coverage['count']}/{coverage['total']}", 18, MUTED, ha="center")

    for row, (key, name) in enumerate((("rubric10", "Rubric 10"), ("rubric20", "Rubric 20"))):
        y = 340 + row * 260
        label(978, y - 29, name, 21, weight="bold")
        for col, model in enumerate(models):
            metric = model["rubrics"][key]
            fraction = metric["score"] / metric["max_score"]
            x = 1010 + 226 * col
            color = cell(x, y, 220, 178, fraction, f"rubric-{key}-{col}",
                         f"{model_labels[col]} — {name}, deterministic hybrid: {metric['score']}/{metric['max_score']}")
            label(x + 110, y + 74, f"{fraction:.0%}", 36, color, "bold", ha="center")
            label(x + 110, y + 132, f"{metric['score']}/{metric['max_score']}", 21, color, ha="center")

    ax.plot([872, 872], [200, 880], color=GRID, linewidth=1)

    # One legend for both panels, centered and above y=931 so the Standards Portfolio
    # poster's center crop of this figure keeps it.
    legend_y, bar_width = 906, 240
    parts = [label(0, legend_y, "Shade = fraction of maximum (both panels)", 16), label(0, legend_y, "Lower", 16),
             None, label(0, legend_y, "Higher", 16)]
    gaps = [48, 16, 16, 0]
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    widths = [bar_width if part is None else part.get_window_extent(renderer).transformed(ax.transData.inverted()).width
              for part in parts]
    x = (W - sum(widths) - sum(gaps)) / 2
    for part, width, gap in zip(parts, widths, gaps):
        if part is None:
            step = bar_width / 80
            for stop in range(80):
                ax.add_patch(Rectangle((x + stop * step, legend_y - 10), step + 0.1, 20, facecolor=cmap(stop / 79), edgecolor="none"))
        else:
            part.set_x(x)
        x += width + gap

    ax.plot([58, 1542], [947, 947], color=GRID, linewidth=1.2)
    label(58, 983, "Presence includes optional fields; an empty field is not necessarily a defect.", 18, MUTED)
    label(58, 1020, "Documentation measures, not model performance. No new semantic scoring.", 18, MUTED)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas = fig.bbox
    for item in texts:
        box = item.get_window_extent(renderer)
        if box.x0 < canvas.x0 or box.x1 > canvas.x1 or box.y0 < canvas.y0 or box.y1 > canvas.y1:
            raise ValueError(f"Poster text clipped: {item.get_text()}")
    for first, a in enumerate(texts):
        for b in texts[first + 1:]:
            if a.get_window_extent(renderer).overlaps(b.get_window_extent(renderer)):
                raise ValueError(f"Poster text overlaps: {a.get_text()!r}, {b.get_text()!r}")

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / "model_cards_poster"
    fig.savefig(stem.with_suffix(".svg"), facecolor=BACKGROUND)
    fig.savefig(stem.with_suffix(".pdf"), facecolor=BACKGROUND, metadata={"Title": "Model-card documentation: poster summary"})
    fig.savefig(stem.with_suffix(".png"), dpi=300, facecolor=BACKGROUND)
    plt.close(fig)
    svg_path = stem.with_suffix(".svg")
    namespace = "http://www.w3.org/2000/svg"
    ET.register_namespace("", namespace)
    tree = ET.parse(svg_path)
    for node in tree.iter():
        if node.tag == f"{{{namespace}}}image":
            raise ValueError("Poster SVG must contain only vector artwork")
        if node.get("id") in tips:
            title = ET.Element(f"{{{namespace}}}title")
            title.text = tips[node.get("id")]
            node.insert(0, title)
    tree.write(svg_path, encoding="utf-8", xml_declaration=True)
    metadata = {
        "input": input_path.name, "input_sha256": hashlib.sha256(data_bytes).hexdigest(),
        "renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "Same counts and hybrid totals as detailed figure; section-level aggregation only",
        "percentage_display": "Rounded to whole percentages; exact fractions retained in every cell",
        "files": {str(stem.with_suffix(ext).name): hashlib.sha256(stem.with_suffix(ext).read_bytes()).hexdigest() for ext in (".png", ".svg", ".pdf")},
    }
    (output_dir / "poster_provenance.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Poster exported: {stem}.{{png,svg,pdf}}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="figure_data.json from build_model_card_heatmaps.py")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    render(args.input, args.output_dir)


if __name__ == "__main__":
    main()
