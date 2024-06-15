"""PyTorch implementations for Bitfount Dataset classes."""

from typing import Iterator, List, Sequence, Tuple, Union, cast

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset as PTDataset, IterableDataset as PTIterableDataset

from bitfount.backends.pytorch.data.utils import _index_tensor_handler
from bitfount.data.datasets import (
    _BaseBitfountDataset,
    _BitfountDataset,
    _FileSystemBitfountDataset,
    _FileSystemIterableBitfountDataset,
    _IterableBitfountDataset,
)
from bitfount.data.datasources.base_source import FileSystemIterableSource
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.types import (
    _DataEntry,
    _DataEntryWithKey,
    _ImagesData,
    _SupportData,
    _TabularData,
)


class BasePyTorchDataset(_BaseBitfountDataset):
    """Base class for representing a Pytorch dataset."""

    def _getitem(self, idx: Union[int, Sequence[int]]) -> _DataEntry:
        """Returns the item referenced by index `idx` in the data."""
        image: _ImagesData
        tab: _TabularData
        sup: _SupportData

        target: Union[np.ndarray, Tuple[np.ndarray, ...]]
        if self.schema is not None:
            # Schema is None for HuggingFace datasets which is
            # handled separately, so we can cast.
            if len(self.y_var) == 0:
                # Set the target, if the dataset has no supervision,
                # choose set the default value to be 0.
                target = np.array(0)
            elif (
                "image" in self.schema.features
                and self.target in self.schema.features["image"]
            ):
                # Check if the target is an image and load it.
                target = self._load_images(idx, what_to_load="target")
            else:
                target = self.y_var[idx]

            # If the Dataset contains both tabular and image data
            if self.image.size and self.tabular.size:
                tab = self.tabular[idx]
                sup = self.support_cols[idx]
                image = self._load_images(idx)
                if self.ignore_support_cols:
                    # _ImageAndTabularEntry[no support data] or
                    # _Segmentation_ImageAndTabEntry[no support data]
                    return (
                        tab,
                        image,
                    ), target

                # _ImageAndTabularEntry[support data] or
                # _Segmentation_ImageAndTabEntry[support data]
                return (tab, image, sup), target

            # If the Dataset contains only tabular data
            elif self.tabular.size:
                tab = self.tabular[idx]
                sup = self.support_cols[idx]
                if self.ignore_support_cols:
                    # _TabularEntry[no support data]
                    return tab, target

                # _TabularEntry[support data]
                return (tab, sup), target

            # If the Dataset contains only image data
            else:
                sup = self.support_cols[idx]
                image = self._load_images(idx)
                if self.ignore_support_cols:
                    # _ImageEntry[no support data] or
                    # _Segmentation_ImageEntry[no support data]
                    return image, target

                # _ImageEntry[support data] or
                # _Segmentation_ImageEntry[support data]
                return (image, sup), target
        else:
            raise TypeError(
                "Dataset initialised without a schema. "
                "The only datasets that support this are the Huggingface algorithms, "
                "so make sure to use the correct datafactory for the dataset."
            )


class _PyTorchDataset(_BitfountDataset, BasePyTorchDataset, PTDataset):
    """See base class."""

    def __getitem__(self, idx: Union[int, Sequence[int], torch.Tensor]) -> _DataEntry:
        idx = _index_tensor_handler(idx)
        return self._getitem(idx)

    def __iter__(self) -> Iterator[_DataEntry]:
        """Iterates over the dataset."""
        # This is to make mypy happy in the case
        # where not all images have the same number of frames.
        for idx in range(len(self)):
            yield self[idx]


class _PyTorchIterableDataset(
    _IterableBitfountDataset, BasePyTorchDataset, PTIterableDataset
):
    """See base class."""

    def __iter__(self) -> Iterator[_DataEntry]:
        """Iterates over the dataset."""
        for data_partition in self.yield_dataset_split(
            split=self.data_split, data_splitter=self.data_splitter
        ):
            self._reformat_data(data_partition)

            for idx in range(len(self.data)):
                yield self._getitem(idx)


class _PytorchFileIterableDataset(
    _FileSystemIterableBitfountDataset, _PyTorchIterableDataset, PTIterableDataset
):
    """See base class.

    This class specifically has support for keyed-data entries to be returned,
    i.e. data elements will be associated with the filename that they came from.
    """

    data_keys: List[str]

    datasource: FileSystemIterableSource

    def __iter__(self) -> Iterator[_DataEntryWithKey]:  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(Iterator[_DataEntryWithKey], super().__iter__())

    def _reformat_data(self, data: pd.DataFrame) -> None:
        super()._reformat_data(data)

        # Also extract the key for the data (currently filename)
        self.data_keys = cast(
            np.ndarray, data.loc[:, ORIGINAL_FILENAME_METADATA_COLUMN].values
        ).tolist()

    def __getitem__(
        self, idx: Union[int, Sequence[int], torch.Tensor]
    ) -> _DataEntryWithKey:
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(_DataEntryWithKey, super().__getitem__(idx))

    def _getitem(self, idx: Union[int, Sequence[int]]) -> _DataEntryWithKey:  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        d: _DataEntry = super()._getitem(idx)
        if isinstance(idx, int):
            data_key = self.data_keys[idx]
        else:
            # TODO: [BIT-3851] support multi-index
            raise TypeError(f"idx of type ({type(idx)}) is not supported")

        # Combine main data with the appropriate key
        # mypy: lack of support for tuple unpacking means we need to manually cast this
        new_d: _DataEntryWithKey = cast(_DataEntryWithKey, (*d, data_key))
        return new_d


class _PytorchFileSystemDataset(_FileSystemBitfountDataset, _PyTorchDataset, PTDataset):
    """See base class.

    This class specifically has support for keyed-data entries to be returned,
    i.e. data elements will be associated with the filename that they came from.
    """

    data_keys: List[str]

    datasource: FileSystemIterableSource

    def _reformat_data(self, data: pd.DataFrame) -> None:
        super()._reformat_data(data)

        # Also extract the key for the data (currently filename)
        self.data_keys = cast(
            np.ndarray, data.loc[:, ORIGINAL_FILENAME_METADATA_COLUMN].values
        ).tolist()

    def __getitem__(  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        self,
        idx: Union[int, Sequence[int], torch.Tensor],
    ) -> _DataEntryWithKey:
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(_DataEntryWithKey, super().__getitem__(idx))

    def _getitem(  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        self, idx: Union[int, Sequence[int]]
    ) -> _DataEntryWithKey:
        # Super method actually only returns a subset of _DataEntry types;
        # the wider typing is due to the base class's. We can constrain it to the
        # actual types as returned by that method.
        d: _DataEntry = super()._getitem(idx)
        if isinstance(idx, int):
            data_key = self.data_keys[idx]
        else:
            # TODO: [BIT-3851] support multi-index
            raise TypeError(f"idx of type ({type(idx)}) is not supported")

        # Combine main data with the appropriate key
        # mypy: lack of support for tuple unpacking means we need to manually cast this
        new_d: _DataEntryWithKey = cast(_DataEntryWithKey, (*d, data_key))
        return new_d

    def __iter__(self) -> Iterator[_DataEntryWithKey]:  # type: ignore[override] # Reason: [BIT-3851] temp fix for supporting data key passthrough # noqa: B950
        # Super method relies on calls to _getitem(), etc, which we have changed in
        # this class; this means we can constrain the return type even though we are
        # calling the super method
        return cast(Iterator[_DataEntryWithKey], super().__iter__())
