# SubCell public dataset history audit

Reviewed September 28, 2026 for [issue #35](https://github.com/bridge2ai/model-card-schema/issues/35). **Validation/test overlap exists in the earliest public dataset snapshot, May 3, 2024. Subsequent CSV conversion preserves it.** This narrows the provenance question but does not establish which splits produced the model's reported 85.75% accuracy. Keep #35 open pending a scored-run manifest.

## Scope and evidence

The audit inspected all 26 dataset commits reachable from the observed main branch, including recursive file trees and dotfiles, and downloaded all 12 distinct CSV/LMDB artifacts in that history (207,672,650 bytes). Each artifact was checked against its size and SHA-256; the initial retrieval also checked the published LFS hash or Git blob identity. Raw dataset files are cached outside this repository. No model weights were downloaded and no inference or training was run.

- [sources.json](sources.json): exact dataset download URLs, revisions, filenames, sizes and SHA-256 hashes; five comparable snapshots.
- [dataset_history.json](dataset_history.json): commit dates and recursive dataset file listings, including dotfiles.
- [audit.json](audit.json): computed split counts, intersections, chronological equivalence and confidence-masking checks, with manifest and script fingerprints.
- [shared_ids.csv](shared_ids.csv): the 232 shared validation/test identifiers with labels and sequence hashes; no raw sequences.
- [model_timeline.json](model_timeline.json): extracted model publication events and README/configuration claims.
- [model_sources.json](model_sources.json): URLs and fingerprints for 43 inspected public source responses. This is a retrieval manifest, not an archive of their contents. Revision-pinned files can be fetched again; mutable API response hashes may change as repositories evolve.
- [Audit script](../../../../scripts/audit_subcell_split_history.py): verifies files before parsing, reads LMDB values as JSON and performs the comparisons.

The observed dataset head is `78096a0eff765cf8988323ca3c21c0f19ca1ae79` (February 4, 2025); it still contains the October 30, 2024 CSV bytes. The model head is `ffc656cde0bbfaf4933b364036753674520663b6`.

## Five comparable snapshots

Every snapshot contains 10,414 train, 1,368 validation and 1,368 test records. Dates below are publication dates in the repository, not verified training dates.

| Date | Revision | Format and identifiers | Change from preceding snapshot |
|---|---|---|---|
| 2024-05-03 | [`f1f914e`](https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/tree/f1f914e9ce4bf5ceefa33823f1a09562aac872b4) | Three LMDBs; `name`, `seq`, `label`, `plddt` | Earliest public data upload |
| 2024-05-06 | [`c7af324`](https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/tree/c7af324a2eb84f834895e4febe34cf55cae6da00) | Three LMDBs; `name`, `seq`, `label` | Structural tokens below pLDDT 70 masked; identifiers, amino-acid sequences, labels and row order preserved |
| 2024-07-10 | [`a2ba7f6`](https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/tree/a2ba7f6e25cbb19130d418c86d0d27ec71233ff7) | Three CSVs; `name`, `seq`, `label`, `stage` | Same ordered records as May 6 |
| 2024-08-08 | [`ea88ea2`](https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/tree/ea88ea2785269900ed84577127fc474e7cd53319) | Combined CSV; `sequence`, `label`, `stage` | Identifiers dropped; labelled sequences and per-split order preserved |
| 2024-10-30 | [`c5247cf`](https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/tree/c5247cfea75c7b74e7a1b36734c3c2502317390e) | Combined CSV; `protein`, `label`, `stage` | Sequence column renamed; labelled sequences and per-split order preserved |

Equivalence checks compare both ordered records and multisets, after normalizing column names and accounting explicitly for dropped identifiers. They do not compare CSV byte hashes across changed formats.

A separate, short-lived 48-row file (git blob `3e6000bf`) appeared on July 10. It has columns `Sequence,label,stage`, stages train 39 / valid 4 / test 5, and continuous labels such as `10.15988` and `17.5`. From 02:06 UTC it sat at root `test.csv`, then also at `train.csv`, `valid.csv` and `validation.csv`. From about 02:20 UTC it sat at `train/train.csv`, `valid/valid.csv` and `test/test.csv`. It was removed from all of them by 04:37 UTC, before the ten-class CSVs were uploaded at 05:48–05:51 UTC. Every path and revision is in the source manifest. The file is excluded from the ten-class SA comparisons. Its filenames do not establish that it is localization data; this audit does not assign it another task identity.

## Split intersections

SA comparisons use the complete structure-aware strings; AA comparisons take every other character, dropping structural tokens. Counts below are intersections of unique strings or identifiers, without truncation, sequence alignment or clustering. They do not retest the publisher's structure-similarity criterion.

| Split pair | Shared SA strings, all five snapshots | Shared AA strings, all five snapshots | Shared identifiers in May/July artifacts |
|---|---:|---:|---:|
| train / valid | 0 | 0 | 0 |
| train / test | 0 | 1 | 0 |
| valid / test | 232 | 233 | 232 |

The 232 shared identifiers have matching labels and SA strings within each historical snapshot and occur in 232 rows of each split (16.96% of validation and of test). Later combined CSVs lack identifiers: their identifier counts are **unknown (`null`), not zero**.

The extra AA-only overlaps have distinct record identifiers: train `P69243` and test `P69242` share a 977-residue AA string with label 6; validation `Q9XH37` and test `Q6K498` share a 277-residue AA string with label 0. These checks establish exact sequence identity, not species or family annotations.

The audit script records every count above, and `shared_ids.csv` lists the 232 shared July identifiers with their labels and sequence hashes. Two statements come from a supplementary check that the script does not yet write out: the named AA-only pairs in the previous paragraph, and per-identifier label and SA agreement in the May snapshots. Both were re-verified independently against the same cached artifacts; issue #58 tracks adding them to `audit.json`.

## Confidence masking explains the May change

For every May 3 record, retain each amino-acid character and replace its paired structural character with `#` if the corresponding recorded pLDDT is below 70. The resulting full string exactly matches the same record in the May 6 LMDBs for all 13,150 rows. Identifiers, labels, amino-acid sequences and order also match.

| Split | Rows | Rows with changed SA strings | Exact reconstruction matches |
|---|---:|---:|---:|
| train | 10,414 | 10,242 | 10,414 |
| valid | 1,368 | 1,361 | 1,368 |
| test | 1,368 | 1,322 | 1,368 |

This establishes the transformation between public artifacts. It does not establish the scored run's preprocessing settings or exact code.

## Relationship to the model score

The first adapter upload was May 7, 2024, at [`f63c2fe`](https://huggingface.co/SaProtHub/Model-Subcellular_Localization-650M/tree/f63c2fe958a2918dab97f214880f0aacc4ac33fc). All 11 weight-bearing model commits advertise the same LFS SHA-256, `af06be30281f9b02fb30f867fc163a9c2ba9ee299b2d8e0fdb648972444d1ea1`, for the 55,417,357-byte adapter. This is upstream file metadata, not an independently recomputed weight hash.

The README first reports **85.75% accuracy** on May 8 at [`9c36e2a`](https://huggingface.co/SaProtHub/Model-Subcellular_Localization-650M/blob/9c36e2a1cab36ed9d119412b8806f4c3232cb33e/README.md). An earlier README that morning states a different metric; subsequent edits change LoRA rank/alpha, learning rate and epoch settings without changing the advertised weights. Those documentation edits do not prove distinct training runs. The adapter configuration already specifies rank 16 and alpha 32 at the initial upload.

Every historical README links an unpinned dataset repository. None supplies a score-to-split revision binding or run ID. The May dataset snapshots precede the first score publication, but chronology alone cannot identify the scored data. **The audit does not prove contamination of the historical 85.75% result, adjust that score or reproduce it.**

The contemporaneous official [DeepLoc configuration](https://github.com/westlake-repl/SaprotHub/blob/58aa28427bb4174748e31cac76afa5a766d73a95/saprot/config/DeepLoc/cls10/saprot.yaml) is a 35M example with different hyperparameters. Its seed and device values cannot fill the 650M adapter's historical reproducibility fields.

## Remaining evidence requests

- **#35:** Obtain the run/checkpoint identity and exact scored train/validation/test membership manifest; reconcile these public overlaps with checkpoint selection and test evaluation. The historical identifier files recovered here can support that comparison.
- **#33:** Obtain the actual base revision, training code/configuration, seed, environment, completed training logs, compute measurements and funding evidence. Public example settings do not establish those run-specific values.
- **#34:** Obtain historical predictions/logits and evaluation protocol, or run a separately identified new evaluation. Public weights and inputs alone are not predictions. For DenseNet, official [ImageNet validation](https://huggingface.co/datasets/ILSVRC/imagenet-1k/tree/49e2ee26f3810fb5a7536bbf732a7b07389a47b5) remains gated; new evaluation requires authorized access to its 50,000 images (about 6.69 GB stored), a tested inference environment and execution. No gated access request was submitted.

No issues are resolved solely by acquiring these dataset artifacts.

## Reproduction

From the repository root, use an isolated Python environment with `lmdb==2.3.0`. The audit uses Python's standard library plus LMDB, loads JSON records only, and opens the databases read-only without creating locks. It does not import model code.

```bash
python3 -m venv /tmp/subcell-audit-env
/tmp/subcell-audit-env/bin/python -m pip install lmdb==2.3.0
/tmp/subcell-audit-env/bin/python scripts/audit_subcell_split_history.py \
  --manifest data/evaluation/subcell_split_history/2026-09-28/sources.json \
  --cache-dir /tmp/subcell-audit-cache \
  --output-dir /tmp/subcell-audit-output \
  --download
```

The explicit `--download` option retrieves missing public blobs (about 208 MB); omit it to require an existing verified cache. Missing or mismatched artifacts fail before parsing. Output contains summary evidence and hashes rather than raw protein sequences. Generation time and runtime metadata can differ across reruns; compare the substantive counts and equivalence results.
