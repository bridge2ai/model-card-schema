# Migration Guide: Adopting Model Cards + Datasheets Integration

**Version**: 1.0
**Last Updated**: November 22, 2025
**Target Audience**: ML practitioners, data scientists, ML engineers

---

## Table of Contents

1. [Overview](#overview)
2. [Why Migrate?](#why-migrate)
3. [Migration Paths](#migration-paths)
4. [Step-by-Step Guide](#step-by-step-guide)
5. [Tools and Utilities](#tools-and-utilities)
6. [Examples](#examples)
7. [Validation](#validation)
8. [FAQ](#faq)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide helps you migrate existing Model Cards to leverage Datasheets for Datasets, providing comprehensive dataset documentation while maintaining backward compatibility.

**What Changes**:
- Datasets get comprehensive documentation (60+ fields vs 7 fields)
- Model cards reference external datasheets
- Better ethics, privacy, and governance support
- Single source of truth for datasets

**What Stays the Same**:
- Model-specific documentation structure
- Performance metrics and considerations
- HuggingFace/Papers with Code integration
- Existing tooling compatibility

---

## Why Migrate?

### Current Limitations

**Simple Dataset Documentation** (Current `dataSet` class):
```yaml
data:
  - name: "IMDb Reviews"
    link: "https://example.com"
    description: "Movie reviews"
    # Only 7 fields total
```

**Problems**:
- ❌ Minimal documentation (name, link, description, sensitive, graphics, bias_input, unit)
- ❌ No creator attribution (ORCID, affiliations)
- ❌ No collection methodology documentation
- ❌ Limited ethics/privacy information
- ❌ No maintenance or versioning details
- ❌ Duplicated across multiple model cards

### After Migration

**Comprehensive Dataset Documentation** (Datasheets):
```yaml
# In model card:
dataset_documentation:
  training_datasets:
    - id: "imdb-reviews-v1"
      datasheet_url: "https://datasheets.example.org/imdb-reviews-v1.yaml"

# In separate datasheet file (60+ fields):
- motivation (purpose, tasks, creators, funding)
- composition (50K instances, balanced, subsets)
- collection (web scraping, sampling, timeframes)
- ethics (reviews, consent, privacy, GDPR compliance)
- preprocessing (cleaning, labeling, raw data)
- uses (existing, discouraged, impact analysis)
- distribution (formats, licensing, IP restrictions)
- maintenance (maintainers, updates, version access)
- variables (detailed field descriptions)
```

**Benefits**:
- ✅ Comprehensive documentation (60+ fields)
- ✅ Proper creator attribution (ORCID, CRediT roles)
- ✅ Detailed methodology and ethics
- ✅ Better governance and compliance
- ✅ Single source of truth (document once, reference everywhere)
- ✅ Backward compatible

---

## Migration Paths

### Path A: Automated Migration (Recommended)

**Best for**: Existing model cards with simple dataset references

**Tools**: `utils/migrate_to_harmonized.py`

**Effort**: ~15 minutes per model card + 1-2 hours per unique dataset

**Process**:
1. Run migration tool
2. Complete generated datasheet stubs
3. Validate

### Path B: Manual Migration

**Best for**: New model cards or custom requirements

**Effort**: ~30 minutes per model card + 1-2 hours per unique dataset

**Process**:
1. Create datasheets manually
2. Add `dataset_documentation` section to model card
3. Validate

### Path C: Hybrid Approach

**Best for**: Large-scale migrations with diverse model cards

**Effort**: Variable

**Process**:
1. Use automated migration for standard cases
2. Manual migration for edge cases
3. Batch validation

---

## Step-by-Step Guide

### Prerequisites

- Python 3.9+ installed
- YAML files for existing model cards
- Basic understanding of your datasets

### Step 1: Backup

```bash
# Create backup
cp my_model_card.yaml my_model_card.yaml.backup
```

### Step 2: Run Migration Tool

```bash
python utils/migrate_to_harmonized.py \
  my_model_card.yaml \
  my_model_card_migrated.yaml
```

**Output**:
- `my_model_card_migrated.yaml` - Migrated model card
- `datasheets/*.yaml` - Stub datasheet files (one per dataset)

### Step 3: Review Migrated Model Card

```bash
# View migrated model card
cat my_model_card_migrated.yaml
```

**Key Changes**:
- ✓ `language` → `model_language`
- ✓ New `dataset_documentation` section
- ✓ Original `data` section preserved (backward compatible)
- ✓ Migration metadata added

### Step 4: Complete Datasheets

For each generated datasheet in `datasheets/`:

```bash
# Edit datasheet
vi datasheets/my-dataset-v1.yaml
```

**Required Actions**:
1. Replace all `TODO:` markers with actual information
2. Fill in creator information (names, ORCID, emails, affiliations)
3. Document collection methodology
4. Add ethics and privacy considerations
5. Describe preprocessing steps
6. List existing and discouraged uses
7. Specify license and distribution terms
8. Add maintainer information

**Reference**: See `src/data/examples/harmonized/imdb-sentiment-datasheet-v1.yaml` for a complete example.

### Step 5: Update Datasheet URLs

In the migrated model card, update placeholder URLs:

```yaml
dataset_documentation:
  training_datasets:
    - id: "my-dataset-v1"
      # UPDATE THIS:
      datasheet_url: "https://your-org.example.org/datasheets/my-dataset-v1.yaml"
      datasheet_format: "datasheets-for-datasets-v1.0"
```

### Step 6: Validate

```bash
python utils/validate_integration.py my_model_card_migrated.yaml
```

**Expected Output**:
```
✅ No errors found!
OVERALL: ✅ VALID
```

**Fix any warnings** (missing fields, incomplete documentation, etc.)

### Step 7: Publish

1. **Publish Datasheets**:
   ```bash
   # Upload datasheets to your repository/registry
   cp datasheets/*.yaml /path/to/datasheet/repository/
   ```

2. **Update Model Card**:
   - Update `datasheet_url` to actual hosted locations
   - Commit and push model card

3. **Verify**:
   ```bash
   # Validate again with final URLs
   python utils/validate_integration.py my_model_card_migrated.yaml
   ```

---

## Tools and Utilities

### Migration Tool

**Location**: `utils/migrate_to_harmonized.py`

**Purpose**: Automate conversion of model cards to reference datasheets

**Usage**:
```bash
python utils/migrate_to_harmonized.py INPUT.yaml OUTPUT.yaml
```

**Features**:
- Renames `language` → `model_language`
- Creates datasheet stubs
- Adds `dataset_documentation` section
- Preserves backward compatibility

### Validation Tool

**Location**: `utils/validate_integration.py`

**Purpose**: Validate model cards and datasheet references

**Usage**:
```bash
python utils/validate_integration.py MODEL_CARD.yaml
python utils/validate_integration.py MODEL_CARD.yaml --datasheets-dir ./my_datasheets
```

**Checks**:
- Dataset documentation section exists
- Datasheet references are valid
- Local datasheets are complete
- Migration status

---

## Examples

### Example 1: Simple Migration

**Before** (`old_model.yaml`):
```yaml
model_details:
  name: "Sentiment Classifier"

language:
  - "en"

model_parameters:
  data:
    - name: "Twitter Sentiment"
      link: "https://example.com/twitter-data"
      description: "100K tweets"
```

**Migrate**:
```bash
python utils/migrate_to_harmonized.py old_model.yaml new_model.yaml
```

**After** (`new_model.yaml`):
```yaml
model_details:
  name: "Sentiment Classifier"

model_language:  # ← Changed
  - "en"

model_parameters:
  data:  # ← Preserved
    - name: "Twitter Sentiment"
      link: "https://example.com/twitter-data"
      description: "100K tweets"
      datasheet_info: "See dataset_documentation section"

dataset_documentation:  # ← NEW
  training_datasets:
    - id: "twitter-sentiment-v1"
      name: "Twitter Sentiment"
      datasheet_url: "https://datasheets.example.org/twitter-sentiment-v1.yaml"
      datasheet_format: "datasheets-for-datasets-v1.0"

migration_info:
  migrated_on: "2025-11-22T10:00:00"
  migration_pattern: "Pattern 1: External References"
```

**Generated Datasheet** (`datasheets/twitter-sentiment-v1.yaml`):
```yaml
id: "twitter-sentiment-v1"
name: "Twitter Sentiment"

# ... sections with TODO markers to complete ...
motivation:
  purposes:
    - description: "TODO: Document why this dataset was created"

creators:
  - principal_investigator:
      name: "TODO: Add creator name"
      # ... complete all TODO sections ...
```

### Example 2: Multiple Datasets

**Before**:
```yaml
model_parameters:
  data:
    - name: "Training Set A"
      link: "https://example.com/train-a"
    - name: "Training Set B"
      link: "https://example.com/train-b"
    - name: "Validation Set"
      link: "https://example.com/val"
```

**After**:
```yaml
dataset_documentation:
  training_datasets:
    - id: "training-set-a-v1"
      datasheet_url: "..."
    - id: "training-set-b-v1"
      datasheet_url: "..."

  evaluation_datasets:
    - id: "validation-set-v1"
      datasheet_url: "..."
```

**Generated**: 3 datasheet stubs in `datasheets/`

---

## Validation

### Validation Checklist

Before publishing migrated model cards:

- [ ] Migration tool ran successfully
- [ ] All datasheet stubs completed (no TODO markers)
- [ ] Datasheet URLs updated to actual locations
- [ ] Validation tool reports no errors
- [ ] Creator attribution complete (ORCID, affiliations)
- [ ] Ethics and privacy sections filled
- [ ] License terms specified
- [ ] Maintainer information added

### Running Validation

```bash
# Basic validation
python utils/validate_integration.py model_card.yaml

# With custom datasheets directory
python utils/validate_integration.py model_card.yaml --datasheets-dir /path/to/datasheets

# Exit code: 0 = valid, 1 = invalid (use in CI/CD)
python utils/validate_integration.py model_card.yaml && echo "Valid!" || echo "Invalid!"
```

### Common Validation Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing dataset_documentation | Old format | Run migration tool |
| Missing required field 'id' | Incomplete reference | Add `id`, `name`, `datasheet_url` |
| Contains TODO markers | Incomplete datasheet | Complete all TODO sections |
| Datasheet file not found | Wrong path or not published | Update `--datasheets-dir` or publish remotely |
| Using 'language' field | Not migrated | Run migration tool |

---

## FAQ

### Q: Do I have to migrate?

**A**: No, existing model cards continue to work. Migration is optional but recommended for:
- Better dataset documentation
- Governance and compliance requirements
- Reducing duplication (shared datasets)
- Ethics and privacy documentation

### Q: Will my existing tools break?

**A**: No, migration maintains backward compatibility:
- Original `data` section is preserved
- All existing fields remain
- New sections added, nothing removed

### Q: Can I migrate partially?

**A**: Yes, you can migrate model cards incrementally:
- Start with high-value models
- Prioritize shared datasets
- Migrate as needed for compliance

### Q: What if my dataset changes?

**A**: Update the datasheet and increment version:
- Create `dataset-v2.yaml`
- Update model card to reference v2
- Keep v1 for reproducibility

### Q: Can multiple models reference one datasheet?

**A**: Yes! This is the main benefit:
- Document dataset once
- Reference from many model cards
- Update in one place

### Q: How do I handle proprietary datasets?

**A**: Create datasheets with appropriate licensing:
- Use `license_and_use_terms` for restrictions
- Add `ip_restrictions` if applicable
- Mark sensitive sections as internal-only

### Q: What about datasets from third parties?

**A**: Reference existing datasheets or create stubs:
- Check if datasheet already exists
- If not, create comprehensive datasheet
- Give proper attribution to creators

---

## Troubleshooting

### Migration Tool Errors

**Error**: `KeyError: 'model_details'`
- **Cause**: Model card missing required structure
- **Fix**: Ensure model card has `model_details.name` field

**Error**: `FileNotFoundError`
- **Cause**: Input file doesn't exist
- **Fix**: Check input file path

### Validation Errors

**Error**: "Missing required field 'datasheet_url'"
- **Cause**: Datasheet reference incomplete
- **Fix**: Add `id`, `name`, and `datasheet_url` to all references

**Warning**: "Contains TODO markers"
- **Cause**: Datasheet not completed
- **Fix**: Replace all TODO with actual information

**Warning**: "Missing recommended field 'description'"
- **Cause**: Optional field not provided
- **Fix**: Add description for better documentation (optional)

### Datasheet Completion

**Q**: Which sections are required?
**A**: All major sections should be completed:
- motivation, composition, collection
- ethics, preprocessing, uses
- distribution, maintenance, variables

**Q**: Can I skip sections if not applicable?
**A**: Yes, but document why:
```yaml
preprocessing:
  preprocessing_strategies:
    - description: "No preprocessing applied - raw data used directly"
```

---

## Next Steps

After successful migration:

1. **Publish Datasheets**: Host on accessible repository
2. **Update Documentation**: Reference migration in README
3. **Train Team**: Share benefits and usage patterns
4. **Automate**: Integrate validation in CI/CD
5. **Community**: Contribute examples back to repository

---

## Support and Resources

- **Integration Guide**: `INTEGRATION_GUIDE.md` - Technical integration patterns
- **Examples**: `src/data/examples/harmonized/` - Complete working examples
- **Utils README**: `utils/README.md` - Tool documentation
- **CLAUDE.md**: Repository guidance for Claude Code
- **Datasheets Schema**: https://github.com/bridge2ai/data-sheets-schema

---

## Appendix: Complete Migration Example

See `src/data/examples/harmonized/` for:
- `sentiment-classifier-with-datasheet-refs.yaml` - Migrated model card
- `imdb-sentiment-datasheet-v1.yaml` - Complete datasheet
- `README.md` - Usage guide

These examples demonstrate best practices for the integrated approach.

---

**Document Version**: 1.0
**Last Updated**: November 22, 2025
**Maintainers**: Model Card Schema Team
**Feedback**: Submit issues to repository
