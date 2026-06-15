#!/usr/bin/env python3
"""
Render Model Card rubric evaluation JSONs to a single HTML report.

Handles both rubric10 (10 elements × 5 sub-elements, 50 pts) and
rubric20 (4 categories × 5 questions, 84 pts) shapes — including the
semantic variants which add a `semantic_analysis` block per row.

Usage:
    poetry run python scripts/render_evaluation_html.py \\
        --input-glob 'data/evaluation/rubric10/*.json' \\
        --output data/evaluation/rubric10/report.html

    # Mix rubrics — they render in separate sections
    poetry run python scripts/render_evaluation_html.py \\
        --input data/evaluation/rubric10/foo_evaluation.json \\
        --input data/evaluation/rubric20/foo_rubric20_evaluation.json \\
        --output data/evaluation/report.html
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CSS = """
:root {
  --good: #16a34a; --ok: #ca8a04; --bad: #dc2626;
  --bg: #fafafa; --card: #fff; --border: #e5e5e5; --muted: #6b7280;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg); color: #111;
  margin: 0; padding: 2rem 1.5rem; line-height: 1.5;
}
header {
  max-width: 1200px; margin: 0 auto 2rem;
}
h1 { font-size: 1.75rem; margin: 0 0 .25rem; }
h2 { font-size: 1.35rem; margin: 2rem 0 .75rem; padding-bottom: .35rem; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.05rem; margin: 1.25rem 0 .5rem; }
.meta { color: var(--muted); font-size: .9rem; }
main { max-width: 1200px; margin: 0 auto; }

.summary-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem; margin-bottom: 1.5rem;
}
.summary-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 1rem;
}
.summary-card h4 { margin: 0 0 .5rem; font-size: .95rem; font-weight: 600; }
.summary-card .file { color: var(--muted); font-size: .8rem; word-break: break-all; }
.score-big {
  display: flex; align-items: baseline; gap: .5rem; margin-top: .5rem;
}
.score-big .pct { font-size: 1.5rem; font-weight: 700; }
.score-big .raw { color: var(--muted); font-size: .9rem; }

.bar { background: #f3f4f6; border-radius: 4px; height: 8px; overflow: hidden; margin-top: .4rem; }
.bar > div { height: 100%; transition: width .2s; }
.bar.good > div { background: var(--good); }
.bar.ok   > div { background: var(--ok); }
.bar.bad  > div { background: var(--bad); }

details { margin: .75rem 0; background: var(--card); border: 1px solid var(--border); border-radius: 6px; }
details > summary {
  padding: .65rem .9rem; cursor: pointer; list-style: none;
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
}
details > summary::-webkit-details-marker { display: none; }
details[open] > summary { border-bottom: 1px solid var(--border); }
.elem-name { font-weight: 600; }
.elem-score { font-weight: 600; font-variant-numeric: tabular-nums; }
.elem-score.good { color: var(--good); }
.elem-score.ok   { color: var(--ok); }
.elem-score.bad  { color: var(--bad); }

table { width: 100%; border-collapse: collapse; margin: 0; }
th, td { padding: .55rem .9rem; text-align: left; vertical-align: top; border-top: 1px solid var(--border); font-size: .9rem; }
th { background: #f9fafb; font-weight: 600; }
td.score, th.score { text-align: right; width: 70px; font-variant-numeric: tabular-nums; }
td.score.good { color: var(--good); font-weight: 600; }
td.score.bad  { color: var(--bad); font-weight: 600; }
td.evidence { color: var(--muted); font-family: ui-monospace, "SF Mono", monospace; font-size: .8rem; }
td .note { color: #374151; }

.assessment {
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin: 1.5rem 0;
}
@media (max-width: 800px) { .assessment { grid-template-columns: 1fr; } }
.assessment .col {
  background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: .9rem 1rem;
}
.assessment h4 { margin: 0 0 .5rem; font-size: .95rem; }
.assessment ul { margin: 0; padding-left: 1.25rem; font-size: .88rem; }
.assessment li { margin-bottom: .35rem; }

.section-tag {
  display: inline-block; font-size: .75rem; font-weight: 600; padding: .15rem .5rem;
  border-radius: 4px; background: #eff6ff; color: #1e3a8a; margin-right: .5rem;
}
.section-tag.semantic { background: #f3e8ff; color: #6b21a8; }
.section-tag.r20 { background: #ecfeff; color: #155e75; }

.semantic-analysis {
  background: #faf5ff; border-left: 3px solid #a855f7;
  margin: .35rem 0 0; padding: .5rem .75rem; font-size: .82rem; color: #4c1d95;
  border-radius: 0 4px 4px 0;
}
.error {
  background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px;
  padding: 1rem; color: #991b1b; margin: 1rem 0;
}
.error code { background: #fff1f2; padding: 0 .35rem; border-radius: 3px; }

/* Comparison view */
.compare-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 1rem 1.25rem; margin: 1.25rem 0;
}
.compare-card h3 { margin-top: 0; }
.compare-matrix {
  width: 100%; border-collapse: collapse; margin: .5rem 0 1rem;
}
.compare-matrix th, .compare-matrix td {
  padding: .55rem .8rem; border: 1px solid var(--border); text-align: center;
  font-size: .9rem; vertical-align: middle;
}
.compare-matrix th { background: #f9fafb; font-weight: 600; }
.compare-matrix td.score-cell {
  font-variant-numeric: tabular-nums; font-weight: 600;
}
.compare-matrix td.score-cell .pct { font-size: 1.1rem; }
.compare-matrix td.score-cell .raw { color: var(--muted); font-size: .75rem; display: block; }
.compare-matrix td.empty { color: var(--muted); font-size: .8rem; background: #fafafa; }
.delta {
  font-size: .75rem; padding: .15rem .45rem; border-radius: 4px;
  display: inline-block; margin-top: .2rem;
}
.delta.lenient { background: #fef3c7; color: #92400e; }
.delta.strict  { background: #fce7f3; color: #9d174d; }
.delta.match   { background: #dcfce7; color: #166534; }
.element-diff {
  background: #f9fafb; border: 1px solid var(--border); border-radius: 6px;
  padding: .75rem 1rem; margin: 1rem 0;
}
.element-diff h4 { margin: 0 0 .5rem; font-size: .9rem; }
.element-diff table { width: 100%; border-collapse: collapse; font-size: .85rem; }
.element-diff th, .element-diff td {
  padding: .35rem .6rem; border-top: 1px solid var(--border); text-align: left;
}
.element-diff th { background: #f3f4f6; }
.element-diff td.score { text-align: right; font-variant-numeric: tabular-nums; }
footer { color: var(--muted); font-size: .8rem; text-align: center; margin: 2rem 0 0; }
"""


def color_class(pct: float) -> str:
    if pct >= 80:
        return "good"
    if pct >= 50:
        return "ok"
    return "bad"


def esc(s: Any) -> str:
    if s is None:
        return ""
    return html.escape(str(s))


def render_rubric10(report: dict) -> str:
    overall = report.get("overall_score", {})
    pct = overall.get("percentage", 0)
    cls = color_class(pct)
    parts: list[str] = []
    parts.append(f'<details open><summary>'
                 f'<span class="elem-name">{esc(Path(report["model_card_file"]).name)}</span>'
                 f' <span class="section-tag">rubric10</span>'
                 f'<span class="elem-score {cls}">{overall.get("total_points", 0)}/{overall.get("max_points", 50)} ({pct}%)</span>'
                 f'</summary>')
    parts.append('<div style="padding: .9rem 1rem;">')

    # Elements
    for elem in report.get("elements", []):
        score = elem.get("element_score", 0)
        emax = elem.get("element_max", 5)
        epct = (score / emax * 100) if emax else 0
        ec = color_class(epct)
        parts.append(f'<details><summary>'
                     f'<span class="elem-name">Element {elem.get("id")}: {esc(elem.get("name"))}</span>'
                     f'<span class="elem-score {ec}">{score}/{emax}</span>'
                     f'</summary>')
        parts.append(f'<div class="meta" style="padding: 0 .9rem;">{esc(elem.get("description", ""))}</div>')
        parts.append('<table><thead><tr>'
                     '<th>Sub-element</th><th class="score">Score</th><th>Evidence</th>'
                     '</tr></thead><tbody>')
        for sub in elem.get("sub_elements", []):
            s = sub.get("score", 0)
            scls = "good" if s >= 1 else "bad"
            parts.append('<tr>')
            parts.append(f'<td><div class="elem-name">{esc(sub.get("name"))}</div>'
                         f'<div class="note">{esc(sub.get("quality_note", ""))}</div>')
            sa = sub.get("semantic_analysis")
            if sa:
                parts.append(f'<div class="semantic-analysis">'
                             f'<span class="section-tag semantic">semantic</span>'
                             f'{esc(json.dumps(sa, separators=(", ", ": ")))}</div>')
            parts.append('</td>')
            parts.append(f'<td class="score {scls}">{s}/1</td>')
            parts.append(f'<td class="evidence">{esc(sub.get("evidence", ""))}</td>')
            parts.append('</tr>')
        parts.append('</tbody></table></details>')

    parts.append(render_assessment(report.get("assessment", {})))
    parts.append('</div></details>')
    return "\n".join(parts)


def render_rubric20(report: dict) -> str:
    overall = report.get("overall_score", {})
    pct = overall.get("percentage", 0)
    cls = color_class(pct)
    parts: list[str] = []
    parts.append(f'<details open><summary>'
                 f'<span class="elem-name">{esc(Path(report["model_card_file"]).name)}</span>'
                 f' <span class="section-tag r20">rubric20</span>'
                 f'<span class="elem-score {cls}">{overall.get("total_points", 0)}/{overall.get("max_points", 84)} ({pct}%)</span>'
                 f'</summary>')
    parts.append('<div style="padding: .9rem 1rem;">')

    for cat in report.get("categories", []):
        score = cat.get("category_score", 0)
        cmax = cat.get("category_max", 21)
        cpct = (score / cmax * 100) if cmax else 0
        cc = color_class(cpct)
        parts.append(f'<details><summary>'
                     f'<span class="elem-name">{esc(cat.get("name"))}</span>'
                     f'<span class="elem-score {cc}">{score}/{cmax}</span>'
                     f'</summary>')
        parts.append('<table><thead><tr>'
                     '<th>Question</th><th class="score">Score</th><th>Evidence</th>'
                     '</tr></thead><tbody>')
        for q in cat.get("questions", []):
            s = q.get("score", 0)
            sm = q.get("max_score", 5)
            spct = (s / sm * 100) if sm else 0
            scls = color_class(spct)
            parts.append('<tr>')
            parts.append(f'<td><div class="elem-name">Q{q.get("id")}: {esc(q.get("name"))}</div>'
                         f'<div class="note">{esc(q.get("score_label", q.get("quality_note", "")))}</div>')
            sa = q.get("semantic_analysis")
            if sa:
                parts.append(f'<div class="semantic-analysis">'
                             f'<span class="section-tag semantic">semantic</span>'
                             f'{esc(json.dumps(sa, separators=(", ", ": ")))}</div>')
            parts.append('</td>')
            parts.append(f'<td class="score {scls}">{s}/{sm}</td>')
            parts.append(f'<td class="evidence">{esc(q.get("evidence", ""))}</td>')
            parts.append('</tr>')
        parts.append('</tbody></table></details>')

    parts.append(render_assessment(report.get("assessment", {})))
    parts.append('</div></details>')
    return "\n".join(parts)


def render_assessment(assess: dict) -> str:
    parts = ['<div class="assessment">']
    for col, items in (
        ("Strengths", assess.get("strengths") or []),
        ("Weaknesses", assess.get("weaknesses") or []),
        ("Recommendations", assess.get("recommendations") or []),
    ):
        parts.append(f'<div class="col"><h4>{col}</h4>')
        if items:
            parts.append("<ul>")
            for it in items:
                parts.append(f"<li>{esc(it)}</li>")
            parts.append("</ul>")
        else:
            parts.append('<div class="meta">None</div>')
        parts.append("</div>")
    parts.append("</div>")
    return "\n".join(parts)


def summary_card(report: dict) -> str:
    pct = report.get("overall_score", {}).get("percentage", 0)
    total = report.get("overall_score", {}).get("total_points", 0)
    rmax = report.get("overall_score", {}).get("max_points", 0)
    rubric = report.get("rubric", "?")
    file_name = Path(report.get("model_card_file", "?")).name
    cls = color_class(pct)
    return (
        f'<div class="summary-card">'
        f'<h4>{esc(file_name)} <span class="section-tag">{esc(rubric)}</span></h4>'
        f'<div class="score-big">'
        f'<span class="pct" style="color: var(--{cls})">{pct}%</span>'
        f'<span class="raw">{total}/{rmax}</span>'
        f'</div>'
        f'<div class="bar {cls}"><div style="width: {min(pct,100)}%"></div></div>'
        f'</div>'
    )


def load_one(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception as e:
        return {"_load_error": str(e), "_path": str(path)}


# ---------------------------------------------------------------------------
# Comparison view
# ---------------------------------------------------------------------------
RUBRIC_BASE = {
    "mc_rubric10": "rubric10",
    "mc_rubric10_semantic": "rubric10",
    "mc_rubric20": "rubric20",
    "mc_rubric20_semantic": "rubric20",
}


def evaluator_kind(report: dict) -> str:
    """Classify the evaluator behind a report as 'hybrid' or 'llm'."""
    ev = report.get("evaluator") or {}
    name = (ev.get("name") or "").lower()
    if "hybrid" in name or "heuristic" in name or "rule_based" in name:
        return "hybrid"
    return "llm"


def variant_kind(report: dict) -> str:
    return "semantic" if report.get("rubric", "").endswith("_semantic") else "standard"


def render_compare_cell(report: dict | None, peer_report: dict | None = None) -> str:
    """Render one (rubric × evaluator) cell. If peer (the other evaluator) is
    provided, add a delta annotation."""
    if report is None:
        return '<td class="empty">—</td>'
    pct = report.get("overall_score", {}).get("percentage", 0)
    total = report.get("overall_score", {}).get("total_points", 0)
    rmax = report.get("overall_score", {}).get("max_points", 0)
    cls = color_class(pct)
    delta_html = ""
    if peer_report is not None:
        peer_pct = peer_report.get("overall_score", {}).get("percentage", 0)
        gap = pct - peer_pct
        if abs(gap) < 2:
            delta_html = '<div class="delta match">≈ peer</div>'
        elif gap > 0:
            delta_html = f'<div class="delta lenient">+{gap:.1f}pp vs peer</div>'
        else:
            delta_html = f'<div class="delta strict">{gap:.1f}pp vs peer</div>'
    return (
        f'<td class="score-cell" style="color: var(--{cls})">'
        f'<span class="pct">{pct}%</span>'
        f'<span class="raw">{total}/{rmax}</span>'
        f'{delta_html}'
        f'</td>'
    )


def render_element_diff(rubric10_hybrid: dict | None, rubric10_llm: dict | None) -> str:
    """Render per-element score deltas between hybrid and LLM rubric10 evaluations."""
    if not rubric10_hybrid or not rubric10_llm:
        return ""
    h = {e["id"]: e for e in rubric10_hybrid.get("elements", [])}
    l = {e["id"]: e for e in rubric10_llm.get("elements", [])}
    rows = []
    for eid in sorted(set(h) | set(l)):
        he = h.get(eid)
        le = l.get(eid)
        h_score = he.get("element_score", 0) if he else "—"
        l_score = le.get("element_score", 0) if le else "—"
        name = (he or le).get("name", "?")
        gap = ""
        if isinstance(h_score, int) and isinstance(l_score, int):
            d = h_score - l_score
            if d > 0:
                gap = f'<span class="delta lenient">+{d}</span>'
            elif d < 0:
                gap = f'<span class="delta strict">{d}</span>'
            else:
                gap = '<span class="delta match">≡</span>'
        rows.append(
            f'<tr><td>{eid}. {esc(name)}</td>'
            f'<td class="score">{h_score}/5</td>'
            f'<td class="score">{l_score}/5</td>'
            f'<td>{gap}</td></tr>'
        )
    if not rows:
        return ""
    return (
        '<div class="element-diff">'
        '<h4>Rubric10 element-by-element: hybrid vs LLM</h4>'
        '<table><thead><tr>'
        '<th>Element</th><th class="score">Hybrid</th><th class="score">LLM</th><th>Δ</th>'
        '</tr></thead><tbody>'
        + "".join(rows) +
        '</tbody></table></div>'
    )


def render_category_diff(rubric20_hybrid: dict | None, rubric20_llm: dict | None) -> str:
    """Render per-category score deltas between hybrid and LLM rubric20 evaluations."""
    if not rubric20_hybrid or not rubric20_llm:
        return ""
    h = {c["name"]: c for c in rubric20_hybrid.get("categories", [])}
    l = {c["name"]: c for c in rubric20_llm.get("categories", [])}
    rows = []
    for name in sorted(set(h) | set(l)):
        he = h.get(name)
        le = l.get(name)
        h_score = he.get("category_score", 0) if he else "—"
        l_score = le.get("category_score", 0) if le else "—"
        cmax = (he or le).get("category_max", "?")
        gap = ""
        if isinstance(h_score, int) and isinstance(l_score, int):
            d = h_score - l_score
            if d > 0:
                gap = f'<span class="delta lenient">+{d}</span>'
            elif d < 0:
                gap = f'<span class="delta strict">{d}</span>'
            else:
                gap = '<span class="delta match">≡</span>'
        rows.append(
            f'<tr><td>{esc(name)}</td>'
            f'<td class="score">{h_score}/{cmax}</td>'
            f'<td class="score">{l_score}/{cmax}</td>'
            f'<td>{gap}</td></tr>'
        )
    if not rows:
        return ""
    return (
        '<div class="element-diff">'
        '<h4>Rubric20 category-by-category: hybrid vs LLM</h4>'
        '<table><thead><tr>'
        '<th>Category</th><th class="score">Hybrid</th><th class="score">LLM</th><th>Δ</th>'
        '</tr></thead><tbody>'
        + "".join(rows) +
        '</tbody></table></div>'
    )


def render_compare_block(file_name: str, group: list[dict]) -> str:
    """Render one model-card comparison block: matrix + per-element diff tables."""
    # bucket by (rubric_base, evaluator_kind, variant)
    by_key: dict[tuple[str, str, str], dict] = {}
    for r in group:
        rb = RUBRIC_BASE.get(r.get("rubric"), r.get("rubric", "unknown"))
        by_key[(rb, evaluator_kind(r), variant_kind(r))] = r

    # rows are rubric_base × variant; columns are hybrid / llm
    rows: list[tuple[str, str, str]] = []
    for rb in ("rubric10", "rubric20"):
        for variant in ("standard", "semantic"):
            if any(k == (rb, ek, variant) for k in by_key for ek in ("hybrid", "llm")):
                rows.append((rb, variant, f"{rb} {variant}".replace(" standard", "")))

    parts = ['<div class="compare-card">']
    parts.append(f'<h3>{esc(file_name)}</h3>')

    if rows:
        parts.append('<table class="compare-matrix"><thead><tr>'
                     '<th>Rubric / variant</th>'
                     '<th>Hybrid (heuristic)</th>'
                     '<th>LLM (semantic judge)</th>'
                     '</tr></thead><tbody>')
        for rb, variant, label in rows:
            hybrid = by_key.get((rb, "hybrid", variant))
            llm = by_key.get((rb, "llm", variant))
            parts.append('<tr>')
            parts.append(f'<td><strong>{esc(label)}</strong></td>')
            parts.append(render_compare_cell(hybrid, peer_report=llm))
            parts.append(render_compare_cell(llm, peer_report=hybrid))
            parts.append('</tr>')
        parts.append('</tbody></table>')

    # Per-rubric element/category diff tables (only when BOTH hybrid and LLM are present)
    parts.append(render_element_diff(
        by_key.get(("rubric10", "hybrid", "standard")),
        by_key.get(("rubric10", "llm", "standard")),
    ))
    parts.append(render_category_diff(
        by_key.get(("rubric20", "hybrid", "standard")),
        by_key.get(("rubric20", "llm", "standard")),
    ))

    parts.append('</div>')
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# SVG badge mode (shields.io-style quality badges)
# ---------------------------------------------------------------------------
BADGE_COLORS = {
    "good":     "#4c1",  # ≥80%
    "ok":       "#dfb317",  # ≥50%
    "bad":      "#e05d44",  # <50%
    "label_bg": "#555",
}

# Approximate per-char widths so the SVG sizes the boxes correctly without a
# font-metrics dependency. Values are tuned for Verdana 11px (shields.io's font).
def _badge_text_width(s: str) -> int:
    return max(20, int(7 * len(s) + 10))


def render_badge_svg(label: str, value: str, color_class: str) -> str:
    """Render a single shields.io-style badge as an SVG string.

    `label` is the left (dark grey) text; `value` is the right (colored) text.
    `color_class` is one of {good, ok, bad}.
    """
    color = BADGE_COLORS.get(color_class, BADGE_COLORS["ok"])
    label_w = _badge_text_width(label)
    value_w = _badge_text_width(value)
    total_w = label_w + value_w
    label_x = label_w / 2
    value_x = label_w + value_w / 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20" '
        f'role="img" aria-label="{esc(label)}: {esc(value)}">'
        f'<title>{esc(label)}: {esc(value)}</title>'
        f'<linearGradient id="s" x2="0" y2="100%">'
        f'<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>'
        f'<stop offset="1" stop-opacity=".1"/>'
        f'</linearGradient>'
        f'<clipPath id="r"><rect width="{total_w}" height="20" rx="3" fill="#fff"/></clipPath>'
        f'<g clip-path="url(#r)">'
        f'<rect width="{label_w}" height="20" fill="{BADGE_COLORS["label_bg"]}"/>'
        f'<rect x="{label_w}" width="{value_w}" height="20" fill="{color}"/>'
        f'<rect width="{total_w}" height="20" fill="url(#s)"/>'
        f'</g>'
        f'<g fill="#fff" text-anchor="middle" '
        f'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        f'<text x="{label_x}" y="15" fill="#010101" fill-opacity=".3">{esc(label)}</text>'
        f'<text x="{label_x}" y="14">{esc(label)}</text>'
        f'<text x="{value_x}" y="15" fill="#010101" fill-opacity=".3">{esc(value)}</text>'
        f'<text x="{value_x}" y="14">{esc(value)}</text>'
        f'</g>'
        f'</svg>'
    )


def badge_label_for(report: dict) -> str:
    """Construct the badge's label text, e.g. 'mc-rubric10 (hybrid)'."""
    rubric = report.get("rubric", "model card")
    pretty = {
        "mc_rubric10": "mc-rubric10",
        "mc_rubric10_semantic": "mc-rubric10·sem",
        "mc_rubric20": "mc-rubric20",
        "mc_rubric20_semantic": "mc-rubric20·sem",
    }.get(rubric, rubric)
    kind = evaluator_kind(report)
    return f"{pretty} ({kind})"


def write_badges(reports: list[dict], output_dir: Path) -> dict[str, Path]:
    """Write one SVG badge per non-error report. Returns a mapping of
    badge_id → path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for r in reports:
        if "_load_error" in r:
            continue
        pct = r.get("overall_score", {}).get("percentage", 0)
        total = r.get("overall_score", {}).get("total_points", 0)
        rmax = r.get("overall_score", {}).get("max_points", 0)
        label = badge_label_for(r)
        value = f"{pct}% ({total}/{rmax})"
        color = color_class(pct)
        svg = render_badge_svg(label, value, color)

        # filename: <model_card_stem>_<rubric>_<evaluator>.svg
        model_stem = Path(r.get("model_card_file", "model_card")).stem
        rubric = r.get("rubric", "rubric").replace("mc_", "")
        kind = evaluator_kind(r)
        badge_id = f"{model_stem}_{rubric}_{kind}"
        path = output_dir / f"{badge_id}.svg"
        path.write_text(svg)
        written[badge_id] = path
    return written


def render_badge_index(badges: dict[str, Path], output_dir: Path, title: str) -> str:
    """Render an index.html with markdown snippets for each badge."""
    rows = []
    for badge_id, path in sorted(badges.items()):
        rel = path.name
        rows.append(
            '<tr>'
            f'<td><img src="{esc(rel)}" alt="{esc(badge_id)}"></td>'
            f'<td><code>{esc(badge_id)}</code></td>'
            f'<td><code>![{esc(badge_id)}](./{esc(rel)})</code></td>'
            '</tr>'
        )
    return (
        f'<!doctype html><html><head>'
        f'<meta charset="utf-8">'
        f'<title>{esc(title)}</title>'
        f'<style>{CSS}'
        'table { width: 100%; border-collapse: collapse; margin: 1rem 0; }'
        'th, td { padding: .55rem .9rem; border-top: 1px solid var(--border); text-align: left; vertical-align: middle; }'
        'th { background: #f9fafb; font-weight: 600; }'
        'code { font-size: .85rem; background: #f3f4f6; padding: .1rem .35rem; border-radius: 3px; }'
        '</style>'
        f'</head><body>'
        f'<header><h1>{esc(title)}</h1>'
        f'<div class="meta">Generated {datetime.now(timezone.utc).isoformat()} · {len(badges)} badge(s)</div>'
        f'</header><main>'
        f'<table><thead><tr><th>Badge</th><th>Filename</th><th>Markdown snippet</th></tr></thead><tbody>'
        + "\n".join(rows) +
        '</tbody></table></main></body></html>'
    )


def render_compare(reports: list[dict], title: str) -> str:
    """Top-level renderer for --compare mode. Groups all reports by model card
    file basename, then emits one comparison block per model card."""
    by_file: dict[str, list[dict]] = defaultdict(list)
    errors: list[dict] = []
    for r in reports:
        if "_load_error" in r:
            errors.append(r)
            continue
        name = Path(r.get("model_card_file", "?")).name
        by_file[name].append(r)

    head = (
        f'<!doctype html><html><head>'
        f'<meta charset="utf-8">'
        f'<title>{esc(title)}</title>'
        f'<style>{CSS}</style>'
        f'</head><body>'
        f'<header>'
        f'<h1>{esc(title)}</h1>'
        f'<div class="meta">Generated {datetime.now(timezone.utc).isoformat()} '
        f'· comparison across {sum(len(v) for v in by_file.values())} evaluation(s) '
        f'over {len(by_file)} model card(s)</div>'
        f'</header>'
        f'<main>'
    )

    parts = [head]

    parts.append('<h2>Cross-Evaluator Comparison</h2>')
    parts.append(
        '<p class="meta">Per-cell color shows score band (green ≥80%, yellow ≥50%, red &lt;50%). '
        'Δ pills show the gap between hybrid and LLM on the same rubric — '
        '<span class="delta lenient">+Δ</span> means hybrid is more lenient, '
        '<span class="delta strict">−Δ</span> means hybrid is stricter, '
        '<span class="delta match">≈</span> means they agree within 2pp.</p>'
    )

    for file_name in sorted(by_file):
        parts.append(render_compare_block(file_name, by_file[file_name]))

    if errors:
        parts.append('<h2>Errors</h2>')
        for e in errors:
            parts.append(f'<div class="error">Failed to load <code>{esc(e["_path"])}</code>: {esc(e["_load_error"])}</div>')

    parts.append('</main>')
    parts.append(f'<footer>Model Card Schema evaluation comparison · {esc(title)}</footer>')
    parts.append('</body></html>')
    return "\n".join(parts)


def render_report(reports: list[dict], title: str) -> str:
    by_rubric: dict[str, list[dict]] = defaultdict(list)
    errors: list[dict] = []
    for r in reports:
        if "_load_error" in r:
            errors.append(r)
            continue
        rubric = r.get("rubric", "unknown")
        by_rubric[rubric].append(r)

    head = (
        f'<!doctype html><html><head>'
        f'<meta charset="utf-8">'
        f'<title>{esc(title)}</title>'
        f'<style>{CSS}</style>'
        f'</head><body>'
        f'<header>'
        f'<h1>{esc(title)}</h1>'
        f'<div class="meta">Generated {datetime.now(timezone.utc).isoformat()} '
        f'· {sum(len(v) for v in by_rubric.values())} report(s)</div>'
        f'</header>'
        f'<main>'
    )

    parts = [head]

    # Summary grid (across all rubrics)
    parts.append('<h2>Summary</h2>')
    parts.append('<div class="summary-grid">')
    for rubric in sorted(by_rubric):
        for r in by_rubric[rubric]:
            parts.append(summary_card(r))
    parts.append('</div>')

    # Errors
    if errors:
        parts.append('<h2>Errors</h2>')
        for e in errors:
            parts.append(f'<div class="error">Failed to load <code>{esc(e["_path"])}</code>: {esc(e["_load_error"])}</div>')

    # Per-rubric sections
    for rubric in sorted(by_rubric):
        label = {
            "mc_rubric10": "Rubric10 — 10 elements / 50 points",
            "mc_rubric10_semantic": "Rubric10 (semantic) — 10 elements / 50 points",
            "mc_rubric20": "Rubric20 — 4 categories / 84 points",
            "mc_rubric20_semantic": "Rubric20 (semantic) — 4 categories / 84 points",
        }.get(rubric, rubric)
        parts.append(f'<h2>{esc(label)}</h2>')
        for r in sorted(by_rubric[rubric], key=lambda x: x.get("model_card_file", "")):
            if rubric.startswith("mc_rubric20"):
                parts.append(render_rubric20(r))
            else:
                parts.append(render_rubric10(r))

    parts.append('</main>')
    parts.append(f'<footer>Model Card Schema evaluation report · {esc(title)}</footer>')
    parts.append('</body></html>')
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", action="append", type=Path,
                   help="Single evaluation JSON. Can be repeated.")
    p.add_argument("--input-glob", action="append",
                   help="Glob of evaluation JSONs. Can be repeated.")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--title", default="Model Card Evaluation Report")
    p.add_argument("--compare", action="store_true",
                   help="Render a cross-evaluator comparison view (groups by model card "
                        "file; shows hybrid vs LLM side-by-side per rubric).")
    p.add_argument("--badge", action="store_true",
                   help="Emit one shields.io-style SVG quality badge per evaluation. "
                        "When set, --output is treated as a DIRECTORY (will be created) "
                        "containing per-evaluation .svg files plus an index.html.")
    args = p.parse_args(argv)

    paths: list[Path] = []
    for inp in args.input or []:
        paths.append(inp)
    for g in args.input_glob or []:
        paths.extend(Path(p) for p in sorted(glob.glob(g, recursive=True)))

    if not paths:
        print("No evaluation JSONs given (use --input or --input-glob).", file=sys.stderr)
        return 1

    reports: list[dict] = []
    for path in paths:
        if not path.exists():
            reports.append({"_load_error": "file not found", "_path": str(path)})
            continue
        loaded = load_one(path)
        if loaded is not None:
            reports.append(loaded)

    if args.badge:
        if args.compare:
            print("--badge and --compare are mutually exclusive.", file=sys.stderr)
            return 1
        out_dir = args.output
        badges = write_badges(reports, out_dir)
        index = out_dir / "index.html"
        index.write_text(render_badge_index(badges, out_dir, args.title))
        print(f"Wrote {len(badges)} SVG badge(s) + index to {out_dir}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    renderer = render_compare if args.compare else render_report
    args.output.write_text(renderer(reports, args.title))
    mode = "comparison" if args.compare else "report"
    print(f"Wrote {mode} HTML with {len(reports)} evaluation(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
