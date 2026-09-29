# Current model-card heatmaps

Updated September 28, 2026 from the committed DenseNet-121 and SubCell 650M cards. Both figures use the same verified inputs. They measure documentation, not model performance.

| Figure | PNG preview | Editable SVG | Vector PDF |
|---|---|---|---|
| Detailed | [PNG](model_cards_scores_and_field_presence.png) | [SVG](model_cards_scores_and_field_presence.svg) | [PDF](model_cards_scores_and_field_presence.pdf) |
| Simplified poster | [PNG](model_cards_poster.png) · [transparent PNG for the portfolio poster](model_cards_poster_transparent.png) | [SVG](model_cards_poster.svg) | [PDF](model_cards_poster.pdf) |

The detailed figure retains all 126 terminal schema paths, 50 rubric10 subitems, 20 rubric20 questions and section totals. Its PNG is 6000 × 3675 pixels. The poster aggregates field presence into ten groups and shows the two overall rubric scores for each model, with larger text and fewer labels. Its PNG is 4800 × 3240 pixels at 300 dpi. Use SVG or PDF for scalable poster placement; SVG text remains editable. Cell hover titles preserve exact group names and counts.

The poster's background is the teal of the Model Cards panel on the Bridge2AI Standards Portfolio poster (`#2f719a`). Its heatmap sits on a white rounded box, where darker cells mean higher values. One legend at the bottom of the box covers both panels, with its color ramp centered on the figure. The box sits inside the part of the figure the portfolio poster shows (its center crop, y 145–931 of 1080). That crop hides the footer caveats, so a note in dark 20-pt text under the rubric scores says they rate the documentation, not model performance.

**Place `model_cards_poster_transparent.png` on the portfolio poster.** It holds only the white box, on a transparent canvas, so the panel's own gradient shows around it; one flat teal cannot match that gradient everywhere. It leaves out the title and caveat lines: the poster's crop hides them, and their light text would vanish on a light background. The teal PNG, SVG and PDF are for standalone use.

## Color and labels

The poster's cells and panel D of the detailed figure use the same continuous blue scale, `#f0efec` → `#9ec5f4` → `#2874d0` → `#104281`, so a given fraction gets the same fill in both figures. Panels A–C of the detailed figure show binary presence, binary checks and 0–5 scores in discrete steps of the same blue palette.

In both figures each cell label is white or black, whichever contrasts more with its fill; one of the two always reaches at least 4.58:1. The scale's middle stop is `#2874d0`, a barely distinguishable shade darker than the earlier `#2a78d6`, so white text reaches 4.67:1 there too. Every cell label in both figures is at least 4.67:1.

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

[provenance.json](provenance.json) records the source schema, cards, evaluators, selected results and builder, each with its SHA-256. It also records whether each input was committed (tracked and unmodified), plus the font files and Matplotlib version used. [figure_data.json](figure_data.json) contains both models' exact totals and section aggregations; [poster_provenance.json](poster_provenance.json) binds the poster to those data and to its renderer, fonts and output files. No local paths are recorded: the builder notes the repository's remote URL without credentials, and it refuses to write a file that would contain the home directory.

- The builder selects only hash-matching hybrid evaluations, takes the latest timestamp and rejects conflicting ties. It reruns the current deterministic evaluators and checks every scoring/evidence field against the selected results.
- It refuses to write into this folder if any input is untracked or modified, so the published provenance never cites files missing from GitHub. `--allow-uncommitted` overrides this for local drafts.
- All 252 presence cells, 140 rubric cells, section sums and displayed totals were checked independently. Poster counts partition the same 126 paths.
- Both SVGs contain vector artwork and editable text, without embedded raster images. Both scripts check that no text leaves the canvas or overlaps other text. The poster also checks that its dark text stays inside the white box and that the box stays inside the portfolio poster's crop.

The exact rows and evidence are in [field_presence.csv](field_presence.csv) and [scores.csv](scores.csv). Archived semantic scores are not included in these current totals; the semantic baseline is in `notes/model_card_remediation/baseline/`.

## Reproduction

Requires Python, Matplotlib and PyYAML. Both scripts also need Arial or a metric-compatible font (Liberation Sans or Arimo), in regular and bold. Without one they stop with an error, because their layouts assume Arial's widths. If you have just installed such a font, delete Matplotlib's font cache (`fontlist-*.json` in `matplotlib.get_cachedir()`) before rerunning.

With the same Matplotlib version (3.10.9 here) and the same font files, re-running on unchanged inputs reproduces every figure and CSV byte for byte. Each builder run rewrites `generated_at` in `figure_data.json` and `provenance.json`, which also changes `poster_provenance.json`'s `input_sha256`. `checkout_commit` records whichever commit is checked out.

From the model-card-schema repository root:

```bash
python scripts/build_model_card_heatmaps.py --repo .
python scripts/render_model_card_poster.py \
  --input data/poster_assets/model-card-heatmaps/figure_data.json \
  --output-dir data/poster_assets/model-card-heatmaps
```

If a card changes, first rerun its hybrid evaluators; the builder rejects stale evaluations.

## What is on GitHub

Both scripts and everything in this folder are published in bridge2ai/model-card-schema:
- #40 published the poster renderer.
- #55 publishes the builder, the detailed figure, the CSVs, `provenance.json` and this README.
- #54 publishes the SubCell card version and the two evaluation results these figures cite.

With both merged, every input hash in `figure_data.json` and `provenance.json` resolves on `main` (issue #43).

## Maintainer's working copy

The maintainer also keeps a private copy of this folder with the slide assets. It is not in this repository. There the builder is named `build_heatmap.py`, and an `archive/` folder keeps earlier versions: the original semantic figure, the white-background poster, and the detailed figure before bold and label-contrast fixes.
