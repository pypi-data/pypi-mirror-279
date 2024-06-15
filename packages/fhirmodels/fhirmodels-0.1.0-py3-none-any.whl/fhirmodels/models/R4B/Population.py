"""
Generated class for Population. 
Time: 2024-06-13 23:34:40
"""

from fhirmodels.generator import FhirBaseModel
from fhirmodels.models.R4B.CodeableConcept import *
from fhirmodels.models.R4B.Extension import *
from fhirmodels.models.R4B.Range import *


class Population(FhirBaseModel):
    """Base StructureDefinition for Population Type: A populatioof people with some set of grouping criteria.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param Range ageRange: The age of the specific population
    :param CodeableConcept ageCodeableConcept: The age of the specific population
    :param CodeableConcept gender: The gender of the specific population
    :param CodeableConcept race: Race of the specific population
    :param CodeableConcept physiologicalCondition: The existing physiological conditions of the specific population to which this applies
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "ageRange": {"class_name": "Range", "is_contained": False},
        "ageCodeableConcept": {"class_name": "CodeableConcept", "is_contained": False},
        "gender": {"class_name": "CodeableConcept", "is_contained": False},
        "race": {"class_name": "CodeableConcept", "is_contained": False},
        "physiologicalCondition": {
            "class_name": "CodeableConcept",
            "is_contained": False,
        },
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        ageRange: "Range" = None,
        ageCodeableConcept: "CodeableConcept" = None,
        gender: "CodeableConcept" = None,
        race: "CodeableConcept" = None,
        physiologicalCondition: "CodeableConcept" = None,
    ):

        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.ageRange = ageRange
        self.ageCodeableConcept = ageCodeableConcept
        self.gender = gender
        self.race = race
        self.physiologicalCondition = physiologicalCondition

    @classmethod
    def from_dict(cls, data: dict) -> "Population":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Population":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
