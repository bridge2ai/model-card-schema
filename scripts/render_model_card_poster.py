#!/usr/bin/env python3
"""Render a compact poster figure from the detailed heatmap's verified data.

The upstream builder performs card/schema/evaluation checks. This renderer keeps
the same measurements while replacing individual fields with section totals.
Place model_cards_poster_transparent.png on the Bridge2AI Standards Portfolio poster;
the teal PNG, SVG and PDF are for standalone use. The layout needs Arial or a
metric-compatible font (Liberation Sans, Arimo).
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
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import FancyBboxPatch, Rectangle

# BACKGROUND is the Model Cards panel of the Bridge2AI Standards Portfolio poster
# (#EEF7FD at 11% opacity) composited over the page gradient behind this figure. Text on
# it uses the poster's light ink; the heatmap keeps its white box and dark-is-higher scale.
BACKGROUND = "#2f719a"
ON_BACKGROUND = "#eef7fd"
INK = "#10263d"
MUTED = "#506174"
BLUE = "#2a78d6"
NAVY = "#184f95"
PALE = "#f0efec"
GRID = "#e0e6ed"
W, H = 1600, 1080
# The poster's srcRect crops 13.465% off the top and 13.829% off the bottom; the white
# box is centered in what remains.
CROP_TOP, CROP_BOTTOM = 0.13465 * H, (1 - 0.13829) * H
BOX_LEFT, BOX_RIGHT, BOX_TOP, BOX_BOTTOM, BOX_PADDING = 22, W - 22, 163, 913, 12
# Every label position assumes Arial's advance widths.
METRIC_FONTS = ["Arial", "Liberation Sans", "Arimo"]

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
    """Choose dark ink or white by actual relative-luminance contrast."""
    def luminance(color):
        linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in color[:3]]
        return sum(weight * value for weight, value in zip((0.2126, 0.7152, 0.0722), linear))

    background = luminance(rgb)
    foreground = luminance(to_rgb(INK))
    dark_contrast = (max(background, foreground) + 0.05) / (min(background, foreground) + 0.05)
    return "white" if (1.05 / (background + 0.05)) > dark_contrast else INK


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

    # Matplotlib reads only the regular face of macOS's Helvetica Neue .ttc, which silently
    # rendered every bold label as regular, so it is not a fallback here.
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": METRIC_FONTS,
        "svg.fonttype": "none", "svg.hashsalt": "model-card-poster", "pdf.fonttype": 42, "axes.unicode_minus": False,
    })
    for weight in ("normal", "bold"):
        font = font_manager.get_font(font_manager.findfont(font_manager.FontProperties(family="sans-serif", weight=weight)))
        if font.family_name not in METRIC_FONTS or (weight == "bold") != ("Bold" in font.style_name):
            raise ValueError(f"Poster layout needs {' or '.join(METRIC_FONTS)} in regular and bold; "
                             f"found {font.family_name} {font.style_name}")
    model_labels = [model["label"] for model in models]
    fig = plt.figure(figsize=(16, 10.8), facecolor=BACKGROUND)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(H, 0))
    ax.axis("off")
    texts, tips = [], {}
    cmap = LinearSegmentedColormap.from_list("documentation_blue", [PALE, "#9ec5f4", BLUE, "#104281"])

    def label(x, y, text, size=19, color=INK, weight="normal", ha="left", va="center"):
        item = ax.text(x, y, text, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, linespacing=1.25)
        texts.append(item)
        return item

    def cell(x, y, width, height, fraction, gid, tip):
        patch = Rectangle((x, y), width, height, facecolor=cmap(fraction), edgecolor="white", linewidth=2)
        patch.set_gid(gid)
        ax.add_patch(patch)
        tips[gid] = tip
        return contrast_color(cmap(fraction))

    label(58, 60, "Model-card documentation", 34, ON_BACKGROUND, "bold")
    label(58, 111, "Current cards · automated rubric checks", 18, ON_BACKGROUND)
    ax.add_patch(FancyBboxPatch((BOX_LEFT, BOX_TOP), BOX_RIGHT - BOX_LEFT, BOX_BOTTOM - BOX_TOP,
                                boxstyle="round,pad=0,rounding_size=18", facecolor="white", edgecolor="none"))

    label(58, 207, "Field coverage", 26, weight="bold")
    label(978, 207, "Evaluating the quality of content", 26, weight="bold")
    label(58, 262, "Model Card Modules", 18, weight="bold")
    for col, name in enumerate(model_labels):
        label(480 + 195 * col, 262, name, 18, weight="bold", ha="center")
        label(1122 + 226 * col, 262, name, 18, weight="bold", ha="center")

    row_y, row_h = 298, 46
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
    label(58, 794, "All fields", 20, weight="bold")
    for col, model in enumerate(models):
        coverage = model["presence"]
        center = 480 + 195 * col
        label(center, 790, f"{coverage['count'] / coverage['total']:.0%}", 29, NAVY, "bold", ha="center")
        label(center, 830, f"{coverage['count']}/{coverage['total']}", 18, MUTED, ha="center")

    for row, (key, name) in enumerate((("rubric10", "Rubric 10"), ("rubric20", "Rubric 20"))):
        y = 338 + row * 250
        label(978, y - 29, name, 21, weight="bold")
        for col, model in enumerate(models):
            metric = model["rubrics"][key]
            fraction = metric["score"] / metric["max_score"]
            x = 1010 + 226 * col
            color = cell(x, y, 220, 170, fraction, f"rubric-{key}-{col}",
                         f"{model_labels[col]} — {name}, deterministic hybrid: {metric['score']}/{metric['max_score']}")
            label(x + 110, y + 71, f"{fraction:.0%}", 36, color, "bold", ha="center")
            label(x + 110, y + 126, f"{metric['score']}/{metric['max_score']}", 21, color, ha="center")

    ax.plot([872, 872], [200, 848], color=GRID, linewidth=1)

    # One legend for both panels: the ramp is centered on the figure.
    legend_y, bar_left, bar_width = 878, W / 2 - 120, 240
    step = bar_width / 80
    for stop in range(80):
        ax.add_patch(Rectangle((bar_left + stop * step, legend_y - 11), step + 0.1, 22, facecolor=cmap(stop / 79), edgecolor="none"))
    lower = label(bar_left - 14, legend_y, "Lower", 18, MUTED, ha="right")
    label(bar_left + bar_width + 14, legend_y, "Higher", 18, MUTED)
    fig.canvas.draw()
    lower_left = lower.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted()).x0
    label(lower_left - 36, legend_y, "Shade = fraction of maximum (both panels)", 18, MUTED, ha="right")

    label(58, 975, "Presence includes optional fields; an empty field is not necessarily a defect.", 18, ON_BACKGROUND)
    label(58, 1012, "Documentation measures, not model performance. No new semantic scoring.", 18, ON_BACKGROUND)

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
    if not CROP_TOP <= BOX_TOP < BOX_BOTTOM <= CROP_BOTTOM:
        raise ValueError("White box extends past the poster's crop")
    for item in texts:
        x0, y0, x1, y1 = item.get_window_extent(renderer).transformed(ax.transData.inverted()).extents
        top, bottom = min(y0, y1), max(y0, y1)
        if item.get_color() == ON_BACKGROUND:
            if bottom > BOX_TOP and top < BOX_BOTTOM:
                raise ValueError(f"Poster text overlaps the white box: {item.get_text()}")
        elif (x0 < BOX_LEFT + BOX_PADDING or x1 > BOX_RIGHT - BOX_PADDING
              or top < BOX_TOP + BOX_PADDING or bottom > BOX_BOTTOM - BOX_PADDING):
            raise ValueError(f"Poster text leaves the white box: {item.get_text()}")

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / "model_cards_poster"
    transparent_path = output_dir / "model_cards_poster_transparent.png"
    fig.savefig(stem.with_suffix(".svg"), facecolor=BACKGROUND, metadata={"Date": None})
    fig.savefig(stem.with_suffix(".pdf"), facecolor=BACKGROUND,
                metadata={"Title": "Model-card documentation: poster summary", "CreationDate": None})
    fig.savefig(stem.with_suffix(".png"), dpi=300, facecolor=BACKGROUND)
    # The poster's panel gradient shows through the transparent canvas; the white box stays opaque.
    fig.savefig(transparent_path, dpi=300, transparent=True)
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
        "files": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in [stem.with_suffix(ext) for ext in (".png", ".svg", ".pdf")] + [transparent_path]},
    }
    (output_dir / "poster_provenance.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Poster exported: {stem}.{{png,svg,pdf}} and {transparent_path.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="figure_data.json from build_model_card_heatmaps.py")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    render(args.input, args.output_dir)


if __name__ == "__main__":
    main()
