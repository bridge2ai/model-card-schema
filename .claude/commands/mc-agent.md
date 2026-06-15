Generate Model Cards using the Claude Code Agent deterministic approach.

## Task Overview

Generate comprehensive Model Cards for ML models using the Task tool with specialized
agents for parallel processing.

## Input Sources

### URL sources (in-session generation)
- Hugging Face model pages
- GitHub repositories with `README.md` / `MODEL_CARD.md`
- Paper PDFs / arXiv links
- DOIs (use `mcp__artl__*`)

### Preprocessed sources (batch generation)
Location: `data/preprocessed/concatenated/`
- `{PROJECT}_preprocessed.txt` — concatenated documentation for one Model Card per project

Location: `data/preprocessed/individual/{PROJECT}/`
- Per-source documents for separate Model Cards per source

## Output Locations

- Concatenated: `data/model_cards_concatenated/claudecode_agent/{PROJECT}_model_card.yaml`
- Individual: `data/model_cards_individual/claudecode_agent/{PROJECT}/{source_file}_model_card.yaml`

## Extraction Checklist

Extract these key elements from source documents:

- **Model identity**: name, short_description, comprehensive overview, version, license
- **Contributors and owners**: names, affiliations, roles (developed_by, contributed_by, etc.), contact info
- **Intended use**: primary use cases, users, out-of-scope uses
- **Model architecture**: model family, layers, params, input/output spec
- **Training data**: source, size, composition, preprocessing
- **Evaluation data**: source, composition, sensitive attributes
- **Quantitative analyses**: performance metrics by slice/factor
- **Considerations**: limitations, tradeoffs, ethical considerations, risks
- **Citations and references**: bibtex, paper URLs, related work
- **Compute infrastructure** (extended): hardware, software, total compute, energy
- **Reproducibility** (extended): seeds, deterministic settings, version pins
- **Mission relevance** (extended): DOE / domain alignment
- **Licensing**: SPDX identifier, restrictions, redistribution terms

## Generation Process

For each model:

1. **Launch Task agents in parallel** using Task tool with `subagent_type='general-purpose'`

2. **Read reference examples FIRST**:
   - Read validated example: `src/data/examples/extended/climate-model-extended.yaml`
   - Study how `ModelDetails`, `ModelParameters`, `QuantitativeAnalyses`, `Considerations` are structured
   - Note: most slots use snake_case; some Google-MCT carryover slots use camelCase

3. **Read schema and extract field definitions**:
   - Path: `src/model_card_schema/schema/model_card_schema.yaml`
   - For each class you'll use, extract EXACT field names
   - **Critical**: Do NOT invent field names based on semantics

4. **Common Field Name Mistakes to AVOID**:
   ```yaml
   # ❌ WRONG - Invented semantic field names
   model_details:
     model_name: "..."          # field is 'name'
     authors:                    # field is 'contributors' / 'owners'
       - author_name: "..."      # field is 'name'
   quantitative_analyses:
     metrics:                    # field is 'performance_metrics'
       - metric_type: "accuracy" # field is 'type'

   # ✅ CORRECT - Schema field names
   model_details:
     name: "..."
     contributors:
       - name: "..."
         role: developed_by
   quantitative_analyses:
     performance_metrics:
       - type: "accuracy"
         value: "0.91"
   ```

5. **Read source documents** from URLs / preprocessed locations

6. **Extract metadata** using the checklist above

7. **Generate valid YAML** conforming to schema:
   - Use ONLY field names found in schema
   - Include required `model_details.name`
   - Merge multi-part information into single description strings where appropriate
   - Follow reference examples for structure

8. **REQUIRED validation** (NON-SKIPPABLE):
   ```bash
   poetry run linkml-validate \
     -s src/model_card_schema/schema/model_card_schema.yaml \
     -C modelCard \
     <file>
   ```
   - If validation fails: analyze errors, fix field names, re-validate
   - DO NOT proceed without passing validation

9. **Verify output**:
   - Check file has comprehensive content (target 200+ lines for concatenated sources)
   - Confirm all major sections populated (model_details, model_parameters, considerations, ...)
   - Verify no invented field names used

10. **Save** to output location

## Merging Multiple Sources

When multiple sources describe the same model:
1. Merge complementary information from all sources
2. Prefer more detailed and specific information over generic descriptions
3. Resolve conflicts by choosing the most authoritative or recent source

## File Header

```yaml
# Model Card for {MODEL} Model
# Generation Method: Claude Code Agent Deterministic
# Source: <list URLs or preprocessed file paths>
# Schema: src/model_card_schema/schema/model_card_schema.yaml
# Temperature: 0.0
# Generated: {DATE}
```

## Settings

- Temperature: 0.0
- Follow schema strictly — only use defined fields
- Prefer null or omission for unknown values

## Validation

### Schema Validation (Required)
```bash
poetry run linkml-validate -s src/model_card_schema/schema/model_card_schema.yaml -C modelCard <file>
```

All Model Cards must pass schema validation before completion.
For detailed validation guidance, see the `mc-validator` agent.
