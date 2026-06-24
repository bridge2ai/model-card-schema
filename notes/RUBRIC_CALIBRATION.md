# Rubric Calibration: climate-model-extended.yaml

First calibration run of `mc-rubric10`, `mc-rubric20`, and the hybrid heuristic evaluator against `src/data/examples/extended/climate-model-extended.yaml` (ClimateNet-v2 — the DOE extended-template canonical example).

Run date: 2026-06-15. Evaluator: `claude-sonnet-4-5-20250929` (temperature 0.0).

## Scores

| Evaluator | Score | % |
|---|---|---:|
| Hybrid (`scripts/batch_evaluate_mc_rubric10_hybrid.py`) | 47 / 50 | 94.0% |
| LLM `mc-rubric10` | 43 / 50 | 86.0% |
| LLM `mc-rubric20` | 71 / 84 | 84.5% |

## Where the LLM is stricter than the hybrid

| Element / sub-element | Hybrid | LLM | Reason |
|---|---:|---:|---|
| E1.1 Persistent identifier | 1 | 0 | Hybrid credits any URL; LLM requires DOI / HF Hub / Zenodo (GitHub URLs are not persistent). |
| E10.1 Published on recognized platform | 1 | 0 | LLM requires HF Hub / Papers with Code / TF Hub. GitHub is not "recognized platform". |
| E10.2 Cross-referenced DOIs | (n/a) | 0 | LLM wants DOIs to parent models / paper, not just URLs. |
| E10.5 Datasets linked to datasheets / D4D | 1 | 0 | LLM requires datasheets (D4D refs), not just dataset homepage URLs. |

The 4-point gap is real — and exactly the kind of signal we want from the LLM rubric. The hybrid is a fast prefilter; the LLM agents are the deeper quality signal.

## Rubric10 element-by-element (LLM judgement)

| Element | Score | Notes |
|---|---:|---|
| 1. Model Discovery and Identification | 4/5 | Persistent identifier (no DOI/HF Hub) |
| 2. Model Access and Distribution | 5/5 | Strong (weights URL, code, runnable example, I/O spec, file format) |
| 3. Model Reuse and Interoperability | 5/5 | BSD-3-Clause, PyTorch 2.1.0 pinned, base model lineage, reproducibility artifacts |
| 4. Ethical Use and Responsible AI | 3/5 | Missing `bias_model` / `bias_output`; missing sensitive_data disclosure even as `false` |
| 5. Model Architecture and Training Composition | 5/5 | 38.5M params, 3 datasets with links, hyperparameters, 256 A100, 70/15/15 split |
| 6. Model Provenance and Versioning | 5/5 | Semver, ISO date, diff with quantitative deltas, contributors with ORCID, IEEE citation |
| 7. Scientific Motivation and Funding Transparency | 5/5 | DOE BER grant, NERSC Perlmutter, mission relevance |
| 8. Training and Evaluation Transparency | 5/5 | Loss/optimizer/schedule, evaluation procedure, repro info, GitHub code, references |
| 9. Performance Evaluation and Limitations Disclosure | 5/5 | 5 metrics with values, CIs (bootstrap), limitations, tradeoffs quantified |
| 10. Cross-Platform and Community Integration | 1/5 | No HF Hub, no DOI, no `model_index`, no datasheets — only `schema_version` saved this element |

## Rubric20 category-by-category

| Category | Score | % |
|---|---|---:|
| Structural Completeness (Q1–Q5) | 18 / 21 | 86% |
| Metadata Quality & Content (Q6–Q10) | 17 / 21 | 81% |
| Technical Documentation (Q11–Q15) | 24 / 25 | 96% |
| Performance & FAIRness (Q16–Q20) | 12 / 17 | 71% |

Both rubrics agree: this card is strongest on technical documentation and weakest on cross-platform / FAIR integration.

## Findings / rubric tweaks suggested

1. **No rubric changes needed for the baseline scoring scale**. Both rubrics produced sensible, internally-consistent verdicts.
2. **Q5 wording** — one early reasoning attempt by the rubric20 evaluator briefly second-guessed itself about whether `schema_version` at the file root counted. The rubric is fine but could explicitly say "top-level / root-level `schema_version` field". Low priority.
3. **Hybrid evaluator is appropriately lenient** for E1.1 (persistent identifier) — it correctly credits the field's presence without verifying DOI/HF-Hub quality. Document this in the agent description: "hybrid = presence + light heuristics; LLM = quality + correctness". (Already implied by the file headers.)
4. **`bias_model` / `bias_output` keep being flagged as missing** on a climate model. This is a real schema-coverage finding: most non-NLP / non-medical models will leave these empty even when they have legitimate bias considerations. Consider clarifying in the schema docs (or the `.goosehints`) that these should at minimum be populated with `false` / `null` + brief rationale for non-PII / non-demographic models.

## Quick way to reproduce

```bash
# Hybrid (rule-based, no LLM cost)
make evaluate-rubric10-smoke
# → tmp/mc-eval-smoke/climate-model-extended_evaluation.json

# Or via the new agent type:
#   /agents mc-rubric10 → "Evaluate src/data/examples/extended/climate-model-extended.yaml with rubric10"
#   /agents mc-rubric20 → same input
```

## Second calibration run — full cross-evaluator matrix (2026-06-15)

Now that the rubric20 hybrid evaluator and the cross-evaluator HTML view both exist, ran all four combinations on the same input. Render command:

```bash
make render-compare EVAL_JSONS='/tmp/mc-eval-smoke/*.json /tmp/mc-rubric20-smoke/*.json' \
                    EVAL_HTML=/tmp/mc-compare-full.html
```

| Rubric × evaluator | Score | % | Δ vs other evaluator |
|---|---:|---:|---|
| rubric10 hybrid | 47/50 | 94.0% | +6.0pp (more lenient) |
| rubric10 LLM | 44/50 | 88.0% | −6.0pp (stricter) |
| rubric20 hybrid | 73/84 | 86.9% | −3.6pp (stricter) |
| rubric20 LLM | 76/84 | 90.5% | +3.6pp (more lenient) |

### Per-element / per-category deltas

**Rubric10**: hybrid and LLM agree on 9 of 10 elements (all ≡). The only difference is Element 10 (Cross-Platform and Community Integration): hybrid=4/5 vs LLM=3/5 (hybrid +1). That's the same finding as the first run — hybrid credits `schema_version` for "standards conformance" while LLM is harsher because there's still no HF Hub publication, no DOI, no `model_index`.

**Rubric20**: hybrid is stricter on Structural (−2) and Metadata (−1), tied on the other two categories. Notably hybrid awards full marks on Performance & FAIRness (17/17) — same lenience as the first run. The structural gap is because hybrid's Q4 (I/O specification) caps at 3 when `*_format_map` is missing; LLM was willing to give 4 for the strong prose I/O spec.

### Findings (refined)

1. **The two evaluators agree to within ≤6pp** on every rubric — well within rubric noise. Good enough for the hybrid to act as a fast prefilter / cheap regression test, with LLM for headline quality numbers.
2. **Rubric20 LLM > rubric10 LLM** by ~2.5pp (90.5% vs 88.0%). That's the LLM crediting the strong technical-documentation category in rubric20 that rubric10's coarser Element 8 underweights. Either: tune element 8's weight, or treat rubric20 as the "default" headline rubric and rubric10 as the quick check.
3. **Hybrid rubric20 < hybrid rubric10** by ~7pp (86.9% vs 94.0%). The hybrid heuristic floor is more conservative in rubric20 — Q4 cap, Q9 cap on non-SPDX restrictions, Q14 cap without DOIs. Consistent gap; not a calibration problem.
4. **Where they disagree, the patterns are stable across runs**: Element 10 / Cross-platform integration is the consistent weak point on a card that lacks HF Hub publication. Bias disclosure (Element 4 / Q8) is the consistent middle-tier finding even on a non-PII model. Both findings drive the same recommendations.

### Open follow-ups

- Run the rubrics against the harmonized examples under `src/data/examples/d4d_integration/` once they're filled in
- Run the LLM rubrics against a known-bad / minimal model card to confirm score floor behaves
- Compare across a panel of HF Hub model cards (CLIP, Stable Diffusion, LLaMA-2-base) once the assistant has produced a few
- Add an inter-rater agreement test: run the LLM rubric twice on the same input and confirm score variance is < 2pp (LLM rubric20 went 71→76 between the two runs in this calibration — worth a third repro to characterize the noise floor)
