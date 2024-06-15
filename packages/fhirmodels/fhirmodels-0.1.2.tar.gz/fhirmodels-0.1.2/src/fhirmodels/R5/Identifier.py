"""
Generated class for Identifier. 
Time: 2024-06-14 18:37:55
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.R5.CodeableConcept import *
from fhirmodels.R5.Extension import *
from fhirmodels.R5.Period import *
from fhirmodels.R5.Reference import *


class Identifier(FhirBaseModel):
    """Identifier Type: An identifier - identifies some entity uniquely and unambiguously. Typically this is used for business identifiers.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param str use: usual | official | temp | secondary | old (If known)
    :param CodeableConcept type: Description of identifier
    :param str system: The namespace for the identifier value
    :param str value: The value that is unique
    :param Period period: Time period when id is/was valid for use
    :param Reference assigner: Organization that issued id (may be just text)
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "type": {"class_name": "CodeableConcept", "is_contained": False},
        "period": {"class_name": "Period", "is_contained": False},
        "assigner": {"class_name": "Reference", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        use: "str" = None,
        type: "CodeableConcept" = None,
        system: "str" = None,
        value: "str" = None,
        period: "Period" = None,
        assigner: "Reference" = None,
    ):

        self.id = id
        self.extension = extension or []
        self.use = use
        self.type = type
        self.system = system
        self.value = value
        self.period = period
        self.assigner = assigner

    @classmethod
    def from_dict(cls, data: dict) -> "Identifier":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Identifier":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
