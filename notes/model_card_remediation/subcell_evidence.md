# SubCell 650M model-card evidence and unresolved inputs

Reviewed 2026-09-28. Target: `SaProtHub/Model-Subcellular_Localization-650M`. This is the public protein-localization adapter identified in the supplied heatmap; the reviewed evidence does not identify a CM4AI-specific derivative. The user confirmed there are no additional local input documents or data for these models. The remaining requests below are for public upstream/maintainer artifacts, not files presumed to exist locally.

The card's original 2026-06-15 generation header is retained as historical provenance. Its revision annotation identifies this source audit separately. No model weights were downloaded, training executed, inference run or performance measurement independently reproduced. The 13.5 MB public dataset CSV was downloaded temporarily for a data audit, not added to this repository. No upstream issue, message or other communication has been transmitted by this work.

## Relationship to the supplied analysis

The supplied heatmap and its README report 59/126 populated terminal paths, semantic rubric10 39/50 and semantic rubric20 64/84 for the old SubCell card. Those are archived documentation evaluations, not model performance scores. The accompanying README dates semantic evaluations to 2026-06-15 and identifies the SubCell rubric10 input hash as `n/a`. These archived ratings do not score the revised card. The field-presence denominator includes optional and extension fields; an absent field is not automatically an applicable defect.

The remediation adds evidence-backed structured usage and evaluation information and a benchmark source, and corrects factual overreach. Seeds, historical environment, compute measurements, run-level uncertainty and funding remain unpopulated where the public artifacts do not establish them. Applicable unknowns are tracked below rather than filled with guessed values. A future fresh semantic evaluation must identify the revised YAML's hash and evaluator configuration.

## Primary sources and supported claims

All links below point to upstream publishers. Revision-pinned files were retrieved on the review date. Generic upstream implementation details are explicitly distinguished from historical run provenance.

| Source | Exact source URL | Supports | Does not establish |
|---|---|---|---|
| Model metadata API | https://huggingface.co/api/models/SaProtHub/Model-Subcellular_Localization-650M | Inspected revision `ffc656cde0bbfaf4933b364036753674520663b6`; last-modified timestamp `2024-10-16T11:57:20.000Z`; file listing | Original training date or semantic release version |
| Model README | https://huggingface.co/SaProtHub/Model-Subcellular_Localization-650M/blob/ffc656cde0bbfaf4933b364036753674520663b6/README.md | Base ID; ten labels and their order; SA input; linked dataset; reported 85.75% accuracy; optimizer, batch/epoch/precision and LoRA settings; MIT declaration | Evaluation run ID, exact scored dataset revision, completed training log, confidence interval or per-class scores |
| Adapter config | https://huggingface.co/SaProtHub/Model-Subcellular_Localization-650M/blob/ffc656cde0bbfaf4933b364036753674520663b6/adapter_config.json | Base ID; `SEQ_CLS`; `LORA`; rank 16, alpha 32, dropout 0; query/key/value and two dense targets; classifier saved with adapter | Exact base revision: `revision` is null; weight dimensions were not loaded |
| Immutable model file listing | https://huggingface.co/api/models/SaProtHub/Model-Subcellular_Localization-650M/tree/ffc656cde0bbfaf4933b364036753674520663b6 | Exact published weight filename `adapter_model.bin`, size 55,417,357 bytes, with `adapter_config.json`; declared LFS SHA-256 `af06be30281f9b02fb30f867fc163a9c2ba9ee299b2d8e0fdb648972444d1ea1` | Weight contents or an independently recomputed weight hash: weights were not downloaded |
| Adapter loader | https://github.com/westlake-repl/SaprotHub/blob/3661c549ec48efc5a480e5e941a204e807b2e68a/saprot/model/saprot/self_peft/save_and_load.py | PyTorch/PEFT `.bin` loading through `torch.load`; the pinned v2 notebook also explicitly loads `adapter_model.bin` with `torch.load` | Weight integrity or successful execution of this particular checkpoint |
| Model task metadata | https://huggingface.co/SaProtHub/Model-Subcellular_Localization-650M/blob/ffc656cde0bbfaf4933b364036753674520663b6/metadata.json | Protein-level classification; SA training data type | Training environment or data split |
| Dataset README | https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/blob/78096a0eff765cf8988323ca3c21c0f19ca1ae79/README.md | Original DeepLoc publication link; exclusion of proteins without AF2 structures; publisher-described 70% structure-similarity split using ProteinShake; 10,414 train / 1,368 valid / 1,368 test; exact label map | Verified independence of the actual rows; a link between this revision and the scored run |
| Dataset CSV | https://huggingface.co/datasets/SaProtHub/Dataset-Subcellular_Localization-DeepLoc/resolve/78096a0eff765cf8988323ca3c21c0f19ca1ae79/dataset.csv | Independently checked row counts, labels, class distribution, sequence formats and exact-string overlaps below | Protein/organism IDs, raw structural files, original scoring manifest or predictions |
| Base-model documentation | https://github.com/westlake-repl/SaProt/blob/e91e4858b55944523f1f8d385f7b96a0d3d34c1d/README.md | SaProt vocabulary, masking examples, 650M AF2 base and 40-million-structure pretraining; supports AA-only modes with qualifications | This adapter's AA-only performance, original training environment, or a directly comparable 35M adapter score |
| Classification implementation | https://github.com/westlake-repl/SaprotHub/blob/3661c549ec48efc5a480e5e941a204e807b2e68a/saprot/model/saprot/saprot_classification_model.py | Current classification forward pass, cross-entropy, accuracy and selection by validation accuracy | That this source commit was used for the historical adapter run |
| Base class implementation | https://github.com/westlake-repl/SaprotHub/blob/3661c549ec48efc5a480e5e941a204e807b2e68a/saprot/model/saprot/base.py | ESM sequence-classification loading and LoRA/classifier handling | Exact checkpoint weights or run settings |
| Classification dataset implementation | https://github.com/westlake-repl/SaprotHub/blob/3661c549ec48efc5a480e5e941a204e807b2e68a/saprot/dataset/saprot/saprot_classification_dataset.py | Current default `max_length=1024` SA/residue tokens and explicit truncation | The adapter's actual historical maximum length or masking settings |
| ColabSaprot v2 notebook | https://github.com/westlake-repl/SaprotHub/blob/3661c549ec48efc5a480e5e941a204e807b2e68a/colab/SaprotHub_v2.ipynb | Actual task/model selection UI, SA-trained input enforcement, `make_predictions`, argmax label and softmax export columns | A fully pinned execution environment: notebook internals fetch remote defaults |
| Local runtime guide | https://github.com/westlake-repl/SaprotHub/blob/3661c549ec48efc5a480e5e941a204e807b2e68a/local_server/README.md | Official local installation route | Original training hardware or dependency lockfile |
| Original dataset publication (linked by publisher) | https://academic.oup.com/bioinformatics/article/33/21/3387/3931857 | Identity of the 2017 DeepLoc source cited by the dataset publisher | DeepLoc 2.0 provenance; the current card does not assert that version |
| SaProt publication | https://openreview.net/forum?id=6MRm3G4NiU | SaProt's ICLR 2024 citation, linked from the official repository | A run-specific report for this adapter |

The model README's optimizer configuration is AdamW with `betas=(0.9, 0.98)`, `weight_decay=0.01`, learning rate `5e-4`, batch size `64`, epoch setting `100` and precision `16-mixed`. The card records these as reported settings, not proof that 100 epochs completed. Current generic requirements were inspected but were deliberately not promoted to `framework_version`, `compute_infrastructure` or the original run's environment.

### Download fingerprints

| Downloaded file | SHA-256 |
|---|---|
| Model README | `77f7dc8398eca80e15d8bc107ea447cd6b14c3830638f86dac851f383e75cca3` |
| Adapter config | `6ba2ec2f29368a3cb4a724bcc410f3f74203a661aef4df80fb1d75381df43c65` |
| Model metadata | `432bfce68a868774799d847eb57a0bdc4cda46745c006f1f1101a6fab0218c0b` |
| Dataset README | `51558f4b4ac002416bbff9b79ca15d4030409c63010268a45a7f66e354ab32db` |
| Dataset metadata | `432bfce68a868774799d847eb57a0bdc4cda46745c006f1f1101a6fab0218c0b` |
| Dataset CSV | `cf9f02e52091739d012189a1d66aad22e0fa906d0ae2c1993e0821a4b9f3b64e` |

## Factual corrections completed locally

| Earlier assertion | Resolution in revised card |
|---|---|
| DeepLoc 2.0 benchmark | Corrected to the dataset publisher's original-DeepLoc citation and documented mirror split/filtering; retained exact adapter identity. |
| Version 1.0; initial release 2024-08-01 | Replaced with inspected repository revision and API last-modified timestamp. No training/release date inferred. |
| `from saprot_hub import load_model` followed by `model.predict` | Replaced with actual upstream ColabSaprot v2 instructions. A tested label-decoding example processes its real CSV output columns; it does not pretend to perform inference. |
| Single linear head on pooled features | Replaced with the documented sequence-classification implementation and saved-classifier metadata; no weight inspection claimed. |
| Single GPU; `torch>=2.0` as framework environment | Removed. Public model metadata does not identify training hardware or an environment lock. |
| SA-free sequences cannot be scored by SaProt at all | Scoped to this SA-trained adapter and current v2 workflow. Generic SaProt has AA-only modes, but this adapter has no supplied AA-only validation. |
| Heavily human / E. coli / yeast-biased training distribution | Replaced with observed class imbalance and AF2-availability filtering. CSV lacks species IDs. |
| Rare compartments are likely under-predicted | Removed as an unmeasured output claim. Request class-level predictions before establishing bias. |
| 650M vs 35M accuracy comparison (85.75% vs about 80%) | Removed. A like-for-like comparison tied to this adapter and split was not established. |
| Score without source/procedure | Added structured benchmark source, author-reported status, task/split description and explicit revision/run uncertainty. |
| Unnamed weight serialization artifact (rubric10 E2.5) | Named `adapter_model.bin` as the inspected PyTorch/PEFT `.bin` artifact; documented size, configuration-declared classifier inclusion, base-weight requirement and that weights were not downloaded. |
| Implied CM4AI linkage | Explicitly scoped to public adapter; a CM4AI-specific identity or evaluation requires separate evidence. |

The revised tradeoffs section also addresses the figure's semantic Q19 gap with a curator recommendation to compare per-compartment recall and macro-F1 alongside aggregate accuracy. The observed training label imbalance motivates that metric choice; it does not establish an observed class-specific error or require inventing subgroup scores.

No boolean assertion of `training_data_separate` or `evaluation_data_separate` was added. A stage column is not proof of independent examples. The model-index result deliberately omits dataset revision: the inspected mirror revision is known, but the revision used to compute 85.75% is not.

## Reproducible audit of the pinned dataset mirror

For each `stage`, **SA unique** is the number of distinct full `protein` strings. **AA unique** is the number of distinct strings obtained as `protein[::2]`, discarding every structural character. All 13,150 rows were checked to have even length, uppercase letters at amino-acid positions and lowercase letters or `#` at structural positions. The overlap tests use the full strings without truncation, clustering or sequence alignment. They do not retest the publisher's 70% structural clustering criterion.

| Stage | Rows | SA unique | AA unique | Excess repeated SA records | Excess repeated AA records | Exact full-row duplicates |
|---|---:|---:|---:|---:|---:|---:|
| train | 10,414 | 10,408 | 10,376 | 6 | 38 | 6 |
| valid | 1,368 | 1,368 | 1,362 | 0 | 6 | 0 |
| test | 1,368 | 1,367 | 1,366 | 1 | 2 | 1 |

“Excess repeated” is rows minus unique strings; it is not the number of duplicate groups. Exact full-row duplicates compare all three CSV columns. All repeated identical SA strings had consistent labels in this snapshot.

| Split pair | Shared unique SA strings | Shared unique AA strings |
|---|---:|---:|
| train / valid | 0 | 0 |
| train / test | 0 | 1 |
| valid / test | 232 | 233 |

The 232 shared SA strings occur in 232 validation rows and 232 test rows. The 233 shared AA strings occur in 233 rows in each of those splits. The single train/test AA overlap occurs in one row in each split. This is a potential independence problem requiring investigation. **It is not proof that the historical 85.75% result used this dataset revision or was affected by leakage.** No score is adjusted or replaced on the basis of this audit.

Class counts by the publisher's label mapping:

| Label | Compartment | train | valid | test |
|---|---|---:|---:|---:|
| 0 | Nucleus | 2,641 | 634 | 527 |
| 1 | Cytoplasm | 1,913 | 240 | 269 |
| 2 | Extracellular | 1,498 | 117 | 195 |
| 3 | Mitochondrion | 1,323 | 74 | 85 |
| 4 | Cell.membrane | 979 | 165 | 128 |
| 5 | Endoplasmic.reticulum | 745 | 42 | 45 |
| 6 | Plastid | 633 | 44 | 48 |
| 7 | Golgi.apparatus | 282 | 33 | 29 |
| 8 | Lysosome/Vacuole | 268 | 14 | 27 |
| 9 | Peroxisome | 132 | 5 | 15 |

To reproduce the counts using Python's standard library (downloads only the public CSV):

```bash
python3 - <<'PY'
import csv
import hashlib
import io
import itertools
import urllib.request
from collections import Counter, defaultdict

url = (
    'https://huggingface.co/datasets/SaProtHub/'
    'Dataset-Subcellular_Localization-DeepLoc/resolve/'
    '78096a0eff765cf8988323ca3c21c0f19ca1ae79/dataset.csv'
)
data = urllib.request.urlopen(url).read()
assert hashlib.sha256(data).hexdigest() == (
    'cf9f02e52091739d012189a1d66aad22e0fa906d0ae2c1993e0821a4b9f3b64e'
)
reader = csv.DictReader(io.StringIO(data.decode('utf-8')))
assert reader.fieldnames == ['protein', 'label', 'stage']
rows = list(reader)
assert len(rows) == 13150
assert {r['stage'] for r in rows} == {'train', 'valid', 'test'}
assert {r['label'] for r in rows} == {str(i) for i in range(10)}
assert all(
    len(r['protein']) % 2 == 0
    and all(c.isupper() for c in r['protein'][::2])
    and all(c.islower() or c == '#' for c in r['protein'][1::2])
    for r in rows
)
stages = ('train', 'valid', 'test')
for stage in stages:
    subset = [r for r in rows if r['stage'] == stage]
    sa = {r['protein'] for r in subset}
    aa = {r['protein'][::2] for r in subset}
    full_rows = {tuple(r[k] for k in reader.fieldnames) for r in subset}
    print(stage, 'rows', len(subset), 'SA unique', len(sa), 'AA unique', len(aa),
          'excess SA', len(subset) - len(sa),
          'excess AA', len(subset) - len(aa),
          'full-row duplicates', len(subset) - len(full_rows))
    print('class counts', dict(sorted(Counter(r['label'] for r in subset).items())))
for name, transform in [('SA', lambda p: p), ('AA', lambda p: p[::2])]:
    by_stage = {s: {transform(r['protein']) for r in rows if r['stage'] == s}
                for s in stages}
    for a, b in itertools.combinations(stages, 2):
        shared = by_stage[a] & by_stage[b]
        affected = [sum(transform(r['protein']) in shared for r in rows
                        if r['stage'] == s) for s in (a, b)]
        print(name, a, b, 'shared unique', len(shared), 'affected rows', affected)
labels_by_sa = defaultdict(set)
for row in rows:
    labels_by_sa[row['protein']].add(row['label'])
assert all(len(labels) == 1 for labels in labels_by_sa.values())
PY
```

## Open requests requiring public maintainer artifacts

These are pending evidence requests, not outbound communications. Nothing is being requested from the user's unavailable local files.

1. **Scored split identity and overlap resolution (priority: high).** Obtain the exact model checkpoint/adapter hash and training run ID underlying 85.75%; original train/validation/test membership manifest with stable protein IDs and sequence/structure hashes; dataset revision and filtering/clustering code/configuration; and a maintainer explanation for the current mirror's overlaps. Compare the scored splits to the audited CSV, then determine whether the evaluation needs rerunning on independent groups. Acceptance requires binding the score to actual scored data and resolving independence, not simply removing duplicate rows in the mirror after the fact.
2. **Run-level performance and uncertainty.** Obtain per-example test predictions/logits and labels, the evaluation script, class-wise confusion matrix, replicate/seed results if run, and the checkpoint-selection rule. These support independent accuracy reproduction, per-class precision/recall and an uncertainty method appropriate to the split dependence. Do not invent a confidence interval from the rounded aggregate alone or transfer one from another model.
3. **Training reproducibility and compute.** Obtain exact base-model revision; training code commit; random seeds; run configuration including SA conversion, pLDDT masking, maximum length/truncation, scheduler and stopping settings; completed epoch/checkpoint logs; environment lock or container digest; GPU type/count, elapsed training time and measured utilization/energy if available. A current generic `requirements.txt` or Colab device suggestion does not establish any historical values.
4. **CM4AI identity, if a CM4AI card is intended.** Obtain a public identifier/checkpoint hash, owning team, lineage connecting that artifact to this public adapter, intended CM4AI use, and validation data/report. Keep this card's public identity until that evidence is available; create a separate derivative card if the artifacts differ.
5. **Coverage and intended scope.** Obtain protein/organism/family identifiers and documented intended-use guidance for the actual scored dataset/run before reporting species-specific bias or generalization. Confirm licensing and source-data provenance at the relevant artifact revisions if a downstream reuse assessment needs more than the publisher's MIT declaration.

These remain open even if optional structured-field presence or a documentation score improves. Publication of issues or requests requires approval of each final destination and message under the supplied communication rule.
