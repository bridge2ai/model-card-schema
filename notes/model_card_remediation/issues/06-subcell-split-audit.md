# Reconcile SubCell split overlap with the reported 85.75% accuracy

An audit of the public DeepLoc mirror at revision `78096a0eff765cf8988323ca3c21c0f19ca1ae79` finds 10,414 train, 1,368 valid and 1,368 test rows. Unique-string intersections include 232 identical structure-aware sequences shared by valid/test. Comparing amino-acid components gives 233 valid/test overlaps and one train/test overlap; train/test structure-aware-string overlap is zero.

This finding concerns the inspected mirror. The model README does not bind its reported 85.75% accuracy to this dataset revision, so the audit does not prove contamination of the historical scored run.

Request the original scored split manifest, base/checkpoint and run IDs, preprocessing/deduplication policy, model-selection history and predictions. Acceptance: reconcile overlapping records and bind the score to exact artifacts, or provide a revised evaluation. The documentation caveat is fixed locally; this investigation remains open pending evidence.
