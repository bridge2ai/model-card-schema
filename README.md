Executive Order 14168: This repository is under review for potential modification in compliance with Administration directives.

# model-card-schema


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
