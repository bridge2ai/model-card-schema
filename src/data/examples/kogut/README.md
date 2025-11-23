# KOGUT Template Examples

This directory contains examples demonstrating the KOGUT template extensions to the Model Cards schema.

## Files

### `climate-model-kogut.yaml`

Complete model card demonstrating all KOGUT template features for a DOE scientific model (ClimateNet-v2).

**Key KOGUT Extensions Demonstrated:**

1. **Enhanced Contributor Attribution** (`contributors` in `model_details`)
   - Role-based attribution (developed_by, contributed_by, maintained_by, funded_by)
   - ORCID identifiers
   - Email and affiliation tracking

2. **Version Extensions** (`version` in `model_details`)
   - `last_updated` timestamp
   - `superseded_by` field for version tracking

3. **License Extensions** (`licenses` in `model_details`)
   - `license_name` for custom licenses
   - `license_link` for license URL

4. **Compute Infrastructure** (`compute_infrastructure` in `model_parameters`)
   - Hardware description (DOE facilities: NERSC, ALCF, OLCF)
   - Detailed hardware list (GPUs, clusters, interconnects)
   - Software stack and dependencies (pip/conda/spack)
   - Training speed metrics

5. **Training Procedure** (`training_procedure` in `model_parameters`)
   - Detailed methodology
   - Reproducibility information with:
     - Random seed
     - Environment configuration
     - Pipeline URL
     - Complete hyperparameters (optimizer, learning rate, batch size, epochs, etc.)

6. **Hyperparameters** (nested in `reproducibility_info`)
   - Model initialization
   - Optimizer and loss function
   - Training epochs/steps
   - Batch size and learning rate
   - Optimization techniques
   - Prompting templates (for LLMs)
   - Fine-tuning methods (LoRA, adapters, etc.)

7. **Evaluation Procedure** (`evaluation_procedure` in `quantitative_analysis`)
   - Benchmarks and test datasets
   - Baseline comparisons
   - State-of-the-art (SOTA) comparison
   - Uncertainty quantification methodology
   - Whether evaluation data is separate/external

8. **Out-of-Scope Uses** (`out_of_scope_uses` in `considerations`)
   - Explicitly prohibited or discouraged uses
   - Clear guidance on inappropriate applications

9. **Mission Relevance** (`mission_relevance` at root level)
   - DOE project identifier
   - DOE facility (NERSC Perlmutter, ALCF Polaris, OLCF Frontier, etc.)
   - Funding source (grants, DOE offices)
   - Description of mission relevance to DOE

10. **Usage Documentation** (`usage_documentation` at root level)
    - Installation instructions (conda, docker, NERSC modules)
    - Training configuration (SLURM scripts, configs)
    - Inference configuration (batch processing)
    - Code examples with language specification

## Schema Coverage

This example demonstrates **100% coverage** of KOGUT template fields:

| KOGUT Section | Schema Mapping | Example Location |
|---------------|----------------|------------------|
| Model Details → Description | `model_details.short_description` | Line 12 |
| Model Details → Developed By | `model_details.contributors` (role: developed_by) | Lines 38-42 |
| Model Details → Shared By | `model_details.contributors` (role: contributed_by) | Lines 44-48 |
| Model Details → Model Type | `model_parameters.model_architecture` | Lines 89-115 |
| Model Details → Version | `model_details.version` | Lines 60-68 |
| Model Details → License | `model_details.licenses` | Lines 70-73 |
| Compute Infrastructure → Hardware | `model_parameters.compute_infrastructure.hardware_list` | Lines 142-145 |
| Compute Infrastructure → Software | `model_parameters.compute_infrastructure.software_dependencies` | Lines 151-165 |
| Training → Dataset | `model_parameters.data` | Lines 112-123 |
| Training → Procedure | `model_parameters.training_procedure` | Lines 172-246 |
| Training → Reproducibility | `training_procedure.reproducibility_info` | Lines 222-246 |
| Evaluation → Metrics | `quantitative_analysis.performance_metrics` | Lines 254-283 |
| Evaluation → Procedure | `quantitative_analysis.evaluation_procedure` | Lines 286-310 |
| Uses → Intended Uses | `considerations.use_cases` | Lines 316-320 |
| Uses → Out-of-Scope | `considerations.out_of_scope_uses` | Lines 357-369 |
| Limitations | `considerations.limitations` | Lines 322-333 |
| Ethical Considerations | `considerations.ethical_considerations` | Lines 342-355 |
| DOE Mission Relevance | `mission_relevance` | Lines 387-407 |
| Usage Documentation | `usage_documentation` | Lines 411-548 |

## Key Differences from Standard Model Cards

### Before (Standard Model Card)
```yaml
model_details:
  owners:
    - name: "Jane Doe"
      contact: "jane.doe@lbl.gov"
```

### After (KOGUT Extended)
```yaml
model_details:
  contributors:
    - name: "Jane Doe"
      role: developed_by
      email: "jane.doe@lbl.gov"
      orcid: "https://orcid.org/0000-0002-1234-5678"
      affiliation: "Lawrence Berkeley National Laboratory"
```

### Before (No compute infrastructure)
```yaml
model_parameters:
  model_architecture: "ResNet-50"
```

### After (KOGUT with compute infrastructure)
```yaml
model_parameters:
  model_architecture: "ResNet-50"
  compute_infrastructure:
    hardware_list:
      - "64 nodes × 4 NVIDIA A100 40GB GPUs"
    software_dependencies: |
      pytorch=2.1.0
      horovod=0.28.1
      ...
```

## Validation

Validate this example against the schema:

```bash
# Lint the schema
poetry run linkml-lint src/linkml/modelcards.yaml

# Generate datamodel (validates schema)
poetry run gen-project -d src/data/examples/kogut src/linkml/modelcards.yaml
```

## Use Cases

This KOGUT example is appropriate for:

1. **DOE Scientific Models**
   - Climate models (E3SM, CESM, MPAS)
   - Materials science models
   - Fusion/plasma physics models
   - Bioinformatics models

2. **HPC/Supercomputing Applications**
   - Models trained on DOE facilities (NERSC, ALCF, OLCF)
   - Large-scale distributed training
   - Petabyte-scale datasets

3. **Reproducible Science**
   - Complete environment specifications
   - Random seeds and configurations
   - Training pipeline URLs
   - Detailed hyperparameters

4. **DOE Mission-Aligned Projects**
   - Office of Science grants
   - BER, ASCR, NP, HEP programs
   - Facility-specific documentation

## Migration from Standard Model Cards

To migrate an existing model card to KOGUT format:

1. **Add contributor information:**
   ```yaml
   contributors:
     - name: "..."
       role: developed_by  # or contributed_by, maintained_by, funded_by
       orcid: "..."
   ```

2. **Add compute infrastructure:**
   ```yaml
   compute_infrastructure:
     hardware_list: [...]
     software_dependencies: "..."
   ```

3. **Add reproducibility info:**
   ```yaml
   training_procedure:
     reproducibility_info:
       random_seed: 42
       hyperparameters: {...}
   ```

4. **Add DOE mission relevance:**
   ```yaml
   mission_relevance:
     doe_facility: "NERSC Perlmutter"
     doe_project: "..."
   ```

5. **Add usage documentation:**
   ```yaml
   usage_documentation:
     installation_instructions: "..."
     code_examples: [...]
   ```

## References

- **KOGUT Template:** `/data/input_docs/KOGUT/model-card.md`
- **Schema:** `/src/linkml/modelcards.yaml`
- **Gap Analysis:** See commit message for detailed analysis

## Questions?

See `CLAUDE.md` in the repository root for development guidance.
