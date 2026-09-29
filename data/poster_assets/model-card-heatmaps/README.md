# Current model-card heatmaps

Updated September 28, 2026 from the current local DenseNet-121 and SubCell 650M cards. Both figures use the same verified inputs. They measure documentation, not model performance.

| Figure | PNG preview | Editable SVG | Vector PDF |
|---|---|---|---|
| Detailed | [PNG](model_cards_scores_and_field_presence.png) | [SVG](model_cards_scores_and_field_presence.svg) | [PDF](model_cards_scores_and_field_presence.pdf) |
| Simplified poster | [PNG](model_cards_poster.png) · [transparent PNG for the portfolio poster](model_cards_poster_transparent.png) | [SVG](model_cards_poster.svg) | [PDF](model_cards_poster.pdf) |

The detailed figure retains all 126 terminal schema paths, 50 rubric10 subitems, 20 rubric20 questions and section totals. Its PNG is 6000 × 3675 pixels. The poster aggregates field presence into ten groups and shows the two overall rubric scores for each model, with larger text and fewer labels. Its PNG is 4800 × 3240 pixels at 300 dpi. Use SVG or PDF for scalable poster placement; SVG text remains editable. Cell hover titles preserve exact group names and counts.

The poster's background is the teal of the Model Cards panel on the Bridge2AI Standards Portfolio poster (`#2f719a`). Its heatmap sits on a white rounded box and keeps the detailed figure's shading: darker cells mean higher values. One legend at the bottom of the box covers both panels, with its color ramp centered on the figure. The box sits inside the part of the figure the portfolio poster shows (its center crop, y 145–931 of 1080). That crop hides the footer caveats, so a note under the rubric scores says they rate the documentation, not model performance.

In both figures, each cell's label is white or black, whichever contrasts more with its fill. One of the two always reaches at least 4.58:1, so the shared blue scale needed no change.

**Place `model_cards_poster_transparent.png` on the portfolio poster.** It holds only the white box, on a transparent canvas, so the panel's own gradient shows around it; one flat teal cannot match that gradient everywhere. It leaves out the title and caveat lines: the poster's crop hides them, and their light text would vanish on a light background. The teal PNG, SVG and PDF are for standalone use. The previous white-background version is kept under `archive/white-background-2026-09-28/` in the slide-assets folder.

## Current values

| Measure | DenseNet-121 | SubCell 650M |
|---|---:|---:|
| Populated terminal paths | 74/126 (58.7%) | 80/126 (63.5%) |
| Hybrid rubric10 | 47/50 (94.0%) | 45/50 (90.0%) |
| Hybrid rubric20 | 67/84 (79.8%) | 62/84 (73.8%) |

Poster percentages are rounded directly from the exact fractions to whole percentages: 59% and 63% field presence; 94% and 90% rubric10; 80% and 74% rubric20. Exact fractions remain visible. Rounding SubCell's 80/126 directly gives 63%; rounding the already rounded 63.5% again would incorrectly give 64%.

The original supplied figure used archived June semantic ratings. **These updated figures use deterministic hybrid evaluations bound to the current YAML hashes. No new semantic/LLM evaluation was performed.** Old semantic scores must not be compared with the current hybrid scores as a before/after improvement. The revised captions identify the method change.

## Counting and interpretation

Presence counts non-empty values at terminal schema paths, collapsing list indices; a path counts once if any entry contains a value. Null, blank and empty values do not count; zero and false do. A narrative elsewhere does not populate an absent structured field. Optional and extension fields remain in the 126-path denominator, so absent values are not automatically defects or applicable omissions.

The poster separates architecture/data, compute and training to preserve visible gaps. Both cards have zero of five structured compute fields populated; this is a documentation finding, not a measurement of compute use. The other seven field groups retain the detailed figure's grouping.

Hybrid evaluators apply structural and keyword heuristics; they are not independent factual verification. Rubric20's dataset-name overlap rule is not proof of data leakage, and its Q19 keyword check can miss relevant prose. Its “Performance & FAIRness” category concerns documentation and FAIR principles, not a demonstrated bias/fairness outcome. Original-run records and prediction-level uncertainty remain unresolved in issues #33–#35.

## Provenance and verification

[provenance.json](provenance.json) records source, schema, evaluator, selected-result and builder hashes. [figure_data.json](figure_data.json) contains both models' exact totals and section aggregations; [poster_provenance.json](poster_provenance.json) binds the poster to those data and its renderer/output files. The recorded Git HEAD is context; individual file hashes identify the exact input bytes, including any uncommitted changes.

- Detailed builder selects only hash-matching hybrid evaluations, takes the latest timestamp and rejects conflicting ties. It reruns the current deterministic evaluators and checks every scoring/evidence field against the selected results.
- All 252 presence cells, 140 rubric cells, section sums and displayed totals were checked independently. Poster counts partition the same 126 paths.
- Both SVGs contain vector artwork and editable text, without embedded raster images. Layout checks and visual review found no clipped or overlapping labels.

The exact rows and evidence are in [field_presence.csv](field_presence.csv) and [scores.csv](scores.csv). Archived semantic scores are not included in these current totals.

## Reproduction

Requires Python, Matplotlib and PyYAML. Both scripts also need Arial or a metric-compatible font (Liberation Sans or Arimo), in regular and bold. Without one they stop with an error, because their layouts assume Arial's widths. Re-running them on unchanged inputs and fonts reproduces every figure byte for byte; only the `generated_at` timestamps in `figure_data.json` and `provenance.json` change. `poster_provenance.json` records the font files the poster used. From the model-card-schema repository root:

```bash
python scripts/build_model_card_heatmaps.py --repo . \
  --output-dir data/poster_assets/model-card-heatmaps
python scripts/render_model_card_poster.py \
  --input data/poster_assets/model-card-heatmaps/figure_data.json \
  --output-dir data/poster_assets/model-card-heatmaps
```

The slide-assets copy includes both builders under `build_heatmap.py` and `render_model_card_poster.py`. From that folder:

```bash
python build_heatmap.py --repo /path/to/model-card-schema --output-dir .
python render_model_card_poster.py --input figure_data.json --output-dir .
```

If a card changes, first rerun its hybrid evaluators; the figure builder rejects stale evaluations. The prior semantic figure and its original supporting files are preserved under `archive/original-semantic-2026-09-28/` in the slide-assets folder.

## What is on GitHub

Both scripts and this whole folder are in bridge2ai/model-card-schema:
- PR #40 published the poster renderer.
- The follow-up heatmap PR publishes the builder (`scripts/build_model_card_heatmaps.py`), the detailed figure, the CSVs, `provenance.json` and this README.
- PR #54 publishes the SubCell card version and the two evaluation results that these figures cite. Once it merges, every input hash in `figure_data.json` and `provenance.json` resolves on GitHub (issue #43).

The slide-assets folder holds the builder as `build_heatmap.py`.
