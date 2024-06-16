from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypeAlias, Union

ResourceId: TypeAlias = str


class ResourceType(Enum):
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    Spreadsheet = "spreadsheet"
    NetCDF4 = "netcdf4"
    NetCDF3 = "netcdf3"
    GeoTIFF = "geotiff"
    NPDict = "np-dict"
    Shapefile = "shapefile"
    Container = "container"


@dataclass
class CSVProp:
    delimiter: str = ","


# @dataclass
# class SpreadsheetProp:
#     worksheet: Optional[str] = None


@dataclass
class Resource:
    id: ResourceId
    type: ResourceType
    prop: Optional[CSVProp] = None

    @staticmethod
    def deserialize(raw: dict):
        if raw["type"] == ResourceType.CSV.value and raw["prop"] is not None:
            prop = CSVProp(raw["prop"]["delimiter"])
        else:
            prop = None
        return Resource(raw["id"], ResourceType(raw["type"]), prop)

    def get_preprocessing_original_resource_id(self):
        return Resource.parse_preprocessing_output_id(self.id)[0]

    def is_preprocessing_output(self):
        """Return true if this resource holds output of preprocessing functions"""
        return (
            self.id.startswith(f"__preproc__") and self.type == ResourceType.Container
        )

    @staticmethod
    def create_preprocessing_output(resource_id: str, attr_id: str) -> Resource:
        return Resource(
            Resource.get_preprocessing_output_id(resource_id, attr_id),
            ResourceType.Container,
        )

    @staticmethod
    def get_preprocessing_output_id(resource_id: str, attr_id: str) -> str:
        if resource_id.startswith("__preproc__"):
            resource_id, _ = Resource.parse_preprocessing_output_id(resource_id)
        assert (
            "__" not in resource_id
        ), "Resource ID for preprocessing cannot contain '__'"
        return f"__preproc__{resource_id}__{attr_id}"

    @staticmethod
    def parse_preprocessing_output_id(output_id: str) -> tuple[str, str]:
        assert output_id.startswith("__preproc__")
        parts = output_id[len("__preproc__") :].split("__")
        return parts[0], parts[1]


class ResourceData(ABC):

    @abstractmethod
    def to_dict(self):
        pass


@dataclass
class ResourceDataFile(ResourceData):
    file: str

    def to_dict(self):
        return {"file": self.file}


@dataclass
class ResourceDataString(ResourceData):
    value: Union[str, bytes]

    def as_str(self):
        if isinstance(self.value, bytes):
            return self.value.decode()
        else:
            assert isinstance(self.value, str)
            return self.value

    def to_dict(self):
        return {
            "string": (
                self.value.decode() if isinstance(self.value, bytes) else self.value
            )
        }
