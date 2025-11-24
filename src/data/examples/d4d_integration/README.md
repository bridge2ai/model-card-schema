# D4D Integration Examples

This directory contains examples demonstrating the **Datasheets for Datasets (D4D) harmonization** approach for Model Cards using the **external reference pattern**.

## Overview

The Model Card schema has been harmonized with the [Datasheets for Datasets schema](https://github.com/bridge2ai/data-sheets-schema) to provide comprehensive documentation for:

- **Creators** (people and organizations) - Replaces simple `owner` and `Contributor` classes
- **Datasets** - Replaces simple `dataSet` class (7 fields → 60+ classes, 200+ fields)
- **Funding** - Replaces simple `funding_source` string with structured Grant instances

## Integration Pattern: External References

This approach **avoids schema imports** and naming conflicts by:

1. Model cards reference external D4D instances via URLs
2. D4D instances are documented separately using the full Datasheets schema
3. No schema conflicts, clean separation of concerns
4. Backward compatible with existing tools

## Directory Structure

```
d4d_integration/
├── README.md (this file)
├── climate-forecasting-model-card.yaml  # Model card using D4D harmonized schema
├── creators/
│   ├── jane-smith-creator.yaml          # D4D Creator instance (Person)
│   └── climate-ai-lab-creator.yaml      # D4D Creator instance (Organization)
├── datasets/
│   └── noaa-historical-climate-dataset.yaml  # D4D Dataset instance
└── grants/
    └── doe-scidac-grant.yaml            # D4D Grant instance
```

## Files

### 1. Model Card (D4D Harmonized Schema)

**File**: `climate-forecasting-model-card.yaml`

**Schema**: Uses `model_card_schema_d4dharmonized.yaml`

**Key D4D Features**:

```yaml
schema_version: d4d-1.0

# NEW: Provenance metadata at root level
created_by: Jane Smith
modified_by: Jane Smith
created_on: 2025-01-15T10:00:00Z
modified_on: 2025-01-20T14:30:00Z

model_details:
  # NEW: References to D4D Creator instances (replaces owners/contributors)
  creator_references:
    - url: file://./creators/jane-smith-creator.yaml
      description: Principal Investigator and Lead Developer
    - url: file://./creators/climate-ai-lab-creator.yaml
      description: Research organization

  # NEW: Provenance metadata at ModelDetails level
  created_by: Jane Smith
  created_on: 2025-01-15T10:00:00Z
  modified_by: Jane Smith
  modified_on: 2025-01-20T14:30:00Z

model_parameters:
  # NEW: References to D4D Dataset instances (replaces simple data field)
  training_datasets:
    - url: file://./datasets/noaa-historical-climate-dataset.yaml
      description: Primary training data - 50 years of NOAA climate observations

  evaluation_datasets:
    - url: file://./datasets/noaa-test-dataset.yaml
      description: Held-out test set - 2020-2024 observations

mission_relevance:
  # NEW: References to D4D Grant instances (replaces funding_source string)
  funding_grants:
    - url: file://./grants/doe-scidac-grant.yaml
      description: Primary funding - DOE SciDAC Climate Modeling
```

### 2. D4D Creator Instances

**Files**:
- `creators/jane-smith-creator.yaml` (Person)
- `creators/climate-ai-lab-creator.yaml` (Organization)

**Schema**: Datasheets for Datasets Creator schema

**Key Features**:
- ORCID identifiers for researchers
- CRediT roles for contribution attribution
- Institutional affiliations
- Contact information
- Publications and expertise

**Example (Person)**:

```yaml
creator_type: Person

personal_information:
  name: Jane Smith
  email: jane.smith@climatelab.org
  orcid: https://orcid.org/0000-0001-2345-6789

affiliation:
  organization: Climate AI Research Laboratory
  department: Atmospheric Sciences

roles:
  - role: Conceptualization
  - role: Methodology
  - role: Software
  - role: Investigation
```

### 3. D4D Dataset Instance

**File**: `datasets/noaa-historical-climate-dataset.yaml`

**Schema**: Datasheets for Datasets Dataset schema

**Key Sections** (simplified - full schema has 60+ classes):

- **Motivation**: Why the dataset was created, who created it, funding
- **Composition**: Instance counts, data types, variables, missing data
- **Collection**: How data was collected, sampling strategy, ethical review
- **Preprocessing**: Cleaning procedures, transformations, data splits
- **Uses**: Recommended and unsuitable use cases
- **Privacy & Ethics**: Personal data, sensitive data, fairness concerns
- **Distribution**: Access methods, formats, license
- **Maintenance**: Who maintains it, update frequency, retention plan

**Example**:

```yaml
dataset_name: NOAA Historical Climate Observations (North America)
dataset_version: v3.2.1

motivation:
  purpose: Provide high-quality surface weather observations for climate research
  creators:
    - name: NOAA National Centers for Environmental Information

composition:
  instance_count: 438000000
  temporal_coverage:
    start_date: 1970-01-01
    end_date: 2024-12-31
    resolution: Hourly

  variables:
    - name: temperature
      unit: Celsius
      type: float
      range: [-50.0, 50.0]

privacy:
  contains_personal_data: false
  contains_sensitive_data: false

distribution:
  license: CC0 1.0 Universal (Public Domain)
  download_url: https://www.ncei.noaa.gov/isd
```

### 4. D4D Grant Instance

**File**: `grants/doe-scidac-grant.yaml`

**Schema**: Datasheets for Datasets Grant schema

**Key Features**:
- Grant ID, title, program
- Funder information
- Principal investigator(s)
- Funding amount and period
- Project abstract and objectives
- DOE relevance and facilities
- Related publications and data products

**Example**:

```yaml
grant_information:
  grant_id: DE-SC0012345
  grant_title: "Scientific Discovery through Advanced Computing: Climate AI at Exascale"
  program: DOE Office of Science - SciDAC

funder:
  organization: U.S. Department of Energy
  division: Office of Science

principal_investigator:
  name: Dr. Jane Smith
  orcid: https://orcid.org/0000-0001-2345-6789

funding_details:
  amount: 2500000
  currency: USD
  duration: 3 years

doe_relevance:
  mission_area:
    - Climate and environmental sciences
    - Advanced scientific computing
  doe_facilities_used:
    - OLCF Frontier
    - ALCF Polaris
```

## Usage Workflow

### 1. Create D4D Instances First

Before creating your model card, document your resources using the Datasheets schema:

```bash
# Document creators (people and organizations)
# Use full D4D Creator schema
vim creators/my-researcher-creator.yaml
vim creators/my-lab-creator.yaml

# Document datasets comprehensively
# Use full D4D Dataset schema with all sections
vim datasets/my-training-dataset.yaml
vim datasets/my-evaluation-dataset.yaml

# Document funding sources
# Use full D4D Grant schema
vim grants/my-grant.yaml
```

### 2. Create Model Card with References

Create your model card using the D4D harmonized schema:

```bash
vim my-model-card.yaml
```

Reference the D4D instances you created:

```yaml
schema_version: d4d-1.0

model_details:
  creator_references:
    - url: file://./creators/my-researcher-creator.yaml
      description: Principal Investigator

model_parameters:
  training_datasets:
    - url: file://./datasets/my-training-dataset.yaml
      description: Primary training data

mission_relevance:
  funding_grants:
    - url: file://./grants/my-grant.yaml
      description: Primary funding source
```

### 3. URL Patterns for References

**Local file references** (relative paths):

```yaml
url: file://./creators/jane-smith-creator.yaml
url: file://./datasets/my-dataset.yaml
url: file://../other-directory/grant.yaml
```

**Web references**:

```yaml
url: https://datasheets.example.org/creators/jane-smith
url: https://github.com/org/repo/blob/main/datasets/dataset.yaml
url: https://doi.org/10.1234/dataset-doi  # Dataset DOI
```

**ORCID references** (for creators):

```yaml
url: https://orcid.org/0000-0001-2345-6789
description: Co-investigator (via ORCID profile)
```

## Validation

### Validate Model Card

```bash
# Using LinkML validator
poetry run linkml-validate \
  -s src/model_card_schema/schema/model_card_schema_d4dharmonized.yaml \
  src/data/examples/d4d_integration/climate-forecasting-model-card.yaml
```

### Validate D4D Instances

```bash
# Note: Requires data-sheets-schema repository
# Clone if not available: git clone https://github.com/bridge2ai/data-sheets-schema

# Validate Creator
poetry run linkml-validate \
  -s /path/to/data-sheets-schema/src/data_sheets_schema/schema/data_sheets_schema.yaml \
  creators/jane-smith-creator.yaml

# Validate Dataset
poetry run linkml-validate \
  -s /path/to/data-sheets-schema/src/data_sheets_schema/schema/data_sheets_schema.yaml \
  datasets/noaa-historical-climate-dataset.yaml

# Validate Grant
poetry run linkml-validate \
  -s /path/to/data-sheets-schema/src/data_sheets_schema/schema/data_sheets_schema.yaml \
  grants/doe-scidac-grant.yaml
```

## Migration from Base Schema

### Migrating from Old Schema

If you have model cards using the base schema:

**Old schema (`model_card_schema.yaml`)**:

```yaml
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
    - name: My Dataset
      description: Training data
      link: https://example.org/dataset
      sensitive:
        sensitive_data:
          - names
          - addresses

mission_relevance:
  funding_source: "DOE Grant DE-SC0012345"
```

**New D4D harmonized schema**:

```yaml
model_details:
  creator_references:
    - url: file://./creators/jane-smith-creator.yaml
      description: Principal Investigator and Lead Developer

model_parameters:
  training_datasets:
    - url: file://./datasets/my-training-dataset.yaml
      description: Primary training data

mission_relevance:
  funding_grants:
    - url: file://./grants/doe-grant.yaml
      description: Primary funding - DOE SciDAC
```

### Migration Steps

1. **Extract Creator Information**:
   - Create D4D Creator instances for each owner/contributor
   - Include ORCID, affiliation, CRediT roles
   - Save as `creators/*.yaml`

2. **Expand Dataset Documentation**:
   - Create comprehensive D4D Dataset instances
   - Document all sections: motivation, composition, collection, preprocessing, uses, privacy, distribution, maintenance
   - Save as `datasets/*.yaml`

3. **Document Funding**:
   - Create D4D Grant instances for each funding source
   - Include grant ID, funder, PI, amount, period, objectives
   - Save as `grants/*.yaml`

4. **Update Model Card**:
   - Change `schema_version` to `d4d-1.0`
   - Replace `owners` → `creator_references`
   - Remove `contributors` (use `creator_references`)
   - Replace `data` → `training_datasets` and `evaluation_datasets`
   - Replace `funding_source` → `funding_grants`
   - Add provenance metadata (`created_by`, `modified_by`, `created_on`, `modified_on`)

## Benefits of D4D Integration

### For Simple Dataset Docs → Comprehensive Dataset Docs

**Before (7 fields)**:
```yaml
data:
  - name: My Dataset
    description: Brief description
    link: https://example.org/dataset
    sensitive: [some PII info]
    graphics: [some visualizations]
    bias_input: Known biases
    unit: measurement units
```

**After (60+ classes, 200+ fields)**:
- Motivation (why created, who created, funding)
- Composition (instance counts, data types, variables, missing data)
- Collection (how collected, sampling strategy, ethical review)
- Preprocessing (cleaning, transformations, splits)
- Uses (recommended/unsuitable uses, tasks)
- Privacy & Ethics (personal data, sensitive data, fairness, mitigation)
- Distribution (access, formats, license)
- Maintenance (maintainer, updates, retention)
- Provenance (version history, citations)

### For Simple Creator Info → Rich Creator Attribution

**Before**:
```yaml
owners:
  - name: Jane Smith
    contact: jane@example.org

contributors:
  - name: Jane Smith
    role: developed_by
```

**After (D4D Creator)**:
- ORCID identifiers
- CRediT roles (14 standardized contribution types)
- Institutional affiliations
- Publications and expertise
- Multiple contact methods
- Professional details

### For Simple Funding → Structured Grant Documentation

**Before**:
```yaml
funding_source: "DOE Grant DE-SC0012345"
```

**After (D4D Grant)**:
- Grant ID, title, program
- Funder organization hierarchy
- PI and co-investigators with ORCID
- Funding amount, currency, duration
- Budget breakdown
- Project abstract and objectives
- DOE relevance and facilities
- Related publications and data products

## Reference Documentation

- **Model Card D4D Harmonized Schema**: `src/model_card_schema/schema/model_card_schema_d4dharmonized.yaml`
- **Datasheets for Datasets Schema**: https://github.com/bridge2ai/data-sheets-schema
- **Integration Guide**: `INTEGRATION_GUIDE.md` (root directory)
- **D4D Harmonization Guide**: `D4D_HARMONIZATION.md` (root directory)
- **Alignment Analysis**: `ALIGNMENT_ANALYSIS.md` (root directory)

## Questions or Issues?

- **Model Card schema issues**: https://github.com/bridge2ai/model-card-schema/issues
- **Datasheets schema issues**: https://github.com/bridge2ai/data-sheets-schema/issues
- **Integration questions**: See `INTEGRATION_GUIDE.md` and `D4D_HARMONIZATION.md`

## License

- Model Card schema and examples: MIT License
- Datasheets for Datasets schema: CC0 1.0 Universal (check repository for current license)
