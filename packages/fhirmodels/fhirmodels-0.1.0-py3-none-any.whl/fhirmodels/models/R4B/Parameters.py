"""
Generated class for Parameters. 
Time: 2024-06-13 23:34:40
"""

from fhirmodels.models.R4B.Address import *
from fhirmodels.models.R4B.Age import *
from fhirmodels.models.R4B.Annotation import *
from fhirmodels.models.R4B.Attachment import *
from fhirmodels.models.R4B.BackboneElement import *
from fhirmodels.models.R4B.CodeableConcept import *
from fhirmodels.models.R4B.Coding import *
from fhirmodels.models.R4B.ContactDetail import *
from fhirmodels.models.R4B.ContactPoint import *
from fhirmodels.models.R4B.Contributor import *
from fhirmodels.models.R4B.Count import *
from fhirmodels.models.R4B.DataRequirement import *
from fhirmodels.models.R4B.Distance import *
from fhirmodels.models.R4B.DomainResource import *
from fhirmodels.models.R4B.Dosage import *
from fhirmodels.models.R4B.Duration import *
from fhirmodels.models.R4B.Expression import *
from fhirmodels.models.R4B.Extension import *
from fhirmodels.models.R4B.HumanName import *
from fhirmodels.models.R4B.Identifier import *
from fhirmodels.models.R4B.Meta import *
from fhirmodels.models.R4B.Money import *
from fhirmodels.models.R4B.ParameterDefinition import *
from fhirmodels.models.R4B.Period import *
from fhirmodels.models.R4B.Quantity import *
from fhirmodels.models.R4B.Range import *
from fhirmodels.models.R4B.Ratio import *
from fhirmodels.models.R4B.Reference import *
from fhirmodels.models.R4B.RelatedArtifact import *
from fhirmodels.models.R4B.Resource import *
from fhirmodels.models.R4B.SampledData import *
from fhirmodels.models.R4B.Signature import *
from fhirmodels.models.R4B.Timing import *
from fhirmodels.models.R4B.TriggerDefinition import *
from fhirmodels.models.R4B.UsageContext import *


class Parameter(FhirBaseModel):
    """A parameter passed to or received from the operation.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param str name: Name from the definition
    :param str valueBase64Binary: If parameter is a data type
    :param bool valueBoolean: If parameter is a data type
    :param str valueCanonical: If parameter is a data type
    :param str valueCode: If parameter is a data type
    :param str valueDate: If parameter is a data type
    :param str valueDateTime: If parameter is a data type
    :param float valueDecimal: If parameter is a data type
    :param str valueId: If parameter is a data type
    :param str valueInstant: If parameter is a data type
    :param int valueInteger: If parameter is a data type
    :param str valueMarkdown: If parameter is a data type
    :param str valueOid: If parameter is a data type
    :param int valuePositiveInt: If parameter is a data type
    :param str valueString: If parameter is a data type
    :param str valueTime: If parameter is a data type
    :param int valueUnsignedInt: If parameter is a data type
    :param str valueUri: If parameter is a data type
    :param str valueUrl: If parameter is a data type
    :param str valueUuid: If parameter is a data type
    :param Address valueAddress: If parameter is a data type
    :param Age valueAge: If parameter is a data type
    :param Annotation valueAnnotation: If parameter is a data type
    :param Attachment valueAttachment: If parameter is a data type
    :param CodeableConcept valueCodeableConcept: If parameter is a data type
    :param Coding valueCoding: If parameter is a data type
    :param ContactPoint valueContactPoint: If parameter is a data type
    :param Count valueCount: If parameter is a data type
    :param Distance valueDistance: If parameter is a data type
    :param Duration valueDuration: If parameter is a data type
    :param HumanName valueHumanName: If parameter is a data type
    :param Identifier valueIdentifier: If parameter is a data type
    :param Money valueMoney: If parameter is a data type
    :param Period valuePeriod: If parameter is a data type
    :param Quantity valueQuantity: If parameter is a data type
    :param Range valueRange: If parameter is a data type
    :param Ratio valueRatio: If parameter is a data type
    :param Reference valueReference: If parameter is a data type
    :param SampledData valueSampledData: If parameter is a data type
    :param Signature valueSignature: If parameter is a data type
    :param Timing valueTiming: If parameter is a data type
    :param ContactDetail valueContactDetail: If parameter is a data type
    :param Contributor valueContributor: If parameter is a data type
    :param DataRequirement valueDataRequirement: If parameter is a data type
    :param Expression valueExpression: If parameter is a data type
    :param ParameterDefinition valueParameterDefinition: If parameter is a data type
    :param RelatedArtifact valueRelatedArtifact: If parameter is a data type
    :param TriggerDefinition valueTriggerDefinition: If parameter is a data type
    :param UsageContext valueUsageContext: If parameter is a data type
    :param Dosage valueDosage: If parameter is a data type
    :param Meta valueMeta: If parameter is a data type
    :param Resource resource: If parameter is a whole resource
    :param Part part: Named part of a multi-part parameter
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "valueAddress": {"class_name": "Address", "is_contained": False},
        "valueAge": {"class_name": "Age", "is_contained": False},
        "valueAnnotation": {"class_name": "Annotation", "is_contained": False},
        "valueAttachment": {"class_name": "Attachment", "is_contained": False},
        "valueCodeableConcept": {
            "class_name": "CodeableConcept",
            "is_contained": False,
        },
        "valueCoding": {"class_name": "Coding", "is_contained": False},
        "valueContactPoint": {"class_name": "ContactPoint", "is_contained": False},
        "valueCount": {"class_name": "Count", "is_contained": False},
        "valueDistance": {"class_name": "Distance", "is_contained": False},
        "valueDuration": {"class_name": "Duration", "is_contained": False},
        "valueHumanName": {"class_name": "HumanName", "is_contained": False},
        "valueIdentifier": {"class_name": "Identifier", "is_contained": False},
        "valueMoney": {"class_name": "Money", "is_contained": False},
        "valuePeriod": {"class_name": "Period", "is_contained": False},
        "valueQuantity": {"class_name": "Quantity", "is_contained": False},
        "valueRange": {"class_name": "Range", "is_contained": False},
        "valueRatio": {"class_name": "Ratio", "is_contained": False},
        "valueReference": {"class_name": "Reference", "is_contained": False},
        "valueSampledData": {"class_name": "SampledData", "is_contained": False},
        "valueSignature": {"class_name": "Signature", "is_contained": False},
        "valueTiming": {"class_name": "Timing", "is_contained": False},
        "valueContactDetail": {"class_name": "ContactDetail", "is_contained": False},
        "valueContributor": {"class_name": "Contributor", "is_contained": False},
        "valueDataRequirement": {
            "class_name": "DataRequirement",
            "is_contained": False,
        },
        "valueExpression": {"class_name": "Expression", "is_contained": False},
        "valueParameterDefinition": {
            "class_name": "ParameterDefinition",
            "is_contained": False,
        },
        "valueRelatedArtifact": {
            "class_name": "RelatedArtifact",
            "is_contained": False,
        },
        "valueTriggerDefinition": {
            "class_name": "TriggerDefinition",
            "is_contained": False,
        },
        "valueUsageContext": {"class_name": "UsageContext", "is_contained": False},
        "valueDosage": {"class_name": "Dosage", "is_contained": False},
        "valueMeta": {"class_name": "Meta", "is_contained": False},
        "resource": {"class_name": "Resource", "is_contained": False},
        "part": {"class_name": "Part", "is_contained": True},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        name: "str" = None,
        valueBase64Binary: "str" = None,
        valueBoolean: "bool" = None,
        valueCanonical: "str" = None,
        valueCode: "str" = None,
        valueDate: "str" = None,
        valueDateTime: "str" = None,
        valueDecimal: "float" = None,
        valueId: "str" = None,
        valueInstant: "str" = None,
        valueInteger: "int" = None,
        valueMarkdown: "str" = None,
        valueOid: "str" = None,
        valuePositiveInt: "int" = None,
        valueString: "str" = None,
        valueTime: "str" = None,
        valueUnsignedInt: "int" = None,
        valueUri: "str" = None,
        valueUrl: "str" = None,
        valueUuid: "str" = None,
        valueAddress: "Address" = None,
        valueAge: "Age" = None,
        valueAnnotation: "Annotation" = None,
        valueAttachment: "Attachment" = None,
        valueCodeableConcept: "CodeableConcept" = None,
        valueCoding: "Coding" = None,
        valueContactPoint: "ContactPoint" = None,
        valueCount: "Count" = None,
        valueDistance: "Distance" = None,
        valueDuration: "Duration" = None,
        valueHumanName: "HumanName" = None,
        valueIdentifier: "Identifier" = None,
        valueMoney: "Money" = None,
        valuePeriod: "Period" = None,
        valueQuantity: "Quantity" = None,
        valueRange: "Range" = None,
        valueRatio: "Ratio" = None,
        valueReference: "Reference" = None,
        valueSampledData: "SampledData" = None,
        valueSignature: "Signature" = None,
        valueTiming: "Timing" = None,
        valueContactDetail: "ContactDetail" = None,
        valueContributor: "Contributor" = None,
        valueDataRequirement: "DataRequirement" = None,
        valueExpression: "Expression" = None,
        valueParameterDefinition: "ParameterDefinition" = None,
        valueRelatedArtifact: "RelatedArtifact" = None,
        valueTriggerDefinition: "TriggerDefinition" = None,
        valueUsageContext: "UsageContext" = None,
        valueDosage: "Dosage" = None,
        valueMeta: "Meta" = None,
        resource: "Resource" = None,
        part: list["Part"] = None,
    ):
        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.name = name
        self.valueBase64Binary = valueBase64Binary
        self.valueBoolean = valueBoolean
        self.valueCanonical = valueCanonical
        self.valueCode = valueCode
        self.valueDate = valueDate
        self.valueDateTime = valueDateTime
        self.valueDecimal = valueDecimal
        self.valueId = valueId
        self.valueInstant = valueInstant
        self.valueInteger = valueInteger
        self.valueMarkdown = valueMarkdown
        self.valueOid = valueOid
        self.valuePositiveInt = valuePositiveInt
        self.valueString = valueString
        self.valueTime = valueTime
        self.valueUnsignedInt = valueUnsignedInt
        self.valueUri = valueUri
        self.valueUrl = valueUrl
        self.valueUuid = valueUuid
        self.valueAddress = valueAddress
        self.valueAge = valueAge
        self.valueAnnotation = valueAnnotation
        self.valueAttachment = valueAttachment
        self.valueCodeableConcept = valueCodeableConcept
        self.valueCoding = valueCoding
        self.valueContactPoint = valueContactPoint
        self.valueCount = valueCount
        self.valueDistance = valueDistance
        self.valueDuration = valueDuration
        self.valueHumanName = valueHumanName
        self.valueIdentifier = valueIdentifier
        self.valueMoney = valueMoney
        self.valuePeriod = valuePeriod
        self.valueQuantity = valueQuantity
        self.valueRange = valueRange
        self.valueRatio = valueRatio
        self.valueReference = valueReference
        self.valueSampledData = valueSampledData
        self.valueSignature = valueSignature
        self.valueTiming = valueTiming
        self.valueContactDetail = valueContactDetail
        self.valueContributor = valueContributor
        self.valueDataRequirement = valueDataRequirement
        self.valueExpression = valueExpression
        self.valueParameterDefinition = valueParameterDefinition
        self.valueRelatedArtifact = valueRelatedArtifact
        self.valueTriggerDefinition = valueTriggerDefinition
        self.valueUsageContext = valueUsageContext
        self.valueDosage = valueDosage
        self.valueMeta = valueMeta
        self.resource = resource
        self.part = part or []

    @classmethod
    def from_dict(cls, data: dict) -> "Parameters":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Parameters":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class Parameters(DomainResource):
    """This resource is a non-persisted resource used to pass information into and back from an [operation](operations.html). It has no other use, and there is no RESTful endpoint associated with it.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    :param Parameter parameter: Operation Parameter
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "meta": {"class_name": "Meta", "is_contained": False},
        "parameter": {"class_name": "Parameter", "is_contained": True},
    }

    def __init__(
        self,
        id: "str" = None,
        meta: "Meta" = None,
        implicitRules: "str" = None,
        language: "str" = None,
        parameter: list["Parameter"] = None,
    ):

        self.id = id
        self.meta = meta
        self.implicitRules = implicitRules
        self.language = language
        self.parameter = parameter or []

    @classmethod
    def from_dict(cls, data: dict) -> "Parameters":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Parameters":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
