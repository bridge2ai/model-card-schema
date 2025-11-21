# Model Cards ↔ Datasheets for Datasets: Schema Alignment Analysis

**Date**: November 19, 2025
**Version**: 1.0
**Authors**: Schema Alignment Analysis Team

---

## Executive Summary

This document provides a comprehensive analysis of the alignment between two LinkML schemas:

- **Model Cards Schema** (source): ML model documentation schema integrating Google Model Card Toolkit v0.0.2, HuggingFace, and Papers with Code standards
- **Datasheets for Datasets Schema** (standard/target): Comprehensive dataset documentation following the "Datasheets for Datasets" framework

### Schema Overview

#### Model Cards Schema
- **Location**: `src/linkml/modelcards.yaml`
- **Purpose**: Document machine learning models with metadata for model details, training data, performance metrics, ethical considerations, and deployment specifications
- **Scope**: 27 classes covering model metadata, datasets, parameters, performance, considerations, and benchmarks
- **Size**: 967 lines
- **Design Philosophy**: Model-centric with dataset documentation support

#### Datasheets for Datasets Schema
- **Location**: `/Users/marcin/Documents/VIMSS/ontology/bridge2ai/data-sheets-schema/src/data_sheets_schema/schema/data_sheets_schema_all.yaml`
- **Purpose**: Comprehensive dataset documentation addressing motivation, composition, collection, preprocessing, uses, distribution, maintenance, ethics, and data governance
- **Scope**: 60+ classes organized into thematic subsets
- **Size**: 22,459 lines
- **Design Philosophy**: Dataset-centric with extensive ethical and governance coverage

### Key Findings

1. **Complementary, Not Conflicting**: The schemas address different primary concerns (models vs. datasets) with overlapping areas in dataset documentation, licensing, creators, and ethics.

2. **Alignment Strength Varies**:
   - **Strong alignment** (90%+): Basic metadata (name, description, id)
   - **Moderate alignment** (50-89%): Creators/ownership, licensing, versioning
   - **Weak alignment** (<50%): Dataset documentation, ethics/privacy, sensitive data

3. **Massive Gap in Dataset Documentation**: Model cards has 1 dataset class with 7 fields; datasheets has 60+ classes with 200+ fields for comprehensive dataset documentation.

4. **Harmonization is Highly Feasible**: Both use LinkML, have compatible patterns, and can be integrated through import/reference without breaking model-specific functionality.

### Recommendations Summary

**Critical Actions**:
1. Import datasheets schema into model cards
2. Replace `dataSet` class with datasheets `Dataset` reference
3. Replace `owner` class with datasheets `Creator`/`Person`/`Organization`
4. Reference datasheets ethics/privacy classes for training data
5. Adopt datasheets provenance metadata

**Impact**: Creates interoperable ecosystem where models reference comprehensive dataset documentation, eliminating duplication while maintaining model-specific capabilities.

---

## 1. Core Alignment Matrix

| Model Cards Element | Datasheets Element | Alignment | Notes |
|---------------------|-------------------|-----------|-------|
| **Basic Metadata** ||||
| `name` | `name` | ✅ Exact | Both use `schema:name` |
| `description` | `description` | ✅ Exact | Both use `schema:description` |
| `id` | `id` | ✅ Exact | Both use `schema:identifier` |
| `Version` class | `version` slot | 🟨 Close | MC has structured class; DS uses string |
| `schema_version` | (none) | ❌ Gap | MC tracks schema version |
| **Creators & Ownership** ||||
| `owner` class | `Person` + `Creator` + `Organization` | 🟨 Related | DS much more comprehensive |
| `owner.name` | `Person.name` + `Creator.principal_investigator` | 🟨 Related | DS distinguishes roles |
| `owner.contact` | `Person.email` + `Person.orcid` | 🟨 Close | DS has structured contact |
| (none) | `Person.affiliation` → `Organization` | ❌ Gap | DS tracks organizations |
| (none) | `Person.credit_roles` → `CRediTRoleEnum` | ❌ Gap | DS uses CRediT taxonomy |
| (none) | `FundingMechanism` + `Grantor` + `Grant` | ❌ Gap | DS documents funding |
| **Licensing** ||||
| `License.identifier` (SPDX) | `license` (string) | 🟨 Close | Both support identifiers |
| `License.custom_text` | `LicenseAndUseTerms.description` | 🟨 Related | DS has structured terms |
| (none) | `IPRestrictions` | ❌ Gap | DS documents IP restrictions |
| (none) | `ExportControlRegulatoryRestrictions` | ❌ Gap | DS documents regulations |
| **Dataset Documentation** ||||
| `dataSet` (7 fields) | `Dataset` (200+ fields, 60+ classes) | 🟥 Very Weak | Massive comprehensiveness gap |
| `dataSet.name` | `Dataset.name` | ✅ Exact | Direct match |
| `dataSet.description` | `Dataset.description` | ✅ Exact | Direct match |
| `dataSet.link` | `Dataset.download_url` | 🟨 Close | Similar concept |
| `dataSet.sensitive` | `Dataset.sensitive_elements` → `SensitiveElement` | 🟨 Close | DS more structured |
| (none) | `Dataset.purposes` → `Purpose` | ❌ Gap | DS documents purpose |
| (none) | `Dataset.tasks` → `Task` | ❌ Gap | DS documents tasks |
| (none) | `Dataset.creators` → `Creator` | ❌ Gap | DS has creator info |
| (none) | `Dataset.subsets` → `DataSubset` | ❌ Gap | DS supports subsets |
| (none) | `Dataset.instances` → `Instance` | ❌ Gap | DS documents instances |
| (none) | `Dataset.variables` → `VariableMetadata` | ❌ Gap | DS has column-level metadata |
| **Data Collection** ||||
| (none) | `InstanceAcquisition` | ❌ Gap | DS documents acquisition |
| (none) | `CollectionMechanism` | ❌ Gap | DS documents collection |
| (none) | `SamplingStrategy` | ❌ Gap | DS documents sampling |
| (none) | `DataCollector` | ❌ Gap | DS tracks collectors |
| (none) | `CollectionTimeframe` | ❌ Gap | DS documents timeframe |
| **Preprocessing** ||||
| (none) | `PreprocessingStrategy` | ❌ Gap | DS documents preprocessing |
| (none) | `CleaningStrategy` | ❌ Gap | DS documents cleaning |
| (none) | `LabelingStrategy` | ❌ Gap | DS documents labeling |
| (none) | `RawData` | ❌ Gap | DS tracks raw sources |
| **Uses** ||||
| `Considerations.use_cases` | `OtherTask` | 🟨 Related | Different granularity |
| `Considerations.limitations` | `DiscouragedUse` | 🟨 Related | Complementary |
| (none) | `ExistingUse` | ❌ Gap | DS documents prior uses |
| (none) | `UseRepository` | ❌ Gap | DS links to use docs |
| (none) | `FutureUseImpact` | ❌ Gap | DS assesses impacts |
| **Distribution** ||||
| (none) | `DistributionFormat` | ❌ Gap | DS documents formats |
| (none) | `DistributionDate` | ❌ Gap | DS tracks dates |
| (none) | `ThirdPartySharing` | ❌ Gap | DS documents sharing |
| **Maintenance** ||||
| (none) | `Maintainer` | ❌ Gap | DS identifies maintainers |
| (none) | `Erratum` | ❌ Gap | DS tracks errors |
| (none) | `UpdatePlan` | ❌ Gap | DS documents updates |
| (none) | `RetentionLimits` | ❌ Gap | DS specifies retention |
| (none) | `VersionAccess` | ❌ Gap | DS documents version access |
| **Ethics & Privacy** ||||
| `Considerations.ethical_considerations` | `EthicalReview` | 🟨 Close | DS more structured |
| `risk` | Various ethics classes | 🟨 Related | DS more granular |
| `SensitiveData` | `SensitiveElement` + `Deidentification` | 🟨 Close | DS more comprehensive |
| (none) | `DataProtectionImpact` | ❌ Gap | DS documents DPIA |
| (none) | `CollectionConsent` | ❌ Gap | DS documents consent |
| (none) | `ConsentRevocation` | ❌ Gap | DS documents revocation |
| (none) | `HumanSubjectResearch` | ❌ Gap | DS documents HSR |
| (none) | `InformedConsent` | ❌ Gap | DS documents consent |
| (none) | `ParticipantPrivacy` | ❌ Gap | DS addresses privacy |
| (none) | `VulnerablePopulations` | ❌ Gap | DS identifies vulnerable groups |
| **Provenance** ||||
| `Version.date` | `created_on`, `issued` | 🟨 Close | Similar temporal data |
| (none) | `created_by`, `modified_by` | ❌ Gap | DS tracks authorship |
| (none) | `last_updated_on` | ❌ Gap | DS tracks updates |
| (none) | `was_derived_from` | ❌ Gap | DS tracks derivation |
| **File Format** ||||
| (none) | `format` → `FormatEnum` | ❌ Gap | DS specifies format |
| (none) | `encoding` → `EncodingEnum` | ❌ Gap | DS specifies encoding |
| (none) | `compression` → `CompressionEnum` | ❌ Gap | DS specifies compression |
| (none) | `media_type` → `MediaTypeEnum` | ❌ Gap | DS specifies MIME type |
| (none) | `hash`, `md5`, `sha256` | ❌ Gap | DS supports integrity |
| **Model-Specific (No DS Equivalent)** ||||
| `ModelDetails`, `ModelParameters` | (none) | N/A | Model-specific, appropriate for MC |
| `QuantitativeAnalysis`, `performanceMetric` | (none) | N/A | Model-specific, appropriate for MC |
| `BenchmarkResult`, `ModelIndex` | (none) | N/A | Model-specific, appropriate for MC |
| `framework`, `pipeline_tag`, `base_model` | (none) | N/A | Model-specific, appropriate for MC |

**Legend**:
- ✅ Exact: Direct 1:1 mapping, identical semantics
- 🟨 Close: Similar concepts, minor differences
- 🟨 Related: Overlapping but different granularity or structure
- 🟥 Very Weak: Massive gap in comprehensiveness
- ❌ Gap: No corresponding element
- N/A: Element is specific to one domain (model vs. dataset)

---

## 2. Detailed Alignments by Category

### 2.1 Basic Metadata & Identification

**Alignment Status**: ✅ **STRONG** (90%+ alignment)

Both schemas share core metadata patterns with minimal differences.

#### Direct Matches

| Field | Model Cards | Datasheets | Semantics |
|-------|-------------|------------|-----------|
| `name` | `schema:name` | `schema:name` | Human-readable name |
| `description` | `schema:description` | `schema:description` | Human-readable description |
| `id` | `schema:identifier` | `schema:identifier` | Unique identifier |

#### Differences

**Version Representation**:
- **Model Cards**: Structured `Version` class with `name` (string), `date` (date), `diff` (changelog string)
- **Datasheets**: Simple `version` slot (string)
- **Assessment**: Model cards approach is more structured and preferable

**Schema Versioning**:
- **Model Cards**: Tracks `schema_version` to indicate which version of the model card schema is used
- **Datasheets**: No schema version tracking
- **Assessment**: Model cards approach is valuable for schema evolution

#### Recommendations
1. **Keep** model cards' structured `Version` class
2. **Keep** model cards' `schema_version` tracking
3. **Adopt** datasheets' provenance slots (`created_by`, `created_on`, `modified_by`, `last_updated_on`) for better temporal tracking

---

### 2.2 Creators, Owners, & Contributors

**Alignment Status**: 🟨 **MODERATE** (50-70% alignment)

Datasheets has significantly more comprehensive creator/contributor documentation.

#### Model Cards Approach

```yaml
owner:
  description: Model owner or maintainer information
  slots:
    - name: Name of owner (individual or organization)
    - contact: Contact information (email, website, etc.)
```

**Limitations**:
- No structured person representation
- No organizational affiliation tracking
- No contributor role taxonomy
- No ORCID or persistent identifiers

#### Datasheets Approach

```yaml
Person:
  description: Individual person with structured metadata
  slots:
    - name: Full name
    - email: Email address
    - orcid: ORCID persistent identifier
    - affiliation: Organization affiliation
    - credit_roles: CRediT contributor roles (multivalued)

Organization:
  description: Organizational entity
  slots:
    - name: Organization name
    - [additional org metadata]

Creator:
  description: Dataset creator information
  slots:
    - principal_investigator: Lead researcher (→ Person)
    - affiliation: Institutional affiliation (→ Organization)
    - [additional creator metadata]

CRediTRoleEnum:
  permissible_values:
    - Conceptualization
    - Data curation
    - Formal analysis
    - Funding acquisition
    - Investigation
    - Methodology
    - Project administration
    - Resources
    - Software
    - Supervision
    - Validation
    - Visualization
    - Writing – original draft
    - Writing – review & editing
```

#### Key Differences

1. **Structured People**: Datasheets uses dedicated `Person` class with ORCID, enabling persistent identification and linking
2. **Contributor Roles**: Datasheets uses CRediT taxonomy (14 standardized roles) for precise attribution
3. **Organizations**: Datasheets has dedicated `Organization` class for institutional tracking
4. **Principal Investigator**: Datasheets distinguishes PI from general team members
5. **Funding**: Datasheets links creators to `FundingMechanism` → `Grantor` + `Grant` for comprehensive funding documentation

#### Alignment Assessment

| Model Cards | Datasheets | Alignment |
|-------------|------------|-----------|
| `owner` | `Creator` | 🟨 Conceptually similar |
| `owner.name` | `Person.name` + `Creator.principal_investigator` | 🟨 DS distinguishes roles |
| `owner.contact` | `Person.email` + `Person.orcid` | 🟨 DS has structured contact |
| (none) | `Person.affiliation` | ❌ Missing in MC |
| (none) | `Person.credit_roles` | ❌ Missing in MC |
| (none) | `Organization` | ❌ Missing in MC |
| (none) | `FundingMechanism` | ❌ Missing in MC |

#### Recommendations

**HIGH PRIORITY**: Replace model cards `owner` with datasheets classes

```yaml
# CURRENT (Model Cards)
owner:
  slots:
    - name
    - contact

ModelDetails:
  slots:
    - owners:
        range: owner
        multivalued: true

# PROPOSED (Harmonized)
# Remove owner class, import from datasheets

ModelDetails:
  slots:
    - creators:
        range: data_sheets_schema:Creator
        multivalued: true
        description: Model creators (uses datasheets Creator class)
    - contributors:
        range: data_sheets_schema:Person
        multivalued: true
        description: Additional contributors with CRediT roles
    - funding:
        range: data_sheets_schema:FundingMechanism
        multivalued: true
        description: Funding sources for model development
```

**Benefits**:
- Persistent identification with ORCID
- Institutional affiliation tracking
- Precise contributor attribution with CRediT roles
- Funding transparency
- Consistency with dataset creator documentation
- Interoperability with academic systems

---

### 2.3 Licensing & Legal

**Alignment Status**: 🟨 **MODERATE** (60% alignment)

Datasheets has more comprehensive legal documentation.

#### Model Cards Approach

```yaml
License:
  description: License information (use SPDX identifier OR custom text)
  slots:
    - identifier: SPDX license identifier (e.g., 'Apache-2.0', 'MIT')
    - custom_text: Custom license text (when SPDX not applicable)
```

**Strengths**:
- Supports SPDX identifiers (industry standard)
- Allows custom license text
- Simple, clear structure

**Limitations**:
- Single license concept (no distinction between model, data, code licenses)
- No IP restriction documentation
- No regulatory restriction documentation
- No detailed use terms

#### Datasheets Approach

```yaml
# Simple license identifier
license:
  slot_uri: dcterms:license
  range: string

# Comprehensive licensing documentation
LicenseAndUseTerms:
  description: Detailed licensing and use terms
  slots:
    - description: Full license terms and conditions
    - links: URLs to license texts
    - costs: Licensing costs or fees
    - constraints: Usage constraints

IPRestrictions:
  description: Third-party intellectual property restrictions
  slots:
    - description: Details of IP restrictions
    - third_party_licenses: Required third-party licenses
    - fees: Associated fees

ExportControlRegulatoryRestrictions:
  description: Export controls and regulatory restrictions
  slots:
    - description: Regulatory restrictions (ITAR, EAR, etc.)
    - jurisdictions: Affected jurisdictions
```

#### Key Differences

1. **Granularity**: Datasheets separates license identifier from comprehensive use terms, IP restrictions, and regulatory restrictions
2. **Legal Complexity**: Datasheets handles more complex scenarios (third-party IP, export controls, fees)
3. **Documentation Focus**: Datasheets emphasizes comprehensive legal documentation over just identifiers

#### Alignment Assessment

| Model Cards | Datasheets | Alignment |
|-------------|------------|-----------|
| `License.identifier` | `license` | ✅ Both support SPDX/identifiers |
| `License.custom_text` | `LicenseAndUseTerms.description` | 🟨 Similar purpose, different structure |
| (none) | `LicenseAndUseTerms` (full) | ❌ MC lacks comprehensive terms |
| (none) | `IPRestrictions` | ❌ MC doesn't track IP restrictions |
| (none) | `ExportControlRegulatoryRestrictions` | ❌ MC doesn't track regulations |

#### Recommendations

**HIGH PRIORITY**: Enhance licensing with datasheets classes

```yaml
# CURRENT (Model Cards)
License:
  slots:
    - identifier
    - custom_text

ModelDetails:
  slots:
    - licenses:
        range: License
        multivalued: true

# PROPOSED (Harmonized)
# Keep License for model artifacts
License:
  slots:
    - identifier
    - custom_text
  description: License for model artifacts (code, weights, architecture)

ModelDetails:
  slots:
    - model_licenses:
        range: License
        multivalued: true
        description: Licenses for model artifacts

    - data_licenses:
        range: data_sheets_schema:LicenseAndUseTerms
        multivalued: true
        description: Licenses for training/evaluation data (from datasheets)

    - data_ip_restrictions:
        range: data_sheets_schema:IPRestrictions
        multivalued: true
        description: Third-party IP restrictions on training data

    - regulatory_restrictions:
        range: data_sheets_schema:ExportControlRegulatoryRestrictions
        multivalued: true
        description: Export controls or regulatory restrictions
```

**Benefits**:
- Clear separation of model vs. data licensing
- Comprehensive legal documentation
- IP restriction tracking for compliance
- Regulatory compliance support (ITAR, EAR, GDPR, etc.)
- Better risk assessment for model deployment

---

### 2.4 Dataset Documentation

**Alignment Status**: 🟥 **VERY WEAK** (<20% alignment)

This is the **largest and most critical gap**. Model cards has minimal dataset documentation; datasheets has comprehensive, production-ready dataset documentation.

#### Model Cards Approach

```yaml
dataSet:
  description: Information about a dataset used for training or evaluation
  slots:
    - name: Dataset name or identifier
    - description: Dataset overview and characteristics
    - link: URL to the dataset (required)
    - sensitive: Sensitive data information (→ SensitiveData)
    - graphics: Visualizations of the dataset (→ GraphicsCollection)
    - bias_input: Known biases present in the input data (string)
    - unit: Unit for values in this dataset (string)

SensitiveData:
  slots:
    - sensitive_data: Types of PII (multivalued strings)
```

**Total**: 2 classes, ~10 fields

#### Datasheets Approach

Datasheets provides **60+ classes** and **200+ fields** for comprehensive dataset documentation, organized into thematic subsets:

##### **Motivation Subset**
Documents why the dataset was created:
- `Purpose`: Dataset purposes and objectives
- `Task`: Intended tasks
- `AddressingGap`: What gap the dataset addresses
- `Creator`: Dataset creators with roles
- `FundingMechanism`, `Grantor`, `Grant`: Funding information

##### **Composition Subset**
Documents what the dataset contains:
- `Instance`: What instances represent (e.g., individual people, photos, documents)
- `DataSubset`: Dataset subsets and splits
- `MissingInfo`: Missing or unavailable information
- `Relationships`: Relationships between instances
- `Splits`: Train/test/validation splits
- `DataAnomaly`: Known data quality issues
- `ExternalResource`: External resources used
- `Confidentiality`: Confidential data elements
- `ContentWarning`: Potentially offensive/disturbing content
- `Subpopulation`: Demographic subpopulations represented
- `Deidentification`: Identifiability assessment
- `SensitiveElement`: PII and sensitive data documentation

##### **Collection Subset**
Documents how data was collected:
- `InstanceAcquisition`: How instances were acquired
- `CollectionMechanism`: Collection methodology
- `SamplingStrategy`: Sampling approach
- `DataCollector`: Who collected the data
- `CollectionTimeframe`: When data was collected
- `DirectCollection`: Direct vs. indirect collection

##### **Preprocessing-Cleaning-Labeling Subset**
Documents data preparation:
- `PreprocessingStrategy`: Preprocessing steps
- `CleaningStrategy`: Data cleaning procedures
- `LabelingStrategy`: Labeling approach
- `RawData`: Raw data sources

##### **Uses Subset**
Documents appropriate and inappropriate uses:
- `ExistingUse`: Prior uses of the dataset
- `UseRepository`: Repository of use documentation
- `OtherTask`: Other potential tasks
- `FutureUseImpact`: Potential future impacts
- `DiscouragedUse`: Uses that should be avoided

##### **Distribution Subset**
Documents how dataset is distributed:
- `DistributionFormat`: Available formats
- `DistributionDate`: Distribution timeline
- `ThirdPartySharing`: Third-party sharing arrangements
- `LicenseAndUseTerms`: License details
- `IPRestrictions`: IP restrictions
- `ExportControlRegulatoryRestrictions`: Regulatory restrictions

##### **Maintenance Subset**
Documents dataset maintenance:
- `Maintainer`: Dataset maintainers
- `Erratum`: Known errors and corrections
- `UpdatePlan`: Update policy
- `RetentionLimits`: Data retention limits
- `VersionAccess`: Access to previous versions
- `ExtensionMechanism`: How dataset can be extended

##### **Ethics Subset**
Documents ethical considerations:
- `EthicalReview`: IRB/ethics board review
- `DataProtectionImpact`: GDPR DPIA or similar
- `CollectionNotification`: Notification to data subjects
- `CollectionConsent`: Consent mechanisms
- `ConsentRevocation`: Consent withdrawal procedures
- `HumanSubjectResearch`: Human subjects protections
- `InformedConsent`: Informed consent documentation
- `ParticipantPrivacy`: Privacy protections
- `HumanSubjectCompensation`: Participant compensation
- `VulnerablePopulations`: Vulnerable population protections

##### **Technical Metadata**
- `format`, `encoding`, `compression`, `media_type`: File format details
- `hash`, `md5`, `sha256`: Integrity verification
- `bytes`: File size
- `path`, `download_url`: Access information
- `is_tabular`: Whether data is tabular
- `variables`: Column/field-level metadata
- `FormatDialect`: CSV dialect specification

##### **Core Dataset Class**

```yaml
Dataset:
  is_a: Information
  attributes:
    # Identity & Description
    - name, description, title
    - id (required)
    - keywords (multivalued)
    - language
    - themes
    - doi
    - same_as
    - page (landing page)
    - download_url

    # Provenance
    - version
    - created_by
    - created_on
    - modified_by
    - last_updated_on
    - issued
    - was_derived_from
    - publisher

    # Licensing
    - license
    - license_and_use_terms → LicenseAndUseTerms
    - ip_restrictions → IPRestrictions
    - regulatory_restrictions → ExportControlRegulatoryRestrictions

    # Format
    - format → FormatEnum
    - encoding → EncodingEnum
    - compression → CompressionEnum
    - media_type → MediaTypeEnum
    - bytes
    - hash, md5, sha256
    - is_tabular
    - dialect → FormatDialect

    # Motivation
    - purposes → Purpose (multivalued)
    - tasks → Task (multivalued)
    - addressing_gaps → AddressingGap (multivalued)
    - creators → Creator (multivalued)
    - funders → FundingMechanism (multivalued)

    # Composition
    - subsets → DataSubset (multivalued)
    - instances → Instance (multivalued)
    - missing_info → MissingInfo (multivalued)
    - relationships → Relationships (multivalued)
    - splits → Splits (multivalued)
    - anomalies → DataAnomaly (multivalued)
    - external_resources → ExternalResource (multivalued)
    - variables → VariableMetadata (multivalued)
    - confidential_elements → Confidentiality (multivalued)
    - content_warnings → ContentWarning (multivalued)
    - subpopulations → Subpopulation (multivalued)
    - is_deidentified → Deidentification
    - sensitive_elements → SensitiveElement (multivalued)

    # Collection
    - acquisition_methods → InstanceAcquisition (multivalued)
    - collection_mechanisms → CollectionMechanism (multivalued)
    - sampling_strategies → SamplingStrategy (multivalued)
    - data_collectors → DataCollector (multivalued)
    - collection_timeframes → CollectionTimeframe (multivalued)

    # Preprocessing
    - preprocessing_strategies → PreprocessingStrategy (multivalued)
    - cleaning_strategies → CleaningStrategy (multivalued)
    - labeling_strategies → LabelingStrategy (multivalued)
    - raw_sources → RawData (multivalued)

    # Uses
    - existing_uses → ExistingUse (multivalued)
    - use_repository → UseRepository
    - other_tasks → OtherTask (multivalued)
    - future_use_impacts → FutureUseImpact (multivalued)
    - discouraged_uses → DiscouragedUse (multivalued)

    # Distribution
    - distribution_formats → DistributionFormat (multivalued)
    - distribution_dates → DistributionDate (multivalued)
    - third_party_sharing → ThirdPartySharing (multivalued)

    # Maintenance
    - maintainers → Maintainer (multivalued)
    - errata → Erratum (multivalued)
    - updates → UpdatePlan (multivalued)
    - retention_limit → RetentionLimits
    - version_access → VersionAccess
    - extension_mechanism → ExtensionMechanism

    # Ethics
    - ethical_reviews → EthicalReview (multivalued)
    - data_protection_impacts → DataProtectionImpact (multivalued)
```

#### Critical Gaps in Model Cards

Model cards is missing comprehensive documentation for:

1. **Dataset Motivation** - Why was the dataset created? What purpose does it serve? What gap does it address? Who funded it?
2. **Dataset Composition** - What instances exist? What's the structure? What subpopulations? What's missing? What anomalies exist?
3. **Collection Methodology** - How was data collected? By whom? When? What sampling strategy? Direct or indirect?
4. **Preprocessing & Labeling** - What preprocessing occurred? How was data cleaned? How was it labeled? What were the raw sources?
5. **Use History & Guidance** - Has it been used before? For what tasks? What uses should be discouraged? What are future impact considerations?
6. **Distribution Policy** - What formats are available? When was it distributed? Are there third-party sharing arrangements?
7. **Maintenance Plan** - Who maintains it? What's the update policy? How are errors corrected? How long will it be retained?
8. **Ethics & Consent** - Was there ethics review? Was consent obtained? Can consent be revoked? Are there human subject protections?
9. **Data Quality** - What anomalies exist? What's missing? What corrections have been made?
10. **Variable-Level Metadata** - For tabular data, what do columns represent? What are their types, ranges, distributions?

#### Alignment Assessment

**Overlap**: Only 3 fields align (name, description, link/download_url)
**Coverage**: Model cards covers ~5% of what datasheets documents

#### Recommendations

**CRITICAL PRIORITY**: Replace model cards `dataSet` with datasheets `Dataset` reference

This is the **single most important harmonization action**.

```yaml
# CURRENT (Model Cards)
dataSet:
  slots:
    - name
    - description
    - link
    - sensitive
    - graphics
    - bias_input
    - unit

ModelParameters:
  slots:
    - data:
        range: dataSet
        multivalued: true

# PROPOSED (Harmonized)
# Remove dataSet class entirely
# Import Dataset from datasheets

ModelParameters:
  slots:
    - training_data:
        range: data_sheets_schema:Dataset
        multivalued: true
        description: |
          Training datasets with comprehensive documentation using datasheets standard.
          Each dataset should be fully documented following the Datasheets for Datasets framework,
          including motivation, composition, collection, preprocessing, uses, distribution,
          maintenance, and ethics.

    - evaluation_data:
        range: data_sheets_schema:Dataset
        multivalued: true
        description: |
          Evaluation/validation datasets with comprehensive documentation.

    - data_usage_notes:
        range: string
        description: |
          Model-specific notes on how training and evaluation data were used.
          Examples: data augmentation applied, subsets used, weighting schemes.
```

**Benefits**:
- Comprehensive dataset documentation (60+ classes vs. 1 class)
- Standardized documentation framework (Datasheets for Datasets is widely recognized)
- Ethics and privacy documentation
- Legal compliance support
- Collection and preprocessing transparency
- Maintenance and versioning
- Reuse of dataset documentation across multiple models
- Interoperability with dataset catalogs and repositories

**Migration Path**:
1. Existing model cards using `dataSet`: Create full `Dataset` documentation following datasheets schema
2. Provide migration guide and templates
3. Offer tooling to convert simple `dataSet` entries to datasheets `Dataset` stubs

---

### 2.5 Sensitive Data & Privacy

**Alignment Status**: 🟥 **WEAK** (<30% alignment)

Datasheets has dramatically more comprehensive privacy and human subjects documentation.

#### Model Cards Approach

```yaml
SensitiveData:
  description: Information about sensitive data in a dataset
  slots:
    - sensitive_data:
        description: Types of PII or sensitive information (e.g., names, addresses)
        multivalued: true
        range: string
```

**Limitations**:
- Simple string list of PII types
- No identifiability assessment
- No deidentification documentation
- No consent documentation
- No ethics review documentation
- No data protection impact assessment

#### Datasheets Approach

Datasheets provides comprehensive privacy, ethics, and human subjects documentation across multiple classes:

##### **Privacy & Sensitive Data**

```yaml
SensitiveElement:
  slots:
    - sensitive_elements_present: boolean
    - description: Detailed description of sensitive elements
    - pii_types: Types of personally identifiable information
    - direct_identifiers: Direct identifiers present
    - indirect_identifiers: Indirect identifiers that could enable re-identification

Deidentification:
  slots:
    - identifiable_elements_present: boolean
    - description: Assessment of identifiability risk
    - deidentification_methods: Methods used for deidentification
    - residual_risk: Remaining re-identification risk

Confidentiality:
  slots:
    - confidential_elements_present: boolean
    - description: Confidential data elements
    - access_restrictions: Who can access confidential data

ContentWarning:
  slots:
    - content_warning_present: boolean
    - description: Content that may be offensive, disturbing, or traumatic
```

##### **Ethics Review**

```yaml
EthicalReview:
  slots:
    - ethical_review_conducted: boolean
    - description: Details of ethical review (IRB, ethics board)
    - review_board: Name of reviewing entity
    - approval_number: Approval reference number
    - approval_date: Date of approval

DataProtectionImpact:
  slots:
    - data_protection_impact_assessment_conducted: boolean
    - description: GDPR Data Protection Impact Assessment or equivalent
    - risks_identified: Privacy risks identified
    - mitigation_measures: Measures to mitigate risks
```

##### **Consent & Notification**

```yaml
CollectionNotification:
  slots:
    - notification_provided: boolean
    - description: Whether and how data subjects were notified
    - notification_method: Method of notification (email, website, etc.)

CollectionConsent:
  slots:
    - consent_obtained: boolean
    - description: Details of consent mechanisms
    - consent_type: Type of consent (explicit, implicit, opt-in, opt-out)
    - consent_form: Reference to consent form or language

ConsentRevocation:
  slots:
    - revocation_mechanism_exists: boolean
    - description: How data subjects can revoke consent
    - revocation_process: Process for consent withdrawal
```

##### **Human Subjects Research**

```yaml
HumanSubjectResearch:
  slots:
    - involves_human_subjects: boolean
    - description: Details of human subject involvement
    - irb_approval: IRB approval obtained
    - common_rule_compliance: Compliance with Common Rule

InformedConsent:
  slots:
    - informed_consent_obtained: boolean
    - description: Informed consent process
    - consent_capacity: Capacity of subjects to consent
    - vulnerable_populations: Whether vulnerable populations involved

ParticipantPrivacy:
  slots:
    - privacy_protections_applied: boolean
    - description: Privacy protections for participants
    - data_access_restrictions: Restrictions on data access

HumanSubjectCompensation:
  slots:
    - compensation_provided: boolean
    - description: Compensation details
    - compensation_amount: Amount of compensation
    - compensation_form: Form of compensation (cash, gift card, etc.)

VulnerablePopulations:
  slots:
    - vulnerable_populations_involved: boolean
    - description: Which vulnerable populations involved
    - additional_protections: Additional protections for vulnerable groups
```

##### **Demographic Fairness**

```yaml
Subpopulation:
  slots:
    - subpopulations_identified: boolean
    - description: Demographic subpopulations represented
    - subpopulation_characteristics: Characteristics defining subpopulations
    - subpopulation_sizes: Sizes of subpopulations
```

#### Key Differences

1. **Granularity**: Datasheets has 10+ classes for privacy/ethics; model cards has 1 class
2. **Ethics Framework**: Datasheets covers IRB review, DPIA, human subjects research
3. **Consent**: Datasheets documents consent mechanisms, revocation procedures
4. **Identifiability**: Datasheets assesses deidentification and re-identification risks
5. **Regulatory Compliance**: Datasheets supports GDPR, Common Rule, ethics board requirements
6. **Vulnerable Populations**: Datasheets identifies and documents special protections

#### Alignment Assessment

| Model Cards | Datasheets | Alignment |
|-------------|------------|-----------|
| `SensitiveData.sensitive_data` | `SensitiveElement.pii_types` | 🟨 Similar concept |
| (none) | `Deidentification` | ❌ No identifiability assessment in MC |
| (none) | `Confidentiality` | ❌ No confidentiality docs in MC |
| (none) | `EthicalReview` | ❌ No ethics review docs in MC |
| (none) | `DataProtectionImpact` | ❌ No DPIA in MC |
| (none) | `CollectionConsent` + `ConsentRevocation` | ❌ No consent docs in MC |
| (none) | `HumanSubjectResearch` | ❌ No HSR docs in MC |
| (none) | `VulnerablePopulations` | ❌ No vulnerable pop docs in MC |

#### Recommendations

**HIGH PRIORITY**: Reference datasheets privacy/ethics classes for training data

```yaml
# CURRENT (Model Cards)
SensitiveData:
  slots:
    - sensitive_data: list of strings

dataSet:
  slots:
    - sensitive: → SensitiveData

# PROPOSED (Harmonized)
# Keep SensitiveData for model-specific concerns (e.g., model memorization)
# Reference datasheets for data privacy/ethics

ModelParameters:
  slots:
    - training_data:
        range: data_sheets_schema:Dataset
        # Dataset class includes:
        # - sensitive_elements → SensitiveElement
        # - is_deidentified → Deidentification
        # - confidential_elements → Confidentiality
        # - ethical_reviews → EthicalReview
        # - data_protection_impacts → DataProtectionImpact
        # - collection_consent, revocation
        # - human subject research documentation
        # - vulnerable populations

Considerations:
  slots:
    - model_privacy_risks:
        description: |
          Model-specific privacy risks such as:
          - Training data memorization
          - Membership inference attacks
          - Model inversion attacks
        range: risk
        multivalued: true

    - data_privacy_considerations:
        description: |
          Reference to privacy considerations in training data
          (documented in datasheets Dataset class)
        range: string
```

**Benefits**:
- Comprehensive privacy documentation for datasets
- Ethics review documentation
- Consent and notification documentation
- GDPR/regulatory compliance support
- Clear separation: data privacy (datasheets) vs. model privacy risks (model cards)
- Vulnerable population protections
- Transparent human subjects research documentation

---

### 2.6 Ethical Considerations & Risks

**Alignment Status**: 🟨 **MODERATE** (40-60% alignment)

Different levels of granularity and focus.

#### Model Cards Approach

```yaml
risk:
  description: An ethical, environmental, or operational risk
  slots:
    - name: Name or type of the risk
    - mitigation_strategy: Strategy to address or mitigate this risk

Considerations:
  slots:
    - ethical_considerations:
        description: Ethical considerations and identified risks
        range: risk
        multivalued: true
```

**Focus**: Model-centric risks including fairness, bias, safety, deployment concerns

**Strengths**:
- Flexible risk documentation
- Mitigation strategy documentation
- Appropriate for model-specific concerns

**Limitations**:
- No structured ethics review
- No systematic ethical framework
- Limited data ethics coverage

#### Datasheets Approach

Comprehensive ethics documentation across multiple classes and thematic subsets:

**Ethics Subset Classes**:
- `EthicalReview`: IRB/ethics board review process
- `DataProtectionImpact`: GDPR DPIA or equivalent
- `CollectionNotification`: Notification to data subjects
- `CollectionConsent`: Consent mechanisms
- `ConsentRevocation`: Consent withdrawal
- `HumanSubjectResearch`: Human subjects protections
- `InformedConsent`: Informed consent process
- `ParticipantPrivacy`: Privacy protections
- `HumanSubjectCompensation`: Participant compensation
- `VulnerablePopulations`: Vulnerable population protections

**Structured Approach**:
- Systematic coverage of ethical dimensions
- Regulatory compliance focus
- Process documentation (review, consent, notification)
- Risk assessment (DPIA)

#### Key Differences

1. **Scope**: Model cards focuses on model risks; datasheets focuses on data collection/use ethics
2. **Structure**: Model cards has flexible risk class; datasheets has systematic ethics framework
3. **Regulatory**: Datasheets explicitly supports regulatory compliance (GDPR, Common Rule, IRB)
4. **Process**: Datasheets documents ethical processes (review, consent, notification)

#### Alignment Assessment

**Complementary Rather Than Overlapping**:
- Model cards documents model-specific ethical concerns (fairness, safety, deployment risks)
- Datasheets documents data collection/use ethical concerns (consent, privacy, human subjects)

Both are needed for comprehensive ethical documentation.

#### Recommendations

**MEDIUM PRIORITY**: Reference datasheets ethics for data; maintain model ethics in model cards

```yaml
# PROPOSED (Harmonized)
risk:
  description: Model-specific risk (deployment, fairness, safety, environmental)
  slots:
    - name
    - mitigation_strategy
    - risk_category:
        description: Category of risk
        range: RiskCategoryEnum  # fairness, safety, privacy, environmental, operational

RiskCategoryEnum:
  permissible_values:
    Fairness: Fairness and bias concerns in model predictions
    Safety: Safety risks from model outputs
    Privacy: Privacy risks (memorization, inference attacks)
    Environmental: Environmental impact (energy, carbon)
    Operational: Operational risks (reliability, robustness)
    Security: Security vulnerabilities
    Misuse: Potential for misuse

Considerations:
  slots:
    - model_ethical_considerations:
        description: Model-specific ethical concerns and risks
        range: risk
        multivalued: true

    - data_ethical_reviews:
        description: |
          Ethics reviews conducted for training/evaluation data.
          Reference Dataset.ethical_reviews in datasheets documentation.
        range: data_sheets_schema:EthicalReview
        multivalued: true

    - data_protection_impacts:
        description: |
          Data protection impact assessments for training data.
          Reference Dataset.data_protection_impacts in datasheets documentation.
        range: data_sheets_schema:DataProtectionImpact
        multivalued: true
```

**Benefits**:
- Clear separation: model ethics (model cards) vs. data ethics (datasheets)
- Comprehensive ethical documentation
- Regulatory compliance support
- Cross-reference to data ethics without duplication

---

### 2.7 Uses & Limitations

**Alignment Status**: 🟨 **MODERATE** (50-70% alignment)

Complementary perspectives: model use cases vs. dataset use history.

#### Model Cards Approach

```yaml
User:
  slots:
    - description: Description of intended user type or role

UseCase:
  slots:
    - description: Description of application scenario

Limitation:
  slots:
    - description: Description of limitation or constraint

Tradeoff:
  slots:
    - description: Description of performance tradeoff

Considerations:
  slots:
    - users: Intended user types (→ User)
    - use_cases: Intended use cases (→ UseCase)
    - limitations: Known limitations (→ Limitation)
    - tradeoffs: Performance tradeoffs (→ Tradeoff)
```

**Focus**: Model-centric documentation of intended users, use cases, limitations, and performance tradeoffs

#### Datasheets Approach

```yaml
ExistingUse:
  slots:
    - description: Prior uses of the dataset
    - publications: Publications using the dataset
    - repositories: Code repositories using the dataset

UseRepository:
  slots:
    - description: Repository documenting dataset uses
    - url: URL to use repository

OtherTask:
  slots:
    - description: Other potential tasks the dataset could support
    - suitability_assessment: Assessment of suitability for task

FutureUseImpact:
  slots:
    - description: Potential impacts of future uses
    - risk_assessment: Risks of particular future uses

DiscouragedUse:
  slots:
    - description: Uses that should be discouraged or avoided
    - rationale: Why use is discouraged
```

**Focus**: Dataset-centric documentation of use history, appropriate uses, and inappropriate uses

#### Key Differences

1. **Temporal**: Model cards focuses on intended future use; datasheets documents past uses and future considerations
2. **Scope**: Model cards documents model applications; datasheets documents dataset applications
3. **Granularity**: Both have similar granularity but different focuses

#### Alignment Assessment

| Model Cards | Datasheets | Relationship |
|-------------|------------|--------------|
| `UseCase` | `OtherTask` | 🟨 Similar but different scope (model vs. data) |
| `Limitation` | `DiscouragedUse` | 🟨 Related but different framing |
| (none) | `ExistingUse` | N/A Model-specific, no data use history |
| (none) | `FutureUseImpact` | 🟨 Both consider future impacts |

#### Recommendations

**LOW-MEDIUM PRIORITY**: Keep model cards approach; optionally reference datasheets for data

```yaml
# PROPOSED (Harmonized)
Considerations:
  slots:
    - users:
        range: User
        multivalued: true
        description: Intended model users

    - use_cases:
        range: UseCase
        multivalued: true
        description: Intended model use cases

    - limitations:
        range: Limitation
        multivalued: true
        description: Model limitations and constraints

    - tradeoffs:
        range: Tradeoff
        multivalued: true
        description: Model performance tradeoffs

    - data_use_considerations:
        description: |
          Notes on training data use considerations.
          Refer to Dataset.existing_uses, Dataset.discouraged_uses,
          and Dataset.future_use_impacts in datasheets documentation.
        range: string
```

**Benefits**:
- Maintain model-specific use documentation
- Cross-reference to dataset use considerations
- Ensure model use cases are compatible with dataset use terms

---

### 2.8 Version & Provenance

**Alignment Status**: 🟨 **MODERATE** (60% alignment)

Datasheets has more granular temporal and provenance tracking.

#### Model Cards Approach

```yaml
Version:
  slots:
    - name: Version identifier (e.g., '1.0.0', 'v2', 'beta')
    - date: Release date of this version
    - diff: Changes from the previous version
```

**Strengths**:
- Structured version information
- Changelog support

**Limitations**:
- No creator/modifier tracking
- No fine-grained temporal metadata
- No derivation provenance

#### Datasheets Approach

**Multiple Provenance Slots**:
```yaml
# Version
version: string (simple identifier)

# Creation
created_by: string (creator identifier)
created_on: datetime (creation timestamp)

# Modification
modified_by: string (modifier identifier)
last_updated_on: datetime (last update timestamp)

# Publication
issued: datetime (publication date)

# Derivation
was_derived_from: string (parent dataset reference)

# Version Management Classes
VersionAccess:
  description: Access to older versions
  slots:
    - older_versions_available: boolean
    - version_access_mechanism: How to access older versions

UpdatePlan:
  description: Dataset update policy
  slots:
    - update_planned: boolean
    - update_frequency: Expected update frequency
    - update_mechanism: How updates are made

Erratum:
  description: Known errors and corrections
  slots:
    - error_description: Description of error
    - correction: How error was corrected
    - date_corrected: When correction was made
```

#### Key Differences

1. **Granularity**: Datasheets separates creation, modification, and publication timestamps
2. **Attribution**: Datasheets tracks who created and who modified
3. **Derivation**: Datasheets documents derivation provenance (parent datasets)
4. **Version Management**: Datasheets documents version access policy, update plans, and error corrections

#### Alignment Assessment

| Model Cards | Datasheets | Alignment |
|-------------|------------|-----------|
| `Version.date` | `created_on`, `issued` | 🟨 Similar temporal data |
| `Version.diff` | `UpdatePlan.description` | 🟨 Different approaches to changes |
| (none) | `created_by`, `modified_by` | ❌ MC doesn't track authorship |
| (none) | `last_updated_on` | ❌ MC doesn't track updates |
| (none) | `was_derived_from` | ❌ MC doesn't track derivation |
| (none) | `VersionAccess`, `UpdatePlan`, `Erratum` | ❌ MC lacks version management |

#### Recommendations

**MEDIUM-HIGH PRIORITY**: Enhance model cards version tracking with datasheets provenance

```yaml
# CURRENT (Model Cards)
Version:
  slots:
    - name
    - date
    - diff

# PROPOSED (Enhanced)
Version:
  slots:
    - name: Version identifier
    - date: Release date
    - diff: Changelog
    - created_by:
        description: Person or system that created this version
        range: string
    - released_by:
        description: Person who released/published this version
        range: string
    - changelog_url:
        range: uri
        description: URL to detailed changelog or release notes

ModelDetails:
  slots:
    # Add fine-grained provenance from datasheets
    - created_on:
        range: datetime
        description: When model development began

    - created_by:
        description: Initial model creator(s)
        range: string

    - last_updated_on:
        range: datetime
        description: When model was last modified

    - modified_by:
        description: Person who last modified the model
        range: string

    - was_derived_from:
        range: uri
        multivalued: true
        description: |
          Parent model(s) this model was derived from.
          Examples: base model for fine-tuning, teacher model for distillation.

    - update_plan:
        description: Plan for model updates and retraining
        range: string

    - known_issues:
        description: Known issues or errors in the model
        multivalued: true
        range: string
```

**Benefits**:
- Better version tracking
- Attribution of creators and modifiers
- Lineage documentation (fine-tuning, distillation, transfer learning)
- Temporal metadata for audit trails
- Update policy documentation
- Issue tracking

---

### 2.9 File Format & Technical Metadata

**Alignment Status**: ❌ **N/A - Model Cards Lacks This Entirely**

Datasheets provides comprehensive technical metadata for dataset files; model cards has no equivalent.

#### Datasheets Approach

```yaml
Dataset:
  slots:
    # Format Specification
    - format:
        range: FormatEnum  # CSV, JSON, XML, Parquet, HDF5, etc.
    - encoding:
        range: EncodingEnum  # UTF-8, ASCII, Latin-1, etc.
    - compression:
        range: CompressionEnum  # gzip, bzip2, zip, none
    - media_type:
        range: MediaTypeEnum  # MIME types

    # File Integrity
    - hash: Generic hash
    - md5: MD5 checksum
    - sha256: SHA-256 checksum

    # Size & Location
    - bytes: File size in bytes
    - path: File path
    - download_url: URL to download

    # Structure
    - is_tabular: boolean (whether data is tabular)
    - dialect: → FormatDialect (for CSV: delimiter, quote char, etc.)
    - variables: → VariableMetadata (column/field metadata)

FormatDialect:
  description: CSV dialect specification
  slots:
    - delimiter: Field delimiter
    - quote_char: Quote character
    - double_quote: Whether quotes are doubled
    - skip_initial_space: Whether to skip initial space
    - line_terminator: Line terminator
    - header: Whether header row present

VariableMetadata:
  description: Metadata for a single variable/column
  slots:
    - name: Variable name
    - description: Variable description
    - type: Data type
    - format: Format specification
    - missing_values: Missing value indicators
    - minimum: Minimum value
    - maximum: Maximum value
    - categories: Categorical values
```

#### Model Cards Situation

**No file format or technical metadata for datasets** - model cards delegates this entirely to the dataset provider.

For **model artifacts**, model cards has some format information through HuggingFace integration:
- `framework`: ML framework (TensorFlow, PyTorch, etc.)
- `framework_version`: Framework version
- `library_name`: Library for loading (transformers, diffusers, etc.)

But no standardized format metadata like:
- Model file format (SavedModel, ONNX, TorchScript, etc.)
- Model file size
- Model file checksums
- Model serialization format

#### Recommendations

**MEDIUM PRIORITY (for datasets)**: Reference datasheets technical metadata

**LOW PRIORITY (for models)**: Consider adding model artifact format metadata

```yaml
# PROPOSED
ModelDetails:
  slots:
    # Model artifact format (new)
    - model_format:
        description: Model serialization format
        range: ModelFormatEnum  # SavedModel, ONNX, TorchScript, pickle, etc.

    - model_file_size:
        description: Size of model files in bytes
        range: integer

    - model_checksum:
        description: Checksum for model files (SHA-256)
        range: string

    # Dataset technical metadata (reference datasheets)
    # Training/evaluation datasets use datasheets Dataset class which includes:
    # - format, encoding, compression, media_type
    # - hash, md5, sha256
    # - bytes (file size)
    # - is_tabular, dialect, variables

ModelFormatEnum:
  permissible_values:
    SavedModel: TensorFlow SavedModel format
    TorchScript: PyTorch TorchScript
    ONNX: Open Neural Network Exchange format
    CoreML: Apple CoreML format
    TFLite: TensorFlow Lite
    Pickle: Python pickle (discouraged for production)
    HDF5: Hierarchical Data Format
    Safetensors: Hugging Face safe tensor format
    GGUF: GPT-Generated Unified Format (llama.cpp)
```

**Benefits (dataset formats)**:
- Standardized format documentation via datasheets
- Integrity verification (checksums)
- Format dialects for interoperability
- Variable-level metadata for understanding data structure

**Benefits (model formats)**:
- Clear model artifact format documentation
- Integrity verification for model files
- Deployment planning (format compatibility)

---

## 3. Model Cards Elements: Complete Mapping to Datasheets

This section provides a comprehensive mapping of every model cards class and slot to corresponding datasheets elements.

### 3.1 Root Class

| Model Cards | Datasheets | Recommendation |
|-------------|------------|----------------|
| `modelCard` (root) | (no equivalent) | **KEEP** - model-specific root |

### 3.2 Core Metadata

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `name` | `name` | ✅ **ALIGNED** |
| `description` | `description` | ✅ **ALIGNED** |
| `Version` class | `version` + provenance slots | 🔧 **ENHANCE** with `created_by`, `modified_by` |
| `Version.name` | `version` | ✅ **ALIGNED** |
| `Version.date` | `created_on` or `issued` | ✅ **ALIGNED** |
| `Version.diff` | `UpdatePlan.description` | 🔧 **KEEP** but add update plan reference |
| `schema_version` | (none) | ✅ **KEEP** - tracks MC schema version |

### 3.3 Creators & Ownership

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `owner` class | `Creator` + `Person` + `Organization` | 🔄 **REPLACE** with datasheets classes |
| `owner.name` | `Person.name` | 🔄 **MIGRATE** to Person |
| `owner.contact` | `Person.email` | 🔄 **MIGRATE** to Person.email |
| (none) | `Person.orcid` | ➕ **ADD** via Person import |
| (none) | `Person.affiliation` | ➕ **ADD** via Person import |
| (none) | `Person.credit_roles` | ➕ **ADD** via Person import |
| (none) | `Organization` | ➕ **ADD** via import |
| (none) | `FundingMechanism` | ➕ **ADD** via import |

### 3.4 Licensing

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `License` class | `license` + `LicenseAndUseTerms` | 🔧 **KEEP** for model, **REFERENCE** DS for data |
| `License.identifier` | `license` | ✅ **KEEP** |
| `License.custom_text` | `LicenseAndUseTerms.description` | ✅ **KEEP** |
| (none) | `LicenseAndUseTerms` (full) | ➕ **REFERENCE** for datasets |
| (none) | `IPRestrictions` | ➕ **REFERENCE** for datasets |
| (none) | `ExportControlRegulatoryRestrictions` | ➕ **REFERENCE** for datasets |

### 3.5 References & Citations

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `Reference` class | `ExternalResource` | 🔧 **KEEP** MC version, optionally reference DS |
| `Citation` class | (bibliographic info in Information) | ✅ **KEEP** - MC approach is good |
| `CitationStyleEnum` | (none) | ✅ **KEEP** - useful for citations |

### 3.6 Model Details

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `ModelDetails` class | (none - model-specific) | ✅ **KEEP** |
| `ModelDetails.name` | `name` | ✅ **ALIGNED** |
| `ModelDetails.overview` | `description` | ✅ **ALIGNED** |
| `ModelDetails.documentation` | (none) | ✅ **KEEP** |
| `ModelDetails.owners` | `Creator` | 🔄 **CHANGE** range to Creator |
| `ModelDetails.version` | `version` + provenance | 🔧 **ENHANCE** |
| `ModelDetails.licenses` | `license` + `LicenseAndUseTerms` | 🔧 **ENHANCE** |
| `ModelDetails.references` | `ExternalResource` | ✅ **KEEP** MC version |
| `ModelDetails.citations` | (none) | ✅ **KEEP** |
| `ModelDetails.path` | `path` | ✅ **ALIGNED** (but different use) |
| (add) `created_on`, `modified_by`, etc. | Provenance slots | ➕ **ADD** from datasheets |

### 3.7 Dataset Documentation

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `dataSet` class | `Dataset` class | 🔄 **REPLACE** entirely with DS Dataset |
| `dataSet.name` | `Dataset.name` | ✅ **ALIGNED** → use DS |
| `dataSet.description` | `Dataset.description` | ✅ **ALIGNED** → use DS |
| `dataSet.link` | `Dataset.download_url` | ✅ **ALIGNED** → use DS |
| `dataSet.sensitive` | `Dataset.sensitive_elements` | 🔄 **USE** DS SensitiveElement |
| `dataSet.graphics` | (visualization metadata) | 🔧 **MIGRATE** or remove |
| `dataSet.bias_input` | `BiasTypeEnum` values | 🔄 **USE** DS bias taxonomy |
| `dataSet.unit` | `VariableMetadata.unit` | 🔄 **USE** DS variable metadata |
| `SensitiveData` class | `SensitiveElement` + `Deidentification` | 🔄 **REPLACE** with DS classes |
| `GraphicsCollection` | `VariableMetadata` + visualization | 🔧 **KEEP** for model visualizations |
| `graphic` | (none) | ✅ **KEEP** for model visualizations |

**Critical Action**: Remove `dataSet` and `SensitiveData` classes; reference `data_sheets_schema:Dataset` in `ModelParameters`

### 3.8 Model Parameters

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `ModelParameters` class | (none - model-specific) | ✅ **KEEP** |
| `ModelParameters.model_architecture` | (none) | ✅ **KEEP** |
| `ModelParameters.data` | `Dataset` | 🔄 **CHANGE** range to DS Dataset |
| `ModelParameters.input_format` | (none for models) | ✅ **KEEP** |
| `ModelParameters.input_format_map` | (none) | ✅ **KEEP** |
| `ModelParameters.output_format` | (none) | ✅ **KEEP** |
| `ModelParameters.output_format_map` | (none) | ✅ **KEEP** |
| `KeyVal` class | (none) | ✅ **KEEP** for I/O formats |

### 3.9 Performance & Quantitative Analysis

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `QuantitativeAnalysis` | (none - model-specific) | ✅ **KEEP** |
| `performanceMetric` | (none - model-specific) | ✅ **KEEP** |
| `ConfidenceInterval` | (none - model-specific) | ✅ **KEEP** |
| All performance-related fields | (none) | ✅ **KEEP** - model-specific |

### 3.10 Considerations

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `Considerations` class | (various DS classes) | 🔧 **ENHANCE** with DS references |
| `User` | (none specific) | ✅ **KEEP** - model user focus |
| `UseCase` | `OtherTask` | ✅ **KEEP** MC version |
| `Limitation` | `DiscouragedUse` | ✅ **KEEP** MC version |
| `Tradeoff` | (none) | ✅ **KEEP** |
| `risk` | Ethics classes | 🔧 **KEEP** + reference DS ethics |
| (add) references to DS ethics | `EthicalReview`, `DataProtectionImpact` | ➕ **ADD** DS references |

### 3.11 HuggingFace / Community Integration

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `framework` | (related: DS has Software class) | ✅ **KEEP** |
| `framework_version` | `Software.version` | ✅ **KEEP** |
| `library_name` | (none) | ✅ **KEEP** |
| `pipeline_tag` | (none) | ✅ **KEEP** |
| `language` | `Dataset.language` | ✅ **ALIGNED** (different use) |
| `base_model` | (none) | ✅ **KEEP** |
| `tags` | `Dataset.keywords` | ✅ **ALIGNED** (different use) |
| `datasets` | (identifiers) | ✅ **KEEP** as simple identifiers |
| `metrics` | (identifiers) | ✅ **KEEP** |

### 3.12 Benchmark Integration

| Model Cards Class/Slot | Datasheets Equivalent | Action |
|------------------------|----------------------|--------|
| `Task` | (similar: DS has Task for datasets) | ✅ **KEEP** MC version |
| `BenchmarkDataset` | `Dataset` | ✅ **KEEP** MC version (lightweight) |
| `BenchmarkMetric` | (none) | ✅ **KEEP** |
| `BenchmarkSource` | `ExternalResource` | ✅ **KEEP** MC version |
| `BenchmarkResult` | (none) | ✅ **KEEP** |
| `ModelIndex` | (none) | ✅ **KEEP** |

All benchmark classes are **model-specific** and should be **retained** in model cards.

---

## 4. Gaps and Opportunities

### 4.1 What's in Model Cards but NOT in Datasheets

The following model cards elements are **model-specific** and appropriately have no datasheets equivalent:

#### Model Architecture & Parameters
- `model_architecture`: Specification of model architecture (e.g., "BERT-base with classification head")
- `ModelParameters` class: Container for model construction parameters
- `input_format` / `output_format`: Model I/O specifications
- `input_format_map` / `output_format_map`: Structured I/O format mappings
- `KeyVal` class: Key-value pairs for format specifications

#### Model Performance
- `QuantitativeAnalysis` class: Container for performance evaluation
- `performanceMetric` class: Performance metrics (accuracy, F1, AUC, etc.)
- `ConfidenceInterval` class: Statistical confidence bounds for metrics
- `threshold`: Decision thresholds for metrics
- `slice`: Data slice identifiers for sliced evaluation
- Performance-related graphics and visualizations

#### ML Framework & Deployment
- `framework`: ML framework (TensorFlow, PyTorch, JAX, Scikit-Learn)
- `framework_version`: Framework version
- `library_name`: Library for loading model (transformers, diffusers, timm)
- `pipeline_tag`: Task type for pipeline usage (text-generation, image-classification)
- `base_model`: Parent model identifier (for fine-tuned models)

#### Benchmark Integration (Papers with Code)
- `Task`: ML task specification for benchmarking
- `BenchmarkDataset`: Dataset reference for benchmark
- `BenchmarkMetric`: Benchmark metric result
- `BenchmarkSource`: Source of benchmark results
- `BenchmarkResult`: Complete benchmark entry
- `ModelIndex`: Papers with Code model-index structure

#### Model-Specific Metadata
- `model_category`: Category or classification of model type
- `schema_version`: Model card schema version tracking
- `bias_model`: Known biases in the model itself (distinct from data bias)
- `bias_output`: Known biases in model outputs
- `Tradeoff` class: Performance tradeoff documentation (specific to models)

#### Documentation
- `Citation` class with `CitationStyleEnum`: Formatted citations for the model (MLA, APA, Chicago, IEEE)
- `overview`: High-level model description (similar to description but model-focused)
- `documentation`: Detailed model usage guide

**Assessment**: All of these are **appropriate for model cards** and should be **retained**.

---

### 4.2 What's in Datasheets that Model Cards Should Consider Adopting

This section identifies datasheets elements that would significantly enhance model cards, organized by priority.

#### 🔴 **CRITICAL PRIORITY** (Essential for Harmonization)

##### 1. Comprehensive Dataset Documentation
**Datasheets Classes**: Entire `Dataset` class hierarchy (60+ classes)

**Current Gap**: Model cards has minimal dataset documentation (1 class, 7 fields)

**Recommendation**: **REPLACE** `dataSet` with reference to `data_sheets_schema:Dataset`

**Impact**:
- Enables comprehensive dataset documentation
- Standardizes dataset metadata across ecosystem
- Supports ethics, privacy, and legal compliance
- Eliminates need to reinvent dataset documentation

**Implementation**:
```yaml
ModelParameters:
  slots:
    - training_data:
        range: data_sheets_schema:Dataset
        multivalued: true
    - evaluation_data:
        range: data_sheets_schema:Dataset
        multivalued: true
```

##### 2. Structured Creator & Contributor Information
**Datasheets Classes**: `Person`, `Creator`, `Organization`, `CRediTRoleEnum`

**Current Gap**: Model cards has simple `owner` class with name and contact only

**Recommendation**: **REPLACE** `owner` with datasheets classes

**Impact**:
- Persistent identification (ORCID)
- Institutional affiliation tracking
- Precise contributor attribution (CRediT taxonomy)
- Interoperability with academic systems

**Implementation**:
```yaml
ModelDetails:
  slots:
    - creators:
        range: data_sheets_schema:Creator
        multivalued: true
    - contributors:
        range: data_sheets_schema:Person
        multivalued: true
```

##### 3. Comprehensive Licensing Documentation
**Datasheets Classes**: `LicenseAndUseTerms`, `IPRestrictions`, `ExportControlRegulatoryRestrictions`

**Current Gap**: Model cards has basic license support; lacks comprehensive legal documentation

**Recommendation**: **Reference** datasheets licensing classes for training data

**Impact**:
- Separation of model vs. data licensing
- IP restriction documentation
- Regulatory compliance (export controls)
- Legal clarity for deployment

**Implementation**:
```yaml
ModelDetails:
  slots:
    - model_licenses: # Keep for model
        range: License
    - data_licenses: # Reference DS for data
        range: data_sheets_schema:LicenseAndUseTerms
    - data_ip_restrictions:
        range: data_sheets_schema:IPRestrictions
```

##### 4. Ethics & Privacy Framework
**Datasheets Classes**: `EthicalReview`, `DataProtectionImpact`, `CollectionConsent`, `ConsentRevocation`, `HumanSubjectResearch`, `InformedConsent`, `ParticipantPrivacy`, `SensitiveElement`, `Deidentification`

**Current Gap**: Model cards has basic risk documentation; lacks systematic ethics framework

**Recommendation**: **REFERENCE** datasheets ethics/privacy classes for training data

**Impact**:
- Ethics review documentation (IRB)
- GDPR compliance (DPIA)
- Consent and notification documentation
- Human subjects research protections
- Systematic privacy assessment

**Implementation**:
```yaml
Considerations:
  slots:
    - data_ethical_reviews:
        range: data_sheets_schema:EthicalReview
    - data_protection_impacts:
        range: data_sheets_schema:DataProtectionImpact
```

---

#### 🟡 **HIGH PRIORITY** (Strongly Recommended)

##### 5. Provenance & Version Management
**Datasheets Slots**: `created_by`, `created_on`, `modified_by`, `last_updated_on`, `was_derived_from`

**Datasheets Classes**: `UpdatePlan`, `Erratum`, `VersionAccess`

**Current Gap**: Model cards has basic version support; lacks fine-grained provenance

**Recommendation**: **ADOPT** provenance slots from datasheets

**Impact**:
- Creator/modifier attribution
- Fine-grained temporal tracking
- Lineage documentation (fine-tuning, distillation)
- Update policy documentation
- Error tracking

**Implementation**:
```yaml
ModelDetails:
  slots:
    - created_by:
    - created_on:
    - modified_by:
    - last_updated_on:
    - was_derived_from:
```

##### 6. Funding Information
**Datasheets Classes**: `FundingMechanism`, `Grantor`, `Grant`

**Current Gap**: No funding documentation in model cards

**Recommendation**: **REFERENCE** datasheets funding classes

**Impact**:
- Research transparency
- Grant compliance
- Funding source attribution
- Conflict of interest disclosure

**Implementation**:
```yaml
ModelDetails:
  slots:
    - funding:
        range: data_sheets_schema:FundingMechanism
```

##### 7. Maintainer Information
**Datasheets Classes**: `Maintainer`

**Current Gap**: No dedicated maintainer documentation in model cards

**Recommendation**: **REFERENCE** datasheets `Maintainer` class

**Impact**:
- Operational clarity
- Contact information for issues
- Responsibility assignment
- Support expectations

**Implementation**:
```yaml
ModelDetails:
  slots:
    - maintainers:
        range: data_sheets_schema:Maintainer
```

---

#### 🟢 **MEDIUM PRIORITY** (Valuable Additions)

##### 8. Data Quality Documentation
**Datasheets Classes**: `DataAnomaly`, `MissingInfo`, `Erratum`

**Current Gap**: No structured data quality documentation in model cards

**Recommendation**: **REFERENCE** via Dataset class

**Impact**:
- Transparency about data quality issues
- Known anomaly documentation
- Missing information tracking
- Error correction history

##### 9. Collection & Preprocessing Documentation
**Datasheets Classes**: `InstanceAcquisition`, `CollectionMechanism`, `SamplingStrategy`, `DataCollector`, `CollectionTimeframe`, `PreprocessingStrategy`, `CleaningStrategy`, `LabelingStrategy`, `RawData`

**Current Gap**: No collection/preprocessing documentation in model cards

**Recommendation**: **REFERENCE** via Dataset class

**Impact**:
- Reproducibility
- Understanding of data provenance
- Transparency about data preparation
- Bias source identification

##### 10. Use History & Guidance
**Datasheets Classes**: `ExistingUse`, `UseRepository`, `DiscouragedUse`, `FutureUseImpact`

**Current Gap**: Model cards documents intended uses; doesn't reference data use history

**Recommendation**: **REFERENCE** via Dataset class

**Impact**:
- Understanding of prior data uses
- Alignment of model and data use cases
- Avoiding inappropriate uses
- Future impact assessment

##### 11. Distribution Policy
**Datasheets Classes**: `DistributionFormat`, `DistributionDate`, `ThirdPartySharing`

**Current Gap**: No distribution policy documentation in model cards

**Recommendation**: **REFERENCE** via Dataset class (for data distribution)

**Impact**:
- Clear data access information
- Format availability documentation
- Third-party sharing transparency

---

#### ⚪ **LOW PRIORITY** (Optional Enhancements)

##### 12. File Format & Technical Metadata (for Datasets)
**Datasheets Classes**: `FormatEnum`, `EncodingEnum`, `CompressionEnum`, `MediaTypeEnum`, `FormatDialect`, `VariableMetadata`

**Datasheets Slots**: `format`, `encoding`, `compression`, `media_type`, `hash`, `md5`, `sha256`, `bytes`, `is_tabular`, `variables`

**Current Gap**: No file format metadata in model cards

**Recommendation**: **REFERENCE** via Dataset class; **OPTIONALLY ADD** for model artifacts

**Impact**:
- Technical interoperability
- Integrity verification (checksums)
- Format compatibility checking
- Variable-level metadata (for tabular data)

##### 13. Model Artifact Format Metadata (Optional Extension)
**Opportunity**: Datasheets' technical metadata approach could inspire model artifact documentation

**Potential Addition**:
```yaml
ModelDetails:
  slots:
    - model_format:  # SavedModel, ONNX, TorchScript, etc.
    - model_file_size:
    - model_checksum:
```

**Impact**:
- Model format clarity
- Deployment compatibility
- Integrity verification for model files

##### 14. Demographic Fairness Analysis
**Datasheets Classes**: `Subpopulation`, `VulnerablePopulations`

**Current Gap**: General bias documentation; no structured demographic analysis

**Recommendation**: **REFERENCE** via Dataset class; **OPTIONALLY ADD** model-specific subgroup performance

**Impact**:
- Fairness analysis
- Vulnerable population identification
- Subgroup performance documentation

---

### 4.3 Priority Recommendations Summary

| Priority | Recommendation | Classes | Impact |
|----------|---------------|---------|--------|
| 🔴 **CRITICAL** | Replace `dataSet` with DS `Dataset` | 60+ classes | Comprehensive dataset docs |
| 🔴 **CRITICAL** | Replace `owner` with DS `Creator`/`Person` | 3 classes | Structured attribution |
| 🔴 **CRITICAL** | Reference DS licensing classes | 3 classes | Legal compliance |
| 🔴 **CRITICAL** | Reference DS ethics/privacy | 10+ classes | Ethical compliance |
| 🟡 **HIGH** | Adopt DS provenance metadata | Slots | Version tracking |
| 🟡 **HIGH** | Reference DS funding | 3 classes | Research transparency |
| 🟡 **HIGH** | Reference DS maintainers | 1 class | Operational clarity |
| 🟢 **MEDIUM** | Reference DS data quality | 3 classes | Transparency |
| 🟢 **MEDIUM** | Reference DS collection/preprocessing | 9 classes | Reproducibility |
| 🟢 **MEDIUM** | Reference DS use guidance | 4 classes | Use alignment |
| ⚪ **LOW** | Reference DS technical metadata | Multiple | Interoperability |

---

## 5. Harmonization Recommendations

This section provides specific, actionable technical recommendations for aligning the model cards and datasheets schemas.

### 5.1 Technical Approach: Import & Reference Pattern

**Recommended Strategy**: Model cards should **import** the datasheets schema and **reference** its classes for dataset-related documentation, rather than duplicating dataset documentation.

**Benefits**:
1. **Single Source of Truth**: Datasets are documented once (in datasheets format), referenced by multiple models
2. **Comprehensive Documentation**: Leverage datasheets' 60+ classes for dataset documentation
3. **Consistency**: Standardized dataset documentation across the ecosystem
4. **Maintainability**: Updates to datasheets benefit all model cards
5. **Interoperability**: Datasets documented with datasheets can be discovered and reused
6. **Separation of Concerns**: Clear distinction between model metadata and dataset metadata

### 5.2 Import Configuration

**Current Model Cards Schema Header**:
```yaml
id: https://w3id.org/linkml/modelcard
name: Model_Card
imports:
  - linkml:types
prefixes:
  modelcard: https://w3id.org/linkml/modelcard/
  linkml: https://w3id.org/linkml/
default_prefix: modelcard
```

**Proposed Harmonized Schema Header**:
```yaml
id: https://w3id.org/linkml/modelcard
name: Model_Card
description: |-
  Comprehensive LinkML schema for ML model cards,
  integrating with Datasheets for Datasets for comprehensive dataset documentation.

imports:
  - linkml:types
  - data_sheets_schema:schema/data_sheets_schema_all  # Import datasheets

prefixes:
  modelcard: https://w3id.org/linkml/modelcard/
  linkml: https://w3id.org/linkml/
  data_sheets_schema: https://w3id.org/bridge2ai/data-sheets-schema/

default_prefix: modelcard
```

### 5.3 Harmonization Action Plan

The following subsections detail 7 specific harmonization actions, each with current state, proposed changes, and implementation guidance.

---

#### **Action 1: Replace `owner` with Datasheets `Creator`**

**Rationale**: Datasheets has comprehensive, structured creator documentation with ORCID, CRediT roles, and organizational affiliations.

**Current State**:
```yaml
owner:
  description: Model owner or maintainer information
  slots:
    - name
    - contact
  slot_usage:
    name:
      description: Name of the owner (individual or organization)
    contact:
      description: Contact information (email, website, etc.)

ModelDetails:
  slots:
    - owners:
        range: owner
        multivalued: true
```

**Proposed Harmonized State**:
```yaml
# Remove owner class entirely
# Import from datasheets: Person, Creator, Organization, CRediTRoleEnum

ModelDetails:
  slots:
    - creators:
        range: data_sheets_schema:Creator
        multivalued: true
        description: |
          Model creators with comprehensive attribution.
          Uses datasheets Creator class which includes:
          - principal_investigator → Person (with ORCID, affiliation)
          - affiliation → Organization
          - CRediT contributor roles

    - contributors:
        range: data_sheets_schema:Person
        multivalued: true
        description: |
          Additional contributors to model development.
          Uses datasheets Person class with credit_roles (CRediT taxonomy).

    - funding:
        range: data_sheets_schema:FundingMechanism
        multivalued: true
        description: |
          Funding sources for model development.
          Links to Grantor and Grant classes in datasheets.
```

**Migration Guide for Existing Model Cards**:
```yaml
# OLD FORMAT
owners:
  - name: "Jane Doe"
    contact: "jane@example.com"
  - name: "ML Lab"
    contact: "ml-lab@university.edu"

# NEW FORMAT
creators:
  - principal_investigator:
      name: "Jane Doe"
      email: "jane@example.com"
      orcid: "0000-0001-2345-6789"
      affiliation:
        name: "University ML Lab"
    affiliation:
      name: "University ML Lab"

contributors:
  - name: "John Smith"
    email: "john@example.com"
    orcid: "0000-0002-3456-7890"
    credit_roles:
      - "Software"
      - "Validation"
```

**Benefits**:
- Persistent identification via ORCID
- Institutional affiliation tracking
- Precise contributor attribution via CRediT taxonomy
- Funding transparency
- Interoperability with academic systems (ORCID, institutional repositories)

---

#### **Action 2: Replace `dataSet` with Datasheets `Dataset` Reference**

**Rationale**: This is the **most critical** harmonization action. Datasheets provides comprehensive, production-ready dataset documentation (60+ classes); model cards has minimal dataset support (1 class, 7 fields).

**Current State**:
```yaml
dataSet:
  description: Information about a dataset used for training or evaluation
  slots:
    - name
    - description
    - link
    - sensitive
    - graphics
    - bias_input
    - unit

SensitiveData:
  slots:
    - sensitive_data

ModelParameters:
  slots:
    - data:
        range: dataSet
        multivalued: true
```

**Proposed Harmonized State**:
```yaml
# Remove dataSet and SensitiveData classes entirely
# Import Dataset from datasheets (includes 60+ related classes)

ModelParameters:
  slots:
    - training_data:
        range: data_sheets_schema:Dataset
        multivalued: true
        description: |
          Training datasets with comprehensive Datasheets for Datasets documentation.

          Each dataset should be fully documented following the datasheets standard:
          - Motivation: purposes, tasks, creators, funding
          - Composition: instances, subsets, anomalies, sensitive elements
          - Collection: acquisition, mechanisms, sampling, collectors, timeframes
          - Preprocessing: strategies for preprocessing, cleaning, labeling
          - Uses: existing uses, discouraged uses, future impacts
          - Distribution: formats, dates, licensing, IP restrictions
          - Maintenance: maintainers, update plans, version access
          - Ethics: ethical reviews, consent, privacy protections

          See: https://w3id.org/bridge2ai/data-sheets-schema

    - evaluation_data:
        range: data_sheets_schema:Dataset
        multivalued: true
        description: |
          Evaluation/validation datasets (documented with datasheets standard).

    - data_augmentation:
        range: string
        description: |
          Description of data augmentation techniques applied during training.

    - data_preprocessing_notes:
        range: string
        description: |
          Model-specific notes on data preprocessing beyond what's documented
          in the dataset's datasheets documentation.

    - data_weighting:
        range: string
        description: |
          Instance weighting or class balancing applied during training.
```

**Migration Guide for Existing Model Cards**:

Existing model cards using the simple `dataSet` class must create full datasheets documentation. This may seem like significant work, but provides **enormous value** for transparency, ethics, and legal compliance.

**Simple Migration (Minimal Compliance)**:
```yaml
# OLD FORMAT (minimal info)
data:
  - name: "IMDb Reviews"
    link: "https://ai.stanford.edu/~amaas/data/sentiment/"
    description: "Movie reviews for sentiment analysis"

# NEW FORMAT (minimal datasheets - basic compliance)
training_data:
  - id: "imdb-reviews-v1"
    name: "IMDb Movie Reviews"
    description: "50,000 movie reviews for binary sentiment classification"
    download_url: "https://ai.stanford.edu/~amaas/data/sentiment/"
    license: "Free for research and educational use"

    # Minimal required fields
    purposes:
      - description: "Sentiment analysis research"
    creators:
      - principal_investigator:
          name: "Andrew Maas"
          affiliation:
            name: "Stanford University"
```

**Comprehensive Migration (Best Practice)**:
```yaml
# NEW FORMAT (comprehensive datasheets - best practice)
training_data:
  - id: "imdb-reviews-v1"
    name: "IMDb Movie Reviews Dataset"
    description: "50,000 highly polar movie reviews for binary sentiment classification"
    download_url: "https://ai.stanford.edu/~amaas/data/sentiment/"
    page: "https://ai.stanford.edu/~amaas/data/sentiment/"
    doi: "10.18653/v1/P11-1015"

    # Provenance
    created_on: "2011-06-19"
    version: "1.0"

    # Licensing
    license: "Free for research and educational use"
    license_and_use_terms:
      description: "Dataset is provided for research purposes only"

    # Format
    format: CSV
    encoding: UTF-8
    is_tabular: true
    bytes: 84125825

    # Motivation
    purposes:
      - description: "Enable sentiment analysis research with highly polar reviews"
    tasks:
      - description: "Binary sentiment classification"
    creators:
      - principal_investigator:
          name: "Andrew L. Maas"
          orcid: "0000-0002-xxxx-xxxx"
          affiliation:
            name: "Stanford University, Computer Science Department"

    # Composition
    instances:
      - description: "Individual movie reviews from IMDb"
        instance_count: 50000
    subsets:
      - name: "train"
        description: "Training set"
        size: 25000
      - name: "test"
        description: "Test set"
        size: 25000
    splits:
      - name: "train"
        description: "25,000 labeled reviews for training"
      - name: "test"
        description: "25,000 labeled reviews for testing"

    # Collection
    acquisition_methods:
      - description: "Scraped from IMDb website"
    collection_timeframes:
      - description: "Reviews from 2001-2010"

    # Sensitive Data
    sensitive_elements:
      - sensitive_elements_present: false
    is_deidentified:
      identifiable_elements_present: false
      description: "Reviews are public and authors are pseudonymous (IMDb usernames)"

    # Uses
    existing_uses:
      - description: "Widely used for sentiment analysis benchmarks"
    discouraged_uses:
      - description: "Should not be used for inferring real individual opinions"
```

**Benefits**:
- **Comprehensive dataset documentation** (motivation, composition, collection, ethics, etc.)
- **Standardized documentation** (Datasheets for Datasets is widely recognized)
- **Reusability**: Dataset documented once, referenced by multiple models
- **Ethics & privacy**: Proper documentation of sensitive data, consent, ethics review
- **Legal compliance**: Licensing, IP restrictions, regulatory restrictions
- **Transparency**: Collection methodology, preprocessing, quality issues
- **Interoperability**: Works with dataset catalogs, repositories

**Backward Compatibility**: Provide migration tools to convert simple `dataSet` to datasheets format.

---

#### **Action 3: Enhance Licensing with Datasheets Classes**

**Rationale**: Separate model licensing from data licensing; enable comprehensive legal documentation.

**Current State**:
```yaml
License:
  slots:
    - identifier  # SPDX
    - custom_text

ModelDetails:
  slots:
    - licenses:
        range: License
        multivalued: true
```

**Proposed Harmonized State**:
```yaml
# Keep License class for model artifacts
License:
  description: License for model artifacts (code, weights, architecture)
  slots:
    - identifier
    - custom_text
  slot_usage:
    identifier:
      description: SPDX license identifier (e.g., 'Apache-2.0', 'MIT')
    custom_text:
      description: Custom license text (when SPDX not applicable)

ModelDetails:
  slots:
    - model_licenses:
        range: License
        multivalued: true
        description: |
          Licenses for model artifacts (weights, architecture, inference code).
          Use SPDX identifiers when possible.

    - training_data_licenses:
        range: data_sheets_schema:LicenseAndUseTerms
        multivalued: true
        description: |
          Licenses and use terms for training data.
          Reference Dataset.license_and_use_terms in datasheets documentation.

    - data_ip_restrictions:
        range: data_sheets_schema:IPRestrictions
        multivalued: true
        description: |
          Third-party intellectual property restrictions on training data.
          Examples: proprietary data, licensed data requiring fees.

    - regulatory_restrictions:
        range: data_sheets_schema:ExportControlRegulatoryRestrictions
        multivalued: true
        description: |
          Export controls or regulatory restrictions.
          Examples: ITAR, EAR, dual-use technology restrictions.
```

**Usage Example**:
```yaml
model_details:
  model_licenses:
    - identifier: "Apache-2.0"

  training_data_licenses:
    - description: |
        Training data includes:
        - Public domain: 70%
        - CC-BY-4.0: 20%
        - Proprietary research license: 10%
      links:
        - "https://creativecommons.org/licenses/by/4.0/"
      constraints: |
        Proprietary data cannot be redistributed.
        Models trained on this data can be used for research only.

  data_ip_restrictions:
    - description: "10% of training data has third-party IP restrictions"
      third_party_licenses:
        - "Research-only license from Data Provider Corp"
      fees: "No fees for research use; commercial use requires negotiation"

  regulatory_restrictions:
    - description: "No export control restrictions"
      jurisdictions: []
```

**Benefits**:
- Clear separation: model vs. data licensing
- Comprehensive legal documentation
- IP restriction transparency
- Regulatory compliance support (ITAR, EAR)
- Risk assessment for commercial deployment

---

#### **Action 4: Enhance Ethics with Datasheets References**

**Rationale**: Separate model ethics from data ethics; leverage datasheets' comprehensive ethics framework for data.

**Current State**:
```yaml
risk:
  slots:
    - name
    - mitigation_strategy

Considerations:
  slots:
    - ethical_considerations:
        range: risk
        multivalued: true
```

**Proposed Harmonized State**:
```yaml
# Enhance risk class with categories
risk:
  description: Model-specific risk (deployment, fairness, safety, environmental)
  slots:
    - name
    - risk_category
    - mitigation_strategy
    - residual_risk
  slot_usage:
    risk_category:
      description: Category of risk
      range: RiskCategoryEnum
    residual_risk:
      description: Remaining risk after mitigation

RiskCategoryEnum:
  permissible_values:
    Fairness:
      description: Fairness and bias concerns in model predictions
    Safety:
      description: Safety risks from model outputs or behavior
    Privacy:
      description: Privacy risks (memorization, membership inference, model inversion)
    Environmental:
      description: Environmental impact (energy consumption, carbon emissions)
    Operational:
      description: Operational risks (reliability, robustness, failure modes)
    Security:
      description: Security vulnerabilities (adversarial attacks, poisoning)
    Misuse:
      description: Potential for malicious use or abuse
    Hallucination:
      description: Generation of false or misleading information (for generative models)

Considerations:
  slots:
    - model_ethical_considerations:
        range: risk
        multivalued: true
        description: |
          Model-specific ethical concerns and risks.
          Focus on model behavior, outputs, and deployment.

    - data_ethical_reviews:
        range: data_sheets_schema:EthicalReview
        multivalued: true
        description: |
          Ethical reviews conducted for training/evaluation data.
          Reference Dataset.ethical_reviews in datasheets documentation.
          Includes IRB approvals, ethics board reviews.

    - data_protection_impacts:
        range: data_sheets_schema:DataProtectionImpact
        multivalued: true
        description: |
          Data protection impact assessments for training data.
          Reference Dataset.data_protection_impacts in datasheets documentation.
          GDPR DPIA or equivalent.

    - human_subjects_considerations:
        description: |
          Notes on human subjects research protections for training data.
          Reference Dataset human subjects classes in datasheets documentation:
          - HumanSubjectResearch
          - InformedConsent
          - CollectionConsent
          - ParticipantPrivacy
        range: string
```

**Usage Example**:
```yaml
considerations:
  model_ethical_considerations:
    - name: "Fairness across demographic groups"
      risk_category: Fairness
      mitigation_strategy: |
        Evaluated performance across demographic subgroups.
        Applied bias mitigation during post-processing.
      residual_risk: |
        Some performance disparity remains for underrepresented groups.

    - name: "Training data memorization"
      risk_category: Privacy
      mitigation_strategy: |
        Applied differential privacy during training (ε=8).
        Conducted membership inference attack evaluation.
      residual_risk: |
        Small memorization risk remains for rare examples.

  data_ethical_reviews:
    - ethical_review_conducted: true
      description: "IRB approval obtained for use of medical records"
      review_board: "University Medical Center IRB"
      approval_number: "IRB-2023-12345"
      approval_date: "2023-03-15"

  data_protection_impacts:
    - data_protection_impact_assessment_conducted: true
      description: "GDPR DPIA conducted for patient data"
      risks_identified:
        - "Re-identification risk from quasi-identifiers"
        - "Inference of sensitive attributes"
      mitigation_measures:
        - "K-anonymity (k=10) applied"
        - "Suppression of rare values"
        - "Access controls and audit logging"
```

**Benefits**:
- **Separation of concerns**: Model ethics (model cards) vs. data ethics (datasheets)
- **Comprehensive ethics documentation** for both model and data
- **Regulatory compliance**: IRB, GDPR, ethics boards
- **Risk categorization**: Structured risk taxonomy
- **Mitigation documentation**: Clear documentation of risk mitigation
- **Residual risk transparency**: Honest assessment of remaining risks

---

#### **Action 5: Adopt Provenance & Versioning from Datasheets**

**Rationale**: Enhanced temporal and attribution metadata for better version tracking and lineage documentation.

**Current State**:
```yaml
Version:
  slots:
    - name
    - date
    - diff
```

**Proposed Harmonized State**:
```yaml
# Enhanced Version class
Version:
  slots:
    - name
    - date
    - diff
    - created_by
    - released_by
    - changelog_url
  slot_usage:
    name:
      description: Version identifier (e.g., '1.0.0', 'v2', 'beta')
    date:
      description: Release date of this version
      range: date
    diff:
      description: Summary of changes from previous version
    created_by:
      description: Person or system that created this version
      range: string
    released_by:
      description: Person who released/published this version
      range: string
    changelog_url:
      description: URL to detailed changelog or release notes
      range: uri

# Add provenance to ModelDetails
ModelDetails:
  slots:
    # Existing slots
    - name
    - overview
    - documentation
    - creators
    - version
    - licenses

    # New provenance slots (from datasheets)
    - created_on:
        range: datetime
        description: When model development began or initial version was created

    - created_by:
        description: Initial model creator(s)
        range: string

    - last_updated_on:
        range: datetime
        description: When model was last modified or retrained

    - modified_by:
        description: Person or team who last modified the model
        range: string

    - issued:
        range: datetime
        description: When model was officially published or released

    - was_derived_from:
        range: uri
        multivalued: true
        description: |
          Parent model(s) this model was derived from.
          Examples:
          - Base model for fine-tuning: "bert-base-uncased"
          - Teacher model for distillation: "gpt-4-large"
          - Pretrained model for transfer learning

    - update_plan:
        description: |
          Plan for model updates, retraining, and maintenance.
          Examples: retraining frequency, triggers for retraining, deprecation timeline.
        range: string

    - known_issues:
        description: Known issues, bugs, or errors in the model
        multivalued: true
        range: string

    - issue_tracker:
        description: URL to issue tracker or bug reports
        range: uri
```

**Usage Example**:
```yaml
model_details:
  name: "sentiment-classifier-v2"

  version:
    name: "2.1.0"
    date: "2025-11-15"
    diff: |
      - Improved accuracy on negation handling (+3% on NegEx benchmark)
      - Fixed bias in handling sarcasm
      - Reduced model size by 20% through pruning
    created_by: "ML Engineering Team"
    released_by: "Jane Doe"
    changelog_url: "https://github.com/org/model/releases/v2.1.0"

  created_on: "2024-06-01T00:00:00Z"
  created_by: "Jane Doe, ML Team"
  last_updated_on: "2025-11-10T00:00:00Z"
  modified_by: "John Smith"
  issued: "2025-11-15T00:00:00Z"

  was_derived_from:
    - "https://huggingface.co/bert-base-uncased"
    - "https://github.com/org/model/releases/v2.0.0"

  update_plan: |
    Model will be retrained quarterly or when:
    - Training data is updated with 10,000+ new examples
    - Performance drops below 90% accuracy on validation set
    - Critical bias or fairness issue is identified

  known_issues:
    - "Struggles with double negatives (e.g., 'not bad' misclassified as negative)"
    - "Lower accuracy on reviews with heavy sarcasm (75% vs 92% overall)"

  issue_tracker: "https://github.com/org/model/issues"
```

**Benefits**:
- **Fine-grained temporal tracking**: Creation, modification, publication dates
- **Attribution**: Who created, modified, released the model
- **Lineage documentation**: Parent models for fine-tuning, distillation, transfer learning
- **Update transparency**: Clear update policy
- **Issue tracking**: Known problems and bug reports
- **Changelog integration**: Link to detailed release notes

---

#### **Action 6: Add Funding Information from Datasheets**

**Rationale**: Research transparency, grant compliance, funding source attribution.

**Current State**: No funding support in model cards

**Proposed Harmonized State**:
```yaml
ModelDetails:
  slots:
    # Existing slots
    - name
    - overview
    - creators

    # New funding slot (reference datasheets)
    - funding:
        range: data_sheets_schema:FundingMechanism
        multivalued: true
        description: |
          Funding sources for model development.
          Uses datasheets FundingMechanism which links to Grantor and Grant.
```

**Datasheets Classes Referenced**:
```yaml
# From datasheets schema
FundingMechanism:
  slots:
    - funding_source: string
    - grantors: → Grantor (multivalued)
    - grants: → Grant (multivalued)

Grantor:
  slots:
    - name: string (e.g., "National Science Foundation")
    - organization: → Organization

Grant:
  slots:
    - grant_number: string
    - grant_title: string
    - grant_amount: float
    - grant_period: string
```

**Usage Example**:
```yaml
model_details:
  funding:
    - funding_source: "Federal research grant and industry partnership"
      grantors:
        - name: "National Science Foundation"
          organization:
            name: "NSF"
        - name: "Tech Company Research"
          organization:
            name: "Tech Corp"
      grants:
        - grant_number: "NSF-1234567"
          grant_title: "Fair and Robust ML for Healthcare"
          grant_amount: 500000.00
          grant_period: "2023-2026"
        - grant_number: "TC-AI-2024"
          grant_title: "Industry Research Partnership"
```

**Benefits**:
- **Research transparency**: Clear funding source disclosure
- **Grant compliance**: Required for many federal grants (NSF, NIH, etc.)
- **Conflict of interest**: Disclosure of industry funding
- **Attribution**: Credit to funding agencies
- **Reproducibility**: Funding information aids reproducibility

---

#### **Action 7: Add Maintainer Information from Datasheets**

**Rationale**: Operational clarity, contact for issues, responsibility assignment.

**Current State**: No dedicated maintainer documentation in model cards

**Proposed Harmonized State**:
```yaml
ModelDetails:
  slots:
    # Existing slots
    - creators
    - documentation

    # New maintainer slot (reference datasheets)
    - maintainers:
        range: data_sheets_schema:Maintainer
        multivalued: true
        description: |
          Model maintainers responsible for updates, bug fixes, and support.
          Uses datasheets Maintainer class.
```

**Datasheets Class Referenced**:
```yaml
# From datasheets schema
Maintainer:
  slots:
    - name: string
    - contact: string (email, URL, etc.)
    - organization: → Organization
    - role: string (e.g., "Primary maintainer", "Support contact")
```

**Usage Example**:
```yaml
model_details:
  creators:
    - principal_investigator:
        name: "Dr. Jane Doe"
        email: "jane@university.edu"

  maintainers:
    - name: "ML Operations Team"
      contact: "ml-ops@company.com"
      organization:
        name: "Company AI Lab"
      role: "Primary maintainer (24/7 support)"

    - name: "Dr. Jane Doe"
      contact: "jane@university.edu"
      organization:
        name: "University ML Lab"
      role: "Research contact"
```

**Benefits**:
- **Operational clarity**: Who maintains the model
- **Contact information**: How to report issues
- **Responsibility**: Clear assignment of maintenance duties
- **Support expectations**: Who provides support and at what level
- **Separation from creators**: Creator ≠ maintainer (important for long-term projects)

---

### 5.4 Migration Strategy

Implementing these harmonization actions requires careful migration planning to minimize disruption.

#### **Phase 1: Additive Changes (Months 1-3)**

**Objective**: Add datasheets imports and new classes without breaking existing model cards.

**Actions**:
1. Add datasheets import to schema
2. Add new slots to `ModelDetails` (created_on, modified_by, funding, maintainers, etc.)
3. Document new classes and usage patterns
4. Mark old classes (`owner`, `dataSet`) as **deprecated** but still functional

**Impact**: **Non-breaking** - existing model cards continue to work

#### **Phase 2: Migration Tools & Documentation (Months 3-4)**

**Objective**: Provide tools and guidance for migrating to harmonized schema.

**Actions**:
1. Create migration scripts:
   - `owner` → `Creator`/`Person` converter
   - `dataSet` → `Dataset` stub generator (with prompt for full documentation)
2. Create migration guide with examples
3. Create templates for common scenarios
4. Provide validation tools

**Impact**: **Non-breaking** - migration is optional

#### **Phase 3: Gradual Adoption (Months 4-9)**

**Objective**: Encourage adoption of harmonized schema.

**Actions**:
1. Migrate example model cards
2. Update documentation to show harmonized patterns
3. Provide support for migration
4. Collect feedback and refine

**Impact**: **Non-breaking** - migration is encouraged but optional

#### **Phase 4: Deprecation (Months 9-12)**

**Objective**: Phase out deprecated classes.

**Actions**:
1. Announce deprecation timeline (e.g., 12 months)
2. Emit warnings for deprecated class usage
3. Provide prominent migration guidance
4. Ensure all tools support harmonized schema

**Impact**: **Breaking (with notice)** - deprecated classes will be removed in next major version

#### **Phase 5: Removal (Month 12+)**

**Objective**: Release major version without deprecated classes.

**Actions**:
1. Release v2.0 of model cards schema
2. Remove `owner`, `dataSet`, `SensitiveData` classes
3. Require harmonized schema for new model cards
4. Continue supporting v1.x for legacy model cards

**Impact**: **Breaking** - requires migration for new model cards

#### **Backward Compatibility Considerations**

**Dual Format Support (Transition Period)**:
```yaml
# Schema v1.5 (transition)
ModelDetails:
  slots:
    # Deprecated (still works, but discouraged)
    - owners:
        range: owner
        deprecated: true
        deprecated_element_has_exact_replacement: creators

    # New (recommended)
    - creators:
        range: data_sheets_schema:Creator
```

**Validation Tool Behavior**:
- **Warn** on deprecated class usage
- **Suggest** migration to new classes
- **Allow** both formats during transition period
- **Enforce** new format in major version

**Documentation Updates**:
- Clearly mark deprecated classes
- Provide side-by-side examples (old vs. new)
- Link to migration guide
- Show benefits of new approach

---

### 5.5 Implementation Roadmap

Detailed timeline for harmonization implementation.

#### **Month 1: Planning & Design**
- Finalize harmonization plan
- Review datasheets schema compatibility
- Design import structure
- Create technical specification

#### **Month 2: Schema Updates**
- Add datasheets import
- Add new classes and slots
- Update documentation
- Mark deprecated elements

**Deliverable**: Updated schema (v1.5) with datasheets import

#### **Month 3: Tooling Development**
- Create migration scripts
- Build validation tools
- Develop testing framework
- Create example model cards

**Deliverable**: Migration tooling

#### **Month 4: Documentation**
- Write migration guide
- Create tutorials
- Document best practices
- Build template library

**Deliverable**: Comprehensive documentation

#### **Month 5-6: Pilot Testing**
- Migrate select model cards
- Test with real users
- Collect feedback
- Refine tools and docs

**Deliverable**: Pilot results and refinements

#### **Month 7-9: Community Adoption**
- Announce harmonized schema
- Provide migration support
- Host workshops/webinars
- Build community examples

**Deliverable**: Growing adoption

#### **Month 10-12: Deprecation Phase**
- Announce deprecation timeline
- Ramp up warnings
- Finalize v2.0 specification
- Prepare for removal

**Deliverable**: Deprecation plan and v2.0-alpha

#### **Month 12+: Major Release**
- Release v2.0 (without deprecated classes)
- Maintain v1.x LTS for legacy support
- Continue community support

**Deliverable**: Model cards schema v2.0

---

### 5.6 Benefits Summary

| Stakeholder | Benefits |
|-------------|----------|
| **Model Card Authors** | - Comprehensive dataset documentation without reinvention<br>- Standardized ethics/privacy documentation<br>- Better legal compliance support<br>- Clear guidance on what to document |
| **Dataset Providers** | - Single source of truth for dataset metadata<br>- Reuse across multiple models<br>- Standardized documentation format |
| **Model Users** | - Complete transparency about training data<br>- Better understanding of model provenance<br>- Easier assessment of ethical/legal compliance<br>- Informed decision-making |
| **Researchers** | - Reproducibility through comprehensive documentation<br>- Standardized benchmarking<br>- Dataset discoverability<br>- Citation support |
| **Organizations** | - Legal compliance (GDPR, IRB, etc.)<br>- Risk assessment support<br>- Audit trails<br>- Governance workflows |
| **Ecosystem** | - Reduced duplication<br>- Better interoperability<br>- Clear separation of concerns (model vs. data)<br>- Alignment with established standards |

---

## 6. Conclusion

### Summary of Findings

This analysis examined the alignment between two complementary LinkML schemas: Model Cards (focused on ML models) and Datasheets for Datasets (focused on datasets). Key findings:

1. **Complementary Design**: The schemas address different primary concerns with overlapping areas in dataset documentation, licensing, creators, and ethics.

2. **Alignment Varies by Category**:
   - **Strong** (90%+): Basic metadata (name, description, id)
   - **Moderate** (50-89%): Creators/ownership, licensing, versioning
   - **Weak** (<50%): Dataset documentation, ethics/privacy

3. **Critical Gap**: Model cards has minimal dataset documentation (1 class, 7 fields); datasheets has comprehensive documentation (60+ classes, 200+ fields).

4. **Harmonization is Highly Feasible**: Both use LinkML, have compatible patterns, and can be integrated through import/reference.

### Key Recommendations

**CRITICAL** (Must Do):
1. **Import datasheets schema** into model cards
2. **Replace `dataSet` with datasheets `Dataset` reference** (most important action)
3. **Replace `owner` with datasheets `Creator`/`Person`/`Organization`**
4. **Reference datasheets ethics/privacy classes** for training data
5. **Reference datasheets licensing classes** for comprehensive legal documentation

**HIGH** (Should Do):
6. **Adopt datasheets provenance metadata** (created_by, modified_by, was_derived_from)
7. **Reference datasheets funding classes** for research transparency
8. **Reference datasheets maintainer classes** for operational clarity

**MEDIUM** (Nice to Have):
9. Reference datasheets data quality, collection, and use guidance classes
10. Reference datasheets distribution policy classes

### Strategic Impact

**For the ML Documentation Ecosystem**:
- Creates interoperable model and dataset documentation
- Eliminates duplication of effort
- Establishes clear separation of concerns (models vs. datasets)
- Aligns with established academic standards (Datasheets for Datasets framework)

**For Practitioners**:
- Single source of truth for datasets (document once, reference many times)
- Comprehensive documentation with clear templates
- Better tools for compliance (ethics, privacy, legal)
- Improved transparency and reproducibility

**For Organizations**:
- Reduced documentation burden
- Better governance and audit trails
- Legal and regulatory compliance support
- Risk assessment and management

### Implementation Path Forward

The harmonization can be implemented gradually:
1. **Phase 1** (Months 1-3): Additive changes (import datasheets, add new classes)
2. **Phase 2** (Months 3-4): Migration tools and documentation
3. **Phase 3** (Months 4-9): Gradual adoption with community support
4. **Phase 4** (Months 9-12): Deprecation of old classes
5. **Phase 5** (Month 12+): Major release (v2.0) without deprecated classes

### Conclusion

The model cards and datasheets schemas are **highly compatible and complementary**. By importing datasheets and referencing its comprehensive dataset documentation classes, model cards can:

- Maintain its focus on model-specific documentation
- Leverage proven, comprehensive dataset documentation standards
- Eliminate duplication and reduce maintenance burden
- Improve transparency, ethics, and legal compliance
- Create a more interoperable ML documentation ecosystem

**The recommended harmonization represents a win-win**: Model cards gains comprehensive dataset documentation capabilities without reinventing the wheel, while datasheets becomes the standard for dataset documentation referenced across the ML ecosystem.

---

## Appendices

### Appendix A: Schema Sizes & Complexity

| Metric | Model Cards | Datasheets |
|--------|-------------|------------|
| **Lines of Code** | 967 | 22,459 |
| **Classes** | 27 | 60+ |
| **Enums** | 1 | 10+ |
| **Slots** | 90+ | 200+ |
| **Primary Focus** | ML models | Datasets |
| **Maturity** | Recently enhanced | Production-ready |

### Appendix B: Alignment Score Summary

| Category | Overlap | Coverage | Score |
|----------|---------|----------|-------|
| Basic metadata | 3/3 fields | 100% | ✅ Strong |
| Creators | 2/7 fields | 29% | 🟨 Moderate |
| Licensing | 2/5 fields | 40% | 🟨 Moderate |
| Datasets | 3/60+ fields | <5% | 🟥 Very Weak |
| Ethics/Privacy | 1/10+ fields | <10% | 🟥 Weak |
| Provenance | 2/7 fields | 29% | 🟨 Moderate |
| Format/Technical | 0/15 fields | 0% | ❌ None |

**Overall Alignment**: ~25% (excluding model-specific elements)

### Appendix C: Reference Links

**Model Cards Schema**:
- Repository: `bridge2ai/model-card-schema`
- Schema: `src/linkml/modelcards.yaml`
- Documentation: `CLAUDE.md`, `SCHEMA_ENHANCEMENT_SUMMARY.md`

**Datasheets Schema**:
- Repository: `bridge2ai/data-sheets-schema`
- Schema: `src/data_sheets_schema/schema/data_sheets_schema_all.yaml`
- Framework: "Datasheets for Datasets" (Gebru et al., 2018)

**Standards Referenced**:
- LinkML: https://linkml.io/
- CRediT Taxonomy: https://credit.niso.org/
- SPDX License List: https://spdx.org/licenses/
- ORCID: https://orcid.org/
- GDPR: https://gdpr.eu/
- Common Rule (HHS): https://www.hhs.gov/ohrp/regulations-and-policy/regulations/common-rule/

### Appendix D: Glossary

- **CRediT**: Contributor Roles Taxonomy - standardized taxonomy of 14 contributor roles
- **DPIA**: Data Protection Impact Assessment - GDPR-required assessment of privacy risks
- **Datasheets for Datasets**: Framework for documenting datasets (Gebru et al., 2018)
- **IRB**: Institutional Review Board - ethics review board for human subjects research
- **LinkML**: Linked Data Modeling Language - framework for data modeling
- **Model Cards**: Framework for documenting ML models (Mitchell et al., 2019)
- **ORCID**: Open Researcher and Contributor ID - persistent identifier for researchers
- **SPDX**: Software Package Data Exchange - standard format for license identifiers

---

**End of Alignment Analysis Report**

**Version**: 1.0
**Date**: November 19, 2025
**Status**: Complete
