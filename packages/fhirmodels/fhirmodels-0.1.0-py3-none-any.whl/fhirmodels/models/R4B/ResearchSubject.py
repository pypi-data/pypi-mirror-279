"""
Generated class for ResearchSubject. 
Time: 2024-06-13 23:34:40
"""

from fhirmodels.models.R4B.DomainResource import *
from fhirmodels.models.R4B.Extension import *
from fhirmodels.models.R4B.Identifier import *
from fhirmodels.models.R4B.Meta import *
from fhirmodels.models.R4B.Narrative import *
from fhirmodels.models.R4B.Period import *
from fhirmodels.models.R4B.Reference import *
from fhirmodels.models.R4B.Resource import *


class ResearchSubject(DomainResource):
    """A physical entity which is the primary unit of operational and/or administrative interest in a study.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    :param Narrative text: Text summary of the resource, for human interpretation
    :param Resource contained: Contained, inline Resources
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored
    :param Identifier identifier: Business Identifier for research subject in a study
    :param str status: candidate | eligible | follow-up | ineligible | not-registered | off-study | on-study | on-study-intervention | on-study-observation | pending-on-study | potential-candidate | screening | withdrawn
    :param Period period: Start and end of participation
    :param Reference study: Study subject is part of
    :param Reference individual: Who is part of study
    :param str assignedArm: What path should be followed
    :param str actualArm: What path was followed
    :param Reference consent: Agreement to participate in study
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "meta": {"class_name": "Meta", "is_contained": False},
        "text": {"class_name": "Narrative", "is_contained": False},
        "contained": {"class_name": "Resource", "is_contained": False},
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "identifier": {"class_name": "Identifier", "is_contained": False},
        "period": {"class_name": "Period", "is_contained": False},
        "study": {"class_name": "Reference", "is_contained": False},
        "individual": {"class_name": "Reference", "is_contained": False},
        "consent": {"class_name": "Reference", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        meta: "Meta" = None,
        implicitRules: "str" = None,
        language: "str" = None,
        text: "Narrative" = None,
        contained: list["Resource"] = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        identifier: list["Identifier"] = None,
        status: "str" = None,
        period: "Period" = None,
        study: "Reference" = None,
        individual: "Reference" = None,
        assignedArm: "str" = None,
        actualArm: "str" = None,
        consent: "Reference" = None,
    ):

        self.resourceType = "ResearchSubject"

        self.id = id
        self.meta = meta
        self.implicitRules = implicitRules
        self.language = language
        self.text = text
        self.contained = contained or []
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.identifier = identifier or []
        self.status = status
        self.period = period
        self.study = study
        self.individual = individual
        self.assignedArm = assignedArm
        self.actualArm = actualArm
        self.consent = consent

    @classmethod
    def from_dict(cls, data: dict) -> "ResearchSubject":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "ResearchSubject":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
