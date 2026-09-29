# Correct DenseNet-121 provenance, usage and benchmark documentation

The supplied heatmap flags missing structured training, usage and evaluation documentation for `timm/densenet121.tv_in1k`. Upstream verification also finds an unsupported release date and a preprocessing distinction: torchvision's reference evaluation uses bilinear resizing, while the timm configuration uses bicubic.

Fix prepared locally: pin the Hub revision, document LuaTorch → torchvision → timm lineage and artifact formats, separate paper-level training/funding from checkpoint-run evidence, add structured usage and benchmark records, and attribute the 74.434%/91.972% reference accuracies precisely. Replace unsupported bias claims with scoped limitations and evaluation recommendations.

Acceptance: schema-valid YAML and standalone HTML retain the source links and distinguish published reference results from unperformed inference. Original-run and prediction-level evidence remain separate follow-ups. Close only after the reviewed fix is merged.
