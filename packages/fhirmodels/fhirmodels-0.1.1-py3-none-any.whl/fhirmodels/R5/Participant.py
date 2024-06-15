"""
Generated class for Participant. 
Time: 2024-06-14 18:37:55
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R5.Identifier import *


class Participant(FhirBaseModel):
    """Logical Model: A pattern followed by resources that represent the participant in some activity, process, or responsible for providing information about a resource.
    :param Identifier identifier: Business Identifier for {{title}}
    :param bool active: Whether the {{title}} is currently active
    :param str name: A name for the {{title}}
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "identifier": {"class_name": "Identifier", "is_contained": False},
    }

    def __init__(
        self,
        identifier: list["Identifier"] = None,
        active: "bool" = None,
        name: "str" = None,
    ):

        self.identifier = identifier or []
        self.active = active
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> "Participant":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Participant":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
