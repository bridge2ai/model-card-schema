# Auto generated from modelcards.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-11-19T19:55:01
# Schema: Model_Card
#
# id: https://w3id.org/linkml/modelcard
# description: A comprehensive LinkML rendering of model card schemas,
#   incorporating Google Model Card Toolkit v0.0.2, HuggingFace,
#   and Papers with Code specifications.
#
#   This schema provides structured metadata for documenting machine learning models
#   including model details, training data, performance metrics, ethical considerations,
#   and deployment specifications.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Date, Float, String, Uri
from linkml_runtime.utils.metamodelcore import URI, XSDDate

metamodel_version = "1.7.0"
version = None

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MODELCARD = CurieNamespace('modelcard', 'https://w3id.org/linkml/modelcard/')
DEFAULT_ = MODELCARD


# Types

# Class references



@dataclass(repr=False)
class Version(YAMLRoot):
    """
    Version information for a model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Version"]
    class_class_curie: ClassVar[str] = "modelcard:Version"
    class_name: ClassVar[str] = "Version"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Version

    name: Optional[str] = None
    date: Optional[Union[str, XSDDate]] = None
    diff: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.date is not None and not isinstance(self.date, XSDDate):
            self.date = XSDDate(self.date)

        if self.diff is not None and not isinstance(self.diff, str):
            self.diff = str(self.diff)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class License(YAMLRoot):
    """
    License information (use SPDX identifier OR custom text, not both)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["License"]
    class_class_curie: ClassVar[str] = "modelcard:License"
    class_name: ClassVar[str] = "License"
    class_model_uri: ClassVar[URIRef] = MODELCARD.License

    identifier: Optional[str] = None
    custom_text: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.identifier is not None and not isinstance(self.identifier, str):
            self.identifier = str(self.identifier)

        if self.custom_text is not None and not isinstance(self.custom_text, str):
            self.custom_text = str(self.custom_text)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Owner(YAMLRoot):
    """
    Model owner or maintainer information
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Owner"]
    class_class_curie: ClassVar[str] = "modelcard:Owner"
    class_name: ClassVar[str] = "owner"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Owner

    name: Optional[str] = None
    contact: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.contact is not None and not isinstance(self.contact, str):
            self.contact = str(self.contact)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reference(YAMLRoot):
    """
    Reference to related resources
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Reference"]
    class_class_curie: ClassVar[str] = "modelcard:Reference"
    class_name: ClassVar[str] = "Reference"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Reference

    reference: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.reference is not None and not isinstance(self.reference, str):
            self.reference = str(self.reference)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Citation(YAMLRoot):
    """
    Citation information for the model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Citation"]
    class_class_curie: ClassVar[str] = "modelcard:Citation"
    class_name: ClassVar[str] = "Citation"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Citation

    style: Optional[Union[str, "CitationStyleEnum"]] = None
    citation: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.style is not None and not isinstance(self.style, CitationStyleEnum):
            self.style = CitationStyleEnum(self.style)

        if self.citation is not None and not isinstance(self.citation, str):
            self.citation = str(self.citation)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ModelDetails(YAMLRoot):
    """
    Comprehensive metadata about the model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["ModelDetails"]
    class_class_curie: ClassVar[str] = "modelcard:ModelDetails"
    class_name: ClassVar[str] = "ModelDetails"
    class_model_uri: ClassVar[URIRef] = MODELCARD.ModelDetails

    name: str = None
    overview: Optional[str] = None
    documentation: Optional[str] = None
    owners: Optional[Union[Union[dict, Owner], list[Union[dict, Owner]]]] = empty_list()
    version: Optional[Union[dict, Version]] = None
    licenses: Optional[Union[Union[dict, License], list[Union[dict, License]]]] = empty_list()
    references: Optional[Union[Union[dict, Reference], list[Union[dict, Reference]]]] = empty_list()
    citations: Optional[Union[Union[dict, Citation], list[Union[dict, Citation]]]] = empty_list()
    path: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.overview is not None and not isinstance(self.overview, str):
            self.overview = str(self.overview)

        if self.documentation is not None and not isinstance(self.documentation, str):
            self.documentation = str(self.documentation)

        if not isinstance(self.owners, list):
            self.owners = [self.owners] if self.owners is not None else []
        self.owners = [v if isinstance(v, Owner) else Owner(**as_dict(v)) for v in self.owners]

        if self.version is not None and not isinstance(self.version, Version):
            self.version = Version(**as_dict(self.version))

        if not isinstance(self.licenses, list):
            self.licenses = [self.licenses] if self.licenses is not None else []
        self.licenses = [v if isinstance(v, License) else License(**as_dict(v)) for v in self.licenses]

        if not isinstance(self.references, list):
            self.references = [self.references] if self.references is not None else []
        self.references = [v if isinstance(v, Reference) else Reference(**as_dict(v)) for v in self.references]

        if not isinstance(self.citations, list):
            self.citations = [self.citations] if self.citations is not None else []
        self.citations = [v if isinstance(v, Citation) else Citation(**as_dict(v)) for v in self.citations]

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SensitiveData(YAMLRoot):
    """
    Information about sensitive data in a dataset
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["SensitiveData"]
    class_class_curie: ClassVar[str] = "modelcard:SensitiveData"
    class_name: ClassVar[str] = "SensitiveData"
    class_model_uri: ClassVar[URIRef] = MODELCARD.SensitiveData

    sensitive_data: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.sensitive_data, list):
            self.sensitive_data = [self.sensitive_data] if self.sensitive_data is not None else []
        self.sensitive_data = [v if isinstance(v, str) else str(v) for v in self.sensitive_data]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GraphicsCollection(YAMLRoot):
    """
    Collection of graphics and visualizations
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["GraphicsCollection"]
    class_class_curie: ClassVar[str] = "modelcard:GraphicsCollection"
    class_name: ClassVar[str] = "GraphicsCollection"
    class_model_uri: ClassVar[URIRef] = MODELCARD.GraphicsCollection

    description: Optional[str] = None
    collection: Optional[Union[Union[dict, "Graphic"], list[Union[dict, "Graphic"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.collection, list):
            self.collection = [self.collection] if self.collection is not None else []
        self.collection = [v if isinstance(v, Graphic) else Graphic(**as_dict(v)) for v in self.collection]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Graphic(YAMLRoot):
    """
    A single graphic or visualization
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Graphic"]
    class_class_curie: ClassVar[str] = "modelcard:Graphic"
    class_name: ClassVar[str] = "graphic"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Graphic

    name: Optional[str] = None
    image: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.image is not None and not isinstance(self.image, str):
            self.image = str(self.image)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSet(YAMLRoot):
    """
    Information about a dataset used for training or evaluation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["DataSet"]
    class_class_curie: ClassVar[str] = "modelcard:DataSet"
    class_name: ClassVar[str] = "dataSet"
    class_model_uri: ClassVar[URIRef] = MODELCARD.DataSet

    link: Union[str, URI] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sensitive: Optional[Union[dict, SensitiveData]] = None
    graphics: Optional[Union[dict, GraphicsCollection]] = None
    bias_input: Optional[str] = None
    unit: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.link):
            self.MissingRequiredField("link")
        if not isinstance(self.link, URI):
            self.link = URI(self.link)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.sensitive is not None and not isinstance(self.sensitive, SensitiveData):
            self.sensitive = SensitiveData(**as_dict(self.sensitive))

        if self.graphics is not None and not isinstance(self.graphics, GraphicsCollection):
            self.graphics = GraphicsCollection(**as_dict(self.graphics))

        if self.bias_input is not None and not isinstance(self.bias_input, str):
            self.bias_input = str(self.bias_input)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class KeyVal(YAMLRoot):
    """
    Key-value pair for format mappings
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["KeyVal"]
    class_class_curie: ClassVar[str] = "modelcard:KeyVal"
    class_name: ClassVar[str] = "KeyVal"
    class_model_uri: ClassVar[URIRef] = MODELCARD.KeyVal

    key: Optional[str] = None
    value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.key is not None and not isinstance(self.key, str):
            self.key = str(self.key)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ModelParameters(YAMLRoot):
    """
    Parameters and specifications for model construction
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["ModelParameters"]
    class_class_curie: ClassVar[str] = "modelcard:ModelParameters"
    class_name: ClassVar[str] = "ModelParameters"
    class_model_uri: ClassVar[URIRef] = MODELCARD.ModelParameters

    model_architecture: Optional[str] = None
    data: Optional[Union[Union[dict, DataSet], list[Union[dict, DataSet]]]] = empty_list()
    input_format: Optional[str] = None
    input_format_map: Optional[Union[Union[dict, KeyVal], list[Union[dict, KeyVal]]]] = empty_list()
    output_format: Optional[str] = None
    output_format_map: Optional[Union[Union[dict, KeyVal], list[Union[dict, KeyVal]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.model_architecture is not None and not isinstance(self.model_architecture, str):
            self.model_architecture = str(self.model_architecture)

        self._normalize_inlined_as_dict(slot_name="data", slot_type=DataSet, key_name="link", keyed=False)

        if self.input_format is not None and not isinstance(self.input_format, str):
            self.input_format = str(self.input_format)

        if not isinstance(self.input_format_map, list):
            self.input_format_map = [self.input_format_map] if self.input_format_map is not None else []
        self.input_format_map = [v if isinstance(v, KeyVal) else KeyVal(**as_dict(v)) for v in self.input_format_map]

        if self.output_format is not None and not isinstance(self.output_format, str):
            self.output_format = str(self.output_format)

        if not isinstance(self.output_format_map, list):
            self.output_format_map = [self.output_format_map] if self.output_format_map is not None else []
        self.output_format_map = [v if isinstance(v, KeyVal) else KeyVal(**as_dict(v)) for v in self.output_format_map]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConfidenceInterval(YAMLRoot):
    """
    Confidence interval for a metric value
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["ConfidenceInterval"]
    class_class_curie: ClassVar[str] = "modelcard:ConfidenceInterval"
    class_name: ClassVar[str] = "ConfidenceInterval"
    class_model_uri: ClassVar[URIRef] = MODELCARD.ConfidenceInterval

    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.lower_bound is not None and not isinstance(self.lower_bound, float):
            self.lower_bound = float(self.lower_bound)

        if self.upper_bound is not None and not isinstance(self.upper_bound, float):
            self.upper_bound = float(self.upper_bound)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PerformanceMetric(YAMLRoot):
    """
    A performance metric with optional confidence interval
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["PerformanceMetric"]
    class_class_curie: ClassVar[str] = "modelcard:PerformanceMetric"
    class_name: ClassVar[str] = "performanceMetric"
    class_model_uri: ClassVar[URIRef] = MODELCARD.PerformanceMetric

    type: str = None
    value: Optional[float] = None
    value_error: Optional[float] = None
    confidence_interval: Optional[Union[dict, ConfidenceInterval]] = None
    threshold: Optional[float] = None
    slice: Optional[str] = None
    unit: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.value_error is not None and not isinstance(self.value_error, float):
            self.value_error = float(self.value_error)

        if self.confidence_interval is not None and not isinstance(self.confidence_interval, ConfidenceInterval):
            self.confidence_interval = ConfidenceInterval(**as_dict(self.confidence_interval))

        if self.threshold is not None and not isinstance(self.threshold, float):
            self.threshold = float(self.threshold)

        if self.slice is not None and not isinstance(self.slice, str):
            self.slice = str(self.slice)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantitativeAnalysis(YAMLRoot):
    """
    Quantitative analysis and performance evaluation of the model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["QuantitativeAnalysis"]
    class_class_curie: ClassVar[str] = "modelcard:QuantitativeAnalysis"
    class_name: ClassVar[str] = "QuantitativeAnalysis"
    class_model_uri: ClassVar[URIRef] = MODELCARD.QuantitativeAnalysis

    performance_metrics: Optional[Union[Union[dict, PerformanceMetric], list[Union[dict, PerformanceMetric]]]] = empty_list()
    graphics: Optional[Union[dict, GraphicsCollection]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_dict(slot_name="performance_metrics", slot_type=PerformanceMetric, key_name="type", keyed=False)

        if self.graphics is not None and not isinstance(self.graphics, GraphicsCollection):
            self.graphics = GraphicsCollection(**as_dict(self.graphics))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class User(YAMLRoot):
    """
    Description of an intended user type
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["User"]
    class_class_curie: ClassVar[str] = "modelcard:User"
    class_name: ClassVar[str] = "User"
    class_model_uri: ClassVar[URIRef] = MODELCARD.User

    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UseCase(YAMLRoot):
    """
    Description of a use case or application scenario
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["UseCase"]
    class_class_curie: ClassVar[str] = "modelcard:UseCase"
    class_name: ClassVar[str] = "UseCase"
    class_model_uri: ClassVar[URIRef] = MODELCARD.UseCase

    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Limitation(YAMLRoot):
    """
    A known limitation or constraint of the model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Limitation"]
    class_class_curie: ClassVar[str] = "modelcard:Limitation"
    class_name: ClassVar[str] = "Limitation"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Limitation

    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Tradeoff(YAMLRoot):
    """
    A performance tradeoff consideration
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Tradeoff"]
    class_class_curie: ClassVar[str] = "modelcard:Tradeoff"
    class_name: ClassVar[str] = "Tradeoff"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Tradeoff

    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Risk(YAMLRoot):
    """
    An ethical, environmental, or operational risk
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Risk"]
    class_class_curie: ClassVar[str] = "modelcard:Risk"
    class_name: ClassVar[str] = "risk"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Risk

    name: Optional[str] = None
    mitigation_strategy: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.mitigation_strategy is not None and not isinstance(self.mitigation_strategy, str):
            self.mitigation_strategy = str(self.mitigation_strategy)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Considerations(YAMLRoot):
    """
    Considerations for model usage including limitations and ethical concerns
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Considerations"]
    class_class_curie: ClassVar[str] = "modelcard:Considerations"
    class_name: ClassVar[str] = "Considerations"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Considerations

    users: Optional[Union[Union[dict, User], list[Union[dict, User]]]] = empty_list()
    use_cases: Optional[Union[Union[dict, UseCase], list[Union[dict, UseCase]]]] = empty_list()
    limitations: Optional[Union[Union[dict, Limitation], list[Union[dict, Limitation]]]] = empty_list()
    tradeoffs: Optional[Union[Union[dict, Tradeoff], list[Union[dict, Tradeoff]]]] = empty_list()
    ethical_considerations: Optional[Union[Union[dict, Risk], list[Union[dict, Risk]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.users, list):
            self.users = [self.users] if self.users is not None else []
        self.users = [v if isinstance(v, User) else User(**as_dict(v)) for v in self.users]

        if not isinstance(self.use_cases, list):
            self.use_cases = [self.use_cases] if self.use_cases is not None else []
        self.use_cases = [v if isinstance(v, UseCase) else UseCase(**as_dict(v)) for v in self.use_cases]

        if not isinstance(self.limitations, list):
            self.limitations = [self.limitations] if self.limitations is not None else []
        self.limitations = [v if isinstance(v, Limitation) else Limitation(**as_dict(v)) for v in self.limitations]

        if not isinstance(self.tradeoffs, list):
            self.tradeoffs = [self.tradeoffs] if self.tradeoffs is not None else []
        self.tradeoffs = [v if isinstance(v, Tradeoff) else Tradeoff(**as_dict(v)) for v in self.tradeoffs]

        if not isinstance(self.ethical_considerations, list):
            self.ethical_considerations = [self.ethical_considerations] if self.ethical_considerations is not None else []
        self.ethical_considerations = [v if isinstance(v, Risk) else Risk(**as_dict(v)) for v in self.ethical_considerations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Task(YAMLRoot):
    """
    ML task specification for benchmarking
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["Task"]
    class_class_curie: ClassVar[str] = "modelcard:Task"
    class_name: ClassVar[str] = "Task"
    class_model_uri: ClassVar[URIRef] = MODELCARD.Task

    type: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BenchmarkDataset(YAMLRoot):
    """
    Dataset used for benchmarking
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["BenchmarkDataset"]
    class_class_curie: ClassVar[str] = "modelcard:BenchmarkDataset"
    class_name: ClassVar[str] = "BenchmarkDataset"
    class_model_uri: ClassVar[URIRef] = MODELCARD.BenchmarkDataset

    type: Optional[str] = None
    name: Optional[str] = None
    config: Optional[str] = None
    split: Optional[str] = None
    revision: Optional[str] = None
    args: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.config is not None and not isinstance(self.config, str):
            self.config = str(self.config)

        if self.split is not None and not isinstance(self.split, str):
            self.split = str(self.split)

        if self.revision is not None and not isinstance(self.revision, str):
            self.revision = str(self.revision)

        if self.args is not None and not isinstance(self.args, str):
            self.args = str(self.args)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BenchmarkMetric(YAMLRoot):
    """
    Benchmark metric result
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["BenchmarkMetric"]
    class_class_curie: ClassVar[str] = "modelcard:BenchmarkMetric"
    class_name: ClassVar[str] = "BenchmarkMetric"
    class_model_uri: ClassVar[URIRef] = MODELCARD.BenchmarkMetric

    type: Optional[str] = None
    value: Optional[float] = None
    name: Optional[str] = None
    config: Optional[str] = None
    args: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.config is not None and not isinstance(self.config, str):
            self.config = str(self.config)

        if self.args is not None and not isinstance(self.args, str):
            self.args = str(self.args)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BenchmarkSource(YAMLRoot):
    """
    Source of benchmark results
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["BenchmarkSource"]
    class_class_curie: ClassVar[str] = "modelcard:BenchmarkSource"
    class_name: ClassVar[str] = "BenchmarkSource"
    class_model_uri: ClassVar[URIRef] = MODELCARD.BenchmarkSource

    name: Optional[str] = None
    url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BenchmarkResult(YAMLRoot):
    """
    Benchmark result entry with task, dataset, and metrics
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["BenchmarkResult"]
    class_class_curie: ClassVar[str] = "modelcard:BenchmarkResult"
    class_name: ClassVar[str] = "BenchmarkResult"
    class_model_uri: ClassVar[URIRef] = MODELCARD.BenchmarkResult

    task: Optional[Union[dict, Task]] = None
    dataset: Optional[Union[dict, BenchmarkDataset]] = None
    metrics: Optional[Union[Union[dict, BenchmarkMetric], list[Union[dict, BenchmarkMetric]]]] = empty_list()
    source: Optional[Union[dict, BenchmarkSource]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.task is not None and not isinstance(self.task, Task):
            self.task = Task(**as_dict(self.task))

        if self.dataset is not None and not isinstance(self.dataset, BenchmarkDataset):
            self.dataset = BenchmarkDataset(**as_dict(self.dataset))

        if not isinstance(self.metrics, list):
            self.metrics = [self.metrics] if self.metrics is not None else []
        self.metrics = [v if isinstance(v, BenchmarkMetric) else BenchmarkMetric(**as_dict(v)) for v in self.metrics]

        if self.source is not None and not isinstance(self.source, BenchmarkSource):
            self.source = BenchmarkSource(**as_dict(self.source))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ModelIndex(YAMLRoot):
    """
    Papers with Code model-index structure for benchmark tracking
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["ModelIndex"]
    class_class_curie: ClassVar[str] = "modelcard:ModelIndex"
    class_name: ClassVar[str] = "ModelIndex"
    class_model_uri: ClassVar[URIRef] = MODELCARD.ModelIndex

    name: Optional[str] = None
    results: Optional[Union[Union[dict, BenchmarkResult], list[Union[dict, BenchmarkResult]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, BenchmarkResult) else BenchmarkResult(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ModelCard(YAMLRoot):
    """
    Complete model card with metadata, performance, and considerations
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MODELCARD["ModelCard"]
    class_class_curie: ClassVar[str] = "modelcard:ModelCard"
    class_name: ClassVar[str] = "modelCard"
    class_model_uri: ClassVar[URIRef] = MODELCARD.ModelCard

    model_details: Union[dict, ModelDetails] = None
    schema_version: Optional[str] = None
    model_parameters: Optional[Union[dict, ModelParameters]] = None
    quantitative_analysis: Optional[Union[dict, QuantitativeAnalysis]] = None
    considerations: Optional[Union[dict, Considerations]] = None
    model_category: Optional[str] = None
    bias_model: Optional[str] = None
    bias_output: Optional[str] = None
    framework: Optional[str] = None
    framework_version: Optional[str] = None
    library_name: Optional[str] = None
    pipeline_tag: Optional[str] = None
    language: Optional[Union[str, list[str]]] = empty_list()
    base_model: Optional[str] = None
    tags: Optional[Union[str, list[str]]] = empty_list()
    datasets: Optional[Union[str, list[str]]] = empty_list()
    metrics: Optional[Union[str, list[str]]] = empty_list()
    model_index: Optional[Union[Union[dict, ModelIndex], list[Union[dict, ModelIndex]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.model_details):
            self.MissingRequiredField("model_details")
        if not isinstance(self.model_details, ModelDetails):
            self.model_details = ModelDetails(**as_dict(self.model_details))

        if self.schema_version is not None and not isinstance(self.schema_version, str):
            self.schema_version = str(self.schema_version)

        if self.model_parameters is not None and not isinstance(self.model_parameters, ModelParameters):
            self.model_parameters = ModelParameters(**as_dict(self.model_parameters))

        if self.quantitative_analysis is not None and not isinstance(self.quantitative_analysis, QuantitativeAnalysis):
            self.quantitative_analysis = QuantitativeAnalysis(**as_dict(self.quantitative_analysis))

        if self.considerations is not None and not isinstance(self.considerations, Considerations):
            self.considerations = Considerations(**as_dict(self.considerations))

        if self.model_category is not None and not isinstance(self.model_category, str):
            self.model_category = str(self.model_category)

        if self.bias_model is not None and not isinstance(self.bias_model, str):
            self.bias_model = str(self.bias_model)

        if self.bias_output is not None and not isinstance(self.bias_output, str):
            self.bias_output = str(self.bias_output)

        if self.framework is not None and not isinstance(self.framework, str):
            self.framework = str(self.framework)

        if self.framework_version is not None and not isinstance(self.framework_version, str):
            self.framework_version = str(self.framework_version)

        if self.library_name is not None and not isinstance(self.library_name, str):
            self.library_name = str(self.library_name)

        if self.pipeline_tag is not None and not isinstance(self.pipeline_tag, str):
            self.pipeline_tag = str(self.pipeline_tag)

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, str) else str(v) for v in self.language]

        if self.base_model is not None and not isinstance(self.base_model, str):
            self.base_model = str(self.base_model)

        if not isinstance(self.tags, list):
            self.tags = [self.tags] if self.tags is not None else []
        self.tags = [v if isinstance(v, str) else str(v) for v in self.tags]

        if not isinstance(self.datasets, list):
            self.datasets = [self.datasets] if self.datasets is not None else []
        self.datasets = [v if isinstance(v, str) else str(v) for v in self.datasets]

        if not isinstance(self.metrics, list):
            self.metrics = [self.metrics] if self.metrics is not None else []
        self.metrics = [v if isinstance(v, str) else str(v) for v in self.metrics]

        if not isinstance(self.model_index, list):
            self.model_index = [self.model_index] if self.model_index is not None else []
        self.model_index = [v if isinstance(v, ModelIndex) else ModelIndex(**as_dict(v)) for v in self.model_index]

        super().__post_init__(**kwargs)


# Enumerations
class CitationStyleEnum(EnumDefinitionImpl):
    """
    Citation format styles
    """
    MLA = PermissibleValue(
        text="MLA",
        description="Modern Language Association style")
    APA = PermissibleValue(
        text="APA",
        description="American Psychological Association style")
    Chicago = PermissibleValue(
        text="Chicago",
        description="Chicago Manual of Style")
    IEEE = PermissibleValue(
        text="IEEE",
        description="Institute of Electrical and Electronics Engineers style")

    _defn = EnumDefinition(
        name="CitationStyleEnum",
        description="Citation format styles",
    )

# Slots
class slots:
    pass

slots.name = Slot(uri=MODELCARD.name, name="name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.name, domain=None, range=Optional[str])

slots.description = Slot(uri=MODELCARD.description, name="description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.description, domain=None, range=Optional[str])

slots.contact = Slot(uri=MODELCARD.contact, name="contact", curie=MODELCARD.curie('contact'),
                   model_uri=MODELCARD.contact, domain=None, range=Optional[str])

slots.date = Slot(uri=MODELCARD.date, name="date", curie=MODELCARD.curie('date'),
                   model_uri=MODELCARD.date, domain=None, range=Optional[Union[str, XSDDate]])

slots.diff = Slot(uri=MODELCARD.diff, name="diff", curie=MODELCARD.curie('diff'),
                   model_uri=MODELCARD.diff, domain=None, range=Optional[str])

slots.identifier = Slot(uri=MODELCARD.identifier, name="identifier", curie=MODELCARD.curie('identifier'),
                   model_uri=MODELCARD.identifier, domain=None, range=Optional[str])

slots.custom_text = Slot(uri=MODELCARD.custom_text, name="custom_text", curie=MODELCARD.curie('custom_text'),
                   model_uri=MODELCARD.custom_text, domain=None, range=Optional[str])

slots.reference = Slot(uri=MODELCARD.reference, name="reference", curie=MODELCARD.curie('reference'),
                   model_uri=MODELCARD.reference, domain=None, range=Optional[str])

slots.style = Slot(uri=MODELCARD.style, name="style", curie=MODELCARD.curie('style'),
                   model_uri=MODELCARD.style, domain=None, range=Optional[Union[str, "CitationStyleEnum"]])

slots.citation = Slot(uri=MODELCARD.citation, name="citation", curie=MODELCARD.curie('citation'),
                   model_uri=MODELCARD.citation, domain=None, range=Optional[str])

slots.overview = Slot(uri=MODELCARD.overview, name="overview", curie=MODELCARD.curie('overview'),
                   model_uri=MODELCARD.overview, domain=None, range=Optional[str])

slots.documentation = Slot(uri=MODELCARD.documentation, name="documentation", curie=MODELCARD.curie('documentation'),
                   model_uri=MODELCARD.documentation, domain=None, range=Optional[str])

slots.owners = Slot(uri=MODELCARD.owners, name="owners", curie=MODELCARD.curie('owners'),
                   model_uri=MODELCARD.owners, domain=None, range=Optional[Union[str, list[str]]])

slots.version = Slot(uri=MODELCARD.version, name="version", curie=MODELCARD.curie('version'),
                   model_uri=MODELCARD.version, domain=None, range=Optional[str])

slots.licenses = Slot(uri=MODELCARD.licenses, name="licenses", curie=MODELCARD.curie('licenses'),
                   model_uri=MODELCARD.licenses, domain=None, range=Optional[Union[str, list[str]]])

slots.references = Slot(uri=MODELCARD.references, name="references", curie=MODELCARD.curie('references'),
                   model_uri=MODELCARD.references, domain=None, range=Optional[Union[str, list[str]]])

slots.citations = Slot(uri=MODELCARD.citations, name="citations", curie=MODELCARD.curie('citations'),
                   model_uri=MODELCARD.citations, domain=None, range=Optional[Union[str, list[str]]])

slots.path = Slot(uri=MODELCARD.path, name="path", curie=MODELCARD.curie('path'),
                   model_uri=MODELCARD.path, domain=None, range=Optional[str])

slots.link = Slot(uri=MODELCARD.link, name="link", curie=MODELCARD.curie('link'),
                   model_uri=MODELCARD.link, domain=None, range=Optional[Union[str, URI]])

slots.sensitive = Slot(uri=MODELCARD.sensitive, name="sensitive", curie=MODELCARD.curie('sensitive'),
                   model_uri=MODELCARD.sensitive, domain=None, range=Optional[str])

slots.graphics = Slot(uri=MODELCARD.graphics, name="graphics", curie=MODELCARD.curie('graphics'),
                   model_uri=MODELCARD.graphics, domain=None, range=Optional[str])

slots.bias_input = Slot(uri=MODELCARD.bias_input, name="bias_input", curie=MODELCARD.curie('bias_input'),
                   model_uri=MODELCARD.bias_input, domain=None, range=Optional[str])

slots.unit = Slot(uri=MODELCARD.unit, name="unit", curie=MODELCARD.curie('unit'),
                   model_uri=MODELCARD.unit, domain=None, range=Optional[str])

slots.sensitive_data = Slot(uri=MODELCARD.sensitive_data, name="sensitive_data", curie=MODELCARD.curie('sensitive_data'),
                   model_uri=MODELCARD.sensitive_data, domain=None, range=Optional[Union[str, list[str]]])

slots.model_architecture = Slot(uri=MODELCARD.model_architecture, name="model_architecture", curie=MODELCARD.curie('model_architecture'),
                   model_uri=MODELCARD.model_architecture, domain=None, range=Optional[str])

slots.data = Slot(uri=MODELCARD.data, name="data", curie=MODELCARD.curie('data'),
                   model_uri=MODELCARD.data, domain=None, range=Optional[Union[str, list[str]]])

slots.input_format = Slot(uri=MODELCARD.input_format, name="input_format", curie=MODELCARD.curie('input_format'),
                   model_uri=MODELCARD.input_format, domain=None, range=Optional[str])

slots.input_format_map = Slot(uri=MODELCARD.input_format_map, name="input_format_map", curie=MODELCARD.curie('input_format_map'),
                   model_uri=MODELCARD.input_format_map, domain=None, range=Optional[Union[str, list[str]]])

slots.output_format = Slot(uri=MODELCARD.output_format, name="output_format", curie=MODELCARD.curie('output_format'),
                   model_uri=MODELCARD.output_format, domain=None, range=Optional[str])

slots.output_format_map = Slot(uri=MODELCARD.output_format_map, name="output_format_map", curie=MODELCARD.curie('output_format_map'),
                   model_uri=MODELCARD.output_format_map, domain=None, range=Optional[Union[str, list[str]]])

slots.key = Slot(uri=MODELCARD.key, name="key", curie=MODELCARD.curie('key'),
                   model_uri=MODELCARD.key, domain=None, range=Optional[str])

slots.value = Slot(uri=MODELCARD.value, name="value", curie=MODELCARD.curie('value'),
                   model_uri=MODELCARD.value, domain=None, range=Optional[str])

slots.type = Slot(uri=MODELCARD.type, name="type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.type, domain=None, range=Optional[str])

slots.value_error = Slot(uri=MODELCARD.value_error, name="value_error", curie=MODELCARD.curie('value_error'),
                   model_uri=MODELCARD.value_error, domain=None, range=Optional[float])

slots.confidence_interval = Slot(uri=MODELCARD.confidence_interval, name="confidence_interval", curie=MODELCARD.curie('confidence_interval'),
                   model_uri=MODELCARD.confidence_interval, domain=None, range=Optional[str])

slots.threshold = Slot(uri=MODELCARD.threshold, name="threshold", curie=MODELCARD.curie('threshold'),
                   model_uri=MODELCARD.threshold, domain=None, range=Optional[float])

slots.slice = Slot(uri=MODELCARD.slice, name="slice", curie=MODELCARD.curie('slice'),
                   model_uri=MODELCARD.slice, domain=None, range=Optional[str])

slots.lower_bound = Slot(uri=MODELCARD.lower_bound, name="lower_bound", curie=MODELCARD.curie('lower_bound'),
                   model_uri=MODELCARD.lower_bound, domain=None, range=Optional[float])

slots.upper_bound = Slot(uri=MODELCARD.upper_bound, name="upper_bound", curie=MODELCARD.curie('upper_bound'),
                   model_uri=MODELCARD.upper_bound, domain=None, range=Optional[float])

slots.collection = Slot(uri=MODELCARD.collection, name="collection", curie=MODELCARD.curie('collection'),
                   model_uri=MODELCARD.collection, domain=None, range=Optional[Union[str, list[str]]])

slots.image = Slot(uri=MODELCARD.image, name="image", curie=MODELCARD.curie('image'),
                   model_uri=MODELCARD.image, domain=None, range=Optional[str])

slots.performance_metrics = Slot(uri=MODELCARD.performance_metrics, name="performance_metrics", curie=MODELCARD.curie('performance_metrics'),
                   model_uri=MODELCARD.performance_metrics, domain=None, range=Optional[Union[str, list[str]]])

slots.users = Slot(uri=MODELCARD.users, name="users", curie=MODELCARD.curie('users'),
                   model_uri=MODELCARD.users, domain=None, range=Optional[Union[str, list[str]]])

slots.use_cases = Slot(uri=MODELCARD.use_cases, name="use_cases", curie=MODELCARD.curie('use_cases'),
                   model_uri=MODELCARD.use_cases, domain=None, range=Optional[Union[str, list[str]]])

slots.limitations = Slot(uri=MODELCARD.limitations, name="limitations", curie=MODELCARD.curie('limitations'),
                   model_uri=MODELCARD.limitations, domain=None, range=Optional[Union[str, list[str]]])

slots.tradeoffs = Slot(uri=MODELCARD.tradeoffs, name="tradeoffs", curie=MODELCARD.curie('tradeoffs'),
                   model_uri=MODELCARD.tradeoffs, domain=None, range=Optional[Union[str, list[str]]])

slots.ethical_considerations = Slot(uri=MODELCARD.ethical_considerations, name="ethical_considerations", curie=MODELCARD.curie('ethical_considerations'),
                   model_uri=MODELCARD.ethical_considerations, domain=None, range=Optional[Union[str, list[str]]])

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

slots.bias_model = Slot(uri=MODELCARD.bias_model, name="bias_model", curie=MODELCARD.curie('bias_model'),
                   model_uri=MODELCARD.bias_model, domain=None, range=Optional[str])

slots.bias_output = Slot(uri=MODELCARD.bias_output, name="bias_output", curie=MODELCARD.curie('bias_output'),
                   model_uri=MODELCARD.bias_output, domain=None, range=Optional[str])

slots.framework = Slot(uri=MODELCARD.framework, name="framework", curie=MODELCARD.curie('framework'),
                   model_uri=MODELCARD.framework, domain=None, range=Optional[str])

slots.framework_version = Slot(uri=MODELCARD.framework_version, name="framework_version", curie=MODELCARD.curie('framework_version'),
                   model_uri=MODELCARD.framework_version, domain=None, range=Optional[str])

slots.library_name = Slot(uri=MODELCARD.library_name, name="library_name", curie=MODELCARD.curie('library_name'),
                   model_uri=MODELCARD.library_name, domain=None, range=Optional[str])

slots.pipeline_tag = Slot(uri=MODELCARD.pipeline_tag, name="pipeline_tag", curie=MODELCARD.curie('pipeline_tag'),
                   model_uri=MODELCARD.pipeline_tag, domain=None, range=Optional[str])

slots.language = Slot(uri=MODELCARD.language, name="language", curie=MODELCARD.curie('language'),
                   model_uri=MODELCARD.language, domain=None, range=Optional[Union[str, list[str]]])

slots.base_model = Slot(uri=MODELCARD.base_model, name="base_model", curie=MODELCARD.curie('base_model'),
                   model_uri=MODELCARD.base_model, domain=None, range=Optional[str])

slots.tags = Slot(uri=MODELCARD.tags, name="tags", curie=MODELCARD.curie('tags'),
                   model_uri=MODELCARD.tags, domain=None, range=Optional[Union[str, list[str]]])

slots.datasets = Slot(uri=MODELCARD.datasets, name="datasets", curie=MODELCARD.curie('datasets'),
                   model_uri=MODELCARD.datasets, domain=None, range=Optional[Union[str, list[str]]])

slots.metrics = Slot(uri=MODELCARD.metrics, name="metrics", curie=MODELCARD.curie('metrics'),
                   model_uri=MODELCARD.metrics, domain=None, range=Optional[Union[str, list[str]]])

slots.task = Slot(uri=MODELCARD.task, name="task", curie=MODELCARD.curie('task'),
                   model_uri=MODELCARD.task, domain=None, range=Optional[str])

slots.dataset = Slot(uri=MODELCARD.dataset, name="dataset", curie=MODELCARD.curie('dataset'),
                   model_uri=MODELCARD.dataset, domain=None, range=Optional[str])

slots.source = Slot(uri=MODELCARD.source, name="source", curie=MODELCARD.curie('source'),
                   model_uri=MODELCARD.source, domain=None, range=Optional[str])

slots.results = Slot(uri=MODELCARD.results, name="results", curie=MODELCARD.curie('results'),
                   model_uri=MODELCARD.results, domain=None, range=Optional[Union[str, list[str]]])

slots.model_index = Slot(uri=MODELCARD.model_index, name="model_index", curie=MODELCARD.curie('model_index'),
                   model_uri=MODELCARD.model_index, domain=None, range=Optional[Union[str, list[str]]])

slots.config = Slot(uri=MODELCARD.config, name="config", curie=MODELCARD.curie('config'),
                   model_uri=MODELCARD.config, domain=None, range=Optional[str])

slots.split = Slot(uri=MODELCARD.split, name="split", curie=MODELCARD.curie('split'),
                   model_uri=MODELCARD.split, domain=None, range=Optional[str])

slots.revision = Slot(uri=MODELCARD.revision, name="revision", curie=MODELCARD.curie('revision'),
                   model_uri=MODELCARD.revision, domain=None, range=Optional[str])

slots.args = Slot(uri=MODELCARD.args, name="args", curie=MODELCARD.curie('args'),
                   model_uri=MODELCARD.args, domain=None, range=Optional[str])

slots.url = Slot(uri=MODELCARD.url, name="url", curie=MODELCARD.curie('url'),
                   model_uri=MODELCARD.url, domain=None, range=Optional[Union[str, URI]])

slots.Version_name = Slot(uri=MODELCARD.name, name="Version_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.Version_name, domain=Version, range=Optional[str])

slots.Version_date = Slot(uri=MODELCARD.date, name="Version_date", curie=MODELCARD.curie('date'),
                   model_uri=MODELCARD.Version_date, domain=Version, range=Optional[Union[str, XSDDate]])

slots.Version_diff = Slot(uri=MODELCARD.diff, name="Version_diff", curie=MODELCARD.curie('diff'),
                   model_uri=MODELCARD.Version_diff, domain=Version, range=Optional[str])

slots.License_identifier = Slot(uri=MODELCARD.identifier, name="License_identifier", curie=MODELCARD.curie('identifier'),
                   model_uri=MODELCARD.License_identifier, domain=License, range=Optional[str])

slots.License_custom_text = Slot(uri=MODELCARD.custom_text, name="License_custom_text", curie=MODELCARD.curie('custom_text'),
                   model_uri=MODELCARD.License_custom_text, domain=License, range=Optional[str])

slots.owner_name = Slot(uri=MODELCARD.name, name="owner_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.owner_name, domain=Owner, range=Optional[str])

slots.owner_contact = Slot(uri=MODELCARD.contact, name="owner_contact", curie=MODELCARD.curie('contact'),
                   model_uri=MODELCARD.owner_contact, domain=Owner, range=Optional[str])

slots.Reference_reference = Slot(uri=MODELCARD.reference, name="Reference_reference", curie=MODELCARD.curie('reference'),
                   model_uri=MODELCARD.Reference_reference, domain=Reference, range=Optional[str])

slots.Citation_style = Slot(uri=MODELCARD.style, name="Citation_style", curie=MODELCARD.curie('style'),
                   model_uri=MODELCARD.Citation_style, domain=Citation, range=Optional[Union[str, "CitationStyleEnum"]])

slots.Citation_citation = Slot(uri=MODELCARD.citation, name="Citation_citation", curie=MODELCARD.curie('citation'),
                   model_uri=MODELCARD.Citation_citation, domain=Citation, range=Optional[str])

slots.ModelDetails_name = Slot(uri=MODELCARD.name, name="ModelDetails_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.ModelDetails_name, domain=ModelDetails, range=str)

slots.ModelDetails_overview = Slot(uri=MODELCARD.overview, name="ModelDetails_overview", curie=MODELCARD.curie('overview'),
                   model_uri=MODELCARD.ModelDetails_overview, domain=ModelDetails, range=Optional[str])

slots.ModelDetails_documentation = Slot(uri=MODELCARD.documentation, name="ModelDetails_documentation", curie=MODELCARD.curie('documentation'),
                   model_uri=MODELCARD.ModelDetails_documentation, domain=ModelDetails, range=Optional[str])

slots.ModelDetails_owners = Slot(uri=MODELCARD.owners, name="ModelDetails_owners", curie=MODELCARD.curie('owners'),
                   model_uri=MODELCARD.ModelDetails_owners, domain=ModelDetails, range=Optional[Union[Union[dict, Owner], list[Union[dict, Owner]]]])

slots.ModelDetails_version = Slot(uri=MODELCARD.version, name="ModelDetails_version", curie=MODELCARD.curie('version'),
                   model_uri=MODELCARD.ModelDetails_version, domain=ModelDetails, range=Optional[Union[dict, Version]])

slots.ModelDetails_licenses = Slot(uri=MODELCARD.licenses, name="ModelDetails_licenses", curie=MODELCARD.curie('licenses'),
                   model_uri=MODELCARD.ModelDetails_licenses, domain=ModelDetails, range=Optional[Union[Union[dict, License], list[Union[dict, License]]]])

slots.ModelDetails_references = Slot(uri=MODELCARD.references, name="ModelDetails_references", curie=MODELCARD.curie('references'),
                   model_uri=MODELCARD.ModelDetails_references, domain=ModelDetails, range=Optional[Union[Union[dict, Reference], list[Union[dict, Reference]]]])

slots.ModelDetails_citations = Slot(uri=MODELCARD.citations, name="ModelDetails_citations", curie=MODELCARD.curie('citations'),
                   model_uri=MODELCARD.ModelDetails_citations, domain=ModelDetails, range=Optional[Union[Union[dict, Citation], list[Union[dict, Citation]]]])

slots.ModelDetails_path = Slot(uri=MODELCARD.path, name="ModelDetails_path", curie=MODELCARD.curie('path'),
                   model_uri=MODELCARD.ModelDetails_path, domain=ModelDetails, range=Optional[str])

slots.SensitiveData_sensitive_data = Slot(uri=MODELCARD.sensitive_data, name="SensitiveData_sensitive_data", curie=MODELCARD.curie('sensitive_data'),
                   model_uri=MODELCARD.SensitiveData_sensitive_data, domain=SensitiveData, range=Optional[Union[str, list[str]]])

slots.GraphicsCollection_description = Slot(uri=MODELCARD.description, name="GraphicsCollection_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.GraphicsCollection_description, domain=GraphicsCollection, range=Optional[str])

slots.GraphicsCollection_collection = Slot(uri=MODELCARD.collection, name="GraphicsCollection_collection", curie=MODELCARD.curie('collection'),
                   model_uri=MODELCARD.GraphicsCollection_collection, domain=GraphicsCollection, range=Optional[Union[Union[dict, "Graphic"], list[Union[dict, "Graphic"]]]])

slots.graphic_name = Slot(uri=MODELCARD.name, name="graphic_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.graphic_name, domain=Graphic, range=Optional[str])

slots.graphic_image = Slot(uri=MODELCARD.image, name="graphic_image", curie=MODELCARD.curie('image'),
                   model_uri=MODELCARD.graphic_image, domain=Graphic, range=Optional[str])

slots.dataSet_name = Slot(uri=MODELCARD.name, name="dataSet_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.dataSet_name, domain=DataSet, range=Optional[str])

slots.dataSet_description = Slot(uri=MODELCARD.description, name="dataSet_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.dataSet_description, domain=DataSet, range=Optional[str])

slots.dataSet_link = Slot(uri=MODELCARD.link, name="dataSet_link", curie=MODELCARD.curie('link'),
                   model_uri=MODELCARD.dataSet_link, domain=DataSet, range=Union[str, URI])

slots.dataSet_sensitive = Slot(uri=MODELCARD.sensitive, name="dataSet_sensitive", curie=MODELCARD.curie('sensitive'),
                   model_uri=MODELCARD.dataSet_sensitive, domain=DataSet, range=Optional[Union[dict, SensitiveData]])

slots.dataSet_graphics = Slot(uri=MODELCARD.graphics, name="dataSet_graphics", curie=MODELCARD.curie('graphics'),
                   model_uri=MODELCARD.dataSet_graphics, domain=DataSet, range=Optional[Union[dict, GraphicsCollection]])

slots.dataSet_bias_input = Slot(uri=MODELCARD.bias_input, name="dataSet_bias_input", curie=MODELCARD.curie('bias_input'),
                   model_uri=MODELCARD.dataSet_bias_input, domain=DataSet, range=Optional[str])

slots.dataSet_unit = Slot(uri=MODELCARD.unit, name="dataSet_unit", curie=MODELCARD.curie('unit'),
                   model_uri=MODELCARD.dataSet_unit, domain=DataSet, range=Optional[str])

slots.KeyVal_key = Slot(uri=MODELCARD.key, name="KeyVal_key", curie=MODELCARD.curie('key'),
                   model_uri=MODELCARD.KeyVal_key, domain=KeyVal, range=Optional[str])

slots.KeyVal_value = Slot(uri=MODELCARD.value, name="KeyVal_value", curie=MODELCARD.curie('value'),
                   model_uri=MODELCARD.KeyVal_value, domain=KeyVal, range=Optional[str])

slots.ModelParameters_model_architecture = Slot(uri=MODELCARD.model_architecture, name="ModelParameters_model_architecture", curie=MODELCARD.curie('model_architecture'),
                   model_uri=MODELCARD.ModelParameters_model_architecture, domain=ModelParameters, range=Optional[str])

slots.ModelParameters_data = Slot(uri=MODELCARD.data, name="ModelParameters_data", curie=MODELCARD.curie('data'),
                   model_uri=MODELCARD.ModelParameters_data, domain=ModelParameters, range=Optional[Union[Union[dict, DataSet], list[Union[dict, DataSet]]]])

slots.ModelParameters_input_format = Slot(uri=MODELCARD.input_format, name="ModelParameters_input_format", curie=MODELCARD.curie('input_format'),
                   model_uri=MODELCARD.ModelParameters_input_format, domain=ModelParameters, range=Optional[str])

slots.ModelParameters_input_format_map = Slot(uri=MODELCARD.input_format_map, name="ModelParameters_input_format_map", curie=MODELCARD.curie('input_format_map'),
                   model_uri=MODELCARD.ModelParameters_input_format_map, domain=ModelParameters, range=Optional[Union[Union[dict, KeyVal], list[Union[dict, KeyVal]]]])

slots.ModelParameters_output_format = Slot(uri=MODELCARD.output_format, name="ModelParameters_output_format", curie=MODELCARD.curie('output_format'),
                   model_uri=MODELCARD.ModelParameters_output_format, domain=ModelParameters, range=Optional[str])

slots.ModelParameters_output_format_map = Slot(uri=MODELCARD.output_format_map, name="ModelParameters_output_format_map", curie=MODELCARD.curie('output_format_map'),
                   model_uri=MODELCARD.ModelParameters_output_format_map, domain=ModelParameters, range=Optional[Union[Union[dict, KeyVal], list[Union[dict, KeyVal]]]])

slots.ConfidenceInterval_lower_bound = Slot(uri=MODELCARD.lower_bound, name="ConfidenceInterval_lower_bound", curie=MODELCARD.curie('lower_bound'),
                   model_uri=MODELCARD.ConfidenceInterval_lower_bound, domain=ConfidenceInterval, range=Optional[float])

slots.ConfidenceInterval_upper_bound = Slot(uri=MODELCARD.upper_bound, name="ConfidenceInterval_upper_bound", curie=MODELCARD.curie('upper_bound'),
                   model_uri=MODELCARD.ConfidenceInterval_upper_bound, domain=ConfidenceInterval, range=Optional[float])

slots.performanceMetric_type = Slot(uri=MODELCARD.type, name="performanceMetric_type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.performanceMetric_type, domain=PerformanceMetric, range=str)

slots.performanceMetric_value = Slot(uri=MODELCARD.value, name="performanceMetric_value", curie=MODELCARD.curie('value'),
                   model_uri=MODELCARD.performanceMetric_value, domain=PerformanceMetric, range=Optional[float])

slots.performanceMetric_value_error = Slot(uri=MODELCARD.value_error, name="performanceMetric_value_error", curie=MODELCARD.curie('value_error'),
                   model_uri=MODELCARD.performanceMetric_value_error, domain=PerformanceMetric, range=Optional[float])

slots.performanceMetric_confidence_interval = Slot(uri=MODELCARD.confidence_interval, name="performanceMetric_confidence_interval", curie=MODELCARD.curie('confidence_interval'),
                   model_uri=MODELCARD.performanceMetric_confidence_interval, domain=PerformanceMetric, range=Optional[Union[dict, ConfidenceInterval]])

slots.performanceMetric_threshold = Slot(uri=MODELCARD.threshold, name="performanceMetric_threshold", curie=MODELCARD.curie('threshold'),
                   model_uri=MODELCARD.performanceMetric_threshold, domain=PerformanceMetric, range=Optional[float])

slots.performanceMetric_slice = Slot(uri=MODELCARD.slice, name="performanceMetric_slice", curie=MODELCARD.curie('slice'),
                   model_uri=MODELCARD.performanceMetric_slice, domain=PerformanceMetric, range=Optional[str])

slots.performanceMetric_unit = Slot(uri=MODELCARD.unit, name="performanceMetric_unit", curie=MODELCARD.curie('unit'),
                   model_uri=MODELCARD.performanceMetric_unit, domain=PerformanceMetric, range=Optional[str])

slots.QuantitativeAnalysis_performance_metrics = Slot(uri=MODELCARD.performance_metrics, name="QuantitativeAnalysis_performance_metrics", curie=MODELCARD.curie('performance_metrics'),
                   model_uri=MODELCARD.QuantitativeAnalysis_performance_metrics, domain=QuantitativeAnalysis, range=Optional[Union[Union[dict, PerformanceMetric], list[Union[dict, PerformanceMetric]]]])

slots.QuantitativeAnalysis_graphics = Slot(uri=MODELCARD.graphics, name="QuantitativeAnalysis_graphics", curie=MODELCARD.curie('graphics'),
                   model_uri=MODELCARD.QuantitativeAnalysis_graphics, domain=QuantitativeAnalysis, range=Optional[Union[dict, GraphicsCollection]])

slots.User_description = Slot(uri=MODELCARD.description, name="User_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.User_description, domain=User, range=Optional[str])

slots.UseCase_description = Slot(uri=MODELCARD.description, name="UseCase_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.UseCase_description, domain=UseCase, range=Optional[str])

slots.Limitation_description = Slot(uri=MODELCARD.description, name="Limitation_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.Limitation_description, domain=Limitation, range=Optional[str])

slots.Tradeoff_description = Slot(uri=MODELCARD.description, name="Tradeoff_description", curie=MODELCARD.curie('description'),
                   model_uri=MODELCARD.Tradeoff_description, domain=Tradeoff, range=Optional[str])

slots.risk_name = Slot(uri=MODELCARD.name, name="risk_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.risk_name, domain=Risk, range=Optional[str])

slots.risk_mitigation_strategy = Slot(uri=MODELCARD.mitigation_strategy, name="risk_mitigation_strategy", curie=MODELCARD.curie('mitigation_strategy'),
                   model_uri=MODELCARD.risk_mitigation_strategy, domain=Risk, range=Optional[str])

slots.Considerations_users = Slot(uri=MODELCARD.users, name="Considerations_users", curie=MODELCARD.curie('users'),
                   model_uri=MODELCARD.Considerations_users, domain=Considerations, range=Optional[Union[Union[dict, User], list[Union[dict, User]]]])

slots.Considerations_use_cases = Slot(uri=MODELCARD.use_cases, name="Considerations_use_cases", curie=MODELCARD.curie('use_cases'),
                   model_uri=MODELCARD.Considerations_use_cases, domain=Considerations, range=Optional[Union[Union[dict, UseCase], list[Union[dict, UseCase]]]])

slots.Considerations_limitations = Slot(uri=MODELCARD.limitations, name="Considerations_limitations", curie=MODELCARD.curie('limitations'),
                   model_uri=MODELCARD.Considerations_limitations, domain=Considerations, range=Optional[Union[Union[dict, Limitation], list[Union[dict, Limitation]]]])

slots.Considerations_tradeoffs = Slot(uri=MODELCARD.tradeoffs, name="Considerations_tradeoffs", curie=MODELCARD.curie('tradeoffs'),
                   model_uri=MODELCARD.Considerations_tradeoffs, domain=Considerations, range=Optional[Union[Union[dict, Tradeoff], list[Union[dict, Tradeoff]]]])

slots.Considerations_ethical_considerations = Slot(uri=MODELCARD.ethical_considerations, name="Considerations_ethical_considerations", curie=MODELCARD.curie('ethical_considerations'),
                   model_uri=MODELCARD.Considerations_ethical_considerations, domain=Considerations, range=Optional[Union[Union[dict, Risk], list[Union[dict, Risk]]]])

slots.Task_type = Slot(uri=MODELCARD.type, name="Task_type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.Task_type, domain=Task, range=Optional[str])

slots.Task_name = Slot(uri=MODELCARD.name, name="Task_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.Task_name, domain=Task, range=Optional[str])

slots.BenchmarkDataset_type = Slot(uri=MODELCARD.type, name="BenchmarkDataset_type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.BenchmarkDataset_type, domain=BenchmarkDataset, range=Optional[str])

slots.BenchmarkDataset_name = Slot(uri=MODELCARD.name, name="BenchmarkDataset_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.BenchmarkDataset_name, domain=BenchmarkDataset, range=Optional[str])

slots.BenchmarkDataset_config = Slot(uri=MODELCARD.config, name="BenchmarkDataset_config", curie=MODELCARD.curie('config'),
                   model_uri=MODELCARD.BenchmarkDataset_config, domain=BenchmarkDataset, range=Optional[str])

slots.BenchmarkDataset_split = Slot(uri=MODELCARD.split, name="BenchmarkDataset_split", curie=MODELCARD.curie('split'),
                   model_uri=MODELCARD.BenchmarkDataset_split, domain=BenchmarkDataset, range=Optional[str])

slots.BenchmarkDataset_revision = Slot(uri=MODELCARD.revision, name="BenchmarkDataset_revision", curie=MODELCARD.curie('revision'),
                   model_uri=MODELCARD.BenchmarkDataset_revision, domain=BenchmarkDataset, range=Optional[str])

slots.BenchmarkDataset_args = Slot(uri=MODELCARD.args, name="BenchmarkDataset_args", curie=MODELCARD.curie('args'),
                   model_uri=MODELCARD.BenchmarkDataset_args, domain=BenchmarkDataset, range=Optional[str])

slots.BenchmarkMetric_type = Slot(uri=MODELCARD.type, name="BenchmarkMetric_type", curie=MODELCARD.curie('type'),
                   model_uri=MODELCARD.BenchmarkMetric_type, domain=BenchmarkMetric, range=Optional[str])

slots.BenchmarkMetric_value = Slot(uri=MODELCARD.value, name="BenchmarkMetric_value", curie=MODELCARD.curie('value'),
                   model_uri=MODELCARD.BenchmarkMetric_value, domain=BenchmarkMetric, range=Optional[float])

slots.BenchmarkMetric_name = Slot(uri=MODELCARD.name, name="BenchmarkMetric_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.BenchmarkMetric_name, domain=BenchmarkMetric, range=Optional[str])

slots.BenchmarkMetric_config = Slot(uri=MODELCARD.config, name="BenchmarkMetric_config", curie=MODELCARD.curie('config'),
                   model_uri=MODELCARD.BenchmarkMetric_config, domain=BenchmarkMetric, range=Optional[str])

slots.BenchmarkMetric_args = Slot(uri=MODELCARD.args, name="BenchmarkMetric_args", curie=MODELCARD.curie('args'),
                   model_uri=MODELCARD.BenchmarkMetric_args, domain=BenchmarkMetric, range=Optional[str])

slots.BenchmarkSource_name = Slot(uri=MODELCARD.name, name="BenchmarkSource_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.BenchmarkSource_name, domain=BenchmarkSource, range=Optional[str])

slots.BenchmarkSource_url = Slot(uri=MODELCARD.url, name="BenchmarkSource_url", curie=MODELCARD.curie('url'),
                   model_uri=MODELCARD.BenchmarkSource_url, domain=BenchmarkSource, range=Optional[Union[str, URI]])

slots.BenchmarkResult_task = Slot(uri=MODELCARD.task, name="BenchmarkResult_task", curie=MODELCARD.curie('task'),
                   model_uri=MODELCARD.BenchmarkResult_task, domain=BenchmarkResult, range=Optional[Union[dict, Task]])

slots.BenchmarkResult_dataset = Slot(uri=MODELCARD.dataset, name="BenchmarkResult_dataset", curie=MODELCARD.curie('dataset'),
                   model_uri=MODELCARD.BenchmarkResult_dataset, domain=BenchmarkResult, range=Optional[Union[dict, BenchmarkDataset]])

slots.BenchmarkResult_metrics = Slot(uri=MODELCARD.metrics, name="BenchmarkResult_metrics", curie=MODELCARD.curie('metrics'),
                   model_uri=MODELCARD.BenchmarkResult_metrics, domain=BenchmarkResult, range=Optional[Union[Union[dict, BenchmarkMetric], list[Union[dict, BenchmarkMetric]]]])

slots.BenchmarkResult_source = Slot(uri=MODELCARD.source, name="BenchmarkResult_source", curie=MODELCARD.curie('source'),
                   model_uri=MODELCARD.BenchmarkResult_source, domain=BenchmarkResult, range=Optional[Union[dict, BenchmarkSource]])

slots.ModelIndex_name = Slot(uri=MODELCARD.name, name="ModelIndex_name", curie=MODELCARD.curie('name'),
                   model_uri=MODELCARD.ModelIndex_name, domain=ModelIndex, range=Optional[str])

slots.ModelIndex_results = Slot(uri=MODELCARD.results, name="ModelIndex_results", curie=MODELCARD.curie('results'),
                   model_uri=MODELCARD.ModelIndex_results, domain=ModelIndex, range=Optional[Union[Union[dict, BenchmarkResult], list[Union[dict, BenchmarkResult]]]])

slots.modelCard_schema_version = Slot(uri=MODELCARD.schema_version, name="modelCard_schema_version", curie=MODELCARD.curie('schema_version'),
                   model_uri=MODELCARD.modelCard_schema_version, domain=ModelCard, range=Optional[str])

slots.modelCard_model_details = Slot(uri=MODELCARD.model_details, name="modelCard_model_details", curie=MODELCARD.curie('model_details'),
                   model_uri=MODELCARD.modelCard_model_details, domain=ModelCard, range=Union[dict, ModelDetails])

slots.modelCard_model_parameters = Slot(uri=MODELCARD.model_parameters, name="modelCard_model_parameters", curie=MODELCARD.curie('model_parameters'),
                   model_uri=MODELCARD.modelCard_model_parameters, domain=ModelCard, range=Optional[Union[dict, ModelParameters]])

slots.modelCard_quantitative_analysis = Slot(uri=MODELCARD.quantitative_analysis, name="modelCard_quantitative_analysis", curie=MODELCARD.curie('quantitative_analysis'),
                   model_uri=MODELCARD.modelCard_quantitative_analysis, domain=ModelCard, range=Optional[Union[dict, QuantitativeAnalysis]])

slots.modelCard_considerations = Slot(uri=MODELCARD.considerations, name="modelCard_considerations", curie=MODELCARD.curie('considerations'),
                   model_uri=MODELCARD.modelCard_considerations, domain=ModelCard, range=Optional[Union[dict, Considerations]])

slots.modelCard_model_category = Slot(uri=MODELCARD.model_category, name="modelCard_model_category", curie=MODELCARD.curie('model_category'),
                   model_uri=MODELCARD.modelCard_model_category, domain=ModelCard, range=Optional[str])

slots.modelCard_bias_model = Slot(uri=MODELCARD.bias_model, name="modelCard_bias_model", curie=MODELCARD.curie('bias_model'),
                   model_uri=MODELCARD.modelCard_bias_model, domain=ModelCard, range=Optional[str])

slots.modelCard_bias_output = Slot(uri=MODELCARD.bias_output, name="modelCard_bias_output", curie=MODELCARD.curie('bias_output'),
                   model_uri=MODELCARD.modelCard_bias_output, domain=ModelCard, range=Optional[str])

slots.modelCard_framework = Slot(uri=MODELCARD.framework, name="modelCard_framework", curie=MODELCARD.curie('framework'),
                   model_uri=MODELCARD.modelCard_framework, domain=ModelCard, range=Optional[str])

slots.modelCard_framework_version = Slot(uri=MODELCARD.framework_version, name="modelCard_framework_version", curie=MODELCARD.curie('framework_version'),
                   model_uri=MODELCARD.modelCard_framework_version, domain=ModelCard, range=Optional[str])

slots.modelCard_library_name = Slot(uri=MODELCARD.library_name, name="modelCard_library_name", curie=MODELCARD.curie('library_name'),
                   model_uri=MODELCARD.modelCard_library_name, domain=ModelCard, range=Optional[str])

slots.modelCard_pipeline_tag = Slot(uri=MODELCARD.pipeline_tag, name="modelCard_pipeline_tag", curie=MODELCARD.curie('pipeline_tag'),
                   model_uri=MODELCARD.modelCard_pipeline_tag, domain=ModelCard, range=Optional[str])

slots.modelCard_language = Slot(uri=MODELCARD.language, name="modelCard_language", curie=MODELCARD.curie('language'),
                   model_uri=MODELCARD.modelCard_language, domain=ModelCard, range=Optional[Union[str, list[str]]])

slots.modelCard_base_model = Slot(uri=MODELCARD.base_model, name="modelCard_base_model", curie=MODELCARD.curie('base_model'),
                   model_uri=MODELCARD.modelCard_base_model, domain=ModelCard, range=Optional[str])

slots.modelCard_tags = Slot(uri=MODELCARD.tags, name="modelCard_tags", curie=MODELCARD.curie('tags'),
                   model_uri=MODELCARD.modelCard_tags, domain=ModelCard, range=Optional[Union[str, list[str]]])

slots.modelCard_datasets = Slot(uri=MODELCARD.datasets, name="modelCard_datasets", curie=MODELCARD.curie('datasets'),
                   model_uri=MODELCARD.modelCard_datasets, domain=ModelCard, range=Optional[Union[str, list[str]]])

slots.modelCard_metrics = Slot(uri=MODELCARD.metrics, name="modelCard_metrics", curie=MODELCARD.curie('metrics'),
                   model_uri=MODELCARD.modelCard_metrics, domain=ModelCard, range=Optional[Union[str, list[str]]])

slots.modelCard_model_index = Slot(uri=MODELCARD.model_index, name="modelCard_model_index", curie=MODELCARD.curie('model_index'),
                   model_uri=MODELCARD.modelCard_model_index, domain=ModelCard, range=Optional[Union[Union[dict, ModelIndex], list[Union[dict, ModelIndex]]]])
