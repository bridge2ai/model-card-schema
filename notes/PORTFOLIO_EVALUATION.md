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

## Hybrid vs LLM (full cross-evaluator)

LLM rubric10 and rubric20 now also run on the HF Hub-ported cards. Updated portfolio:

| Card | r10 hybrid | r10 LLM | Δ | r20 hybrid | r20 LLM | Δ |
|---|---:|---:|---:|---:|---:|---:|
| climate-model-extended | 47/50 (94%) | 44/50 (88%) | hybrid +6 | 73/84 (87%) | 76/84 (91%) | hybrid −4 |
| climate-forecasting (harmonized) | 48/50 (96%) | — | — | 75/84 (89%) | — | — |
| sentiment-classifier (harmonized) | 41/50 (82%) | — | — | 53/84 (63%) | — | — |
| densenet121.tv_in1k (HF) | 41/50 (82%) | 43/50 (86%) | hybrid **−4** | 59/84 (70%) | 63/84 (75%) | hybrid −5 |
| subcell-saprot-650m (HF) | 44/50 (88%) | 42/50 (84%) | hybrid +4 | 65/84 (77%) | 66/84 (79%) | **≈ peer** |

### Where hybrid and LLM disagree

- **DenseNet**: LLM higher than hybrid — the LLM credits Element 7 (Scientific Motivation) at only 2/5 (no NIH/NSF/DOE grant on a permissively-licensed academic model is reasonable) but the hybrid's keyword scan was generous. Hybrid drops Element 5 to 2/5 because the timm card doesn't disclose training hyperparameters; LLM gives 3/5 acknowledging the architecture is well-described. Net: LLM ends 4pp higher because it's more forgiving about missing training procedure on a 2017 checkpoint.
- **SubCell**: hybrid higher than LLM on rubric10 (+4pp). Hybrid credits Element 7 (4/5) for SaProtHub university affiliation as "funding"; LLM disagrees (2/5, "no concrete funding agency named"). LLM also drops Element 6 to 4/5 because contributors lack ORCIDs / explicit roles.
- **SubCell rubric20**: ≈ peer (77.4% vs 78.6%, within 2pp). Best agreement of the portfolio — the SaProtHub card is structurally complete enough that both evaluators agree on the major categories.

### Sign of the gap

Across the 3 cards with both evaluators run:
- 2 of 3 rubric10 runs have hybrid more lenient (climate-extended +6, SubCell +4); 1 has hybrid stricter (DenseNet −4)
- 3 of 3 rubric20 runs have hybrid stricter (climate-extended −4, DenseNet −5, SubCell ≈)

Pattern: **hybrid rubric20 is consistently more conservative than LLM** (no false positives from keyword matching because the rubric20 heuristics are tighter). **Hybrid rubric10 is more variable** — it can go either way depending on the card's surface signals.

Takeaway: rubric20 hybrid is the most calibrated of the four scorers and is the best candidate for CI gating. Rubric10 hybrid is fine as a quick smoke test but shouldn't be the gate.

## Open follow-ups

- Run LLM rubrics against the two harmonized cards (climate-forecasting and sentiment-classifier) to complete the LLM column
- Add the four "authoring gotchas" above to `.goosehints` so the @mcassistant workflow avoids them
- Build a known-bad / minimal Model Card fixture so the rubric score floor is anchored (currently the lowest score in the portfolio is 63% — none of the cards are genuinely bad)
- Consider a `--badge` mode in the renderer that emits SVG quality-tier badges to drop into READMEs
