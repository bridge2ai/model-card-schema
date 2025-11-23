# Harmonized Examples: Model Cards + Datasheets Integration

This directory contains examples demonstrating the integration of Model Cards with Datasheets for Datasets.

## Files

### 1. `sentiment-classifier-with-datasheet-refs.yaml`

**Complete model card using Pattern 1: External References**

This example shows the recommended approach for Phase 1 implementation:
- Uses the current Model Cards schema (`modelcards.yaml`)
- References external datasheets instead of importing the datasheets schema
- Avoids naming conflicts while providing comprehensive documentation

**Key Features**:
- ✅ Backward compatible with existing model cards schema
- ✅ No schema conflicts (Task, language, etc.)
- ✅ Clean separation: models documented in model cards, datasets in datasheets
- ✅ Single source of truth: datasets documented once, referenced many times

**Integration Approach**:
```yaml
# In model card: reference external datasheet
dataset_documentation:
  training_datasets:
    - id: "imdb-sentiment-v1"
      datasheet_url: "https://datasheets.example.org/imdb-sentiment-v1.yaml"
      datasheet_format: "datasheets-for-datasets-v1.0"
```

### 2. `imdb-sentiment-datasheet-v1.yaml`

**Complete dataset documentation using Datasheets for Datasets schema**

This example demonstrates comprehensive dataset documentation following the Datasheets for Datasets framework.

**Sections Documented**:
- **Motivation**: Purpose, tasks, creators, funding
- **Composition**: 50,000 instances, balanced positive/negative, subsets
- **Collection**: Web scraping methodology, sampling strategy, timeframes
- **Ethics**: Public data, no PII, ethical review notes
- **Preprocessing**: HTML cleaning, label derivation, normalization
- **Uses**: Existing uses (1000+ citations), discouraged uses, impact analysis
- **Distribution**: Format, dates, licensing
- **Maintenance**: Maintainers, update policy, version access
- **Variables**: review_text, sentiment, review_id descriptions

**Key Features**:
- ✅ Comprehensive: 60+ fields vs model cards' simple 7-field `dataSet` class
- ✅ Standardized: Follows established "Datasheets for Datasets" framework
- ✅ Reusable: Multiple models can reference this single datasheet
- ✅ Ethics-focused: Detailed privacy, consent, and ethical documentation

## Integration Pattern Comparison

### Pattern 1: External References (Recommended - Used in these examples)

**Pros**:
- No schema conflicts
- Works with current tooling
- Clean separation of concerns
- Datasets documented once, referenced many times

**Cons**:
- Requires maintaining separate files
- Less convenient for quick prototyping

**Use When**:
- Production deployment
- Multiple models using same datasets
- Need for comprehensive dataset documentation

### Pattern 2: Embedded Info (Backward Compatible)

**Pros**:
- Single file
- Quick and simple
- Backward compatible

**Cons**:
- Limited dataset documentation (only 7 fields)
- Duplication across model cards
- No standardized format

**Use When**:
- Quick prototyping
- Simple use cases
- Datasets are not reused

### Pattern 3: Full Import (Future - Phase 2+)

**Pros**:
- Full schema integration
- Type checking and validation
- Rich IDE support

**Cons**:
- Requires resolving naming conflicts
- More complex tooling
- Not yet fully implemented

**Use When**:
- After naming conflicts resolved (Phase 2+)
- Need for strict validation
- Building advanced tooling

## Usage

### Viewing the Model Card

```bash
# View the model card
cat sentiment-classifier-with-datasheet-refs.yaml

# Key sections to review:
# - model_details: Basic model information
# - model_parameters.data: Minimal dataset info with datasheet reference
# - dataset_documentation: External datasheet references
# - quantitative_analysis: Performance metrics
# - considerations: Ethics, limitations, use cases
```

### Viewing the Corresponding Datasheet

```bash
# View the datasheet
cat imdb-sentiment-datasheet-v1.yaml

# Key sections to review:
# - motivation: Why the dataset was created
# - composition: What's in the dataset (50K reviews, balanced)
# - collection: How data was collected (web scraping)
# - ethics: Ethical considerations (public data, no PII)
# - uses: Known uses, discouraged uses, impact analysis
```

### Integration Workflow

1. **Create Dataset Datasheet** (once per dataset):
   ```bash
   # Copy template
   cp imdb-sentiment-datasheet-v1.yaml my-dataset-datasheet.yaml

   # Edit to document your dataset
   # Fill in all sections: motivation, composition, collection, etc.
   ```

2. **Reference in Model Card** (for each model):
   ```yaml
   dataset_documentation:
     training_datasets:
       - id: "my-dataset-v1"
         datasheet_url: "https://datasheets.example.org/my-dataset-v1.yaml"
         datasheet_format: "datasheets-for-datasets-v1.0"
   ```

3. **Publish Both Files**:
   - Model card → Model repository/registry
   - Datasheet → Dataset repository/registry

## Validation

These examples follow the current Model Cards schema and Datasheets schema respectively:

```bash
# Validate model card (uses modelcards.yaml schema)
linkml-validate -s src/linkml/modelcards.yaml \
  src/data/examples/harmonized/sentiment-classifier-with-datasheet-refs.yaml

# Validate datasheet (would use datasheets schema - not shown here)
linkml-validate -s /path/to/data-sheets-schema/schema/data_sheets_schema_all.yaml \
  src/data/examples/harmonized/imdb-sentiment-datasheet-v1.yaml
```

## Migration Path

### From Simple Model Cards

**Before** (current simple approach):
```yaml
model_parameters:
  data:
    - name: "IMDb"
      link: "https://example.com"
      description: "Movie reviews"
```

**After** (with datasheet reference):
```yaml
model_parameters:
  data:
    - name: "IMDb Movie Reviews"
      link: "https://ai.stanford.edu/~amaas/data/sentiment/"
      description: "50,000 highly polar movie reviews"

dataset_documentation:
  training_datasets:
    - id: "imdb-sentiment-v1"
      datasheet_url: "https://datasheets.example.org/imdb-sentiment-v1.yaml"
```

**Then**: Create the corresponding datasheet file with comprehensive documentation.

## Benefits of This Approach

### For ML Practitioners
- **Comprehensive Documentation**: 60+ fields vs 7 fields
- **Reusability**: Document dataset once, reference in many model cards
- **Standards Compliance**: Follows established Datasheets framework
- **No Breaking Changes**: Works with existing model cards schema

### For Organizations
- **Governance**: Clear audit trail for datasets
- **Compliance**: Better support for GDPR, CCPA, ethics requirements
- **Efficiency**: Reduce documentation duplication
- **Transparency**: Comprehensive dataset documentation for stakeholders

### For Researchers
- **Reproducibility**: Detailed methodology documentation
- **Attribution**: Proper creator attribution with ORCID
- **Impact Analysis**: Documented uses, limitations, ethical considerations
- **Interoperability**: Standard format for dataset documentation

## Next Steps

See `INTEGRATION_GUIDE.md` in the repository root for:
- Detailed integration patterns
- Naming conflict resolution strategy
- Phase-by-phase implementation roadmap
- Migration tools and utilities

## References

- **Integration Guide**: `/INTEGRATION_GUIDE.md`
- **Alignment Analysis**: `/ALIGNMENT_ANALYSIS.md`
- **Model Cards Schema**: `/src/linkml/modelcards.yaml`
- **Harmonized Schema (conceptual)**: `/src/linkml/modelcards_harmonized.yaml`
- **Datasheets Schema**: https://github.com/bridge2ai/data-sheets-schema

## Questions?

See `CLAUDE.md` in the repository root for comprehensive guidance on working with this repository.
