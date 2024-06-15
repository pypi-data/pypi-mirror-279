"""Type hints, enums and protocols for the Bitfount libraries."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    List,
    Mapping,
    MutableMapping,
    NewType,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    Union,
    runtime_checkable,
)

import marshmallow
from marshmallow import fields
import numpy as np
import pandas as pd
from pandas._typing import Dtype
from typing_extensions import TypedDict

from bitfount.utils.numpy_utils import check_for_compatible_lengths

if TYPE_CHECKING:
    from bitfount.data.dataloaders import BitfountDataLoader
    from bitfount.data.datasources.base_source import BaseSource
    from bitfount.data.datastructure import DataStructure
    from bitfount.data.schema import BitfountSchema
    from bitfount.federated.helper import TaskContext
    from bitfount.federated.model_reference import BitfountModelReference
    from bitfount.metrics import Metric

__all__: List[str] = ["BaseDistributedModelProtocol", "DistributedModelProtocol"]

# Tensor dtype type variable
T_DTYPE = TypeVar("T_DTYPE", covariant=True)


# TensorLike protocol and TensorLike composite types
class _TensorLike(Protocol):
    """Protocol defining what methods and operations a Generic Tensor can perform."""

    def __mul__(self: _TensorLike, other: Any) -> _TensorLike:
        """Multiplies the self tensor with the other tensor and returns the result."""
        ...

    def __sub__(self: _TensorLike, other: Any) -> _TensorLike:
        """Subtracts the other tensor from the self tensor and returns the result."""
        ...

    def squeeze(self: _TensorLike, axis: Optional[Any] = None) -> _TensorLike:
        """Returns a tensor with all the dimensions of input of size 1 removed."""
        ...


# Weight update types
_SerializedWeights = Mapping[str, List[float]]
_Residuals = Mapping[str, _TensorLike]
_Weights = Mapping[str, _TensorLike]


# Schema dtypes
_DtypesValues = Union[Dtype, np.dtype]
_Dtypes = Dict[str, _DtypesValues]


# Return Types
@dataclass
class EvaluateReturnType:
    """The type of return from model.evaluate() calls.

    Contains the predictions made by the model and the targets that were actually
    expected. Additionally, for file-containing datasets, will contain the keys (
    filenames) that were the source of each prediction.

    `preds` and `targs` will be numpy arrays where the first or second dimension is
    the number of predictions/data entries that were evaluated on.
    """

    preds: np.ndarray
    targs: np.ndarray
    keys: Optional[List[str]] = None

    def __post_init__(self) -> None:
        # The preds and targs should correspond to the same number of
        # predictions/data entries. This means that they should be of equal length in
        # either their first or second dimensions
        check_for_compatible_lengths(self.preds, self.targs, "predictions", "targets")

        if self.keys is not None:
            check_for_compatible_lengths(
                self.preds, self.keys, "predictions", "data keys"
            )

    def msgpack_serialize(self) -> _EvaluateReturnTypeDict:
        """Convert to dict, ready for msgpack serialization."""
        return _EvaluateReturnTypeDict(
            preds=self.preds, targs=self.targs, keys=self.keys
        )


class _EvaluateReturnTypeDict(TypedDict):
    """Dict representation of EvaluateReturnType, for serialization."""

    preds: np.ndarray
    targs: np.ndarray
    keys: Optional[List[str]]


@dataclass
class PredictReturnType:
    """The type of return from model.predict() calls.

    Contains the predictions made by the model. Additionally, for file-containing
    datasets, will contain the keys (filenames) that were the source of each
    prediction.

    If preds is a list, either the number of elements in the list is the number of
    predictions, or each element has a 1st dimension that is the number of predictions.
    """

    preds: Union[List[np.ndarray], pd.DataFrame]
    keys: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.keys is not None:
            if isinstance(self.preds, pd.DataFrame):
                if (keys_len := len(self.keys)) != (preds_len := len(self.preds)):
                    raise ValueError(
                        f"Mismatch in number of predictions vs data keys;"
                        f" got {preds_len} predictions, {keys_len} keys."
                    )
            else:  # if preds is List[np.ndarray]
                # Either the length of the list is the same as the number of keys
                # (i.e. each list-element corresponds to one file) OR each array in
                # the list should be the same length as the number of keys
                check_for_compatible_lengths(
                    self.preds, self.keys, "predictions", "data keys"
                )

    def msgpack_serialize(self) -> _PredictReturnTypeDict:
        """Convert to dict, ready for msgpack serialization."""
        return _PredictReturnTypeDict(preds=self.preds, keys=self.keys)


class _PredictReturnTypeDict(TypedDict):
    """Dict representation of PredictReturnType, for serialization."""

    preds: Union[List[np.ndarray], pd.DataFrame]
    keys: Optional[List[str]]


@runtime_checkable
class BaseDistributedModelProtocol(Protocol[T_DTYPE]):
    """Federated Model structural type that only specifies the methods.

    The reason for this protocol is that `issubclass` checks with Protocols can only
    be performed if the Protocol only specifies methods and not attributes. We still
    want to specify the attributes in another protocol though for greater type safety,
    (both statically and dynamically) so we have this protocol that only specifies
    methods and another protocol that specifies the attributes.
    """

    def tensor_precision(self) -> T_DTYPE:
        """Defined in DistributedModelMixIn."""

    def get_param_states(self) -> _Weights:
        """Defined in DistributedModelMixIn."""

    def apply_weight_updates(self, weight_updates: Sequence[_Weights]) -> _Weights:
        """Defined in DistributedModelMixIn."""

    def update_params(self, new_model_params: _Weights) -> None:
        """Defined in DistributedModelMixIn."""

    def serialize_params(self, weights: _Weights) -> _SerializedWeights:
        """Defined in DistributedModelMixIn."""

    def deserialize_params(self, serialized_weights: _SerializedWeights) -> _Weights:
        """Defined in DistributedModelMixIn."""

    def diff_params(self, old_params: _Weights, new_params: _Weights) -> _Residuals:
        """Defined in DistributedModelMixIn."""

    def set_model_training_iterations(self, iterations: int) -> None:
        """Defined in DistributedModelMixIn."""

    def reset_trainer(self) -> None:
        """Defined in DistributedModelMixIn."""

    def set_datastructure_identifier(self, datastructure_identifier: str) -> None:
        """Defined in DistributedModelMixIn."""

    def fit(
        self,
        data: Optional[BaseSource] = None,
        metrics: Optional[Dict[str, Metric]] = None,
        pod_identifiers: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, str]]:
        """Defined in DistributedModelMixIn."""

    def log_(self, name: str, value: Any, **kwargs: Any) -> Any:
        """Defined in DistributedModelMixIn."""

    def initialise_model(
        self,
        data: Optional[BaseSource] = None,
        context: Optional[TaskContext] = None,
    ) -> None:
        """Defined in _BaseModel."""

    def evaluate(
        self,
        test_dl: Optional[BitfountDataLoader] = None,
        pod_identifiers: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Union[
        EvaluateReturnType,
        Dict[str, float],
    ]:
        """Defined in _BaseModel."""

    def predict(
        self,
        data: Optional[BaseSource] = None,
        pod_identifiers: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Union[
        PredictReturnType,
        Dict[str, List[np.ndarray]],
    ]:
        """Defined in _BaseModel."""

    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Defined in _BaseModel."""

    def deserialize(self, filename: Union[str, os.PathLike]) -> None:
        """Defined in _BaseModel."""


# DistributedModel protocol and types
@runtime_checkable
class DistributedModelProtocol(BaseDistributedModelProtocol, Protocol[T_DTYPE]):
    """Federated Model structural type.

    This protocol should be implemented by classes that inherit from either
    `BitfountModel`, or both of `_BaseModel` and `DistributedModelMixIn`.
    """

    class_name: str
    datastructure: DataStructure
    schema: BitfountSchema  # TODO: [NO_TICKET: To discuss about the schema being here.] # noqa: B950
    # Type hints below indicate that one of either `epochs` or `steps` needs to be
    # supplied by the mixed-in class or other classes in the inheritance hierarchy
    epochs: Optional[int]
    steps: Optional[int]
    _total_num_batches_trained: int
    # Used to identify the relevant section of the datastructure that applies to
    # the pod/logical pod/datasource that this model is being run against (if any)
    _datastructure_identifier: Optional[str] = None
    # Denotes if param_clipping params are given to the model.
    param_clipping: Optional[Dict[str, int]]
    metrics: Optional[MutableMapping[str, Metric]]
    fields_dict: ClassVar[T_FIELDS_DICT]
    nested_fields: ClassVar[T_NESTED_FIELDS]

    @property
    def initialised(self) -> bool:
        """Defined in _BaseModel."""


T_FIELDS_DICT = Dict[str, marshmallow.fields.Field]
T_NESTED_FIELDS = Dict[str, Mapping[str, Any]]


class _BaseSerializableObjectMixIn:
    """The base class from which all serializable objects should inherit from.

    Attributes:
        fields_dict: A dictionary mapping all attributes that will be serialized
            in the class to their marshamllow field type. (e.g.
            fields_dict = `{"class_name": fields.Str()}`).
        nested_fields: A dictionary mapping all nested attributes to a registry
            that contains class names mapped to the respective classes.
            (e.g. nested_fields = `{"datastructure": datastructure.registry}`)
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {"class_name": fields.Str()}
    nested_fields: ClassVar[T_NESTED_FIELDS] = {}


class BinaryFile(fields.Field):
    """A marshmallow field for binary files."""

    def _serialize(
        self, value: str, attr: Optional[str], obj: Any, **kwargs: Any
    ) -> str:
        """Reads the file and returns the contents as a hex string."""
        with open(value, "rb") as f:
            return f.read().hex()

    def _deserialize(
        self,
        value: str,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs: Any,
    ) -> str:
        """Simply returns the hex string."""
        return value


if TYPE_CHECKING:
    _DistributedModelTypeOrReference = Union[
        DistributedModelProtocol, BitfountModelReference
    ]

# Serialization Types
_JSONDict = Dict[str, Any]  # A JSON-esque dictionary that is serializable

# Common Types
_StrAnyDict = Dict[str, Any]  # A dictionary with string keys and any value types

# S3 Interaction Types
_S3PresignedPOSTURL = NewType("_S3PresignedPOSTURL", str)
# HTTPX explicitly expects a `dict` rather than a `mapping`
_S3PresignedPOSTFields = NewType("_S3PresignedPOSTFields", Dict[str, str])
_S3PresignedURL = NewType("_S3PresignedURL", str)  # for GET requests

# SAML Types
_SAMLResponse = Mapping[str, Any]
