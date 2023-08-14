# model-card-schema


A LinkML schema for Model Cards model as published in [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993). Inspired by datasheets as used in the electronics and other industries, Gebru et al. proposed that every dataset "be accompanied with a datasheet that documents its motivation, composition, collection process, recommended uses, and so on". To this end the authors create a series of topics and over 50 questions addressing different aspects of datasets, also useful in an AI/ML context. An example of completed datasheet for datasets can be found here: Structured dataset documentation: a datasheet for CheXpert

Google is working with a different model called Data Cards, which in practice is close to the original Datasheets for Datasets template.

This repository stores a LinkML schema representation for the original Datasheets for Datasets model, representing the topics, sets of questions, and expectations about entities and fields expected in the answers (work in progress). Beyond a less structured markdown template for this model (e.g. template for datasheet for dataset) we are not aware of any other structured form representing Datasheets for Datasets.

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
