"""
Generated class for BackboneElement. 
Time: 2024-06-14 18:37:17
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R4.Extension import *


class BackboneElement(FhirBaseModel):
    """Base StructureDefinition for BackboneElement Type: Base definition for all elements that are defined inside a resource - but not those in a data type.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
    ):

        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []

    @classmethod
    def from_dict(cls, data: dict) -> "BackboneElement":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "BackboneElement":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
