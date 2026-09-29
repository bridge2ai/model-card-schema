# Datasheets for Datasets (D4D) Harmonization Guide

**Version**: 1.0
**Status**: Phase 1 COMPLETED
**Date**: November 23, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Why D4D Harmonization?](#why-d4d-harmonization)
3. [Quick Start](#quick-start)
4. [Key Concepts](#key-concepts)
5. [Schema Comparison](#schema-comparison)
6. [Migration Guide](#migration-guide)
7. [Examples](#examples)
8. [Best Practices](#best-practices)
9. [FAQ](#faq)
10. [References](#references)

---

## Overview

The **D4D Harmonized Model Card Schema** integrates Model Cards with [Datasheets for Datasets](https://github.com/bridge2ai/data-sheets-schema) to provide comprehensive documentation for machine learning models, their creators, and the datasets used to train them.

### What's New

The D4D harmonized schema (`model_card_schema_d4dharmonized.yaml`) extends the base Model Card schema with:

- **CreatorReference**: Link to comprehensive creator documentation (replaces simple `owner` and `Contributor` classes)
- **DatasetReference**: Link to comprehensive dataset documentation (replaces simple `dataSet` class with 7 fields)
- **GrantReference**: Link to detailed funding documentation (replaces simple `funding_source` string)
- **Provenance Metadata**: Track who created/modified model cards and when

### Integration Approach

The harmonization uses the **external reference pattern**:
- Model cards reference external D4D instances via URLs
- D4D instances are documented separately using the full Datasheets schema
- **No schema imports** - avoids naming conflicts
- **Clean separation of concerns** - each schema focused on its domain

---

## Why D4D Harmonization?

### The Problem

The base Model Card schema has **minimal dataset documentation**:

```yaml
# Base schema: Simple dataSet class (7 fields)
data:
  - name: IMDb Reviews
    description: Movie reviews dataset
    link: https://example.org/imdb
    sensitive:
      sensitive_data:
        - names
        - email addresses
    graphics: [some visualization]
    bias_input: "English language bias"
    unit: "reviews"
```

**Limitations**:
- No information about how data was collected
- No composition details (instance counts, data types, variables)
- No preprocessing or data cleaning documentation
- No privacy/ethics analysis beyond simple PII list
- No distribution, licensing, or maintenance information
- No creator attribution

### The Solution

The D4D harmonized schema links to **comprehensive dataset documentation** (60+ classes, 200+ fields):

```yaml
# D4D harmonized schema: DatasetReference
training_datasets:
  - url: file://./datasets/imdb-dataset.yaml
    description: Primary training data
```

Where `imdb-dataset.yaml` is a complete Datasheets for Datasets instance documenting:
- **Motivation**: Why created, who created it, funding
- **Composition**: Instance counts, data types, variables, missing data handling
- **Collection**: How collected, sampling strategy, ethical review
- **Preprocessing**: Cleaning procedures, transformations, data splits
- **Uses**: Recommended and unsuitable use cases
- **Privacy & Ethics**: Personal data, sensitive data, fairness concerns, mitigation strategies
- **Distribution**: Access methods, formats, license
- **Maintenance**: Who maintains it, update frequency, retention plan
- **Provenance**: Version history, citations, DOIs

### Benefits

| Aspect | Base Schema | D4D Harmonized Schema |
|--------|-------------|----------------------|
| **Dataset docs** | 7 fields | 200+ fields (60+ classes) |
| **Creator attribution** | Name + contact | ORCID, CRediT roles, affiliations, publications |
| **Funding** | String | Grant ID, funder, PI, amount, period, objectives |
| **Privacy/Ethics** | Simple PII list | Comprehensive privacy analysis, fairness concerns, mitigation strategies |
| **Provenance** | None | Created/modified by, timestamps |
| **Reusability** | Low | High (dataset documented once, referenced many times) |

---

## Quick Start

### 1. Choose Your Schema

**Use D4D Harmonized Schema if**:
- You need comprehensive dataset documentation
- You want rich creator attribution (ORCID, CRediT roles)
- You need to track funding sources in detail
- You care about privacy, ethics, and fairness documentation
- You want provenance tracking

**Use Base Schema if**:
- You need simple, lightweight model cards
- Minimal dataset documentation is sufficient
- You don't need creator attribution beyond name/contact

### 2. Create a Model Card

```yaml
# my-model-card.yaml
schema_version: d4d-1.0

# Provenance metadata (NEW)
created_by: Your Name
modified_by: Your Name
created_on: 2025-01-23T10:00:00Z
modified_on: 2025-01-23T10:00:00Z

model_details:
  name: My Awesome Model

  # Link to D4D Creator instances (NEW)
  creator_references:
    - url: file://./creators/my-creator.yaml
      description: Principal Investigator

model_parameters:
  # Link to D4D Dataset instances (NEW)
  training_datasets:
    - url: file://./datasets/my-training-dataset.yaml
      description: Primary training data

mission_relevance:
  # Link to D4D Grant instances (NEW)
  funding_grants:
    - url: file://./grants/my-grant.yaml
      description: Primary funding source
```

### 3. Document Your Resources

Create D4D instances for creators, datasets, and grants (see [Examples](#examples) section).

---

## Key Concepts

### CreatorReference

Links to a Datasheets for Datasets **Creator** instance (Person or Organization).

**What it provides**:
- ORCID identifiers for researchers
- CRediT roles for contribution attribution (14 standardized types)
- Institutional affiliations
- Contact information
- Publications and expertise
- Professional details

**Example**:
```yaml
creator_references:
  - url: file://./creators/jane-smith.yaml
    description: Principal Investigator and Lead Developer
  - url: https://orcid.org/0000-0001-2345-6789
    description: Co-investigator (via ORCID)
```

### DatasetReference

Links to a Datasheets for Datasets **Dataset** instance.

**What it provides** (60+ classes, 200+ fields):
- Motivation (purpose, creators, funding)
- Composition (instances, types, variables, missing data)
- Collection (methodology, sampling, ethics)
- Preprocessing (cleaning, transformations, splits)
- Uses (recommended/unsuitable uses)
- Privacy & Ethics (sensitive data, fairness, mitigation)
- Distribution (access, formats, license)
- Maintenance (maintainer, updates, retention)

**Example**:
```yaml
training_datasets:
  - url: file://./datasets/noaa-climate-data.yaml
    description: 50 years of NOAA climate observations

evaluation_datasets:
  - url: https://datasheets.example.org/benchmark-dataset
    description: Standardized evaluation benchmark
```

### GrantReference

Links to a Datasheets for Datasets **Grant** instance.

**What it provides**:
- Grant ID, title, program
- Funder organization
- Principal investigator(s) with ORCID
- Funding amount, currency, duration
- Budget breakdown
- Project abstract and objectives
- Related publications and data products

**Example**:
```yaml
funding_grants:
  - url: file://./grants/nsf-award-12345.yaml
    description: NSF CAREER Award - Primary funding
  - url: file://./grants/doe-scidac-grant.yaml
    description: DOE SciDAC supplemental funding
```

### Provenance Metadata

Track creation and modification of model cards.

**Available at two levels**:
1. **modelCard root** - Tracks the model card document itself
2. **ModelDetails** - Tracks the model metadata

**Fields**:
- `created_by`: Name or identifier of creator
- `modified_by`: Name or identifier of last modifier
- `created_on`: Creation timestamp (ISO 8601)
- `modified_on`: Last modification timestamp (ISO 8601)

**Example**:
```yaml
# At modelCard root level
created_by: Jane Smith
modified_by: John Doe
created_on: 2025-01-15T10:00:00Z
modified_on: 2025-01-20T14:30:00Z

model_details:
  # At ModelDetails level
  created_by: Jane Smith
  created_on: 2025-01-15T10:00:00Z
  modified_by: Jane Smith
  modified_on: 2025-01-15T10:00:00Z
```

---

## Schema Comparison

### Deprecated in D4D Schema

The following classes are **removed** in the D4D harmonized schema:

| Deprecated Class | Replaced By | Reason |
|-----------------|-------------|--------|
| `owner` | `CreatorReference` | Simple name+contact → comprehensive creator documentation |
| `Contributor` | `CreatorReference` | Role enum → D4D CRediT roles (14 standardized types) |
| `ContributorRoleEnum` | D4D CRediT roles | Limited roles → comprehensive contribution taxonomy |
| `dataSet` | `DatasetReference` | 7 fields → 200+ fields via D4D Dataset |
| `SensitiveData` | D4D Dataset privacy section | Simple PII list → comprehensive privacy/ethics analysis |

### New in D4D Schema

| New Class | Purpose | Fields |
|-----------|---------|--------|
| `CreatorReference` | Link to D4D Creator | url (required), description (optional) |
| `DatasetReference` | Link to D4D Dataset | url (required), description (optional) |
| `GrantReference` | Link to D4D Grant | url (required), description (optional) |

### Updated Classes

| Class | Changes |
|-------|---------|
| `ModelDetails` | Removed: `owners`, `contributors`<br>Added: `creator_references`, `created_by`, `modified_by`, `created_on`, `modified_on` |
| `ModelParameters` | Removed: `data`<br>Added: `training_datasets`, `evaluation_datasets` |
| `MissionRelevance` | Removed: `funding_source`<br>Added: `funding_grants` |
| `modelCard` (root) | Added: `created_by`, `modified_by`, `created_on`, `modified_on` |

---

## Migration Guide

### Step 1: Assess Your Current Model Card

Identify fields that need migration:

```yaml
# OLD: Base schema
model_details:
  owners:
    - name: Jane Smith
      contact: jane@example.org

  contributors:
    - name: Jane Smith
      role: developed_by
      email: jane@example.org
      orcid: https://orcid.org/0000-0001-2345-6789

model_parameters:
  data:
    - name: My Training Dataset
      description: Training data description
      link: https://example.org/dataset
      sensitive:
        sensitive_data:
          - names
          - email addresses

mission_relevance:
  funding_source: "NSF Award 12345"
```

### Step 2: Create D4D Instances

#### Creator Instance

Create `creators/jane-smith.yaml`:

```yaml
# Simulated D4D Creator (Person)
creator_type: Person

personal_information:
  name: Jane Smith
  email: jane@example.org
  orcid: https://orcid.org/0000-0001-2345-6789

affiliation:
  organization: Example University
  department: Computer Science

roles:
  # CRediT roles
  - role: Conceptualization
  - role: Methodology
  - role: Software
  - role: Investigation
  - role: Writing - Original Draft

provenance:
  created_on: 2025-01-23T10:00:00Z
  created_by: Jane Smith
```

#### Dataset Instance

Create `datasets/my-training-dataset.yaml`:

```yaml
# Simulated D4D Dataset
dataset_name: My Training Dataset
dataset_version: v1.0
dataset_url: https://example.org/dataset

# Motivation
motivation:
  purpose: Dataset for training my model
  creators:
    - name: Jane Smith

# Composition
composition:
  instance_count: 100000
  data_types:
    - type: text
      description: User-generated text

  variables:
    - name: text
      description: Input text
      type: string
    - name: label
      description: Classification label
      type: categorical

# Privacy
privacy:
  contains_personal_data: true
  contains_sensitive_data: true
  privacy_measures: |-
    Names and email addresses were anonymized using hashing.
    All PII was removed or masked before dataset release.

  sensitive_data_types:
    - PII: names, email addresses
    - Handling: Hashed and anonymized

# Distribution
distribution:
  license: CC-BY-4.0
  download_url: https://example.org/dataset/download

# (Include other D4D sections as needed)
```

#### Grant Instance

Create `grants/nsf-award-12345.yaml`:

```yaml
# Simulated D4D Grant
grant_information:
  grant_id: NSF-12345
  grant_title: "My Research Project"
  program: NSF CAREER Award

funder:
  organization: National Science Foundation
  division: CISE
  country: United States

principal_investigator:
  name: Jane Smith
  orcid: https://orcid.org/0000-0001-2345-6789

funding_details:
  amount: 500000
  currency: USD
  duration: 5 years
  period:
    start_date: 2020-01-01
    end_date: 2025-12-31
```

### Step 3: Update Model Card

Create `my-model-card-d4d.yaml`:

```yaml
# NEW: D4D harmonized schema
schema_version: d4d-1.0

# NEW: Provenance
created_by: Jane Smith
modified_by: Jane Smith
created_on: 2025-01-23T10:00:00Z
modified_on: 2025-01-23T10:00:00Z

model_details:
  name: My Awesome Model

  # NEW: CreatorReference (replaces owners/contributors)
  creator_references:
    - url: file://./creators/jane-smith.yaml
      description: Principal Investigator and Lead Developer

  # NEW: Provenance at ModelDetails level
  created_by: Jane Smith
  created_on: 2025-01-23T10:00:00Z

model_parameters:
  # NEW: DatasetReference (replaces data)
  training_datasets:
    - url: file://./datasets/my-training-dataset.yaml
      description: Primary training data

mission_relevance:
  # NEW: GrantReference (replaces funding_source)
  funding_grants:
    - url: file://./grants/nsf-award-12345.yaml
      description: Primary funding - NSF CAREER Award
```

---

## Examples

Complete examples are available in `src/data/examples/d4d_integration/`:

### Climate Forecasting Example

**Model Card**: `climate-forecasting-model-card.yaml`
- Demonstrates all D4D harmonization features
- References 2 Creator instances (Person + Organization)
- References 2 Dataset instances (training + evaluation)
- References 2 Grant instances (DOE SciDAC + NSF)
- Includes provenance metadata
- Preserves all DOE Extended Template features

**Creator Instances**:
- `creators/jane-smith-creator.yaml` (Person with ORCID, CRediT roles)
- `creators/climate-ai-lab-creator.yaml` (Organization with ROR)

**Dataset Instance**:
- `datasets/noaa-historical-climate-dataset.yaml` (comprehensive 200+ fields)

**Grant Instance**:
- `grants/doe-scidac-grant.yaml` (DOE funding with PI, budget, objectives)

**README**: `src/data/examples/d4d_integration/README.md`
- Complete usage guide
- Migration examples
- Validation instructions

---

## Best Practices

### 1. URL Patterns

**Local file references** (relative paths):
```yaml
url: file://./creators/jane-smith.yaml
url: file://./datasets/my-dataset.yaml
url: file://../grants/my-grant.yaml
```

**Web references**:
```yaml
url: https://datasheets.example.org/creators/jane-smith
url: https://github.com/org/repo/blob/main/datasets/dataset.yaml
```

**Persistent identifiers**:
```yaml
url: https://orcid.org/0000-0001-2345-6789  # ORCID for creators
url: https://doi.org/10.1234/dataset-doi  # DOI for datasets
```

### 2. Provenance Tracking

**Always include provenance at both levels**:

```yaml
# Root level (model card document)
created_by: Jane Smith
modified_by: John Doe
created_on: 2025-01-15T10:00:00Z
modified_on: 2025-01-20T14:30:00Z

model_details:
  # ModelDetails level (model metadata)
  created_by: Jane Smith
  modified_by: Jane Smith
  created_on: 2025-01-15T10:00:00Z
  modified_on: 2025-01-15T10:00:00Z
```

**Use ISO 8601 timestamps**:
- `2025-01-23T10:00:00Z` (UTC)
- `2025-01-23T10:00:00-05:00` (with timezone offset)

### 3. Creator Attribution

**Use CreatorReference for ALL contributors**:

```yaml
creator_references:
  - url: file://./creators/pi-creator.yaml
    description: Principal Investigator
  - url: file://./creators/postdoc-creator.yaml
    description: Lead Developer
  - url: https://orcid.org/0000-0002-3456-7890
    description: Co-investigator (via ORCID)
  - url: file://./creators/institution-creator.yaml
    description: Host institution
```

**Document CRediT roles in Creator instances**:
- Conceptualization
- Methodology
- Software
- Validation
- Formal Analysis
- Investigation
- Resources
- Data Curation
- Writing - Original Draft
- Writing - Review & Editing
- Visualization
- Supervision
- Project Administration
- Funding Acquisition

### 4. Dataset Documentation

**Separate training and evaluation datasets**:

```yaml
training_datasets:
  - url: file://./datasets/training-data.yaml
    description: Primary training data (100K examples)
  - url: file://./datasets/augmented-data.yaml
    description: Augmented training data (50K synthetic examples)

evaluation_datasets:
  - url: file://./datasets/validation-data.yaml
    description: Validation set (10K examples)
  - url: file://./datasets/test-data.yaml
    description: Held-out test set (10K examples)
  - url: https://benchmark.org/extreme-cases
    description: Extreme weather benchmark (1K events)
```

**Document all D4D sections** (motivation, composition, collection, preprocessing, uses, privacy, distribution, maintenance).

### 5. Funding Transparency

**Reference all funding sources**:

```yaml
funding_grants:
  - url: file://./grants/nsf-primary.yaml
    description: Primary funding - NSF CAREER Award
  - url: file://./grants/doe-supplemental.yaml
    description: Supplemental funding - DOE SciDAC
  - url: file://./grants/industry-gift.yaml
    description: Google Research Gift
```

---

## FAQ

### Q: Do I need to use the D4D harmonized schema?

**A**: No. The base schema (`model_card_schema.yaml`) remains fully supported. Use the D4D harmonized schema when you need comprehensive dataset/creator documentation or provenance tracking.

### Q: Can I use ORCID URLs directly as creator references?

**A**: Yes! ORCID is a persistent identifier for researchers:

```yaml
creator_references:
  - url: https://orcid.org/0000-0001-2345-6789
    description: Co-investigator (via ORCID)
```

The ORCID profile provides basic creator information. For richer documentation, create a full D4D Creator instance.

### Q: What if my dataset doesn't have all D4D fields?

**A**: Document what you can. Mark unknown sections with TODO:

```yaml
# datasets/my-partial-dataset.yaml
dataset_name: My Dataset

motivation:
  purpose: Training data for my model
  creators:
    - name: Jane Smith

composition:
  # TODO: Add instance counts and variable definitions

collection:
  # TODO: Document collection methodology

# ... other sections
```

### Q: Can I mix local files and web URLs?

**A**: Yes! Use whatever references are appropriate:

```yaml
creator_references:
  - url: file://./creators/local-creator.yaml
    description: Local creator doc
  - url: https://orcid.org/0000-0001-2345-6789
    description: ORCID profile
  - url: https://datasheets.example.org/creators/web-creator
    description: Published creator doc
```

### Q: How do I validate my D4D harmonized model card?

**A**: Use LinkML validator:

```bash
# Validate model card
poetry run linkml-validate \
  -s src/model_card_schema/schema/model_card_schema_d4dharmonized.yaml \
  my-model-card.yaml
```

For D4D instances (Creator, Dataset, Grant), validate against the Datasheets schema:

```bash
# Clone datasheets schema if needed
git clone https://github.com/bridge2ai/data-sheets-schema

# Validate D4D instances
poetry run linkml-validate \
  -s /path/to/data-sheets-schema/src/data_sheets_schema/schema/data_sheets_schema.yaml \
  creators/my-creator.yaml
```

### Q: Are there tools to help with migration?

**A**: Currently, migration is manual following this guide. Automated migration tools may be added in future phases.

### Q: What about the old `modelcards_harmonized.yaml`?

**A**: That was a conceptual design that attempted schema imports and encountered naming conflicts. It has been deprecated in favor of the production D4D harmonized schema (`model_card_schema_d4dharmonized.yaml`) using the external reference pattern.

---

## References

### Documentation

- **INTEGRATION_GUIDE.md**: Technical integration guide with implementation details
- **ALIGNMENT_ANALYSIS.md**: Comprehensive 50,000+ word schema comparison analysis
- **CLAUDE.md**: Repository guide with D4D harmonization section
- **src/data/examples/d4d_integration/README.md**: Complete usage guide for examples

### Schemas

- **model_card_schema_d4dharmonized.yaml**: D4D harmonized schema (`src/model_card_schema/schema/`)
- **model_card_schema.yaml**: Base schema without D4D integration (`src/model_card_schema/schema/`)
- **Datasheets for Datasets Schema**: https://github.com/bridge2ai/data-sheets-schema

### Examples

- **Climate Model Card**: `src/data/examples/d4d_integration/climate-forecasting-model-card.yaml`
- **Creator Examples**: `src/data/examples/d4d_integration/creators/`
- **Dataset Example**: `src/data/examples/d4d_integration/datasets/noaa-historical-climate-dataset.yaml`
- **Grant Example**: `src/data/examples/d4d_integration/grants/doe-scidac-grant.yaml`

### Papers and Resources

- **Model Cards for Model Reporting**: Mitchell et al., 2019 - https://arxiv.org/abs/1810.03993
- **Datasheets for Datasets**: Gebru et al., 2018 - https://arxiv.org/abs/1803.09010
- **Google Model Card Toolkit**: https://github.com/tensorflow/model-card-toolkit
- **LinkML Documentation**: https://linkml.io/
- **CRediT Taxonomy**: https://credit.niso.org/
- **ORCID**: https://orcid.org/

---

## Support

### Questions or Issues?

- **Model Card schema issues**: https://github.com/bridge2ai/model-card-schema/issues
- **Datasheets schema issues**: https://github.com/bridge2ai/data-sheets-schema/issues
- **Integration questions**: See INTEGRATION_GUIDE.md

### Contributing

We welcome contributions! Areas for future work:
- Automated migration tools
- Validation utilities
- Additional examples
- Documentation improvements

---

**Last Updated**: November 23, 2025
**Status**: Production Ready
**License**: MIT (Model Card schema), CC0 1.0 Universal (Datasheets schema - check repository for current license)
