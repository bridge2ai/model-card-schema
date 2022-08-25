# Auto generated from modelcards.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-08-24T19:22:27
# Schema: Model_Card
#
# id: https://example.org/Model-Card
# description:
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
MODEL_CARD = CurieNamespace('Model_Card', 'https://example.org/Model-Card')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = MODEL_CARD


# Types

# Class references



@dataclass
class Owner(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.Owner
    class_class_curie: ClassVar[str] = "Model_Card:Owner"
    class_name: ClassVar[str] = "owner"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.Owner

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

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.Dataset
    class_class_curie: ClassVar[str] = "Model_Card:Dataset"
    class_name: ClassVar[str] = "dataset"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.Dataset

    name: Optional[str] = None
    link: Optional[str] = None
    sensitive: Optional[Union[bool, Bool]] = None
    graphics: Optional[Union[dict, "Graphics"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.link is not None and not isinstance(self.link, str):
            self.link = str(self.link)

        if self.sensitive is not None and not isinstance(self.sensitive, Bool):
            self.sensitive = Bool(self.sensitive)

        if self.graphics is not None and not isinstance(self.graphics, Graphics):
            self.graphics = Graphics(**as_dict(self.graphics))

        super().__post_init__(**kwargs)


@dataclass
class PerformanceMetric(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.PerformanceMetric
    class_class_curie: ClassVar[str] = "Model_Card:PerformanceMetric"
    class_name: ClassVar[str] = "performance_metric"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.PerformanceMetric

    type: str = None
    value: Optional[str] = None
    confidence_interval: Optional[str] = None
    threshold: Optional[float] = None
    slice: Optional[str] = None

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

        super().__post_init__(**kwargs)


@dataclass
class Graphics(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.Graphics
    class_class_curie: ClassVar[str] = "Model_Card:Graphics"
    class_name: ClassVar[str] = "graphics"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.Graphics

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

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.Graphic
    class_class_curie: ClassVar[str] = "Model_Card:Graphic"
    class_name: ClassVar[str] = "graphic"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.Graphic

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

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.Risk
    class_class_curie: ClassVar[str] = "Model_Card:Risk"
    class_name: ClassVar[str] = "risk"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.Risk

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

    class_class_uri: ClassVar[URIRef] = MODEL_CARD.ModelCard
    class_class_curie: ClassVar[str] = "Model_Card:ModelCard"
    class_name: ClassVar[str] = "Model Card"
    class_model_uri: ClassVar[URIRef] = MODEL_CARD.ModelCard

    model_details: str = None
    schema_version: Optional[str] = None
    model_parameters: Optional[str] = None
    quantitative_analysis: Optional[str] = None
    considerations: Optional[str] = None

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

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.name = Slot(uri=MODEL_CARD.name, name="name", curie=MODEL_CARD.curie('name'),
                   model_uri=MODEL_CARD.name, domain=None, range=Optional[str])

slots.contact = Slot(uri=MODEL_CARD.contact, name="contact", curie=MODEL_CARD.curie('contact'),
                   model_uri=MODEL_CARD.contact, domain=None, range=Optional[str])

slots.link = Slot(uri=MODEL_CARD.link, name="link", curie=MODEL_CARD.curie('link'),
                   model_uri=MODEL_CARD.link, domain=None, range=Optional[str])

slots.sensitive = Slot(uri=MODEL_CARD.sensitive, name="sensitive", curie=MODEL_CARD.curie('sensitive'),
                   model_uri=MODEL_CARD.sensitive, domain=None, range=Optional[Union[bool, Bool]])

slots.graphics = Slot(uri=MODEL_CARD.graphics, name="graphics", curie=MODEL_CARD.curie('graphics'),
                   model_uri=MODEL_CARD.graphics, domain=None, range=Optional[Union[dict, Graphics]])

slots.type = Slot(uri=MODEL_CARD.type, name="type", curie=MODEL_CARD.curie('type'),
                   model_uri=MODEL_CARD.type, domain=None, range=str)

slots.value = Slot(uri=MODEL_CARD.value, name="value", curie=MODEL_CARD.curie('value'),
                   model_uri=MODEL_CARD.value, domain=None, range=Optional[str])

slots.confidence_interval = Slot(uri=MODEL_CARD.confidence_interval, name="confidence_interval", curie=MODEL_CARD.curie('confidence_interval'),
                   model_uri=MODEL_CARD.confidence_interval, domain=None, range=Optional[str])

slots.threshold = Slot(uri=MODEL_CARD.threshold, name="threshold", curie=MODEL_CARD.curie('threshold'),
                   model_uri=MODEL_CARD.threshold, domain=None, range=Optional[float])

slots.slice = Slot(uri=MODEL_CARD.slice, name="slice", curie=MODEL_CARD.curie('slice'),
                   model_uri=MODEL_CARD.slice, domain=None, range=Optional[str])

slots.description = Slot(uri=MODEL_CARD.description, name="description", curie=MODEL_CARD.curie('description'),
                   model_uri=MODEL_CARD.description, domain=None, range=Optional[str])

slots.collection = Slot(uri=MODEL_CARD.collection, name="collection", curie=MODEL_CARD.curie('collection'),
                   model_uri=MODEL_CARD.collection, domain=None, range=Optional[Union[str, List[str]]])

slots.image = Slot(uri=MODEL_CARD.image, name="image", curie=MODEL_CARD.curie('image'),
                   model_uri=MODEL_CARD.image, domain=None, range=Optional[str])

slots.mitigation_strategy = Slot(uri=MODEL_CARD.mitigation_strategy, name="mitigation_strategy", curie=MODEL_CARD.curie('mitigation_strategy'),
                   model_uri=MODEL_CARD.mitigation_strategy, domain=None, range=Optional[str])

slots.schema_version = Slot(uri=MODEL_CARD.schema_version, name="schema_version", curie=MODEL_CARD.curie('schema_version'),
                   model_uri=MODEL_CARD.schema_version, domain=None, range=Optional[str])

slots.model_details = Slot(uri=MODEL_CARD.model_details, name="model_details", curie=MODEL_CARD.curie('model_details'),
                   model_uri=MODEL_CARD.model_details, domain=None, range=str)

slots.model_parameters = Slot(uri=MODEL_CARD.model_parameters, name="model_parameters", curie=MODEL_CARD.curie('model_parameters'),
                   model_uri=MODEL_CARD.model_parameters, domain=None, range=Optional[str])

slots.quantitative_analysis = Slot(uri=MODEL_CARD.quantitative_analysis, name="quantitative_analysis", curie=MODEL_CARD.curie('quantitative_analysis'),
                   model_uri=MODEL_CARD.quantitative_analysis, domain=None, range=Optional[str])

slots.considerations = Slot(uri=MODEL_CARD.considerations, name="considerations", curie=MODEL_CARD.curie('considerations'),
                   model_uri=MODEL_CARD.considerations, domain=None, range=Optional[str])

slots.owner_contact = Slot(uri=MODEL_CARD.contact, name="owner_contact", curie=MODEL_CARD.curie('contact'),
                   model_uri=MODEL_CARD.owner_contact, domain=Owner, range=Optional[str])

slots.dataset_link = Slot(uri=MODEL_CARD.link, name="dataset_link", curie=MODEL_CARD.curie('link'),
                   model_uri=MODEL_CARD.dataset_link, domain=Dataset, range=Optional[str])

slots.dataset_sensitive = Slot(uri=MODEL_CARD.sensitive, name="dataset_sensitive", curie=MODEL_CARD.curie('sensitive'),
                   model_uri=MODEL_CARD.dataset_sensitive, domain=Dataset, range=Optional[Union[bool, Bool]])

slots.dataset_graphics = Slot(uri=MODEL_CARD.graphics, name="dataset_graphics", curie=MODEL_CARD.curie('graphics'),
                   model_uri=MODEL_CARD.dataset_graphics, domain=Dataset, range=Optional[Union[dict, "Graphics"]])

slots.performance_metric_type = Slot(uri=MODEL_CARD.type, name="performance_metric_type", curie=MODEL_CARD.curie('type'),
                   model_uri=MODEL_CARD.performance_metric_type, domain=PerformanceMetric, range=str)

slots.performance_metric_value = Slot(uri=MODEL_CARD.value, name="performance_metric_value", curie=MODEL_CARD.curie('value'),
                   model_uri=MODEL_CARD.performance_metric_value, domain=PerformanceMetric, range=Optional[str])

slots.performance_metric_confidence_interval = Slot(uri=MODEL_CARD.confidence_interval, name="performance_metric_confidence_interval", curie=MODEL_CARD.curie('confidence_interval'),
                   model_uri=MODEL_CARD.performance_metric_confidence_interval, domain=PerformanceMetric, range=Optional[str])

slots.performance_metric_threshold = Slot(uri=MODEL_CARD.threshold, name="performance_metric_threshold", curie=MODEL_CARD.curie('threshold'),
                   model_uri=MODEL_CARD.performance_metric_threshold, domain=PerformanceMetric, range=Optional[float])

slots.performance_metric_slice = Slot(uri=MODEL_CARD.slice, name="performance_metric_slice", curie=MODEL_CARD.curie('slice'),
                   model_uri=MODEL_CARD.performance_metric_slice, domain=PerformanceMetric, range=Optional[str])

slots.graphics_description = Slot(uri=MODEL_CARD.description, name="graphics_description", curie=MODEL_CARD.curie('description'),
                   model_uri=MODEL_CARD.graphics_description, domain=Graphics, range=Optional[str])

slots.graphics_collection = Slot(uri=MODEL_CARD.collection, name="graphics_collection", curie=MODEL_CARD.curie('collection'),
                   model_uri=MODEL_CARD.graphics_collection, domain=Graphics, range=Optional[Union[str, List[str]]])

slots.graphic_image = Slot(uri=MODEL_CARD.image, name="graphic_image", curie=MODEL_CARD.curie('image'),
                   model_uri=MODEL_CARD.graphic_image, domain=Graphic, range=Optional[str])

slots.risk_mitigation_strategy = Slot(uri=MODEL_CARD.mitigation_strategy, name="risk_mitigation_strategy", curie=MODEL_CARD.curie('mitigation_strategy'),
                   model_uri=MODEL_CARD.risk_mitigation_strategy, domain=Risk, range=Optional[str])

slots.Model_Card_schema_version = Slot(uri=MODEL_CARD.schema_version, name="Model Card_schema_version", curie=MODEL_CARD.curie('schema_version'),
                   model_uri=MODEL_CARD.Model_Card_schema_version, domain=ModelCard, range=Optional[str])

slots.Model_Card_model_details = Slot(uri=MODEL_CARD.model_details, name="Model Card_model_details", curie=MODEL_CARD.curie('model_details'),
                   model_uri=MODEL_CARD.Model_Card_model_details, domain=ModelCard, range=str)

slots.Model_Card_model_parameters = Slot(uri=MODEL_CARD.model_parameters, name="Model Card_model_parameters", curie=MODEL_CARD.curie('model_parameters'),
                   model_uri=MODEL_CARD.Model_Card_model_parameters, domain=ModelCard, range=Optional[str])

slots.Model_Card_quantitative_analysis = Slot(uri=MODEL_CARD.quantitative_analysis, name="Model Card_quantitative_analysis", curie=MODEL_CARD.curie('quantitative_analysis'),
                   model_uri=MODEL_CARD.Model_Card_quantitative_analysis, domain=ModelCard, range=Optional[str])

slots.Model_Card_considerations = Slot(uri=MODEL_CARD.considerations, name="Model Card_considerations", curie=MODEL_CARD.curie('considerations'),
                   model_uri=MODEL_CARD.Model_Card_considerations, domain=ModelCard, range=Optional[str])