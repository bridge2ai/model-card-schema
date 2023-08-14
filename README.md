# model-card-schema


A LinkML schema for the Model Cards model as published in [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993), which is an effort to democratize AI/ML technologies including increasing transparency. Model Cards represent information about trained machine learning models and can provide data on benchmarked model evaluations across a variety of conditions, including varying cultural, demographic, or phenotypic factors. Model Cards can also specify the applicable contexts for using the trained model and other relevant information.

This repository stores a LinkML schema representation for the original Model Cards model, representing the topics, sets of questions, and expectations about entities and fields expected in the answers (work in progress).

The Google Model Card model is also supported by the Model Card Toolkit for creating Model Card instances for trained models [Introducing the Model Card Toolkit for Easier Model Transparency Reporting](https://ai.googleblog.com/2020/07/introducing-model-card-toolkit-for.html). In addition HuggingFace has adopted Model Cards and has released a [Model Cart Writing Tool](https://huggingface.co/spaces/huggingface/Model_Cards_Writing_Tool).

## Repository Structure

* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/) - source files (edit these)
  * [model_card_schema](src/model_card_schema)
    * [schema](src/model_card_schema/schema) -- LinkML schema
      (edit this)
    * [datamodel](src/model_card_schema/datamodel) -- generated
      Python datamodel
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
