# Migration and Validation Utilities

This directory contains utilities for migrating Model Cards to use Datasheets for Datasets references and validating the integration.

## Tools

### 1. `migrate_to_harmonized.py`

**Purpose**: Migrate existing model cards to use external Datasheets for Datasets references (Pattern 1 integration).

**Usage**:
```bash
python utils/migrate_to_harmonized.py input.yaml output.yaml
```

**What it does**:
1. Converts `language` → `model_language` (avoids naming conflict)
2. Creates stub datasheet files for each dataset in `model_parameters.data`
3. Adds `dataset_documentation` section with datasheet references
4. Preserves backward compatibility (keeps original `data` section)
5. Adds migration metadata

**Example**:
```bash
# Migrate an existing model card
python utils/migrate_to_harmonized.py \
  src/data/examples/old_model_card.yaml \
  model_card_migrated.yaml

# Output:
# - model_card_migrated.yaml (migrated model card)
# - datasheets/*.yaml (stub datasheet files - need completion)
```

**Output Structure**:
```yaml
# Migrated model card includes:
model_language:  # Changed from 'language'
  - "en"

model_parameters:
  data:  # Original section preserved
    - name: "Dataset Name"
      # ... original fields ...
      datasheet_info: "See dataset_documentation section"

dataset_documentation:  # NEW section
  training_datasets:
    - id: "dataset-name-v1"
      datasheet_url: "https://datasheets.example.org/dataset-name-v1.yaml"
      datasheet_format: "datasheets-for-datasets-v1.0"

migration_info:  # Metadata about migration
  migrated_on: "2025-11-22T..."
  migration_pattern: "Pattern 1: External References"
```

**Next Steps After Migration**:
1. Review the migrated model card
2. Complete the stub datasheet files in `datasheets/`
3. Update datasheet URLs to actual hosting locations
4. Validate using `validate_integration.py`

---

### 2. `validate_integration.py`

**Purpose**: Validate that model cards properly reference datasheets and check datasheet completeness.

**Usage**:
```bash
python utils/validate_integration.py model_card.yaml

# Specify custom datasheets directory
python utils/validate_integration.py model_card.yaml --datasheets-dir ./my_datasheets
```

**What it checks**:
- ✓ Presence of `dataset_documentation` section
- ✓ Valid datasheet references (required fields: id, name, datasheet_url)
- ✓ Local datasheet files exist (if available)
- ✓ Datasheet content structure (motivation, composition, collection, etc.)
- ✓ Incomplete documentation (TODO markers)
- ✓ Migration status (language vs model_language)

**Example Output**:
```
Model Cards + Datasheets Integration Validator
======================================================================
Model Card: model_card.yaml
Datasheets Directory: datasheets
======================================================================

======================================================================
VALIDATION RESULTS
======================================================================

ℹ️  Information:
   Loading model card: model_card.yaml
   Found 2 training dataset reference(s)
   Found local datasheet file: datasheets/imdb-sentiment-v1.yaml
   ✓ Using 'model_language' field (harmonized schema)

⚠️  Warnings (2):
   Missing recommended field 'description' in datasheet reference
   Datasheet 'imdb-sentiment-v1' contains 15 TODO marker(s) - documentation is incomplete

✅ No errors found!

======================================================================
OVERALL: ✅ VALID
======================================================================
```

**Exit Codes**:
- `0` - Validation passed (no errors)
- `1` - Validation failed (errors found)

Can be used in CI/CD pipelines:
```bash
python utils/validate_integration.py model_card.yaml || exit 1
```

---

## Integration Patterns

### Pattern 1: External References (Recommended - Current Phase)

Model cards reference datasheets via URL, datasets documented separately.

**Pros**:
- No schema conflicts
- Clean separation of concerns
- Datasets documented once, referenced many times
- Works with current tooling

**Implementation**: Use `migrate_to_harmonized.py`

### Pattern 2: Embedded Info (Backward Compatible)

Keep simple dataset info in model card, add datasheet pointer.

**Pros**:
- Single file
- Quick prototyping
- Backward compatible

**Implementation**: Manual - add `datasheet_url` to existing `data` entries

### Pattern 3: Full Import (Future - Phase 2+)

Direct schema import with full type checking.

**Status**: Requires resolving all naming conflicts (in progress)

**Implementation**: Will be available after Phase 2 completion

---

## Workflow

### For New Model Cards

1. Create model card using current schema
2. Create comprehensive datasheets for each dataset
3. Reference datasheets in `dataset_documentation` section

### For Existing Model Cards

1. **Migrate**:
   ```bash
   python utils/migrate_to_harmonized.py old_model_card.yaml new_model_card.yaml
   ```

2. **Complete Datasheets**:
   ```bash
   # Edit generated stub files
   vi datasheets/*.yaml

   # Complete all TODO sections
   # See src/data/examples/harmonized/imdb-sentiment-datasheet-v1.yaml for reference
   ```

3. **Update URLs**:
   - Update `datasheet_url` in `dataset_documentation` to actual hosting locations

4. **Validate**:
   ```bash
   python utils/validate_integration.py new_model_card.yaml
   ```

5. **Publish**:
   - Publish datasheets to repository
   - Publish model card with correct datasheet URLs

---

## Examples

### Migrate Example

```bash
# Start with old-format model card
cat > old_model.yaml <<EOF
model_details:
  name: "My Model"

language:
  - "en"

model_parameters:
  data:
    - name: "My Dataset"
      link: "https://example.com/dataset"
      description: "Training data"
EOF

# Migrate
python utils/migrate_to_harmonized.py old_model.yaml new_model.yaml

# Complete the generated datasheet
vi datasheets/my-dataset-v1.yaml

# Validate
python utils/validate_integration.py new_model.yaml
```

### Validation Example

```bash
# Validate harmonized example
python utils/validate_integration.py \
  src/data/examples/harmonized/sentiment-classifier-with-datasheet-refs.yaml \
  --datasheets-dir src/data/examples/harmonized

# Expected output: ✅ VALID
```

---

## Datasheet Template

When completing stub datasheets, ensure all sections are documented:

```yaml
id: "dataset-id-v1"
name: "Dataset Name"
description: "..."

# Required sections:
motivation:
  purposes: [...]
  tasks: [...]
  creators: [...]

composition:
  instances: [...]
  sensitive_elements: [...]

collection:
  acquisition_methods: [...]
  collection_mechanisms: [...]

ethics:
  ethical_reviews: [...]
  data_protection_impacts: [...]

preprocessing:
  preprocessing_strategies: [...]

uses:
  existing_uses: [...]
  discouraged_uses: [...]

distribution:
  license_and_use_terms: [...]

maintenance:
  maintainers: [...]
  updates: [...]

variables: [...]  # Field descriptions
```

See `src/data/examples/harmonized/imdb-sentiment-datasheet-v1.yaml` for a complete example.

---

## Troubleshooting

### "Migration failed: KeyError"
- **Cause**: Model card missing expected fields
- **Solution**: Ensure model card has at least `model_details.name`

### "Datasheet file not found"
- **Cause**: Datasheet not in expected location
- **Solution**: This is a warning, not an error. Update `--datasheets-dir` or publish remotely

### "Contains TODO markers"
- **Cause**: Incomplete datasheet documentation
- **Solution**: Complete all sections marked with TODO

### "Missing required field"
- **Cause**: Datasheet reference missing required metadata
- **Solution**: Add `id`, `name`, and `datasheet_url` to references

---

## References

- **Integration Guide**: `/INTEGRATION_GUIDE.md`
- **Examples**: `/src/data/examples/harmonized/`
- **Datasheets Schema**: https://github.com/bridge2ai/data-sheets-schema
- **Model Cards Schema**: `/src/linkml/modelcards.yaml`

---

## Contributing

To improve these utilities:
1. Add error handling for edge cases
2. Support batch migration of multiple model cards
3. Add datasheet completeness scoring
4. Create conversion between integration patterns

See `CLAUDE.md` for development guidance.
