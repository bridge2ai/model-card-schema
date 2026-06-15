# Model Card Schema Description Review

**Reviewed files**:
- `src/model_card_schema/schema/model_card_schema.yaml` (~1515 lines; ~250 descriptions across slots, slot_usage, classes, enums)
- `src/model_card_schema/schema/model_card_schema_d4dharmonized.yaml` (~1568 lines; ~260 descriptions)
- `src/model_card_schema/schema/personinfo_enums.yaml` — out of scope (auto-generated)

**Reviewer**: mc-description-reviewer
**Date**: 2026-06-15

## Summary

- Descriptions reviewed: ~510 across both files
- Pass: ~470
- Marginal: ~30
- Fail: ~12

Most issues cluster into four patterns:

1. **Cardinality mismatches** — multivalued slots described in the singular ("the metric", "URL to dataset", "code snippet") or non-multivalued slots described as plural.
2. **Stale base/extended overlap** — slots renamed or replaced in the harmonized variant still retain old base-schema phrasing, or `slot_usage` overrides leave the base description from the global slot unchanged (and misleading for the class-specific role).
3. **Range/description disagreement** — slot description implies a class (rich object) but range is plain `string`, or vice versa.
4. **Boilerplate global descriptions** — generic `slots:` block descriptions ("Reference URL or citation string", "Reference to related resources") that the class-level `slot_usage` is supposed to refine but doesn't.

## Failures (must fix)

### 1. `slots.code_examples` (global slot, base schema, line 510-512)

- **Issue**: Cardinality vs range mismatch — multivalued but range singular `CodeExample`. Description omits plurality.
- **Current**: `Code examples for using the model` (`multivalued: true`, `range: CodeExample`)
- **Suggested**: `List of code examples demonstrating model usage`
- **Severity**: low (description is plural-friendly but should be explicit; range is fine)

### 2. `slots.confidence_interval` (global slot, both schemas, base line 200-201, harmonized line 209-210)

- **Issue**: Range is unset (defaults to `string`) at the global level, but description and downstream `slot_usage` use it as a class (`ConfidenceInterval`). The global slot looks like a free-text field on its own.
- **Current**: `Confidence interval for the metric` (no `range:` declared → defaults to string)
- **Suggested**: Either set `range: ConfidenceInterval` at the global slot level, or change description to `Confidence interval for the metric value (set range to ConfidenceInterval on usage)`.
- **Severity**: medium

### 3. `slots.sensitive` (base schema, line 138-139)

- **Issue**: No range declared (defaults to `string`), but description says "Sensitive data information" and `dataSet.slot_usage` later sets `range: SensitiveData`. The standalone slot is misleading.
- **Current**: `Sensitive data information` (no range → string)
- **Suggested**: Set `range: SensitiveData` at the global slot, or change description to `Sensitive data information for the dataset (typically a SensitiveData object via slot_usage)`.
- **Severity**: medium

### 4. `slots.graphics` (both schemas, base line 141-142, harmonized line 160-161)

- **Issue**: Same problem as `sensitive`/`confidence_interval`. Description "Visualizations and graphics" implies a class, but no range is declared → defaults to string. `slot_usage` in `dataSet`, `QuantitativeAnalysis` raises it to `GraphicsCollection`.
- **Current**: `Visualizations and graphics`
- **Suggested**: Add `range: GraphicsCollection` to the global slot.
- **Severity**: medium

### 5. `slots.version` (both schemas, base line 114-115, harmonized line 127-128)

- **Issue**: No range declared at the global slot. `slot_usage` in ModelDetails sets it to `Version` (a class). Generic description "Version information" applies, but a user reading the global slot would assume string.
- **Current**: `Version information` (no range)
- **Suggested**: Add `range: Version` to the global slot.
- **Severity**: medium

### 6. `slots.task` / `slots.dataset` / `slots.source` (both schemas, base lines 332-339, harmonized lines 341-348)

- **Issue**: All three have stub descriptions and no range — defaults to string. They are intended for `BenchmarkResult` usage where they refer to `Task`, `BenchmarkDataset`, `BenchmarkSource` classes respectively. Standalone, these descriptions are too generic to be useful and the range mismatches their slot_usage.
- **Current**:
  - `task`: `ML task specification`
  - `dataset`: `Dataset information`
  - `source`: `Source of information or results`
- **Suggested**:
  - `task`: `ML task being evaluated (BenchmarkResult.task references a Task object)`, set `range: Task`
  - `dataset`: `Benchmark dataset (BenchmarkResult.dataset references a BenchmarkDataset object)`, set `range: BenchmarkDataset`
  - `source`: `Source of benchmark results (BenchmarkResult.source references a BenchmarkSource object)`, set `range: BenchmarkSource`
- **Severity**: medium

### 7. `slots.results` (both schemas, base line 341-343, harmonized line 350-352)

- **Issue**: Multivalued, but range missing. Used in `ModelIndex.slot_usage` as `BenchmarkResult`. Description "Benchmark or evaluation results" is acceptable but the missing global range is misleading.
- **Current**: `Benchmark or evaluation results` (`multivalued: true`, no range)
- **Suggested**: Add `range: BenchmarkResult` at the global slot level.
- **Severity**: medium

### 8. `slots.model_index` (both schemas, base line 345-347, harmonized line 354-356)

- **Issue**: Multivalued; description names the upstream concept (Papers with Code model-index) but range is unset → defaults to string. `modelCard.slot_usage` correctly sets `range: ModelIndex`.
- **Current**: `Papers with Code model-index for benchmark tracking`
- **Suggested**: Set `range: ModelIndex` and update description to `List of Papers with Code model-index entries, one per benchmark configuration`.
- **Severity**: medium

### 9. `slots.model_details` (both schemas, base line 269-271, harmonized line 278-280)

- **Issue**: Required at the global slot level, no range declared (defaults to string), but is the top-level structural anchor → must be `ModelDetails`. The global slot says "Comprehensive model metadata" but a user can't tell it's a class without reading `modelCard.slot_usage`.
- **Current**: `Comprehensive model metadata` (`required: true`, no range)
- **Suggested**: Add `range: ModelDetails`.
- **Severity**: high

### 10. `slots.model_parameters`, `slots.quantitative_analysis`, `slots.considerations` (both schemas)

- **Issue**: Same pattern as `model_details` — all are container classes at the top-level slot definition but lack `range:` declarations.
- **Current**:
  - `model_parameters`: `Model construction and architecture parameters`
  - `quantitative_analysis`: `Quantitative analysis and performance evaluation`
  - `considerations`: `Usage considerations, limitations, and ethical concerns`
- **Suggested**: Add `range: ModelParameters`, `range: QuantitativeAnalysis`, `range: Considerations` respectively.
- **Severity**: high

### 11. `slots.input_format_map` / `slots.output_format_map` (both schemas, base lines 171-181, harmonized lines 180-190)

- **Issue**: Multivalued, no global range. `ModelParameters.slot_usage` sets them to `KeyVal`. The description "Structured input format mapping" doesn't reflect that they're lists of KeyVal pairs.
- **Current**: `Structured input format mapping` / `Structured output format mapping`
- **Suggested**:
  - `input_format_map`: `List of key/value pairs describing input format fields`, add `range: KeyVal`
  - `output_format_map`: `List of key/value pairs describing output format fields`, add `range: KeyVal`
- **Severity**: medium

### 12. `slots.data` (base schema only, line 163-165)

- **Issue**: Multivalued, no global range; `ModelParameters.slot_usage` sets `range: dataSet`. Description is generic.
- **Current**: `Training and evaluation datasets`
- **Suggested**: Keep description; add `range: dataSet` at the global slot level.
- **Severity**: medium

### 13. `slots.owners` (base schema only, line 110-112)

- **Issue**: Multivalued, no global range, no description of *who* owners are. `ModelDetails.slot_usage` sets `range: owner` (note: lowercase class — matches an unusual base-schema convention).
- **Current**: `Model owners or maintainers`
- **Suggested**: `List of owners or maintainers (individuals or organizations)`, add `range: owner`.
- **Severity**: medium

### 14. `slots.contributors` (base schema only, line 541-544)

- **Issue**: Description says "Model contributors with roles" but the global slot has `range: Contributor` set correctly. The current text is acceptable; combine with cardinality wording.
- **Current**: `Model contributors with roles`
- **Suggested**: `List of model contributors with role-based attribution`.
- **Severity**: low

### 15. `slots.creator_references` (harmonized schema, line 123-125)

- **Issue**: Multivalued, no global range declared — but `ModelDetails.slot_usage` sets `range: CreatorReference`. Description does say "replaces owners/contributors" which is helpful.
- **Current**: `References to Datasheets for Datasets Creator instances (replaces owners/contributors)`
- **Suggested**: Add `range: CreatorReference` at the global slot. Description is otherwise fine.
- **Severity**: medium

### 16. `slots.training_datasets` / `slots.evaluation_datasets` (harmonized schema, lines 151-157)

- **Issue**: Multivalued, no global range; `ModelParameters.slot_usage` sets `range: DatasetReference`.
- **Current**:
  - `training_datasets`: `References to training datasets (D4D Dataset instances)`
  - `evaluation_datasets`: `References to evaluation/test datasets (D4D Dataset instances)`
- **Suggested**: Both descriptions are accurate; add `range: DatasetReference` at the global slot.
- **Severity**: medium

### 17. `slots.funding_grants` (harmonized schema, line 516-518)

- **Issue**: Multivalued, no global range. `MissionRelevance.slot_usage` sets `range: GrantReference`.
- **Current**: `References to funding grants (D4D Grant instances)`
- **Suggested**: Add `range: GrantReference` to global slot. Description is otherwise correct.
- **Severity**: medium

### 18. `slots.hyperparameters` (both schemas, base line 446-448, harmonized line 430-432)

- **Issue**: Range *is* set to `Hyperparameters` at the global slot — this is a positive example. The description "Training hyperparameters" is fine.
- **Status**: Pass — kept here only to contrast with the other slots above (the rest should follow this pattern).

## Marginals (should improve)

### 1. `slots.value` (both schemas, base line 188-189, harmonized line 197-198)

- **Issue**: No range declared; description "Value in key-value pair or metric value" tries to cover two distinct uses. `KeyVal.slot_usage` sets `string`, `performanceMetric.slot_usage` sets `float`, `BenchmarkMetric.slot_usage` sets `float`. The dual-purpose phrasing is fine because the global slot is deliberately polymorphic, but flag for clarity.
- **Suggested**: `Generic value field; range is refined per class (string for KeyVal, float for metrics)`.

### 2. `slots.args` (both schemas, base line 361-362, harmonized line 370-371)

- **Issue**: Description "Additional arguments or parameters" is generic; no range; used in `BenchmarkDataset` and `BenchmarkMetric` as `kwargs`-like map. Used as string in slot_usage but truly polymorphic.
- **Suggested**: `Additional arguments or keyword parameters (free-form, format depends on usage)`.

### 3. `slots.url` (both schemas)

- **Issue (base, line 364-366)**: Description "URL reference" is minimal. Used only by `BenchmarkSource`. OK.
- **Issue (harmonized, line 147-149)**: Description was *changed* to "URL to external resource (Creator, Dataset, Grant, etc.)" because `url` is now used by `CreatorReference`, `DatasetReference`, `GrantReference`. This is good — but `BenchmarkSource` *also* uses it for the leaderboard URL, which is unrelated. Description should cover both:
- **Suggested (harmonized)**: `URL to external resource — Creator/Dataset/Grant instance, or benchmark source page`.

### 4. `slots.environment_config` (both schemas, base line 438-440, harmonized line 422-424)

- **Issue**: Global slot description says "Link to environment configuration files" → implies a URL. But `ReproducibilityInfo.slot_usage` says "Complete environment configuration (YAML, JSON, or text)" — inline content, not a link. Mismatch between global and per-class.
- **Suggested global**: `Environment configuration — inline content (YAML/JSON/text) or URL to config file`.

### 5. `slots.identifier` (both schemas, line 79-80 / 75-76)

- **Issue**: Description "SPDX license identifier (e.g., 'Apache-2.0', 'MIT')" is correct only because the slot is currently used only by `License`. Calling a global slot `identifier` but constraining the description to "SPDX license identifier" is brittle if it is ever reused for a model/version identifier.
- **Suggested**: Either rename slot to `license_identifier`, or keep name and say `License identifier (SPDX style, e.g., 'Apache-2.0', 'MIT')`. Low priority.

### 6. `slots.custom_text` (both schemas, line 83-84 / 79-80)

- **Issue**: Same — generic slot name with a license-specific description. Fine as long as scope stays narrow.
- **Suggested**: Add `License ` prefix: `License custom text (use when SPDX identifier is not applicable)`.

### 7. `slots.path` (both schemas, line 129-131 / 142-144)

- **Issue**: "Storage location or path to model artifacts" — ambiguous between file path and URL. Used in `ModelDetails`. Good enough.
- **Suggested**: `Filesystem path, URI, or storage location of model artifacts`.

### 8. `slots.contact` (both schemas)

- **Issue**: Description "Contact information (email, URL, etc.)" is correct but used (in base) only in `owner`. In harmonized schema the `owner` class is removed → `contact` slot is unused. The slot should either be removed from the harmonized schema, or kept with rationale.
- **Suggested (harmonized)**: Add comment or remove the now-orphan `contact` slot. Marginal because unused slots don't break validation.

### 9. `slots.reference` (both schemas, line 88-90 / 84-86)

- **Issue**: Global slot description says "Reference URL or citation string", and the `Reference` class uses it exactly that way. But the *class* `Reference` itself is described as "Reference to related resources" while it has only a single `reference` field of string. So the `Reference` class is barely more than a typed string wrapper. Acceptable but worth noting.
- **Suggested class description**: `Reference to a related resource (URL or citation string)`.

### 10. `slots.image` (both schemas)

- **Issue**: Description "Base64-encoded image (PNG format)" is accurate. PNG is restrictive — many real-world images are JPEG/SVG. Confirm intent.
- **Suggested**: `Base64-encoded image (PNG preferred)` — only if non-PNG is allowed.

### 11. `slots.bias_input` / `bias_model` / `bias_output` (both schemas)

- **Issue**: All three are single string fields. Descriptions are minimal but consistent. Consider whether free-text bias documentation should be multivalued (e.g., a list of identified biases) — but that's a schema design choice, not a description bug.

### 12. `slots.language` (both schemas, line 307-310 / 316-319)

- **Issue**: Description "Natural language(s) processed by the model" — `multivalued: true, range: string`. Fine.
- **Cross-class concern**: There is no separate `model_language` vs `documentation_language` distinction; the HuggingFace `language` tag is for *content* the model processes. Description is consistent with HF semantics. Pass.

### 13. `slots.framework` (both schemas)

- **Issue**: Description: "ML framework (TensorFlow, PyTorch, JAX, Scikit-Learn, etc.)" at global slot. `modelCard.slot_usage` repeats: "ML framework used (TensorFlow, PyTorch, JAX, Scikit-Learn, etc.)". Identical info repeated; consider tightening one.

### 14. `slots.config` (both schemas, line 349-351 / 358-360)

- **Issue**: "Configuration specification" — very generic, no context. Used in `BenchmarkDataset` and `BenchmarkMetric` for the HuggingFace `config_name` style argument.
- **Suggested**: `Configuration name or identifier (e.g., HuggingFace dataset config name)`.

### 15. `slots.split` (both schemas)

- **Issue**: "Dataset split (train, test, validation)" — fine and consistent.

### 16. `slots.revision` (both schemas)

- **Issue**: "Dataset or model revision/version" used only for `BenchmarkDataset`. Fine.

### 17. `slots.type` (both schemas, line 192-194 / 201-203)

- **Issue**: "Type or category" is overly generic. Used in `performanceMetric` (metric type — accuracy/F1/AUC), `Task` (task type — HF task tag), `BenchmarkDataset` (dataset type), `BenchmarkMetric` (metric type).
- **Suggested**: `Type identifier (semantics depend on owning class — metric type, task type, dataset type)`.

### 18. `slots.collection` (both schemas, line 221-223 / 230-232)

- **Issue**: "Collection of items" is too generic to be useful at the slot level. Used in `GraphicsCollection` where `slot_usage` correctly sets `range: graphic` and improves description.
- **Suggested global**: `Collection (refined per class — e.g., graphics in a GraphicsCollection)`.

### 19. `Citation` class description (both schemas, line 689-690 / 734-735)

- **Issue**: Class description "Citation information for the model" duplicates the description of the global slot `citations`. The class is *one* citation, not citations-plural.
- **Suggested**: `A single citation entry (style + formatted text)`.

### 20. `risk` class description (both schemas, line 992-993 / 1031-1032)

- **Issue**: Class name is lowercase `risk` (a style carryover noted in CLAUDE.md gotchas). Description "An ethical, environmental, or operational risk" — accurate.
- **Cross-class note**: The slot it's used through is `ethical_considerations` (range: `risk`), but `ethical_considerations.description` says "Ethical considerations and identified risks" — fine but slightly redundant.

### 21. `BenchmarkSource.url` description (both schemas, line 1116-1118 / 1155-1157)

- **Issue**: Description "URL to the source" is correct but minimal. Compare with the much richer `CreatorReference.url`, `DatasetReference.url`, `GrantReference.url` in harmonized.
- **Suggested**: `URL to the benchmark source page (e.g., leaderboard, paper, evaluation site)`.

### 22. `slots.created_by` / `modified_by` (harmonized, line 98-104)

- **Issue**: "Name or identifier of person/organization who created/modified this resource". Slightly redundant when shadowed by `slot_usage` in `ModelDetails` and `modelCard` (which both repeat the same wording with "this model card"). Acceptable but watch for drift.

### 23. `slots.created_on` / `modified_on` (harmonized, line 106-112)

- **Issue**: "Timestamp when this resource was created/last modified". Consider mentioning expected format (ISO-8601) since range is `datetime`.
- **Suggested**: `ISO-8601 timestamp when this resource was created` / `ISO-8601 timestamp when this resource was last modified`.

### 24. `dataSet.link` (base schema, line 815-818)

- **Issue**: `slot_usage` requires `link: required: true`. Description "URL to the dataset" is fine. Note inconsistency: in HuggingFace metadata, datasets are commonly listed as IDs/names without a URL — requiring a URL here may be stricter than upstream.
- **Severity**: Marginal — schema design, not description.

### 25. `dataSet.description` (base schema, line 812-814)

- **Issue**: Class-level `description` field is described as "Dataset overview and characteristics", which is great. But the global slot `description` says "Textual description" — not enough cue that subclasses redefine the meaning. Cross-class consistency issue rather than per-field bug.

### 26. `Hyperparameters.optimization_techniques` (both schemas)

- **Issue**: Global slot description says "Model optimization techniques (distillation, quantization, pruning, sparsity)". Per-class `slot_usage` says "Additional optimization techniques (e.g., 'gradient clipping', 'mixed precision')". These describe *different* categories of optimization (the global is about post-training compression; the slot_usage is about training-time numerical optimization). This is a real semantic drift.
- **Suggested global**: `Optimization techniques applied during or after training (e.g., quantization, pruning, gradient clipping, mixed precision)`.

### 27. `Hyperparameters` class — `optimization_techniques` in `slot_usage`

- **Issue**: In `slot_usage`, `multivalued: true` is set on `optimization_techniques`. The slot description is singular ("Additional optimization techniques"). Fine.

### 28. `EvaluationProcedure.benchmarks` (both schemas)

- **Issue**: `slot_usage` says "Benchmark datasets and tasks", range `string`, multivalued. Global slot `benchmarks` description says "Benchmarks used for evaluation". Acceptable but slight overlap with `QuantitativeAnalysis.performance_metrics` which holds the actual results.
- **Suggested**: `Names/identifiers of benchmark suites used for evaluation (e.g., 'MMLU', 'HELM')`.

### 29. `TrainingProcedure.description` and other class-`description` slot_usage entries

- **Issue**: Classes (`TrainingProcedure`, `EvaluationProcedure`, `CodeExample`, `UsageDocumentation`, `MissionRelevance`, `User`, `UseCase`, `Limitation`, `Tradeoff`, `OutOfScopeUse`, `GraphicsCollection`) all use the generic `description` slot for class-specific content. Each `slot_usage.description` overrides with the per-class meaning (good). Verify that the overrides don't drift over time.

### 30. `slots.users` (both schemas)

- **Issue**: Description "Intended users or user types" → good. Class `User` description "Description of an intended user type" — good. But `Considerations.users.slot_usage` is just "Intended user types" (no mention of *intended* vs *actual* user distinction). Pass.

## Cross-schema observations

1. **Container slots missing global range** — The most common defect across both files is global slot definitions that lack a `range:` declaration despite being used as class containers in `slot_usage`. While LinkML allows this (range can be lifted from `slot_usage`), it confuses users and downstream tooling that reads the global slot definition. Slots affected: `model_details`, `model_parameters`, `quantitative_analysis`, `considerations`, `version`, `graphics`, `sensitive`, `confidence_interval`, `hyperparameters` (this one is correct — keep as model), `task`, `dataset`, `source`, `results`, `model_index`, `data` (base only), `owners` (base), `input_format_map`, `output_format_map`, `creator_references` (harmonized), `training_datasets` (harmonized), `evaluation_datasets` (harmonized), `funding_grants` (harmonized).

2. **Base vs harmonized inconsistency** — the harmonized schema correctly removes `Contributor` class, `owner` class, `dataSet` class, `funding_source` slot, and `slots.role`/`slots.email`/`slots.orcid`/`slots.affiliation`/`slots.contributors`/`slots.owners`/`slots.data`/`slots.sensitive_data`/`slots.sensitive`/`slots.funding_source`. However, the `SensitiveData` class is also gone from harmonized, but `slots.bias_input` is retained (now orphan unless reused — it isn't used by any class in the harmonized file). Confirm whether `bias_input` is intentionally retained for forward compatibility.

3. **Orphan slots in harmonized schema** — slots present at global level but not used by any class in the harmonized variant: `contact`, `bias_input`, `unit` (used in `performanceMetric`, OK). Suggest pruning or commenting.

4. **`graphic` (lowercase) is used as a range** in both schemas (`GraphicsCollection.collection: range: graphic`). LinkML is case-sensitive for class names; the class exists as lowercase `graphic` in both files, which is unusual but functional. Documented as a styling carryover.

5. **`owner` (lowercase) class** in base schema — referenced as `range: owner` in `ModelDetails.slot_usage.owners`. Consistent within base. Removed from harmonized. No description problem.

6. **D4D reference classes (`CreatorReference`, `DatasetReference`, `GrantReference`)** have well-crafted multi-paragraph descriptions in the harmonized schema. Their `url` and `description` slot_usage entries are good. No description failures here.

7. **`modelCard` class** in harmonized has a useful "D4D Harmonization changes" comment block in its description — good practice. Base `modelCard` description is one line; consider expanding to mention extensions.

8. **`schema_version` slot_usage in harmonized `modelCard`** says "use 'd4d-1.0' for this harmonized version" — good hint. Base equivalent doesn't suggest a value; consider adding `(e.g., '1.0')`.

9. **`enums.CitationStyleEnum`** — identical in both files. Pass.

10. **Base schema has `ContributorRoleEnum`** with 4 permissible values; harmonized schema does *not* have this enum because `Contributor` is replaced. Good consistency.

## Suggested batch fixes

```yaml
# ============================================
# BATCH FIX A: Add explicit range to global slots that are class containers
# (apply to BOTH model_card_schema.yaml AND model_card_schema_d4dharmonized.yaml)
# ============================================

slots:
  model_details:
    description: Comprehensive model metadata
    range: ModelDetails        # ADD
    required: true

  model_parameters:
    description: Model construction and architecture parameters
    range: ModelParameters     # ADD

  quantitative_analysis:
    description: Quantitative analysis and performance evaluation
    range: QuantitativeAnalysis  # ADD

  considerations:
    description: Usage considerations, limitations, and ethical concerns
    range: Considerations      # ADD

  version:
    description: Version information for the model
    range: Version             # ADD

  graphics:
    description: Visualizations and graphics
    range: GraphicsCollection  # ADD

  sensitive:                   # (base schema only)
    description: Sensitive data information
    range: SensitiveData       # ADD

  confidence_interval:
    description: Confidence interval for the metric
    range: ConfidenceInterval  # ADD

  task:
    description: ML task being evaluated
    range: Task                # ADD

  dataset:
    description: Benchmark dataset reference
    range: BenchmarkDataset    # ADD

  source:
    description: Source of benchmark results
    range: BenchmarkSource     # ADD

  results:
    description: Benchmark or evaluation results
    range: BenchmarkResult     # ADD
    multivalued: true

  model_index:
    description: List of Papers with Code model-index entries, one per benchmark configuration
    range: ModelIndex          # ADD
    multivalued: true

  input_format_map:
    description: List of key/value pairs describing input format fields
    range: KeyVal              # ADD
    multivalued: true

  output_format_map:
    description: List of key/value pairs describing output format fields
    range: KeyVal              # ADD
    multivalued: true

# ============================================
# BATCH FIX B: Base-schema-only ranges
# ============================================

slots:
  data:
    description: Training and evaluation datasets
    range: dataSet             # ADD
    multivalued: true

  owners:
    description: List of model owners or maintainers (individuals or organizations)  # CLARIFY
    range: owner               # ADD
    multivalued: true

# ============================================
# BATCH FIX C: Harmonized-schema-only ranges
# ============================================

slots:
  creator_references:
    description: References to Datasheets for Datasets Creator instances (replaces owners/contributors)
    range: CreatorReference    # ADD
    multivalued: true

  training_datasets:
    description: References to training datasets (D4D Dataset instances)
    range: DatasetReference    # ADD
    multivalued: true

  evaluation_datasets:
    description: References to evaluation/test datasets (D4D Dataset instances)
    range: DatasetReference    # ADD
    multivalued: true

  funding_grants:
    description: References to funding grants (D4D Grant instances)
    range: GrantReference      # ADD
    multivalued: true

# ============================================
# BATCH FIX D: Disambiguate cross-class slot descriptions
# ============================================

slots:
  type:
    description: |
      Type identifier (semantics depend on owning class —
      e.g., performance metric type, ML task type, dataset type).
    range: string

  value:
    description: |
      Generic value field; the range is refined per class
      (string for KeyVal, float for performanceMetric and BenchmarkMetric).

  config:
    description: Configuration name or identifier (e.g., HuggingFace dataset config name)
    range: string

  environment_config:
    description: Environment configuration — inline content (YAML/JSON/text) or URL to config file
    range: string

  # (harmonized only) — broaden url description
  url:
    description: URL to external resource — Creator/Dataset/Grant instance, or benchmark source page
    range: uri

# ============================================
# BATCH FIX E: Hyperparameters.optimization_techniques semantic drift
# (apply to BOTH schemas)
# ============================================

slots:
  optimization_techniques:
    description: |
      Optimization techniques applied during or after training
      (e.g., quantization, pruning, distillation, sparsity,
      gradient clipping, mixed precision).
    multivalued: true
    range: string

# ============================================
# BATCH FIX F: Provenance timestamp format hint (harmonized only)
# ============================================

slots:
  created_on:
    description: ISO-8601 timestamp when this resource was created
    range: datetime

  modified_on:
    description: ISO-8601 timestamp when this resource was last modified
    range: datetime

# ============================================
# BATCH FIX G: Class-level tightening
# ============================================

classes:
  Citation:
    description: A single citation entry (style + formatted citation text)

  Reference:
    description: A reference to a related resource (URL or citation string)
```

## Notes for future passes

- **Naming-convention warnings** from `linkml-lint` (lowercase classes `owner`, `risk`, `graphic`, `dataSet`, `performanceMetric`, `modelCard`) are stylistic carryovers and not addressed here per scope.
- **`personinfo_enums.yaml`** is regenerated by `make compile-sheets` from a Google Sheet; descriptions there should be edited in the source sheet, not the YAML.
- **Examples directory** (`src/data/examples/`) was not reviewed — that's instance data, not schema. Use `mc-validator` for those.
