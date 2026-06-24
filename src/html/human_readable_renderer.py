#!/usr/bin/env python3
"""
Render a Model Card YAML to a self-contained human-readable HTML page.

Writes the HTML next to the input YAML by default — so
``data/model_cards_assistant/foo_model_card.yaml`` produces
``data/model_cards_assistant/foo_model_card.html``.

Usage:
    poetry run python src/html/human_readable_renderer.py path/to/card.yaml
    poetry run python src/html/human_readable_renderer.py card.yaml --output custom.html
    poetry run python src/html/human_readable_renderer.py 'data/model_cards_assistant/*.yaml'

The renderer walks the Model Card structure heuristically — it doesn't require
the LinkML schema to be loaded. It renders the well-known sections
(model_details, model_parameters, quantitative_analysis, considerations, etc.)
into themed cards, then falls through to a generic key/value table for any
remaining keys. Inline CSS only; no external assets.

If a sibling badge SVG exists under ``data/evaluation/badges/<stem>_*.svg`` it
is embedded under the title.
"""
from __future__ import annotations

import argparse
import glob
import html
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
CSS = """
:root {
  --bg: #fafafa; --card: #fff; --border: #e5e5e5;
  --text: #111; --muted: #6b7280; --accent: #2563eb;
  --good: #16a34a; --warn: #ca8a04; --bad: #dc2626;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg); color: var(--text);
  margin: 0; padding: 2rem 1.5rem; line-height: 1.5;
}
header, main, footer { max-width: 980px; margin: 0 auto; }
header { padding-bottom: 1.25rem; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; }
h1 { font-size: 1.85rem; margin: 0 0 .35rem; }
h2 {
  font-size: 1.2rem; margin: 1.5rem 0 .6rem;
  padding-bottom: .3rem; border-bottom: 1px solid var(--border);
}
h3 { font-size: 1rem; margin: 1rem 0 .35rem; color: var(--accent); }
.short { color: var(--muted); font-size: 1rem; margin: 0 0 .75rem; }
.meta-row { color: var(--muted); font-size: .85rem; }
.meta-row span + span::before { content: " · "; padding: 0 .2rem; }
.badge-row { margin: .75rem 0; display: flex; flex-wrap: wrap; gap: .3rem; }
.badge-row img { height: 20px; }

.card {
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 1rem 1.25rem; margin: 1rem 0;
}
.card h2 { margin-top: 0; border-bottom: none; }

dl.kv { margin: 0; }
dl.kv > div { display: grid; grid-template-columns: 200px 1fr; gap: .5rem 1rem; padding: .35rem 0; border-top: 1px solid var(--border); }
dl.kv > div:first-child { border-top: 0; }
dl.kv dt { color: var(--muted); font-weight: 500; font-size: .9rem; }
dl.kv dd { margin: 0; word-break: break-word; }
dl.kv code { background: #f3f4f6; padding: .05rem .3rem; border-radius: 3px; font-size: .85rem; }

.chip-row { display: flex; flex-wrap: wrap; gap: .35rem; }
.chip { background: #eef2ff; color: #3730a3; padding: .15rem .55rem; border-radius: 999px; font-size: .8rem; }

ul.bullet { padding-left: 1.2rem; margin: .3rem 0; }
ul.bullet li { margin: .2rem 0; }

.contrib-row { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem 1rem; padding: .35rem 0; border-top: 1px solid var(--border); font-size: .9rem; }
.contrib-row:first-child { border-top: 0; }
.contrib-role { display: inline-block; background: #fef3c7; color: #92400e; padding: .05rem .4rem; border-radius: 4px; font-size: .75rem; margin-left: .35rem; }

table.metrics { width: 100%; border-collapse: collapse; margin: .3rem 0; font-size: .9rem; }
table.metrics th, table.metrics td {
  padding: .4rem .75rem; border-top: 1px solid var(--border); text-align: left; vertical-align: top;
}
table.metrics th { background: #f9fafb; font-weight: 600; }
table.metrics td.num { text-align: right; font-variant-numeric: tabular-nums; }

pre {
  background: #f3f4f6; padding: .75rem 1rem; border-radius: 6px;
  overflow-x: auto; font-size: .85rem;
}
pre code { background: transparent; padding: 0; }

.markdown p { margin: .4rem 0; }
.markdown code { background: #f3f4f6; padding: .05rem .3rem; border-radius: 3px; font-size: .9rem; }

footer { color: var(--muted); font-size: .8rem; text-align: center; margin: 2rem 0 0; }
.tag-license { background: #d1fae5; color: #065f46; padding: .1rem .45rem; border-radius: 4px; font-size: .8rem; }
.bias-block { background: #fff7ed; border-left: 3px solid #f97316; padding: .5rem .75rem; margin: .35rem 0; border-radius: 0 4px 4px 0; font-size: .9rem; }
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def esc(s: Any) -> str:
    if s is None:
        return ""
    return html.escape(str(s))


def fmt_inline(value: Any) -> str:
    """Render a scalar or simple value as an inline HTML snippet."""
    if value is None:
        return "<em>—</em>"
    if isinstance(value, bool):
        return f'<code>{value}</code>'
    if isinstance(value, (int, float)):
        return f'<code>{value}</code>'
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            return f'<a href="{esc(value)}">{esc(value)}</a>'
        if "\n" in value:
            return f'<pre>{esc(value)}</pre>'
        return esc(value)
    if isinstance(value, list):
        if all(isinstance(v, (str, int, float, bool)) for v in value):
            chips = " ".join(
                f'<span class="chip">{esc(v)}</span>' for v in value
            )
            return f'<div class="chip-row">{chips}</div>'
        items = "".join(f"<li>{fmt_inline(v)}</li>" for v in value)
        return f'<ul class="bullet">{items}</ul>'
    if isinstance(value, dict):
        return render_kv_table(value)
    return esc(value)


def render_kv_table(d: dict[str, Any], skip: set[str] | None = None) -> str:
    if skip is None:
        skip = set()
    rows = []
    for k, v in d.items():
        if k in skip:
            continue
        rows.append(
            f'<div><dt>{esc(k)}</dt><dd>{fmt_inline(v)}</dd></div>'
        )
    if not rows:
        return ""
    return f'<dl class="kv">{"".join(rows)}</dl>'


def section(title: str, body_html: str) -> str:
    if not body_html.strip():
        return ""
    return f'<section class="card"><h2>{esc(title)}</h2>{body_html}</section>'


# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------
def render_model_details(md: dict) -> str:
    if not isinstance(md, dict):
        return ""
    parts = []
    # version + license inline header
    version = md.get("version") or {}
    if isinstance(version, dict):
        v_name = version.get("name", "")
        v_date = version.get("date", "")
        v_diff = version.get("diff", "")
        if v_name or v_date:
            label = f"<strong>{esc(v_name)}</strong>"
            if v_date:
                label += f' <span class="meta-row">{esc(v_date)}</span>'
            parts.append(f"<p>{label}</p>")
        if v_diff:
            parts.append(f'<h3>Change description</h3><div class="markdown"><p>{esc(v_diff)}</p></div>')

    if md.get("overview"):
        parts.append(f'<h3>Overview</h3><div class="markdown"><p>{esc(md["overview"]).replace(chr(10), "<br>")}</p></div>')
    if md.get("documentation"):
        doc = md["documentation"]
        parts.append(f'<h3>Documentation</h3><pre>{esc(doc)}</pre>')

    # owners + contributors
    owners = md.get("owners") or []
    contributors = md.get("contributors") or []
    if owners or contributors:
        parts.append("<h3>Owners / Contributors</h3>")
        rows = []
        for o in (owners or []):
            if not isinstance(o, dict):
                continue
            rows.append(
                f'<div class="contrib-row">'
                f'<span><strong>{esc(o.get("name", ""))}</strong>'
                f'{f"<span class=contrib-role>owner</span>" if o.get("name") else ""}</span>'
                f'<span>{esc(o.get("contact", ""))} {esc(o.get("affiliation", ""))}</span>'
                f'</div>'
            )
        for c in (contributors or []):
            if not isinstance(c, dict):
                continue
            role = c.get("role", "")
            role_html = f' <span class="contrib-role">{esc(role)}</span>' if role else ""
            extra = " · ".join(
                esc(c[k]) for k in ("email", "orcid", "affiliation") if c.get(k)
            )
            rows.append(
                f'<div class="contrib-row">'
                f'<span><strong>{esc(c.get("name", ""))}</strong>{role_html}</span>'
                f'<span>{extra}</span>'
                f'</div>'
            )
        parts.append("".join(rows))

    # licenses
    licenses = md.get("licenses") or []
    if licenses:
        parts.append("<h3>Licenses</h3>")
        chips = []
        for lic in licenses:
            if isinstance(lic, dict):
                ident = lic.get("identifier", "")
                link = lic.get("license_link") or ""
                label = esc(ident)
                if link:
                    label = f'<a href="{esc(link)}">{label}</a>'
                chips.append(f'<span class="tag-license">{label}</span>')
            else:
                chips.append(f'<span class="tag-license">{esc(lic)}</span>')
        parts.append(f'<div class="chip-row">{" ".join(chips)}</div>')

    # citations
    citations = md.get("citations") or []
    if citations:
        parts.append("<h3>Citations</h3>")
        for c in citations:
            if isinstance(c, dict):
                style = c.get("style", "")
                cite = c.get("citation", "")
                parts.append(
                    f'<p><span class="chip">{esc(style)}</span> '
                    f'<span class="markdown">{esc(cite)}</span></p>'
                )

    # references
    refs = md.get("references") or []
    if refs:
        parts.append("<h3>References</h3>")
        items = []
        for r in refs:
            if isinstance(r, dict):
                items.append(f'<li>{fmt_inline(r.get("reference"))}</li>')
            else:
                items.append(f"<li>{fmt_inline(r)}</li>")
        parts.append(f'<ul class="bullet">{"".join(items)}</ul>')

    # path
    if md.get("path"):
        parts.append(f'<h3>Path</h3>{fmt_inline(md["path"])}')

    return "".join(parts)


def render_model_parameters(mp: dict) -> str:
    if not isinstance(mp, dict):
        return ""
    parts = []
    if mp.get("model_architecture"):
        parts.append(
            f'<h3>Architecture</h3>'
            f'<div class="markdown"><p>{esc(mp["model_architecture"]).replace(chr(10), "<br>")}</p></div>'
        )

    for io_key, io_map_key, label in (
        ("input_format", "input_format_map", "Input"),
        ("output_format", "output_format_map", "Output"),
    ):
        io = mp.get(io_key)
        io_map = mp.get(io_map_key) or []
        if io or io_map:
            parts.append(f'<h3>{label} format</h3>')
            if io:
                parts.append(f'<p>{esc(io)}</p>')
            if io_map:
                rows = []
                for kv in io_map:
                    if isinstance(kv, dict):
                        rows.append(
                            f'<div><dt><code>{esc(kv.get("key", ""))}</code></dt>'
                            f'<dd>{fmt_inline(kv.get("value"))}</dd></div>'
                        )
                if rows:
                    parts.append(f'<dl class="kv">{"".join(rows)}</dl>')

    # data (training/eval datasets)
    data = mp.get("data") or []
    if data:
        parts.append("<h3>Datasets</h3>")
        for ds in data:
            if isinstance(ds, dict):
                name = esc(ds.get("name", ""))
                link = ds.get("link") or ""
                title = f'<a href="{esc(link)}">{name}</a>' if link else name
                desc = ds.get("description") or ""
                bias_input = ds.get("bias_input") or ""
                sensitive = (ds.get("sensitive") or {}).get("sensitive_data") or []
                inner = []
                if desc:
                    inner.append(f"<p>{esc(desc)}</p>")
                if sensitive:
                    sens_str = ", ".join(esc(s) for s in sensitive) if isinstance(sensitive, list) else esc(sensitive)
                    inner.append(f'<div class="meta-row"><strong>Sensitive data:</strong> {sens_str}</div>')
                if bias_input:
                    inner.append(f'<div class="bias-block"><strong>bias_input:</strong> {esc(bias_input)}</div>')
                parts.append(f'<div style="margin-bottom: .5rem;"><strong>{title}</strong>{"".join(inner)}</div>')

    # training procedure
    tp = mp.get("training_procedure")
    if isinstance(tp, dict):
        parts.append("<h3>Training procedure</h3>")
        if tp.get("description"):
            parts.append(f'<p>{esc(tp["description"])}</p>')
        hp_block = tp.get("reproducibility_info", {}).get("hyperparameters") if isinstance(tp.get("reproducibility_info"), dict) else None
        if not hp_block:
            hp_block = tp.get("hyperparameters")
        if isinstance(hp_block, dict):
            rows = []
            for k, v in hp_block.items():
                rows.append(f'<div><dt><code>{esc(k)}</code></dt><dd>{fmt_inline(v)}</dd></div>')
            parts.append(f'<dl class="kv">{"".join(rows)}</dl>')

    # compute infrastructure
    ci = mp.get("compute_infrastructure")
    if isinstance(ci, dict) and ci:
        parts.append("<h3>Compute infrastructure</h3>")
        parts.append(render_kv_table(ci))

    return "".join(parts)


def render_quantitative_analysis(qa: dict) -> str:
    if not isinstance(qa, dict):
        return ""
    metrics = qa.get("performance_metrics") or []
    if not metrics:
        return ""
    parts = ['<table class="metrics"><thead><tr>'
             '<th>Metric</th><th>Slice</th><th class="num">Value</th><th class="num">Unit</th>'
             '<th class="num">CI</th></tr></thead><tbody>']
    for m in metrics:
        if not isinstance(m, dict):
            continue
        t = esc(m.get("type", ""))
        slc = esc(m.get("slice", ""))
        val = m.get("value", "")
        unit = esc(m.get("unit", ""))
        ci_obj = m.get("confidence_interval") or {}
        ci_txt = ""
        if isinstance(ci_obj, dict) and ci_obj:
            lo, hi = ci_obj.get("lower_bound"), ci_obj.get("upper_bound")
            if lo is not None and hi is not None:
                ci_txt = f"[{lo} – {hi}]"
        elif m.get("value_error") is not None:
            ci_txt = f"± {m['value_error']}"
        parts.append(
            f'<tr><td>{t}</td><td>{slc}</td>'
            f'<td class="num">{esc(val)}</td><td class="num">{unit}</td>'
            f'<td class="num">{esc(ci_txt)}</td></tr>'
        )
    parts.append("</tbody></table>")
    return "".join(parts)


def render_considerations(c: dict) -> str:
    if not isinstance(c, dict):
        return ""
    blocks = []
    for key, label in (
        ("users", "Intended users"),
        ("use_cases", "Use cases"),
        ("limitations", "Limitations"),
        ("tradeoffs", "Tradeoffs"),
        ("ethical_considerations", "Ethical considerations"),
        ("out_of_scope_uses", "Out-of-scope uses"),
    ):
        items = c.get(key) or []
        if not items:
            continue
        blocks.append(f"<h3>{label}</h3>")
        bullets = []
        for it in items:
            if isinstance(it, dict):
                title = it.get("name") or it.get("description") or ""
                desc = it.get("description") if it.get("name") else ""
                mit = it.get("mitigation_strategy") or ""
                line = f"<strong>{esc(title)}</strong>"
                if desc and desc != title:
                    line += f"<br><span class='markdown'>{esc(desc)}</span>"
                if mit:
                    line += f"<br><em>Mitigation:</em> {esc(mit)}"
                bullets.append(f"<li>{line}</li>")
            else:
                bullets.append(f"<li>{esc(it)}</li>")
        blocks.append(f'<ul class="bullet">{"".join(bullets)}</ul>')
    return "".join(blocks)


def render_bias(card: dict) -> str:
    rows = []
    for key in ("bias_model", "bias_output"):
        v = card.get(key)
        if v:
            rows.append(f'<div class="bias-block"><strong>{key}:</strong> {esc(v)}</div>')
    return "".join(rows)


# ---------------------------------------------------------------------------
# Top-level render
# ---------------------------------------------------------------------------
KNOWN_TOPLEVEL = {
    "schema_version", "model_details", "model_parameters", "quantitative_analysis",
    "considerations", "model_category", "bias_model", "bias_output", "framework",
    "framework_version", "library_name", "pipeline_tag", "language", "base_model",
    "tags", "datasets", "metrics", "model_index", "mission_relevance",
    "usage_documentation",
}


def find_badge_files(yaml_path: Path) -> list[Path]:
    badge_dir = Path("data/evaluation/badges")
    if not badge_dir.is_dir():
        return []
    stem = yaml_path.stem
    return sorted(badge_dir.glob(f"{stem}_rubric*_*.svg"))


def render_card(yaml_path: Path) -> str:
    raw = yaml_path.read_text()
    card = yaml.safe_load(raw)
    if not isinstance(card, dict):
        raise SystemExit(f"{yaml_path}: top-level YAML is not a mapping")

    md = card.get("model_details") or {}
    name = md.get("name") or yaml_path.stem
    short = md.get("short_description") or ""

    # meta row
    meta_pieces = []
    if card.get("pipeline_tag"):
        meta_pieces.append(f'<span><code>{esc(card["pipeline_tag"])}</code></span>')
    if card.get("framework"):
        fw = card["framework"]
        if card.get("framework_version"):
            fw = f"{fw} {card['framework_version']}"
        meta_pieces.append(f"<span>{esc(fw)}</span>")
    if card.get("library_name"):
        meta_pieces.append(f"<span>library: <code>{esc(card['library_name'])}</code></span>")
    if card.get("base_model"):
        meta_pieces.append(f"<span>base: <code>{esc(card['base_model'])}</code></span>")
    meta_row = f'<div class="meta-row">{"".join(meta_pieces)}</div>' if meta_pieces else ""

    # tags chip row
    tags = card.get("tags") or []
    tags_row = ""
    if tags:
        chips = " ".join(f'<span class="chip">{esc(t)}</span>' for t in tags)
        tags_row = f'<div class="chip-row" style="margin-top:.4rem;">{chips}</div>'

    # badges
    badges = find_badge_files(yaml_path)
    badge_row = ""
    if badges:
        imgs = " ".join(
            f'<img src="../evaluation/badges/{b.name}" alt="{b.stem}">'
            for b in badges
        )
        badge_row = f'<div class="badge-row">{imgs}</div>'

    header = (
        f'<header>'
        f'<h1>{esc(name)}</h1>'
        f'{f"<p class=short>{esc(short)}</p>" if short else ""}'
        f'{meta_row}'
        f'{tags_row}'
        f'{badge_row}'
        f'<div class="meta-row" style="margin-top:.5rem;">'
        f'Source YAML: <code>{esc(yaml_path)}</code>'
        f'</div>'
        f'</header>'
    )

    body_parts = []
    body_parts.append(section("Model Details", render_model_details(md)))
    body_parts.append(section("Model Parameters", render_model_parameters(card.get("model_parameters") or {})))
    body_parts.append(section("Quantitative Analysis", render_quantitative_analysis(card.get("quantitative_analysis") or {})))
    body_parts.append(section("Considerations", render_considerations(card.get("considerations") or {})))
    body_parts.append(section("Bias Disclosure", render_bias(card)))

    # Anything top-level not consumed above
    leftovers = {k: v for k, v in card.items() if k not in KNOWN_TOPLEVEL}
    if leftovers:
        body_parts.append(section("Other fields", render_kv_table(leftovers)))

    body = "".join(p for p in body_parts if p)

    return (
        '<!doctype html><html><head>'
        '<meta charset="utf-8">'
        f'<title>{esc(name)} — Model Card</title>'
        f'<style>{CSS}</style>'
        '</head><body>'
        + header
        + f'<main>{body}</main>'
        f'<footer>Rendered {datetime.now(timezone.utc).isoformat()} from '
        f'<code>{esc(yaml_path)}</code></footer>'
        '</body></html>'
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", nargs="+", help="Model Card YAML file(s) or glob(s)")
    p.add_argument("--output", type=Path, default=None,
                   help="Output HTML path (only valid for a single input)")
    args = p.parse_args(argv)

    paths: list[Path] = []
    for entry in args.input:
        ps = sorted(Path(p) for p in glob.glob(entry))
        if not ps and Path(entry).exists():
            ps = [Path(entry)]
        paths.extend(ps)

    if not paths:
        print("No matching input files.", file=sys.stderr)
        return 1
    if args.output and len(paths) > 1:
        print("--output is only valid with a single input", file=sys.stderr)
        return 2

    for yaml_path in paths:
        html_doc = render_card(yaml_path)
        out = args.output or yaml_path.with_suffix(".html")
        out.write_text(html_doc)
        print(f"{yaml_path} → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
