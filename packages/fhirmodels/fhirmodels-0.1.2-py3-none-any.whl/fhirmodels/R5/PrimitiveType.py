"""
Generated class for PrimitiveType. 
Time: 2024-06-14 18:37:55
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R5.Extension import *


class PrimitiveType(FhirBaseModel):
    """PrimitiveType Type: The base type for all re-useable types defined that have a simple property.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
    ):

        self.id = id
        self.extension = extension or []

    @classmethod
    def from_dict(cls, data: dict) -> "PrimitiveType":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "PrimitiveType":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
