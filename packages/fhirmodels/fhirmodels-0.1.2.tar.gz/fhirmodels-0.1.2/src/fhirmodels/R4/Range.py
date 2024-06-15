"""
Generated class for Range. 
Time: 2024-06-14 18:37:17
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R4.Extension import *
from fhirmodels.R4.Quantity import *


class Range(FhirBaseModel):
    """Base StructureDefinition for Range Type: A set of ordered Quantities defined by a low and high limit.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Quantity low: Low limit
    :param Quantity high: High limit
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "low": {"class_name": "Quantity", "is_contained": False},
        "high": {"class_name": "Quantity", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        low: "Quantity" = None,
        high: "Quantity" = None,
    ):

        self.id = id
        self.extension = extension or []
        self.low = low
        self.high = high

    @classmethod
    def from_dict(cls, data: dict) -> "Range":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Range":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
