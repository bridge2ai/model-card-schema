Executive Order 14168: This repository is under review for potential modification in compliance with Administration directives.

# model-card-schema

**Canonical example quality** ([climate-model-extended.yaml](src/data/examples/extended/climate-model-extended.yaml)):

![rubric10 hybrid](data/evaluation/badges/climate-model-extended_rubric10_hybrid.svg)
![rubric20 hybrid](data/evaluation/badges/climate-model-extended_rubric20_hybrid.svg)

A LinkML schema for the Model Cards model as published in [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993), which is an effort to democratize AI/ML technologies including increasing transparency. Model Cards represent information about trained machine learning models and can provide data on benchmarked model evaluations across a variety of conditions, including varying cultural, demographic, or phenotypic factors. Model Cards can also specify the applicable contexts for using the trained model and other relevant information.

This repository stores a LinkML schema representation for the original Model Cards model, representing the topics, sets of questions, and expectations about entities and fields expected in the answers (work in progress). [HuggingFace provides a markdown Model Card template](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/modelcard_template.md) and their are [JSON and Proto versions provided by the Model Card Toolkit](https://www.tensorflow.org/responsible_ai/model_card_toolkit/guide/concepts###schema).

The Google Model Card model is also supported by the Model Card Toolkit for creating Model Card instances for trained models [Introducing the Model Card Toolkit for Easier Model Transparency Reporting](https://ai.googleblog.com/2020/07/introducing-model-card-toolkit-for.html). In addition HuggingFace has adopted Model Cards and has released a [Model Cart Writing Tool](https://huggingface.co/spaces/huggingface/Model_Cards_Writing_Tool), Amazon AWS also has support for [Amazon SageMaker Model Cards](https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html) including creation of Model Card instances using the [SageMaker Python SDK](https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards-create.html), and Model Cards can also be generated via scikit-learn [How to create and deploy a model card in the cloud with Scikit-Learn](https://cloud.google.com/blog/products/ai-machine-learning/create-a-model-card-with-scikit-learn).

## ✨ What's New: Datasheets for Datasets Integration

This repository now includes comprehensive integration with **Datasheets for Datasets**, enabling:

- 📊 **Comprehensive dataset documentation** (60+ fields vs 7 fields)
- 🔗 **Single source of truth** - Document datasets once, reference from many model cards
- ✅ **Better governance** - Ethics, privacy, and legal compliance support
- 🛠️ **Migration utilities** - Automated tools to upgrade existing model cards
- 📚 **Complete examples** - Working examples with full documentation

**Quick Start**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for step-by-step instructions.

## 🎯 Quality Evaluation

This repo ships **two rubrics** for scoring Model Card YAMLs, plus a hybrid (rule-based) batch evaluator and an LLM-based judge for each:

- **rubric10** — 10 elements × 5 sub-elements (50 points). Coarse, fast quality check.
- **rubric20** — 20 questions across 4 categories: Structural Completeness, Metadata Quality, Technical Documentation, Performance & FAIRness (84 points). Detailed audit.

Each rubric runs in two flavors: a **hybrid** scorer (rule-based + heuristics, no LLM cost) and an **LLM** scorer (`mc-rubric10` / `mc-rubric20` Claude sub-agents). The hybrid acts as a fast prefilter; the LLM provides the deeper quality signal.

### Portfolio scores (live)

| Card | Source | rubric10 hybrid | rubric10 LLM | rubric20 hybrid | rubric20 LLM |
| --- | --- | :---: | :---: | :---: | :---: |
| [`climate-model-extended.yaml`](src/data/examples/extended/climate-model-extended.yaml) | DOE canonical example | ![](data/evaluation/badges/climate-model-extended_rubric10_hybrid.svg) | ![](data/evaluation/badges/climate-model-extended_rubric10_llm.svg) | ![](data/evaluation/badges/climate-model-extended_rubric20_hybrid.svg) | ![](data/evaluation/badges/climate-model-extended_rubric20_llm.svg) |
| [`climate-forecasting-model-card.yaml`](src/data/examples/d4d_integration/climate-forecasting-model-card.yaml) | Harmonized + D4D refs | ![](data/evaluation/badges/climate-forecasting-model-card_rubric10_hybrid.svg) | ![](data/evaluation/badges/climate-forecasting-model-card_rubric10_llm.svg) | ![](data/evaluation/badges/climate-forecasting-model-card_rubric20_hybrid.svg) | ![](data/evaluation/badges/climate-forecasting-model-card_rubric20_llm.svg) |
| [`sentiment-classifier-with-datasheet-refs.yaml`](src/data/examples/harmonized/sentiment-classifier-with-datasheet-refs.yaml) | Harmonized | ![](data/evaluation/badges/sentiment-classifier-with-datasheet-refs_rubric10_hybrid.svg) | ![](data/evaluation/badges/sentiment-classifier-with-datasheet-refs_rubric10_llm.svg) | ![](data/evaluation/badges/sentiment-classifier-with-datasheet-refs_rubric20_hybrid.svg) | ![](data/evaluation/badges/sentiment-classifier-with-datasheet-refs_rubric20_llm.svg) |
| [`densenet121_tv_in1k_model_card.yaml`](data/model_cards_assistant/densenet121_tv_in1k_model_card.yaml) | HF Hub (timm) | ![](data/evaluation/badges/densenet121_tv_in1k_model_card_rubric10_hybrid.svg) | ![](data/evaluation/badges/densenet121_tv_in1k_model_card_rubric10_llm.svg) | ![](data/evaluation/badges/densenet121_tv_in1k_model_card_rubric20_hybrid.svg) | ![](data/evaluation/badges/densenet121_tv_in1k_model_card_rubric20_llm.svg) |
| [`subcell_saprot_650m_model_card.yaml`](data/model_cards_assistant/subcell_saprot_650m_model_card.yaml) | HF Hub (SaProtHub) | ![](data/evaluation/badges/subcell_saprot_650m_model_card_rubric10_hybrid.svg) | ![](data/evaluation/badges/subcell_saprot_650m_model_card_rubric10_llm.svg) | ![](data/evaluation/badges/subcell_saprot_650m_model_card_rubric20_hybrid.svg) | ![](data/evaluation/badges/subcell_saprot_650m_model_card_rubric20_llm.svg) |
| [`minimal-viable-model-card.yaml`](src/data/examples/fixtures/minimal-viable-model-card.yaml) | Floor anchor (mid) | ![](data/evaluation/badges/minimal-viable-model-card_rubric10_hybrid.svg) | — | ![](data/evaluation/badges/minimal-viable-model-card_rubric20_hybrid.svg) | — |
| [`minimal-model-card.yaml`](src/data/examples/fixtures/minimal-model-card.yaml) | Floor anchor (zero) | ![](data/evaluation/badges/minimal-model-card_rubric10_hybrid.svg) | — | ![](data/evaluation/badges/minimal-model-card_rubric20_hybrid.svg) | — |

Color band: 🟢 ≥80% · 🟡 ≥50% · 🔴 <50%.

**Dashboards** (open locally — GitHub doesn't render embedded HTML):
- [`data/evaluation/all/portfolio_compare.html`](data/evaluation/all/portfolio_compare.html) — cross-evaluator comparison matrix with element-level diffs
- [`data/evaluation/badges/index.html`](data/evaluation/badges/index.html) — all badges with copy-paste markdown snippets

### Reproduce

```bash
# Hybrid evaluators (fast, no LLM cost)
make evaluate-rubric10 MC_INPUT=path/to/card.yaml MC_EVAL_DIR=data/evaluation/mine/rubric10
make evaluate-rubric20 MC_INPUT=path/to/card.yaml MC_EVAL20_DIR=data/evaluation/mine/rubric20

# LLM evaluators (via Claude Code sub-agents in this session) — tell the
# agent where to write the JSON so the render-* targets below pick it up:
# > "Evaluate path/to/card.yaml with rubric10 and save the JSON to
# >  data/evaluation/mine/rubric10/<stem>_llm_evaluation.json"
# > "Evaluate path/to/card.yaml with rubric20 and save the JSON to
# >  data/evaluation/mine/rubric20/<stem>_llm_rubric20_evaluation.json"

# Render reports + badges
make render-eval     EVAL_JSONS='data/evaluation/mine/**/*.json' EVAL_HTML=data/evaluation/mine/report.html
make render-compare  EVAL_JSONS='data/evaluation/mine/**/*.json' EVAL_HTML=data/evaluation/mine/compare.html
make render-badges   EVAL_JSONS='data/evaluation/mine/**/*.json' BADGE_DIR=data/evaluation/mine/badges
```

### `@mcassistant` GitHub Action

Mention `@mcassistant` in an issue with a HuggingFace Hub URL (or a GitHub README link) and the assistant will generate a Model Card YAML in `data/model_cards_assistant/`, validate it against the schema, score it against the quality gate, and open a PR. See [`.goosehints`](.goosehints) for the full workflow contract.

## Repository Structure

* **[src/linkml/](src/linkml/)** - LinkML schema files
  * `modelcards.yaml` - Production schema (100% Google MCT v0.0.2 + HuggingFace + Papers with Code)
  * `modelcards_harmonized.yaml` - Proposed harmonized schema (with datasheets integration)
* **[src/data/examples/harmonized/](src/data/examples/harmonized/)** - Integration examples
  * Complete model card with datasheet references
  * Complete datasheet example (IMDb dataset)
  * Usage guide and patterns
* **[utils/](utils/)** - Migration and validation tools
  * `migrate_to_harmonized.py` - Automated migration utility
  * `validate_integration.py` - Validation utility
  * Complete tool documentation
* **Documentation**
  * [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Step-by-step migration guide
  * [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Technical integration patterns
  * [ALIGNMENT_ANALYSIS.md](ALIGNMENT_ANALYSIS.md) - Comprehensive schema analysis
  * [CLAUDE.md](CLAUDE.md) - Developer guidance
* [project/](project/) - Generated artifacts (do not edit)
* [tests/](tests/) - Python tests

## Developer Documentation

<details>
Use the `make` command to generate project artefacts:

* `make all`: make everything
* `make deploy`: deploys site
</details>

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
