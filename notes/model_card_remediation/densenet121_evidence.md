# DenseNet-121 evidence review

Reviewed 2026-09-28. Card: `data/model_cards_assistant/densenet121_tv_in1k_model_card.yaml`.
Original generation date and method remain in the YAML header. No weights, training jobs or new model-performance measurements were used in this review.

The supplied heatmap records 53/126 populated terminal paths, semantic rubric10 37/50, and semantic rubric20 61/84 for the previous card. These are archived documentation ratings, not new ratings of the revised card. The rubric20 record has a placeholder input hash. Presence includes optional and inapplicable fields, so increasing it is not an independent objective.

## Evidence ledger

| Source | Supported claim and card action | Status |
|---|---|---|
| [Hub model card](https://huggingface.co/timm/densenet121.tv_in1k/blob/f0d0f2698a02cb133b09d48396db6e1e46fe9f3b/README.md) and [file tree](https://huggingface.co/timm/densenet121.tv_in1k/tree/f0d0f2698a02cb133b09d48396db6e1e46fe9f3b) | The ImageNet checkpoint comes from torchvision; distribution includes Safetensors, a PyTorch state dictionary and JSON configuration. The Hub declares Apache-2.0. Added format and distribution details. | Verified upstream declaration; no weight download. |
| [Hub commit](https://huggingface.co/timm/densenet121.tv_in1k/commit/f0d0f2698a02cb133b09d48396db6e1e46fe9f3b) | This snapshot's metadata commit is dated 2025-01-21 and adds a Transformers tag. Replaced unsupported `2017-08-25` with a clearly scoped snapshot date; pinned the repository revision. | Verified; not a training date. |
| [Torchvision weight documentation](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.densenet121.html) and [original port PR](https://github.com/pytorch/vision/pull/116) | Weights were ported from LuaTorch. Reference accuracy is 74.434% top-1 and 91.972% top-5. Added benchmark source, split and preprocessing to `evaluation_procedure` and `model_index`; corrected the values. | Verified reference values; not reproduced locally. |
| [Hub config](https://huggingface.co/timm/densenet121.tv_in1k/blob/f0d0f2698a02cb133b09d48396db6e1e46fe9f3b/config.json) | timm uses bicubic interpolation, crop fraction 0.875, center crop and ImageNet normalization. Torchvision's reference uses bilinear interpolation. Card explicitly separates these pipelines. | Verified config; timm performance still requires a separate measurement. |
| [DenseNet paper, version 5](https://arxiv.org/html/1608.06993v5) | Added the original paper's ImageNet training recipe and paper-level funding acknowledgements. | Verified research context; not a recovered checkpoint run manifest or CM4AI funding claim. |
| [Original authors' training example](https://github.com/liuzhuang13/DenseNet#usage) | Added the documented LuaTorch ImageNet command in structured usage documentation and linked the training pipeline. | Reproduction example only; GPU count and later memory options are not asserted as original-run facts. |
| [ILSVRC2012 organizers](https://image-net.org/challenges/LSVRC/2012/index.php) | Dataset description identifies separate training and validation splits and distinguishes validation from the hidden-label test set. | Verified benchmark definition; artifact-specific data manifests remain unavailable in reviewed evidence. |
| [timm model factory](https://github.com/huggingface/pytorch-image-models/blob/main/timm/models/_factory.py) and [Hub loader](https://github.com/huggingface/pytorch-image-models/blob/main/timm/models/_hub.py) | The inference example uses supported `hf-hub:repo@revision` syntax and complete image preprocessing. | Source inspected and Python syntax parsed; not executed with weights. |
| [Torchvision license](https://github.com/pytorch/vision/blob/main/LICENSE) and [timm DenseNet source attribution](https://github.com/huggingface/pytorch-image-models/blob/main/timm/models/densenet.py) | Distinguished BSD-3-Clause code attribution from the Hub's Apache-2.0 distribution metadata. | Code licenses verified; no blanket claim about training-image rights. |

## Corrections beyond field presence

- Removed the unsupported `torch>=1.13` compatibility assertion, English-language tag and `torchvision/densenet121` pseudo-Hub identifier. The upstream checkpoint relationship remains in sourced prose.
- Removed unsupported current organizational affiliations for maintainers; retained paper-author affiliations from the paper.
- Replaced categorical claims about PII, absence of any fairness audit, calibration to class priors, rare-class underprediction and comparative wall-clock speed with scoped limitations and application-evaluation recommendations.
- Kept numeric training hyperparameters, exact environment versions, hardware, energy, confidence intervals and subgroup results absent where the evidence does not bind them to this checkpoint. The paper recipe is explicitly contextual prose.
- Added a model-selection recommendation to compare aggregate accuracy with per-class recall and worst-subgroup error, including sample sizes and uncertainty. This addresses the Q19 tradeoff documentation gap without claiming measured disparities.

## Additional inputs needed

| Input | Purpose / unresolved gap | Suggested source |
|---|---|---|
| Owner-confirmed CM4AI model identifier, checkpoint hash, and relationship to this public backbone | Establish whether this is a CM4AI-used baseline, an ancestor of a fine-tuned model, or the intended model itself. | CM4AI model owners. |
| Original checkpoint training log/configuration, seed, environment lock and data manifest | Bind numeric hyperparameters and software versions to the distributed artifact. | Original authors or checkpoint distributor. |
| Exact validated inference environment and example input/output | Convert source-checked instructions into a tested, locked reproduction. | Local benchmark owner or distributor. |
| Prediction-level validation outputs, labels and evaluation script; relevant deployment slices | Re-evaluate the pinned timm model with its specified preprocessing; compute defensible intervals, per-class results and calibration. | Evaluation owner; subject to data-access permissions. |
| Hardware allocation, measured runtime and energy records | Report run-specific compute and environmental cost without estimating from model size. | Training-run operator. |
| Funding attribution for the port, Hub redistribution and any CM4AI adaptation | Complete the provenance chain beyond original paper acknowledgements. | Responsible project owners. |

These inputs are not established by the reviewed upstream documents. This is not a claim that they do not exist elsewhere. The local reference search used `rg --no-ignore --hidden` for YAML/JSON/Markdown sources, excluding `.git`, dependency directories and virtual environments. No external requests or messages were sent.

## Checks

The revised YAML loads with PyYAML and its Python inference example parses with `ast.parse`. A recursive check of every populated object against the class slots and slot ranges in `src/model_card_schema/schema/model_card_schema.yaml` passed. `mission_relevance` and `usage_documentation` are root `modelCard` slots. Root-task validation is responsible for full LinkML validation, refreshed HTML and correctly labeling or replacing archived documentation scores. No inference accuracy, confidence interval or training result was generated here.
