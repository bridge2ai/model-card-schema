# Portfolio Evaluation: Harmonized Examples + HF Hub Cards

First multi-card hybrid evaluation across the full example set. Run date: 2026-06-15.
Render commands at the bottom; HTML reports in `data/evaluation/all/`.

## Hybrid scores

| Model card | Source | rubric10 | rubric20 |
|---|---|---:|---:|
| climate-model-extended.yaml | Curated DOE example (base schema) | **47/50 (94%)** | **73/84 (87%)** |
| climate-forecasting-model-card.yaml | Curated DOE example (harmonized + D4D refs) | **48/50 (96%)** | **75/84 (89%)** |
| sentiment-classifier-with-datasheet-refs.yaml | Curated example (harmonized + D4D refs) | **41/50 (82%)** | **53/84 (63%)** |
| densenet121_tv_in1k_model_card.yaml | Ported from HF Hub (timm) | **41/50 (82%)** | **59/84 (70%)** |
| subcell_saprot_650m_model_card.yaml | Ported from HF Hub (SaProtHub) | **44/50 (88%)** | **65/84 (77%)** |

## Findings

### Harmonized examples

Both harmonized cards validate cleanly with the schema-description-audit fixes applied. The hybrid evaluators needed to be taught about harmonized-specific slots:

- `model_details.creator_references` (replaces `owners` / `contributors`)
- `model_parameters.training_datasets` + `evaluation_datasets` (replaces `data`)
- `funding_grants` (replaces `funding_source` / inline acknowledgements)

After the fix, `climate-forecasting-model-card.yaml` went from 92% → 96% on rubric10 — picking up Element 5 (Training Data Documented) and Element 6 (Owners/Contributors Identified) once it recognized the harmonized layout.

### HF Hub porting

Translating two real Hugging Face Hub cards into the MC schema:

- **DenseNet-121** (`timm/densenet121.tv_in1k`): 82% rubric10 / 70% rubric20. Strong on identity, license, references, citations, and architecture. Weak on:
  - Training procedure (HF card doesn't disclose original torchvision hyperparameters)
  - Compute infrastructure (not on the HF card)
  - No `model_index` benchmark block; metrics included but not Papers-with-Code shape
  - No CIs on accuracy values
- **SubCell SaProt 650M** (`SaProtHub/Model-Subcellular_Localization-650M`): 88% rubric10 / 77% rubric20. The HF card was unusually complete on training hyperparameters (optimizer, LR, epochs, batch size, LoRA config) which lifted Technical Documentation. Still missing:
  - Compute infrastructure
  - No CIs on the 85.75% test accuracy
  - No `model_index` block

The DenseNet card's lower rubric20 score traces to **Technical Documentation 11/25 (44%)** — that category is hardest to populate from an HF Hub source because most HF cards don't publish training details. Suggests rubric20 is correctly identifying the gap between "well-described model" and "reproducibly-trained model".

### Schema validation gotchas hit during porting

Common mistakes when authoring an MC YAML from scratch — useful for the `mcassistant` agent to know:

1. **CitationStyleEnum** is `[MLA, APA, Chicago, IEEE]` — not `bibtex` (despite many users having BibTeX entries). Use `IEEE` and put the formatted text into `citation:`.
2. **`bias_input`** is a slot on `dataSet`, NOT at the `modelCard` root. Only `bias_model` and `bias_output` are root-level.
3. **`SensitiveData`** only has the `sensitive_data` slot (multivalued string list). It does NOT have `sensitive_data_used` (boolean) — that field doesn't exist.
4. **`performance_metrics[].value`** is a number (float/int) — not a string. Don't prefix with `~`; use raw numbers.

These are not rubric issues — they're authoring traps. Worth adding to `.goosehints` as explicit "things the assistant will get wrong on first try".

## Comparison view

Open `data/evaluation/all/portfolio_compare.html` to see all 5 cards in the cross-evaluator matrix UI (hybrid scores only for now; LLM scores join automatically when you run the LLM rubric agents and save their JSON).

## Reproduce

```bash
# Re-run hybrid evals
make evaluate-rubric10 MC_INPUT_GLOB='src/data/examples/{extended,harmonized,d4d_integration}/*.yaml data/model_cards_assistant/*.yaml' MC_EVAL_DIR=data/evaluation/all/rubric10
make evaluate-rubric20 MC_INPUT_GLOB='src/data/examples/{extended,harmonized,d4d_integration}/*.yaml data/model_cards_assistant/*.yaml' MC_EVAL20_DIR=data/evaluation/all/rubric20

# Render portfolio and comparison
make render-eval     EVAL_JSONS='data/evaluation/all/**/*.json' EVAL_HTML=data/evaluation/all/portfolio.html
make render-compare  EVAL_JSONS='data/evaluation/all/**/*.json' EVAL_HTML=data/evaluation/all/portfolio_compare.html
```

## Hybrid vs LLM (historical — partial coverage, pre-PR-#25-fix)

> **Note**: this section is preserved for the calibration history. The numbers here are from before the PR #25 scoring fixes (the q19 list-vs-string fix, the q9 SPDX-permissive-can-reach-5/5 fix, the harmonized funding_grants path fix) and before the harmonized cards had LLM scores. **The canonical post-fix numbers are in the "Final cross-evaluator portfolio" section below.**

| Card | r10 hybrid (pre-fix) | r10 LLM (pre-fix) | Δ | r20 hybrid (pre-fix) | r20 LLM (pre-fix) | Δ |
|---|---:|---:|---:|---:|---:|---:|
| climate-model-extended | 47/50 (94%) | 44/50 (88%) | hybrid +6 | 73/84 (87%) | 76/84 (91%) | hybrid −4 |
| climate-forecasting (harmonized) | 48/50 (96%) | — | — | 75/84 (89%) | — | — |
| sentiment-classifier (harmonized) | 41/50 (82%) | — | — | 53/84 (63%) | — | — |
| densenet121.tv_in1k (HF) | 41/50 (82%) | 43/50 (86%) | hybrid −4 | 59/84 (70%) | 63/84 (75%) | hybrid −5 |
| subcell-saprot-650m (HF) | 44/50 (88%) | 42/50 (84%) | hybrid +4 | 65/84 (77%) | 66/84 (79%) | ≈ peer |

The analysis below the table (where hybrid/LLM disagree, sign of the gap) used these pre-fix scores. The post-fix tables show smaller divergences because of the PR #25 evaluator improvements.

## Final cross-evaluator portfolio (full LLM coverage)

After running mc-rubric10 + mc-rubric20 LLM agents against both harmonized cards, **all 5 example cards now have both hybrid and LLM scores on both rubrics**:

All scores below are read from the committed evaluation JSONs (post the PR #26 arithmetic fixes). Δ columns are percentage-point deltas. \"hybrid +N\" = hybrid scored N pp higher than LLM.

| Card | r10 hybrid | r10 LLM | Δ r10 | r20 hybrid | r20 LLM | Δ r20 |
|---|---:|---:|---:|---:|---:|---:|
| climate-model-extended (base) | 47/50 (94%) | 46/50 (92%) | hybrid +2 | 74/84 (88%) | 76/84 (91%) | hybrid −3 |
| **climate-forecasting (harmonized + D4D)** | **48/50 (96%)** | **49/50 (98%)** | **hybrid −2** | **79/84 (94%)** | **79/84 (94%)** | **≈ peer** |
| sentiment-classifier (harmonized) | 41/50 (82%) | 31/50 (62%) | hybrid **+20** | 54/84 (64%) | 59/84 (70%) | hybrid −6 |
| DenseNet-121 (HF Hub port) | 41/50 (82%) | 40/50 (80%) | hybrid +2 | 61/84 (73%) | 63/84 (75%) | hybrid −2 |
| SubCell SaProt 650M (HF Hub port) | 44/50 (88%) | 40/50 (80%) | hybrid +8 | 65/84 (77%) | 66/84 (79%) | hybrid −2 |

### Headline findings

1. **Climate-forecasting (harmonized + D4D) is now the top scorer** — 98% r10 LLM / 94% r20 LLM. r20 hybrid + LLM are exactly tied at 79/84. The harmonized + D4D pattern is the production target for new model cards.
2. **Sentiment-classifier r10 hybrid +20pp** is the largest divergence in the whole calibration. The hybrid awards generous presence-only credit (82%); the LLM downgrades to 62% for thin training procedure (1/5), thin model access (2/5), and placeholder URLs. **This is the LLM correctly punishing thin content the hybrid can't distinguish from substantive content.**
3. **r20 hybrid is consistently within ≤6pp of LLM** across all 5 cards, always within the LLM's favor — meaning r20 hybrid will not falsely pass thin content. Safe as a quality gate.
4. **r10 hybrid is NOT safe as a sole gate** — it can over-credit thin cards by up to 20pp. Smoke-test only.
5. The harmonized variant pattern (creator_references, training_datasets, evaluation_datasets, mission_relevance.funding_grants) scores cleanly across both rubrics now that the post-review fixes landed.

### Score range

Across the 20 (5 cards × 4 evaluators) scores in the Final table, the portfolio spans:

- **High**: 98% / 49/50 — climate-forecasting r10 LLM
- **Median**: ~82–88% — most cards on most evaluators
- **Low**: 62% / 31/50 — sentiment-classifier r10 LLM

Distinct from the original "everyone scored 70%+" symptom that motivated the floor fixtures (which anchor 0% and ~30%). The 36pp spread between the highest and lowest card establishes that the rubrics do discriminate.

## Open follow-ups

- Now that all 5 cards have both hybrid + LLM scores, port a couple more HF Hub cards (CLIP, Llama-2-7B-base, Stable Diffusion XL) to expand the calibration set beyond CV / proteins / sentiment
- Run the semantic rubric variants (mc-rubric10-semantic, mc-rubric20-semantic) on the same portfolio to characterize the cost in points of failing format / consistency / plausibility checks
- Build a `make compare-portfolio` Makefile target that re-renders portfolio_compare.html + badges from the canonical evaluation directories in one command
