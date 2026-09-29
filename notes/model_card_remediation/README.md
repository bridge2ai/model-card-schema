# DenseNet and SubCell model-card remediation

The September 28, 2026 review uses the supplied [heatmap and its original inputs](baseline/README.md)
to prioritize source verification and documentation fixes for the two public checkpoints named
in the figure. It does not establish that either checkpoint is a CM4AI-trained model.

The user confirmed that no additional local model documents or data are available. Public
primary sources support the completed documentation changes below; unresolved factual
fields require upstream artifacts. No model weights, new inference or training jobs were
used. The public SubCell dataset CSV was inspected to audit its documented splits.

The subsequent [adversarial review](adversarial/README.md) records the portfolio rebuild,
HTML metadata/layout and CI detection fixes, with regression evidence and publication drafts.

## Work and issue drafts

At preparation on September 28, 2026, all six items below are local drafts for
`bridge2ai/model-card-schema`; no issue has been created or closed, and these changes
have not been pushed. The supplied outbound approval rule requires review of the exact
destination and text before those actions. This file does not track subsequent remote state.

| Draft | Disposition | Resolution / remaining input |
|---|---|---|
| [1. DenseNet provenance and documentation](issues/01-densenet-provenance.md) | Implemented locally; merge pending | Correct LuaTorch lineage, snapshot date, artifact formats, scoped training/funding evidence, preprocessing and reference scores; add structured usage and benchmark sources. |
| [2. SubCell provenance and documentation](issues/02-subcell-documentation.md) | Implemented locally; merge pending | Correct original-DeepLoc lineage, adapter/base distinction, label mapping, reported settings, actual notebook workflow and evaluation caveats. |
| [3. Evaluation provenance and HTML completeness](issues/03-evaluation-provenance.md) | Implemented locally; merge pending | Bind badges to YAML hashes, omit stale scores, render previously dropped fields, preserve baseline and produce separate current analysis. |
| [4. Original-run reproducibility, compute and funding](issues/04-original-run-evidence.md) | Needs external evidence | Checkpoint/run manifest, environment, seeds, training/compute logs and scoped funding; CM4AI checkpoint mapping if applicable. |
| [5. Prediction-level evaluation](issues/05-evaluation-evidence.md) | Needs external evidence | Exact scoring protocol/split and predictions for class/slice metrics, calibration and uncertainty. |
| [6. SubCell split-overlap investigation](issues/06-subcell-split-audit.md) | Needs external evidence | Original scored split manifest and run/checkpoint binding; reconcile the current mirror's overlaps before judging independence of the published score. |

Implementation and evidence: [DenseNet ledger](densenet121_evidence.md),
[SubCell ledger and reproducible split audit](subcell_evidence.md).

## Source verification changed more than field presence

DenseNet's reported reference accuracies are 74.434% top-1 and 91.972% top-5. They belong
to torchvision's documented bilinear evaluation. The inspected timm configuration uses
bicubic preprocessing, so the card does not claim a newly reproduced timm measurement.
The original paper's training recipe and funding acknowledgements are explicitly
research-level context, not recovered records for the exact distributed checkpoint.

The SubCell publisher cites the original 2017 DeepLoc dataset, not DeepLoc 2.0. Inspection
of its pinned mirror found 232 identical structure-aware strings shared by validation
and test, 233 amino-acid-only strings shared by those splits, and one amino-acid-only
string shared by train and test. These are unique-string intersections, not necessarily
row counts. The mirror is not bound to the historical 85.75% reported score; this audit
does not establish that the scored run used overlapping examples. The score remains
clearly attributed to its publisher pending the original split manifest and predictions.

Unsupported framework floors, release facts and output-bias assertions were removed.
Both cards distinguish published facts, direct artifact observations and curator
recommendations. Unknown historical hardware, energy, seeds and uncertainty remain unset.

## Evaluation and comparison

See the [current analysis](../../data/evaluation/remediation/2026-09-28/README.md),
[per-path comparison](../../data/evaluation/remediation/2026-09-28/field_presence.csv)
and [input/evaluator hashes](../../data/evaluation/remediation/2026-09-28/comparison.json).

The original archived semantic scores are not rescored or attached to the revised YAMLs.
Fresh results use the existing deterministic hybrid evaluators on both the original and
revised cards with the same evaluator source. This is an audit aid, not proof that every
statement is correct. The input figure's missing/placeholder rating hashes remain recorded
as limitations; they were not repaired by assigning a new hash to an old judgment.

Optional fields are not completion targets. In particular, a non-LLM does not need a
prompting template; a model without DOE evidence does not need an invented DOE facility;
and standard licenses do not require invented custom terms. A populated prose field can
document an uncertainty without resolving it.

## Validation and reproduction

Both cards pass LinkML validation against the unchanged base schema. A compatible local
validator used Python 3.11.5, LinkML 1.11.1 and linkml-runtime 1.10.0. These are documentation
validation tools, not a claim about either model's training environment.

The full unit suite passed 23 tests with one existing optional-package skip. Headless
Chromium loaded both embedded badges in each standalone page with no horizontal
overflow at a 1360-pixel viewport. The supplied usage snippets were checked locally
for syntax or, for SubCell's CSV label decoder, with a small synthetic output fixture;
neither check executes the models or reproduces the published accuracy.

```bash
linkml-validate -s src/model_card_schema/schema/model_card_schema.yaml -C modelCard data/model_cards_assistant/densenet121_tv_in1k_model_card.yaml
linkml-validate -s src/model_card_schema/schema/model_card_schema.yaml -C modelCard data/model_cards_assistant/subcell_saprot_650m_model_card.yaml
python -m unittest discover -s tests -v
python scripts/analyze_model_card_remediation.py
```

The analysis needs PyYAML and Matplotlib. It verifies the immutable baseline hashes,
reproduces all original field-presence cells, rejects undeclared fields and checks that
each evaluator read the same YAML revision as the presence calculation. It writes paired
hybrid JSONs, input/evaluator hashes, the detailed CSV and a separate presence figure.
It does not modify or reuse the supplied heatmap as a new semantic evaluation.

Regenerate only the four current hybrid badges, retaining all archived artifacts:

```bash
python - <<'PY'
import importlib.util
import json
from pathlib import Path
spec = importlib.util.spec_from_file_location('renderer', 'scripts/render_evaluation_html.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
reports = [json.loads(p.read_text()) for p in sorted(Path('data/evaluation/remediation/2026-09-28/after').glob('*/*.json'))]
renderer.write_badges(reports, Path('data/evaluation/badges'))
PY
python src/html/human_readable_renderer.py data/model_cards_assistant/densenet121_tv_in1k_model_card.yaml data/model_cards_assistant/subcell_saprot_650m_model_card.yaml
```

The renderer accepts only badges whose recorded YAML SHA-256 matches its input, and
embeds accepted SVGs as data URLs. Archived or unverified evaluations are omitted with
a visible note. New regression tests cover hash changes, missing/placeholder hashes,
mixed current/archived badges, portable images and retention of structured documentation.
