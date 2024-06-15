"""
Generated class for Base. 
Time: 2024-06-13 23:38:27
"""

from fhirmodels.generator import FhirBaseModel


class Base(FhirBaseModel):
    """Base Type: Base definition for all types defined in FHIR type system."""

    # needed for complex properties where the element name is different from the class name
    property_class_info = {}

    def __init__(
        self,
    ):

        self.resourceType = "Base"

    @classmethod
    def from_dict(cls, data: dict) -> "Base":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Base":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
