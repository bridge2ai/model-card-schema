# Correct SubCell dataset lineage, adapter provenance and structured usage

The supplied heatmap identifies missing formats, split/evaluation documentation and structured benchmark/usage records for `SaProtHub/Model-Subcellular_Localization-650M`. Its linked dataset cites the original 2017 DeepLoc dataset, not DeepLoc 2.0. The old example used an unverified inference API.

Fix prepared locally: pin inspected model/dataset revisions, document adapter/base separation, exact class mapping, reported hyperparameters, observed split/class counts, official notebook usage and structured benchmark attribution. Remove invented run details and separate measured class imbalance from unmeasured output bias. Preserve 85.75% only as an author-reported score with unresolved run provenance.

Acceptance: schema-valid YAML and HTML expose these distinctions and the split-overlap caveat. The overlap investigation and additional evaluation data remain separate follow-ups. Close only after the reviewed fix is merged.
