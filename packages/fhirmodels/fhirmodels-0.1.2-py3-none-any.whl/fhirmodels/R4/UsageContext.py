"""
Generated class for UsageContext. 
Time: 2024-06-14 18:37:17
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R4.CodeableConcept import *
from fhirmodels.R4.Coding import *
from fhirmodels.R4.Extension import *
from fhirmodels.R4.Quantity import *
from fhirmodels.R4.Range import *
from fhirmodels.R4.Reference import *


class UsageContext(FhirBaseModel):
    """Base StructureDefinition for UsageContext Type: Specifies clinical/business/etc. metadata that can be used to retrieve, index and/or categorize an artifact. This metadata can either be specific to the applicable population (e.g., age category, DRG) or the specific context of care (e.g., venue, care setting, provider of care).
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Coding code: Type of context being specified
    :param CodeableConcept valueCodeableConcept: Value that defines the context
    :param Quantity valueQuantity: Value that defines the context
    :param Range valueRange: Value that defines the context
    :param Reference valueReference: Value that defines the context
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "code": {"class_name": "Coding", "is_contained": False},
        "valueCodeableConcept": {
            "class_name": "CodeableConcept",
            "is_contained": False,
        },
        "valueQuantity": {"class_name": "Quantity", "is_contained": False},
        "valueRange": {"class_name": "Range", "is_contained": False},
        "valueReference": {"class_name": "Reference", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        code: "Coding" = None,
        valueCodeableConcept: "CodeableConcept" = None,
        valueQuantity: "Quantity" = None,
        valueRange: "Range" = None,
        valueReference: "Reference" = None,
    ):

        self.id = id
        self.extension = extension or []
        self.code = code
        self.valueCodeableConcept = valueCodeableConcept
        self.valueQuantity = valueQuantity
        self.valueRange = valueRange
        self.valueReference = valueReference

    @classmethod
    def from_dict(cls, data: dict) -> "UsageContext":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "UsageContext":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
