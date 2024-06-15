"""
Generated class for RatioRange. 
Time: 2024-06-14 18:37:55
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R5.Extension import *
from fhirmodels.R5.Quantity import *


class RatioRange(FhirBaseModel):
    """RatioRange Type: A range of ratios expressed as a low and high numerator and a denominator.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Quantity lowNumerator: Low Numerator limit
    :param Quantity highNumerator: High Numerator limit
    :param Quantity denominator: Denominator value
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "lowNumerator": {"class_name": "Quantity", "is_contained": False},
        "highNumerator": {"class_name": "Quantity", "is_contained": False},
        "denominator": {"class_name": "Quantity", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        lowNumerator: "Quantity" = None,
        highNumerator: "Quantity" = None,
        denominator: "Quantity" = None,
    ):

        self.id = id
        self.extension = extension or []
        self.lowNumerator = lowNumerator
        self.highNumerator = highNumerator
        self.denominator = denominator

    @classmethod
    def from_dict(cls, data: dict) -> "RatioRange":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "RatioRange":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
