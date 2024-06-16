import csv
import json
import pickle
from collections import defaultdict
from csv import Dialect
from pathlib import Path
from typing import Optional, TextIO, Any, BinaryIO, TYPE_CHECKING, Iterator, Protocol

from .dataset import Sample
from .types import StorageIndexing, FeatureName, SampleID

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass


class StorageProtocol(Protocol):

    def store(self, sample_id: SampleID, feat: FeatureName, value: Any):
        pass

    def store_aggregation(self, feature_name: FeatureName, value: Any):
        pass


class BaseStorage:

    def __init__(self, indexing: StorageIndexing):
        self.indexing = indexing
        self._data: dict[SampleID, dict[FeatureName, Any]] = defaultdict(dict)
        self._features: set[FeatureName] = set()

    @staticmethod
    def flatten_tuple(t: tuple[Any, ...], separator: str):
        return separator.join(str(v) for v in t)

    def flatten_dict(self, data : dict[str, Any] | Any, feat_name: Optional[str], separator: str = "_") -> Iterator[tuple[str, Any]]:
        if not isinstance(data, dict):
            yield feat_name, data
        else:
            for key, value in data.items():
                if isinstance(key, tuple):
                    key = self.flatten_tuple(key, separator)
                subfeature_name = f"{feat_name}{separator}{key}" if feat_name is not None else key
                yield from self.flatten_dict(value, subfeature_name, separator)

    def check_samples(self):
        for sample_id, sample_dict in self._data.items():
            for feat_name, feat_value in sample_dict.items():
                try:
                    self._check_feat_value(feat_value)
                except Exception as err:
                    raise TypeError(f"Error while trying to save feature {feat_name} for sample {sample_id} : "
                                    f"{str(err)}.\n (value: {repr(feat_value)})")

    def _check_feat_value(self, sample_value: Any):
        """Needs to be overloaded: checks if the sample can be properly serialized by the storage format,
        else, raises an error"""
        pass

    def store_feat(self, feature: str, data: dict[SampleID, Any], flatten: bool = False):
        if flatten:
            for sample_id, sample_feat in data.items():
                for feat_name, feat_value in self.flatten_dict(sample_feat, feature):
                    self._data[sample_id][feat_name] = feat_value
                    self._features.add(feat_name)
        else:
            self._features.add(feature)
            for sample_id, value in data.items():
                self._data[sample_id][feature] = value

    def store_sample(self, sample: Sample, data: dict[FeatureName, Any], flatten: bool = False):
        if flatten:
            data = dict(self.flatten_dict(data, feat_name=None))
        self._features.update(set(data.keys()))
        self._data[sample.id] = data

    def get_data(self):
        """Returns the stored data with the proper indexing,
         mainly used when the storage backend writes its stored data"""
        if self.indexing == "feature":
            out_data = defaultdict(dict)
            for sample_id, feat_dict in self._data.items():
                for feat, value in feat_dict.items():
                    out_data[feat][sample_id] = value
        else:
            out_data = self._data
        return dict(out_data)


class CSVStorage(BaseStorage):

    def __init__(self,
                 indexing: StorageIndexing,
                 output_file: TextIO,
                 dialect: Optional[Dialect] = None):
        super().__init__(indexing)
        self.file = output_file
        self.dialect = dialect

    def write(self):
        data = self.get_data()
        if self.indexing == "sample":
            index_column = "sample_id"
            fields = [index_column] + sorted(list(self._features))
        else:
            index_column = "feature"
            fields = [index_column] + sorted(list(self._data.keys()))
        writer = csv.DictWriter(self.file, fieldnames=fields, dialect=self.dialect)
        writer.writeheader()
        for key, data in data.items():
            row_dict = {index_column: key}
            row_dict.update(**data)
            writer.writerow(row_dict)


class PickleStorage(BaseStorage):

    def __init__(self,
                 indexing: StorageIndexing,
                 output_file: BinaryIO):
        super().__init__(indexing)
        self.file = output_file

    def write(self):
        pickle.dump(self.get_data(), self.file)


class SplitPickleStorage(BaseStorage):

    def __init__(self,
                 indexing: StorageIndexing,
                 output_folder: Path,
                 streaming: bool):
        super().__init__(indexing)
        self.folder = output_folder
        self.streaming = streaming

    def store_sample(self, sample: Sample, data: dict[FeatureName, Any], flatten: bool = False):
        super().store_sample(sample, data, flatten)
        # if the indexing allows it, dumping all stored data to disk and clearing current storage
        if self.indexing == "sample" and self.streaming:
            self.flush()

    def store_feat(self, feature: str, data: dict[SampleID, Any], flatten: bool = False):
        super().store_feat(feature, data, flatten)
        # if the indexing allows it, dumping all stored data to disk and clearing current storage
        if self.indexing == "feature" and self.streaming:
            self.flush()

    def flush(self):
        # writing to disk and emptying storage cache
        self.write()
        self._data = defaultdict(dict)
        self._features = set()

    def write(self):
        data = self.get_data()
        for key, data in data.items():
            with open(self.folder / Path(f"{key}.pckl"), "wb") as pkfile:
                pickle.dump(data, pkfile)


class JSONStorage(BaseStorage):

    def __init__(self,
                 indexing: StorageIndexing,
                 output_file: TextIO):
        super().__init__(indexing)
        self.file = output_file

    def _check_feat_value(self, sample_value: Any):
        json.dumps(sample_value)

    def write(self):
        json.dump(self.get_data(), self.file)


class DataFrameStorage(BaseStorage):

    def get_data(self) -> 'pd.DataFrame':
        data = super().get_data()
        import pandas as pd
        return pd.DataFrame.from_dict(data)


class HDF5Storage(BaseStorage):
    pass  # TODO
