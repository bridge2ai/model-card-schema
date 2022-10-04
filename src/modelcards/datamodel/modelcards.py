# Auto generated from modelcards.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-10-04T16:30:09
# Schema: Model_Card
#
# id: https://w3id.org/linkml/modelcard
# description: An EXPERIMENTAL rendering of the model card schema in LinkML This is not the official model card
#              schema!
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Float, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MODELCARD = CurieNamespace('modelcard', 'https://w3id.org/linkml/modelcard/')
DEFAULT_ = MODELCARD


# Types

# Class references



@dataclass
class Owner(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.Owner
    class_class_curie: ClassVar[str] = "modelcard:Owner"
    class_name: ClassVar[str] = "owner"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Owner

    name: Optional[str] = None
    contact: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.contact is not None and not isinstance(self.contact, str):
            self.contact = str(self.contact)

        super().__post_init__(**kwargs)


@dataclass
class Dataset(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.Dataset
    class_class_curie: ClassVar[str] = "modelcard:Dataset"
    class_name: ClassVar[str] = "dataset"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Dataset

    name: Optional[str] = None
    link: Optional[str] = None
    sensitive: Optional[Union[bool, Bool]] = None
    graphics: Optional[Union[dict, "Graphics"]] = None
    bias_input: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.link is not None and not isinstance(self.link, str):
            self.link = str(self.link)

        if self.sensitive is not None and not isinstance(self.sensitive, Bool):
            self.sensitive = Bool(self.sensitive)

        if self.graphics is not None and not isinstance(self.graphics, Graphics):
            self.graphics = Graphics(**as_dict(self.graphics))

        if self.bias_input is not None and not isinstance(self.bias_input, str):
            self.bias_input = str(self.bias_input)

        super().__post_init__(**kwargs)


@dataclass
class PerformanceMetric(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.PerformanceMetric
    class_class_curie: ClassVar[str] = "modelcard:PerformanceMetric"
    class_name: ClassVar[str] = "performance_metric"
    class_model_uri: ClassVar[URIRef] = MODELCARD.PerformanceMetric

    type: str = None
    value: Optional[str] = None
    confidence_interval: Optional[str] = None
    threshold: Optional[float] = None
    slice: Optional[str] = None
    value_error: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.confidence_interval is not None and not isinstance(self.confidence_interval, str):
            self.confidence_interval = str(self.confidence_interval)

        if self.threshold is not None and not isinstance(self.threshold, float):
            self.threshold = float(self.threshold)

        if self.slice is not None and not isinstance(self.slice, str):
            self.slice = str(self.slice)

        if self.value_error is not None and not isinstance(self.value_error, str):
            self.value_error = str(self.value_error)

        super().__post_init__(**kwargs)


@dataclass
class Graphics(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.Graphics
    class_class_curie: ClassVar[str] = "modelcard:Graphics"
    class_name: ClassVar[str] = "graphics"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Graphics

    description: Optional[str] = None
    collection: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.collection, list):
            self.collection = [self.collection] if self.collection is not None else []
        self.collection = [v if isinstance(v, str) else str(v) for v in self.collection]

        super().__post_init__(**kwargs)


@dataclass
class Graphic(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.Graphic
    class_class_curie: ClassVar[str] = "modelcard:Graphic"
    class_name: ClassVar[str] = "graphic"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Graphic

    name: Optional[str] = None
    image: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.image is not None and not isinstance(self.image, str):
            self.image = str(self.image)

        super().__post_init__(**kwargs)


@dataclass
class Risk(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.Risk
    class_class_curie: ClassVar[str] = "modelcard:Risk"
    class_name: ClassVar[str] = "risk"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Risk

    name: Optional[str] = None
    mitigation_strategy: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.mitigation_strategy is not None and not isinstance(self.mitigation_strategy, str):
            self.mitigation_strategy = str(self.mitigation_strategy)

        super().__post_init__(**kwargs)


@dataclass
class ModelCard(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD.ModelCard
    class_class_curie: ClassVar[str] = "modelcard:ModelCard"
    class_name: ClassVar[str] = "ModelCard"
    class_model_uri: ClassVar[URIRef] = MODELCARD.ModelCard

    model_details: str = None
    schema_version: Optional[str] = None
    model_parameters: Optional[str] = None
    quantitative_analysis: Optional[str] = None
    considerations: Optional[str] = None
    model_category: Optional[str] = None
    bias_model: Optional[str] = None
    bias_output: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.model_details):
            self.MissingRequiredField("model_details")
        if not isinstance(self.model_details, str):
            self.model_details = str(self.model_details)

        if self.schema_version is not None and not isinstance(self.schema_version, str):
            self.schema_version = str(self.schema_version)

        if self.model_parameters is not None and not isinstance(self.model_parameters, str):
            self.model_parameters = str(self.model_parameters)

        if self.quantitative_analysis is not None and not isinstance(self.quantitative_analysis, str):
            self.quantitative_analysis = str(self.quantitative_analysis)

        if self.considerations is not None and not isinstance(self.considerations, str):
            self.considerations = str(self.considerations)

        if self.model_category is not None and not isinstance(self.model_category, str):
            self.model_category = str(self.model_category)

        if self.bias_model is not None and not isinstance(self.bias_model, str):
            self.bias_model = str(self.bias_model)

        if self.bias_output is not None and not isinstance(self.bias_output, str):
            self.bias_output = str(self.bias_output)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.name = Slot(uri=MODELCARD.name, name="name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.name, domain=None, range=Optional[str])

slots.contact = Slot(uri=MODELCARD.contact, name="contact", curie=MODELCARD.curie('contact'),
                   model_uri=MODELCARD.contact, domain=None, range=Optional[str])

slots.link = Slot(uri=MODELCARD.link, name="link", curie=MODELCARD.curie('link'),
                   model_uri=MODELCARD.link, domain=None, range=Optional[str])

slots.sensitive = Slot(uri=MODELCARD.sensitive, name="sensitive", curie=MODELCARD.curie('sensitive'),
                   model_uri=MODELCARD.sensitive, domain=None, range=Optional[Union[bool, Bool]])

slots.graphics = Slot(uri=MODELCARD.graphics, name="graphics", curie=MODELCARD.curie('graphics'),
                   model_uri=MODELCARD.graphics, domain=None, range=Optional[Union[dict, Graphics]])

slots.type = Slot(uri=MODELCARD.type, name="type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.type, domain=None, range=str)

slots.value = Slot(uri=MODELCARD.value, name="value", curie=MODELCARD.curie('value'),
                   model_uri=MODELCARD.value, domain=None, range=Optional[str])

slots.value_error = Slot(uri=MODELCARD.value_error, name="value_error", curie=MODELCARD.curie('value_error'),
                   model_uri=MODELCARD.value_error, domain=None, range=Optional[str])

slots.confidence_interval = Slot(uri=MODELCARD.confidence_interval, name="confidence_interval", curie=MODELCARD.curie('confidence_interval'),
                   model_uri=MODELCARD.confidence_interval, domain=None, range=Optional[str])

slots.threshold = Slot(uri=MODELCARD.threshold, name="threshold", curie=MODELCARD.curie('threshold'),
                   model_uri=MODELCARD.threshold, domain=None, range=Optional[float])

slots.slice = Slot(uri=MODELCARD.slice, name="slice", curie=MODELCARD.curie('slice'),
                   model_uri=MODELCARD.slice, domain=None, range=Optional[str])

slots.description = Slot(uri=MODELCARD.description, name="description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.description, domain=None, range=Optional[str])

slots.collection = Slot(uri=MODELCARD.collection, name="collection", curie=MODELCARD.curie('collection'),
                   model_uri=MODELCARD.collection, domain=None, range=Optional[Union[str, List[str]]])

slots.image = Slot(uri=MODELCARD.image, name="image", curie=MODELCARD.curie('image'),
                   model_uri=MODELCARD.image, domain=None, range=Optional[str])

slots.bias_input = Slot(uri=MODELCARD.bias_input, name="bias_input", curie=MODELCARD.curie('bias_input'),
                   model_uri=MODELCARD.bias_input, domain=None, range=Optional[str])

slots.bias_model = Slot(uri=MODELCARD.bias_model, name="bias_model", curie=MODELCARD.curie('bias_model'),
                   model_uri=MODELCARD.bias_model, domain=None, range=Optional[str])

slots.bias_output = Slot(uri=MODELCARD.bias_output, name="bias_output", curie=MODELCARD.curie('bias_output'),
                   model_uri=MODELCARD.bias_output, domain=None, range=Optional[str])

slots.mitigation_strategy = Slot(uri=MODELCARD.mitigation_strategy, name="mitigation_strategy", curie=MODELCARD.curie('mitigation_strategy'),
                   model_uri=MODELCARD.mitigation_strategy, domain=None, range=Optional[str])

slots.schema_version = Slot(uri=MODELCARD.schema_version, name="schema_version", curie=MODELCARD.curie('schema_version'),
                   model_uri=MODELCARD.schema_version, domain=None, range=Optional[str])

slots.model_category = Slot(uri=MODELCARD.model_category, name="model_category", curie=MODELCARD.curie('model_category'),
                   model_uri=MODELCARD.model_category, domain=None, range=Optional[str])

slots.model_details = Slot(uri=MODELCARD.model_details, name="model_details", curie=MODELCARD.curie('model_details'),
                   model_uri=MODELCARD.model_details, domain=None, range=str)

slots.model_parameters = Slot(uri=MODELCARD.model_parameters, name="model_parameters", curie=MODELCARD.curie('model_parameters'),
                   model_uri=MODELCARD.model_parameters, domain=None, range=Optional[str])

slots.quantitative_analysis = Slot(uri=MODELCARD.quantitative_analysis, name="quantitative_analysis", curie=MODELCARD.curie('quantitative_analysis'),
                   model_uri=MODELCARD.quantitative_analysis, domain=None, range=Optional[str])

slots.considerations = Slot(uri=MODELCARD.considerations, name="considerations", curie=MODELCARD.curie('considerations'),
                   model_uri=MODELCARD.considerations, domain=None, range=Optional[str])

slots.owner_name = Slot(uri=MODELCARD.name, name="owner_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.owner_name, domain=Owner, range=Optional[str])

slots.owner_contact = Slot(uri=MODELCARD.contact, name="owner_contact", curie=MODELCARD.curie('contact'),
                   model_uri=MODELCARD.owner_contact, domain=Owner, range=Optional[str])

slots.dataset_name = Slot(uri=MODELCARD.name, name="dataset_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.dataset_name, domain=Dataset, range=Optional[str])

slots.dataset_link = Slot(uri=MODELCARD.link, name="dataset_link", curie=MODELCARD.curie('link'),
                   model_uri=MODELCARD.dataset_link, domain=Dataset, range=Optional[str])

slots.dataset_sensitive = Slot(uri=MODELCARD.sensitive, name="dataset_sensitive", curie=MODELCARD.curie('sensitive'),
                   model_uri=MODELCARD.dataset_sensitive, domain=Dataset, range=Optional[Union[bool, Bool]])

slots.dataset_graphics = Slot(uri=MODELCARD.graphics, name="dataset_graphics", curie=MODELCARD.curie('graphics'),
                   model_uri=MODELCARD.dataset_graphics, domain=Dataset, range=Optional[Union[dict, "Graphics"]])

slots.dataset_bias_input = Slot(uri=MODELCARD.bias_input, name="dataset_bias_input", curie=MODELCARD.curie('bias_input'),
                   model_uri=MODELCARD.dataset_bias_input, domain=Dataset, range=Optional[str])

slots.performance_metric_type = Slot(uri=MODELCARD.type, name="performance_metric_type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.performance_metric_type, domain=PerformanceMetric, range=str)

slots.performance_metric_value = Slot(uri=MODELCARD.value, name="performance_metric_value", curie=MODELCARD.curie('value'),
                   model_uri=MODELCARD.performance_metric_value, domain=PerformanceMetric, range=Optional[str])

slots.performance_metric_confidence_interval = Slot(uri=MODELCARD.confidence_interval, name="performance_metric_confidence_interval", curie=MODELCARD.curie('confidence_interval'),
                   model_uri=MODELCARD.performance_metric_confidence_interval, domain=PerformanceMetric, range=Optional[str])

slots.performance_metric_value_error = Slot(uri=MODELCARD.value_error, name="performance_metric_value_error", curie=MODELCARD.curie('value_error'),
                   model_uri=MODELCARD.performance_metric_value_error, domain=PerformanceMetric, range=Optional[str])

slots.performance_metric_threshold = Slot(uri=MODELCARD.threshold, name="performance_metric_threshold", curie=MODELCARD.curie('threshold'),
                   model_uri=MODELCARD.performance_metric_threshold, domain=PerformanceMetric, range=Optional[float])

slots.performance_metric_slice = Slot(uri=MODELCARD.slice, name="performance_metric_slice", curie=MODELCARD.curie('slice'),
                   model_uri=MODELCARD.performance_metric_slice, domain=PerformanceMetric, range=Optional[str])

slots.graphics_description = Slot(uri=MODELCARD.description, name="graphics_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.graphics_description, domain=Graphics, range=Optional[str])

slots.graphics_collection = Slot(uri=MODELCARD.collection, name="graphics_collection", curie=MODELCARD.curie('collection'),
                   model_uri=MODELCARD.graphics_collection, domain=Graphics, range=Optional[Union[str, List[str]]])

slots.graphic_image = Slot(uri=MODELCARD.image, name="graphic_image", curie=MODELCARD.curie('image'),
                   model_uri=MODELCARD.graphic_image, domain=Graphic, range=Optional[str])

slots.risk_mitigation_strategy = Slot(uri=MODELCARD.mitigation_strategy, name="risk_mitigation_strategy", curie=MODELCARD.curie('mitigation_strategy'),
                   model_uri=MODELCARD.risk_mitigation_strategy, domain=Risk, range=Optional[str])

slots.ModelCard_schema_version = Slot(uri=MODELCARD.schema_version, name="ModelCard_schema_version", curie=MODELCARD.curie('schema_version'),
                   model_uri=MODELCARD.ModelCard_schema_version, domain=ModelCard, range=Optional[str])

slots.ModelCard_model_details = Slot(uri=MODELCARD.model_details, name="ModelCard_model_details", curie=MODELCARD.curie('model_details'),
                   model_uri=MODELCARD.ModelCard_model_details, domain=ModelCard, range=str)

slots.ModelCard_model_parameters = Slot(uri=MODELCARD.model_parameters, name="ModelCard_model_parameters", curie=MODELCARD.curie('model_parameters'),
                   model_uri=MODELCARD.ModelCard_model_parameters, domain=ModelCard, range=Optional[str])

slots.ModelCard_quantitative_analysis = Slot(uri=MODELCARD.quantitative_analysis, name="ModelCard_quantitative_analysis", curie=MODELCARD.curie('quantitative_analysis'),
                   model_uri=MODELCARD.ModelCard_quantitative_analysis, domain=ModelCard, range=Optional[str])

slots.ModelCard_considerations = Slot(uri=MODELCARD.considerations, name="ModelCard_considerations", curie=MODELCARD.curie('considerations'),
                   model_uri=MODELCARD.ModelCard_considerations, domain=ModelCard, range=Optional[str])

slots.ModelCard_model_category = Slot(uri=MODELCARD.model_category, name="ModelCard_model_category", curie=MODELCARD.curie('model_category'),
                   model_uri=MODELCARD.ModelCard_model_category, domain=ModelCard, range=Optional[str])

slots.ModelCard_bias_model = Slot(uri=MODELCARD.bias_model, name="ModelCard_bias_model", curie=MODELCARD.curie('bias_model'),
                   model_uri=MODELCARD.ModelCard_bias_model, domain=ModelCard, range=Optional[str])

slots.ModelCard_bias_output = Slot(uri=MODELCARD.bias_output, name="ModelCard_bias_output", curie=MODELCARD.curie('bias_output'),
                   model_uri=MODELCARD.ModelCard_bias_output, domain=ModelCard, range=Optional[str])