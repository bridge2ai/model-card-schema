# Common Semantic Findings — Portfolio Report

Aggregated from 10 semantic evaluation file(s) covering 5 card(s).  Ranked by number of distinct cards affected. Findings already encoded as deterministic hybrid rules are marked with a coverage tag — these no longer need an LLM to flag them. Uncovered findings near the top are the next candidates to encode.

## Top findings (ranked by card coverage)

| # | Cards | Category | Rubric | Rule / Field | Hybrid coverage |
|---|---:|---|---|---|---|
| 1 | 3 | format | rubric10 | model_parameters.compute_infrastructure | — |
| 2 | 2 | format | rubric10 | framework_version | — |
| 3 | 2 | format | rubric20 | framework_version | — |
| 4 | 2 | format | rubric10 | mission_relevance | — |
| 5 | 2 | format | rubric10 | model file format | — |
| 6 | 2 | format | rubric10 | model_details.path | — |
| 7 | 2 | format | rubric10 | model_details.version.name | — |
| 8 | 2 | format | rubric10 | model_index | — |
| 9 | 2 | format | rubric10 | model_parameters.training_procedure | — |
| 10 | 1 | format | rubric10 | base_model (top-level) | — |
| 11 | 1 | plausibility | rubric10 | base_model / lineage | — |
| 12 | 1 | consistency | rubric10 | base_model ↔ license compatibility | — |
| 13 | 1 | consistency | rubric20 | benchmark dataset != training dataset | ✅ `train_eval_leakage` |
| 14 | 1 | consistency | rubric20 | benchmark dataset != training dataset (no train/eval leakage) | ✅ `train_eval_leakage` |
| 15 | 1 | consistency | rubric20 | benchmark dataset ↔ training data (train/eval leakage) | ✅ `train_eval_leakage` |
| 16 | 1 | consistency | rubric10 | bias acknowledged -> fairness-vs-accuracy tradeoff expected in tradeoffs[] | ✅ `bias_tradeoff_gap` |
| 17 | 1 | consistency | rubric20 | bias disclosure -> tradeoffs (accuracy vs fairness) | ✅ `bias_tradeoff_gap` |
| 18 | 1 | consistency | rubric10 | Bias narrative -> sliced performance metrics | — |
| 19 | 1 | consistency | rubric20 | bias_* fields ↔ ethical_considerations | — |
| 20 | 1 | format | rubric10 | bias_model / bias_output | — |
| 21 | 1 | consistency | rubric10 | bias_model / bias_output → slice-level performance metrics | — |
| 22 | 1 | consistency | rubric10 | bias_model / bias_output → tradeoffs[] acknowledging accuracy vs fairness | ✅ `bias_tradeoff_gap` |
| 23 | 1 | consistency | rubric10 | bias_model/bias_output non-empty -> tradeoffs acknowledge accuracy-vs-fairness | ✅ `bias_tradeoff_gap` |
| 24 | 1 | consistency | rubric20 | bias_model/bias_output populated → tradeoffs must acknowledge accuracy-vs-fairness | ✅ `bias_tradeoff_gap` |
| 25 | 1 | consistency | rubric10 | Climate_justice ethical consideration ↔ bias disclosure | — |
| 26 | 1 | consistency | rubric10 | Climate_justice mitigation ↔ slice diversity | — |
| 27 | 1 | format | rubric10 | considerations (bias_model, bias_output) | — |
| 28 | 1 | format | rubric10 | considerations.out_of_scope_uses | — |
| 29 | 1 | plausibility | rubric10 | documentation completeness ratio | — |
| 30 | 1 | consistency | rubric10 | Documentation completeness ratio | — |
| 31 | 1 | consistency | rubric20 | ethical_considerations + out_of_scope_uses → at least one of bias_{input,model,output} populated | — |
| 32 | 1 | consistency | rubric20 | ethical_considerations mention bias -> bias_model/bias_input/bias_output fields populated | — |
| 33 | 1 | plausibility | rubric20 | evaluation_datasets vs. quantitative_analysis | — |
| 34 | 1 | consistency | rubric20 | funding / acknowledgement disclosure | — |
| 35 | 1 | consistency | rubric20 | high-risk / moderation model -> considerations.out_of_scope_uses populated | — |
| 36 | 1 | consistency | rubric10 | input_format vs code_examples | — |
| 37 | 1 | consistency | rubric20 | Large model scale → non-trivial compute_infrastructure expected | — |
| 38 | 1 | consistency | rubric10 | library_name 'transformers' -> HF Hub identifier expected | — |
| 39 | 1 | consistency | rubric10 | limitations[polar bias] vs bias_model / quantitative_analysis slices | — |
| 40 | 1 | format | rubric10 | model_details.citations | — |
| 41 | 1 | format | rubric20 | model_details.citations[0] | — |
| 42 | 1 | format | rubric10 | model_details.citations[0] | — |
| 43 | 1 | format | rubric10 | model_details.citations[] and references[] | — |
| 44 | 1 | format | rubric10 | model_details.citations[].citation | — |
| 45 | 1 | plausibility | rubric10 | model_details.contributors[].orcid | — |
| 46 | 1 | format | rubric10 | model_details.contributors[].orcid / email | — |
| 47 | 1 | format | rubric10 | model_details.creator_references[2].url | — |
| 48 | 1 | format | rubric10 | model_details.references | — |
| 49 | 1 | format | rubric20 | model_details.references | — |
| 50 | 1 | format | rubric10 | model_details.references / cross-refs | — |
| 51 | 1 | format | rubric20 | model_details.references[0].reference | — |
| 52 | 1 | plausibility | rubric10 | model_details.references[1].reference (DOI) | — |
| 53 | 1 | format | rubric10 | model_details.references[1].reference / model_details.citations[0].citation | — |
| 54 | 1 | format | rubric20 | model_details.references[].reference | — |
| 55 | 1 | format | rubric20 | model_details.version.name | — |
| 56 | 1 | format | rubric20 | model_parameters.compute_infrastructure | — |
| 57 | 1 | format | rubric10 | model_parameters.data[0].link | — |
| 58 | 1 | format | rubric10 | model_parameters.data[0].sensitive | — |
| 59 | 1 | format | rubric10 | model_parameters.data[0].sensitive.sensitive_data_used | — |
| 60 | 1 | format | rubric10 | model_parameters.data[].link | — |
| 61 | 1 | format | rubric10 | model_parameters.data[].sensitive.sensitive_data_used | — |
| 62 | 1 | format | rubric20 | model_parameters.input_format / output_format | — |
| 63 | 1 | format | rubric20 | model_parameters.output_format_map | — |
| 64 | 1 | format | rubric20 | model_parameters.training_procedure | — |
| 65 | 1 | plausibility | rubric10 | owner / landing page domains | — |
| 66 | 1 | format | rubric10 | pipeline_tag | — |
| 67 | 1 | consistency | rubric10 | pipeline_tag ↔ input/output format | — |
| 68 | 1 | consistency | rubric10 | primary use 'product reviews' vs training data 'movie reviews' | — |
| 69 | 1 | plausibility | rubric20 | quantitative_analysis.performance_metrics | — |
| 70 | 1 | format | rubric10 | quantitative_analysis.performance_metrics[].confidence_interval | — |
| 71 | 1 | consistency | rubric10 | Sensitive data disclosure (top-level affirmation) | — |
| 72 | 1 | consistency | rubric10 | sensitive/bias acknowledgement -> bias_model + out_of_scope_uses populated | — |
| 73 | 1 | consistency | rubric10 | training data vs evaluation benchmark models | — |
| 74 | 1 | consistency | rubric10 | training_procedure.description vs reproducibility_info.hyperparameters.optimizer | — |
| 75 | 1 | consistency | rubric20 | training_procedure.description ↔ hyperparameters.optimizer | — |
| 76 | 1 | format | rubric20 | usage_documentation.code_examples | — |
| 77 | 1 | consistency | rubric10 | version.diff vs model_parameters.data[] | — |

## Details (top 15)

### 1. [format / rubric10] model_parameters.compute_infrastructure

- Cards affected (3): densenet121_tv_in1k_model_card, sentiment-classifier-with-datasheet-refs, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: Absent — only inference deployment_info.hardware_requirements is provided

### 2. [format / rubric10] framework_version

- Cards affected (2): densenet121_tv_in1k_model_card, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: Floating constraint 'torch>=1.13' rather than a pinned version; marginal for reproducibility

### 3. [format / rubric20] framework_version

- Cards affected (2): densenet121_tv_in1k_model_card, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Questions impacted: Q10, Q11
- Example issue: Floating pin 'torch>=1.13' rather than fixed semver; format rule caps Q10/Q11 at 4 (Q10=3 and Q11=3 are already below cap, so no additional reduction).

### 4. [format / rubric10] mission_relevance

- Cards affected (2): densenet121_tv_in1k_model_card, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: Block absent — no DOE/domain mission alignment or reproducibility info

### 5. [format / rubric10] model file format

- Cards affected (2): densenet121_tv_in1k_model_card, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: No explicit on-disk format (safetensors / state_dict / ONNX) declared

### 6. [format / rubric10] model_details.path

- Cards affected (2): climate-forecasting-model-card, sentiment-classifier-with-datasheet-refs
- Hybrid coverage: — (candidate to encode)
- Example issue: Only an S3 directory URI is given; no explicit model file format (safetensors / .pt / ONNX / SavedModel).

### 7. [format / rubric10] model_details.version.name

- Cards affected (2): densenet121_tv_in1k_model_card, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: 'tv_in1k' is a recognizable release tag but not semver; accepted by rubric as a release tag

### 8. [format / rubric10] model_index

- Cards affected (2): densenet121_tv_in1k_model_card, subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: No model_index[].results[] entries — metrics not exposed as Papers-with-Code-style benchmark records

### 9. [format / rubric10] model_parameters.training_procedure

- Cards affected (2): densenet121_tv_in1k_model_card, sentiment-classifier-with-datasheet-refs
- Hybrid coverage: — (candidate to encode)
- Example issue: Absent — no optimizer, schedule, loss, or hyperparameter fields

### 10. [format / rubric10] base_model (top-level)

- Cards affected (1): climate-model-extended
- Hybrid coverage: — (candidate to encode)
- Example issue: Base model (ResNet-50 ImageNet pretrained) described in prose but top-level base_model slot is not populated

### 11. [plausibility / rubric10] base_model / lineage

- Cards affected (1): climate-forecasting-model-card
- Hybrid coverage: — (candidate to encode)
- Example issue: No base_model declared and no 'trained from scratch' affirmation; lineage is implicit.

### 12. [consistency / rubric10] base_model ↔ license compatibility

- Cards affected (1): subcell_saprot_650m_model_card
- Hybrid coverage: — (candidate to encode)
- Example issue: Licence declared MIT, but base SaProt_650M_AF2's own license is not cross-referenced; downstream MIT relicensing of weights derived from a non-MIT base would be inconsistent if applicable

### 13. [consistency / rubric20] benchmark dataset != training dataset

- Cards affected (1): densenet121_tv_in1k_model_card
- Hybrid coverage: ✅ `train_eval_leakage`
- Questions impacted: Q18
- Example issue: model_parameters.data[0].name='ImageNet-1k (ILSVRC2012)' is the training set; quantitative_analysis.performance_metrics evaluate on 'ImageNet-1k validation' (held-out split of same dataset family). This is the conventional ImageNet protocol but means metrics are within-distribution only with no external benchmark.

### 14. [consistency / rubric20] benchmark dataset != training dataset (no train/eval leakage)

- Cards affected (1): sentiment-classifier-with-datasheet-refs
- Hybrid coverage: ✅ `train_eval_leakage`
- Questions impacted: Q18
- Example issue: model_index[0].results[0].dataset.type='imdb' matches model_parameters.data[0].name='IMDb Movie Reviews' (the training dataset); accuracy=0.92 reported on the same dataset family used for training

### 15. [consistency / rubric20] benchmark dataset ↔ training data (train/eval leakage)

- Cards affected (1): climate-model-extended
- Hybrid coverage: ✅ `train_eval_leakage`
- Questions impacted: Q18
- Example issue: model_parameters.data lists 'E3SM v2 High-Resolution' and 'MPAS-A 15km' as training data; quantitative_analysis.performance_metrics[*].slice='Test set (E3SM v2)' and evaluation_procedure.benchmarks names 'Test set: 3 climate models (E3SM v2, MPAS-A, GFDL CM4)'. Same climate-model families appear in both. The methodology claims a by-simulation-year split (mitigating control), but the dataset-name match still triggers the leakage rule

## Capped deductions surfaced

| Card | Rubric | Question | Raw → Capped | Reason |
|---|---|---|---|---|
| climate-forecasting-model-card | rubric10 |  | 0 → 0 |  |
| climate-forecasting-model-card | rubric10 |  | 0 → 0 |  |
| climate-forecasting-model-card | rubric10 |  | 0 → 0 |  |
| climate-forecasting-model-card | rubric10 |  | 0 → 0 |  |
| climate-forecasting-model-card | rubric10 |  | 0 → 0 |  |
| climate-forecasting-model-card | rubric20 | Q14 | 5 → 4 | Only one citation (APA) present; rubric requires multiple BibTeX citations for full score. Placeholder DOI prefix 10.1234 is not a real Crossref prefix |
| climate-forecasting-model-card | rubric20 | Q15 | 5 → 4 | Hardware + hardware_list + software + training_speed present, but no total compute (GPU-hours / FLOPs) and no energy/carbon estimate |
| climate-forecasting-model-card | rubric20 | Q4 | 5 → 4 | input_format_map populated but output_format_map is missing; output quantile semantics described in prose only |
| climate-forecasting-model-card | rubric20 | Q8 | 4 → 3 | ethical_considerations and out_of_scope_uses are populated, but none of {bias_model, bias_output, bias_input} are populated — rubric requires concrete bias disclosure for score >= 4 |
| climate-model-extended | rubric20 | Q18 | 5 → 3 | Benchmark dataset overlap with training data: 'Test set (E3SM v2)' references the same model family used in training (E3SM v2 High-Resolution, MPAS-A). Train/eval separation is claimed by simulation y… |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric10 |  | 0 → 0 |  |
| densenet121_tv_in1k_model_card | rubric20 | Q19 | 5 → 3 | bias_model and bias_output are populated, but considerations.tradeoffs only discusses parameter-count vs wall-clock (DenseNet-121 vs ResNet-50). No accuracy-vs-fairness or other bias-related tradeoff … |
| sentiment-classifier-with-datasheet-refs | rubric10 |  | 0 → 0 |  |
| sentiment-classifier-with-datasheet-refs | rubric10 |  | 0 → 0 |  |
| sentiment-classifier-with-datasheet-refs | rubric10 |  | 0 → 0 |  |
| sentiment-classifier-with-datasheet-refs | rubric10 |  | 0 → 0 |  |
| sentiment-classifier-with-datasheet-refs | rubric10 |  | 0 → 0 |  |
| sentiment-classifier-with-datasheet-refs | rubric10 |  | 0 → 0 |  |
| sentiment-classifier-with-datasheet-refs | rubric20 | Q18 | 5 → 3 | Benchmark dataset (IMDb) overlaps with training dataset (IMDb) — potential train/eval leakage |
| sentiment-classifier-with-datasheet-refs | rubric20 | Q19 | 4 → 3 | out_of_scope_uses empty (one of three sub-fields missing entirely) |
| sentiment-classifier-with-datasheet-refs | rubric20 | Q8 | 3 → 3 | out_of_scope_uses empty for a moderation/content-filtering model; ethical considerations partial. Base score already at cap. |
| subcell_saprot_650m_model_card | rubric10 |  | 0 → 0 |  |
| subcell_saprot_650m_model_card | rubric10 |  | 0 → 0 |  |
| subcell_saprot_650m_model_card | rubric20 | Q19 | 5 → 3 | bias_model and bias_output are populated, but considerations.tradeoffs[] only addresses model-size vs accuracy/cost; it does not acknowledge accuracy-vs-fairness or rare-class performance tradeoffs im… |

## Encoded hybrid rules

These rules already fire in `scripts/batch_evaluate_mc_rubric20_hybrid.py`:

- `bias_tradeoff_gap` — matches findings containing: _[{'tradeoffs', 'bias_model'}, {'tradeoffs', 'bias_output'}, {'bias', 'tradeoffs', 'fairness'}, {'bias', 'tradeoffs', 'considerations'}]_
- `train_eval_leakage` — matches findings containing: _[{'benchmark', 'dataset', 'training'}, {'evaluation', 'overlap', 'training'}, {'leakage', 'eval', 'train'}]_
