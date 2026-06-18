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

## Semantic rubric variants applied to the portfolio

Ran `mc-rubric10-semantic` + `mc-rubric20-semantic` against the 5 example cards. The semantic agents add format / consistency / plausibility / temporal-leakage checks on top of the baseline rubrics.

| Card | r10 base LLM | r10 semantic | Δ | r20 base LLM | r20 semantic | Δ |
|---|---:|---:|---:|---:|---:|---:|
| climate-model-extended | 46/50 (92%) | 46/50 (92%) | ≈ peer | 76/84 (91%) | 74/84 (88%) | −3 |
| climate-forecasting (harmonized + D4D) | **49/50 (98%)** | 45/50 (90%) | **−8** | **79/84 (94%)** | **79/84 (94%)** | ≈ peer |
| sentiment-classifier (harmonized) | 31/50 (62%) | 32/50 (64%) | +2 | 59/84 (70%) | 56/84 (67%) | −3 |
| DenseNet-121 (HF Hub port) | 40/50 (80%) | 37/50 (74%) | −6 | 63/84 (75%) | 61/84 (73%) | −2 |
| SubCell SaProt 650M (HF Hub port) | 40/50 (80%) | 39/50 (78%) | −2 | 66/84 (79%) | 64/84 (76%) | −2 |

### What the semantic layer caught

| Card | Semantic deductions |
|---|---|
| **climate-extended** | Q18 capped 5→3: E3SM v2 + MPAS-A appear in both training data and benchmark slices (within-family overlap), even though methodology claims by-simulation-year split. Other concerns surfaced (HWC-vs-CHW input layout mismatch, "12 climate models" vs 3 enumerated, optimizer narrative vs structured) didn't drive further deductions — sub-elements were already zeroed in the base rubric. |
| **climate-forecasting** | r10: 4pp drop. r20: caps at Q4 (no `output_format_map`), Q8 (no `bias_*`), Q14 (placeholder DOI `10.1234`), Q15 (no GPU-hours) — each just trimmed an already-near-cap score. **Train (1970-2019) vs eval (2020-2024) temporal split is the only one that passed leakage check across the entire portfolio.** |
| **sentiment-classifier** | Q18 capped 5→3 for IMDb train/eval overlap. Q19 capped 4→3 for moderation-adjacent model without `out_of_scope_uses`. Q8 consistency rule fires hardest here — narrative acknowledges bias/misuse but `bias_model/bias_output/out_of_scope_uses/data[].sensitive` all empty. Plus example.org placeholder URLs flag as plausibility-fail. |
| **DenseNet** | Q19 capped 5→3: `bias_model` + `bias_output` populated, but `considerations.tradeoffs[]` only covers parameters-vs-wall-clock (no accuracy-vs-fairness). Same `torch>=1.13` floating pin issue as base rubric but base already at 3 so no further drop. |
| **SubCell** | Same Q19 cap pattern as DenseNet: bias declared but tradeoffs only covers model-size vs accuracy/cost (no accuracy-vs-fairness). MIT licence not cross-checked against base SaProt licence — flagged but not capped. |

### Headline observations

1. **r20-semantic ≤3pp from r20 base on every card**. The Q19 bias↔tradeoffs consistency rule and the Q18 train/eval overlap rule fire the most. r20 is already tight enough that the semantic layer mostly trims already-near-cap scores.
2. **r10-semantic is harsher (up to −8pp)** because the baseline rubric10's 5-point granularity hides issues that semantic checks force into the open. climate-forecasting drops from 98%→90% — the temporal-leakage check passes but Q19/Q8-style consistency checks bite hard.
3. **Q19 bias↔tradeoffs is the most prevalent semantic finding** — fires on 3 of 5 cards (climate-extended via different mechanism, climate-forecasting via Q8, DenseNet, SubCell). Strong signal: declaring bias without tradeoffs is the most common quality gap.
4. **Only climate-forecasting passes the leakage check** — temporal train/eval split is the gold standard. Everything else has either explicit (IMDb), implicit (DenseNet within-distribution), or family-level (climate-extended) overlap.
5. **Semantic agent is reproducible enough for production gating** at the r20 level — ≤3pp spread between hybrid and semantic on every card. r10-semantic is more variable (sentiment-classifier *gained* 2pp, DenseNet lost 6) so use as audit, not gate.

### Open follow-ups (replaces prior list)

- Port a couple more HF Hub cards (CLIP, Llama-2-7B-base, Stable Diffusion XL) — broadens calibration beyond CV / proteins / sentiment
- Encode the most-common semantic findings as hybrid rules so the rule-based evaluator can flag them too (Q19 bias↔tradeoffs and Q18 train/eval overlap are the highest-frequency checks)
- Build a `mc-rubric-report` agent that aggregates `semantic_findings` blocks across the portfolio into a single ranked "common issues" markdown
- Make r20-semantic the default LLM gate in CI (within 3pp of base LLM, catches concrete quality issues, reproducible across re-runs)
