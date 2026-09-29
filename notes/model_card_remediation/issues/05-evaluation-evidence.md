# Obtain predictions and protocols for slice metrics and uncertainty estimates

Both cards lack independently supported class/subgroup results, confidence intervals and calibration evidence. Aggregate published accuracies and model-size metrics cannot supply these measurements. DenseNet's timm and torchvision preprocessing also differ.

Request checkpoint hash, exact evaluation dataset/version and split IDs, label mapping, preprocessing/configuration, evaluation code/environment, and per-example targets and predictions or logits. Include appropriate grouping identifiers and repeated-run information when available. For DenseNet, identify whether results use the timm or torchvision protocol; for SubCell, resolve the separate split-provenance concern before treating results as independent.

Acceptance: report suitable per-class metrics and supported slices with sample counts, a justified uncertainty method and explicit provenance. Do not infer confidence bounds from rounded aggregate scores or invent subgroup labels. Status: awaiting evaluation artifacts.
