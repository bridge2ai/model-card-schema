Generate Model Cards using the Claude Code Assistant deterministic approach,
following the GitHub Actions workflow methodology with preprocessed source documents.

## Workflow Reference

First, read `.github/workflows/mc_assistant_create.md` to understand the full workflow,
including schema loading, metadata extraction patterns, validation requirements, and
output formatting guidelines.

## Input Sources

### URL-based (most common for in-session use)
Provide one or more URLs:
- Hugging Face model page (e.g. `https://huggingface.co/openai/clip-vit-base-patch32`)
- GitHub repository README / `MODEL_CARD.md`
- Paper PDF or landing page
- DOI for papers (use `mcp__artl__*`)

### File-based (preferred for reproducibility)
Location: `data/model_cards_assistant/inputs/{model}/`
Provide a path to a directory of preprocessed text/markdown/JSON dumps describing the model.

### Concatenated sources
For projects with many source docs, prefer concatenated files for ONE comprehensive Model Card:
- `data/preprocessed/concatenated/{MODEL}_preprocessed.txt`

## Output Locations

- In-session generation: `data/model_cards_assistant/{model_name}_model_card.yaml`
- HTML preview: `data/model_cards_assistant/{model_name}_model_card.html`
- Metadata sidecar: `data/model_cards_assistant/{model_name}_model_card_metadata.yaml`

## Generation Process

Follow the workflow in `.github/workflows/mc_assistant_create.md`:

1. **Load the Model Card Schema** (Step 1)
   - Read schema from `src/model_card_schema/schema/model_card_schema.yaml`
     (or `model_card_schema_d4dharmonized.yaml` if user requests D4D harmonization)
   - Understand all 34 classes, slots, and enums

2. **Read reference examples** (CRITICAL)
   - `src/data/examples/extended/climate-model-extended.yaml` — comprehensive DOE example
   - Study how `model_details`, `model_parameters`, `quantitative_analyses`, `considerations` are structured
   - Note exact field naming patterns — most slots use snake_case; some Google-MCT carryover slots use camelCase

3. **Gather Source Content** (Step 2)
   - Read source documents using Read tool / WebFetch
   - Combine HF page + GitHub README + paper text where available

4. **Extract Metadata** (Step 3)
   - Map information to schema classes
   - Only populate fields you are confident about
   - Ensure required fields present (`model_details.name`)
   - Follow schema strictly for field names, types, structure
   - Use null or omit for missing information

5. **Generate Valid YAML** (Step 4)
   - Use proper YAML syntax with 2-space indentation
   - Include `schema_version` and `model_details` at top level
   - Structure nested objects per schema class definitions
   - Use lists where schema specifies `multivalued: true`

6. **Validate Schema Compliance** (Step 5)
   - Run: `poetry run linkml-validate -s src/model_card_schema/schema/model_card_schema.yaml -C modelCard <file>`
   - Fix any validation errors before proceeding

7. **Save** to output location

## File Header

```yaml
# Model Card for {MODEL} Model
# Generation Method: Claude Code Deterministic ASSISTANT (in-session synthesis)
# Workflow: .github/workflows/mc_assistant_create.md
# Source: <list URLs or preprocessed files>
# Schema: src/model_card_schema/schema/model_card_schema.yaml
# Temperature: 0.0
# Generated: {DATE}
```

## Field Population Rules

- Required fields: MUST be populated (`model_details.name`)
- Optional fields: Only populate if information is explicitly available
- Multivalued fields: Use YAML list syntax
- Enum fields: Only use values defined in schema enums (e.g. `role`, license identifiers)
- Dates: Use ISO 8601 format (YYYY-MM-DD)

## Validation

### Schema Validation (Required)
```bash
poetry run linkml-validate \
  -s src/model_card_schema/schema/model_card_schema.yaml \
  -C modelCard \
  <file>
```

### Example Test Suite (Required if file lives under src/data/examples/extended/)
```bash
make test-examples
```

All Model Cards must pass schema validation before completion.
For detailed validation guidance, see the `mc-validator` agent (if available).
