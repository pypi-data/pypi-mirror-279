from typing import List, Optional, Dict, Any, Union

from dataclasses import dataclass, field
from code_loader.contract.enums import DatasetMetadataType, LeapDataType


@dataclass
class DatasetPreprocess:
    training_length: int
    validation_length: int
    test_length: Optional[int] = None
    unlabeled_length: Optional[int] = None


@dataclass
class DatasetBaseSectionInstance:
    name: str


@dataclass
class DatasetInputInstance(DatasetBaseSectionInstance):
    shape: List[int]


@dataclass
class DatasetMetadataInstance(DatasetBaseSectionInstance):
    type: DatasetMetadataType


@dataclass
class DatasetOutputInstance(DatasetBaseSectionInstance):
    shape: List[int]


@dataclass
class VisualizerInstance:
    name: str
    type: LeapDataType
    arg_names: List[str]


@dataclass
class MetricInstance:
    name: str
    arg_names: List[str]


@dataclass
class CustomLossInstance:
    name: str
    arg_names: List[str]


@dataclass
class CustomLayerInstance:
    name: str
    init_arg_names: List[str]
    call_arg_names: List[str]
    use_custom_latent_space: bool = False


@dataclass
class PredictionTypeInstance:
    name: str
    labels: List[str]
    channel_dim: int


@dataclass
class DatasetSetup:
    preprocess: DatasetPreprocess
    inputs: List[DatasetInputInstance]
    metadata: List[DatasetMetadataInstance]
    outputs: List[DatasetOutputInstance]
    visualizers: List[VisualizerInstance]
    prediction_types: List[PredictionTypeInstance]
    custom_losses: List[CustomLossInstance]
    metrics: List[MetricInstance] = field(default_factory=list)


@dataclass
class ModelSetup:
    custom_layers: List[CustomLayerInstance]


@dataclass
class DatasetTestResultPayload:
    name: str
    display: Dict[str, str] = field(default_factory=dict)
    is_passed: bool = True
    shape: Optional[List[int]] = None
    raw_result: Optional[Any] = None
    handler_type: Optional[str] = None


@dataclass
class BoundingBox:
    # (x, y) is the center of the bounding box
    x: float  # value between [0, 1], represent the percentage according to the image size.
    y: float  # value between [0, 1], represent the percentage according to the image size.

    width: float  # value between [0, 1], represent the percentage according to the image size.
    height: float  # value between [0, 1], represent the percentage according to the image size.
    confidence: float
    label: str
    rotation: float = 0.0  # value between [0, 360], represent the degree of rotation.
    metadata: Optional[Dict[str, Union[str, int, float]]] = None


@dataclass
class DatasetIntegParseResult:
    payloads: List[DatasetTestResultPayload]
    is_valid: bool
    is_valid_for_model: Optional[bool] = False
    setup: Optional[DatasetSetup] = None
    model_setup: Optional[ModelSetup] = None
    general_error: Optional[str] = None
    print_log: Optional[str] = None
