"""
Generated class for Ingredient. 
Time: 2024-06-13 23:34:40
"""

from fhirmodels.models.R4B.BackboneElement import *
from fhirmodels.models.R4B.CodeableConcept import *
from fhirmodels.models.R4B.CodeableReference import *
from fhirmodels.models.R4B.DomainResource import *
from fhirmodels.models.R4B.Extension import *
from fhirmodels.models.R4B.Identifier import *
from fhirmodels.models.R4B.Meta import *
from fhirmodels.models.R4B.Narrative import *
from fhirmodels.models.R4B.Ratio import *
from fhirmodels.models.R4B.RatioRange import *
from fhirmodels.models.R4B.Reference import *
from fhirmodels.models.R4B.Resource import *


class Manufacturer(FhirBaseModel):
    """The organization(s) that manufacture this ingredient. Can be used to indicate:         1) Organizations we are aware of that manufacture this ingredient         2) Specific Manufacturer(s) currently being used         3) Set of organisations allowed to manufacture this ingredient for this product         Users must be clear on the application of context relevant to their use case.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param str role: allowed | possible | actual
    :param Reference manufacturer: An organization that manufactures this ingredient
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "manufacturer": {"class_name": "Reference", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        role: "str" = None,
        manufacturer: "Reference" = None,
    ):
        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.role = role
        self.manufacturer = manufacturer

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Ingredient":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class ReferenceStrength(FhirBaseModel):
    """Strength expressed in terms of a reference substance. For when the ingredient strength is additionally expressed as equivalent to the strength of some other closely related substance (e.g. salt vs. base). Reference strength represents the strength (quantitative composition) of the active moiety of the active substance. There are situations when the active substance and active moiety are different, therefore both a strength and a reference strength are needed.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param CodeableReference substance: Relevant reference substance
    :param Ratio strengthRatio: Strength expressed in terms of a reference substance
    :param RatioRange strengthRatioRange: Strength expressed in terms of a reference substance
    :param str measurementPoint: When strength is measured at a particular point or distance
    :param CodeableConcept country: Where the strength range applies
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "substance": {"class_name": "CodeableReference", "is_contained": False},
        "strengthRatio": {"class_name": "Ratio", "is_contained": False},
        "strengthRatioRange": {"class_name": "RatioRange", "is_contained": False},
        "country": {"class_name": "CodeableConcept", "is_contained": False},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        substance: "CodeableReference" = None,
        strengthRatio: "Ratio" = None,
        strengthRatioRange: "RatioRange" = None,
        measurementPoint: "str" = None,
        country: list["CodeableConcept"] = None,
    ):
        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.substance = substance
        self.strengthRatio = strengthRatio
        self.strengthRatioRange = strengthRatioRange
        self.measurementPoint = measurementPoint
        self.country = country or []

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Ingredient":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class Strength(FhirBaseModel):
    """The quantity of substance in the unit of presentation, or in the volume (or mass) of the single pharmaceutical product or manufactured item. The allowed repetitions do not represent different strengths, but are different representations - mathematically equivalent - of a single strength.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param Ratio presentationRatio: The quantity of substance in the unit of presentation
    :param RatioRange presentationRatioRange: The quantity of substance in the unit of presentation
    :param str textPresentation: Text of either the whole presentation strength or a part of it (rest being in Strength.presentation as a ratio)
    :param Ratio concentrationRatio: The strength per unitary volume (or mass)
    :param RatioRange concentrationRatioRange: The strength per unitary volume (or mass)
    :param str textConcentration: Text of either the whole concentration strength or a part of it (rest being in Strength.concentration as a ratio)
    :param str measurementPoint: When strength is measured at a particular point or distance
    :param CodeableConcept country: Where the strength range applies
    :param ReferenceStrength referenceStrength: Strength expressed in terms of a reference substance
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "presentationRatio": {"class_name": "Ratio", "is_contained": False},
        "presentationRatioRange": {"class_name": "RatioRange", "is_contained": False},
        "concentrationRatio": {"class_name": "Ratio", "is_contained": False},
        "concentrationRatioRange": {"class_name": "RatioRange", "is_contained": False},
        "country": {"class_name": "CodeableConcept", "is_contained": False},
        "referenceStrength": {"class_name": "ReferenceStrength", "is_contained": True},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        presentationRatio: "Ratio" = None,
        presentationRatioRange: "RatioRange" = None,
        textPresentation: "str" = None,
        concentrationRatio: "Ratio" = None,
        concentrationRatioRange: "RatioRange" = None,
        textConcentration: "str" = None,
        measurementPoint: "str" = None,
        country: list["CodeableConcept"] = None,
        referenceStrength: list["ReferenceStrength"] = None,
    ):
        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.presentationRatio = presentationRatio
        self.presentationRatioRange = presentationRatioRange
        self.textPresentation = textPresentation
        self.concentrationRatio = concentrationRatio
        self.concentrationRatioRange = concentrationRatioRange
        self.textConcentration = textConcentration
        self.measurementPoint = measurementPoint
        self.country = country or []
        self.referenceStrength = referenceStrength or []

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Ingredient":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class Substance(FhirBaseModel):
    """The substance that comprises this ingredient.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param CodeableReference code: A code or full resource that represents the ingredient substance
    :param Strength strength: The quantity of substance, per presentation, or per volume or mass, and type of quantity
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "code": {"class_name": "CodeableReference", "is_contained": False},
        "strength": {"class_name": "Strength", "is_contained": True},
    }

    def __init__(
        self,
        id: "str" = None,
        extension: list["Extension"] = None,
        modifierExtension: list["Extension"] = None,
        code: "CodeableReference" = None,
        strength: list["Strength"] = None,
    ):
        self.id = id
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.code = code
        self.strength = strength or []

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Ingredient":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class Ingredient(DomainResource):
    """An ingredient of a manufactured item or pharmaceutical product.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    :param Narrative text: Text summary of the resource, for human interpretation
    :param Resource contained: Contained, inline Resources
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored
    :param Identifier identifier: An identifier or code by which the ingredient can be referenced
    :param str status: draft | active | retired | unknown
    :param Reference _for: The product which this ingredient is a constituent part of
    :param CodeableConcept role: Purpose of the ingredient within the product, e.g. active, inactive
    :param CodeableConcept function: Precise action within the drug product, e.g. antioxidant, alkalizing agent
    :param bool allergenicIndicator: If the ingredient is a known or suspected allergen
    :param Manufacturer manufacturer: An organization that manufactures this ingredient
    :param Substance substance: The substance that comprises this ingredient
    """

    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        "meta": {"class_name": "Meta", "is_contained": False},
        "text": {"class_name": "Narrative", "is_contained": False},
        "contained": {"class_name": "Resource", "is_contained": False},
        "extension": {"class_name": "Extension", "is_contained": False},
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        "identifier": {"class_name": "Identifier", "is_contained": False},
        "_for": {"class_name": "Reference", "is_contained": False},
        "role": {"class_name": "CodeableConcept", "is_contained": False},
        "function": {"class_name": "CodeableConcept", "is_contained": False},
        "manufacturer": {"class_name": "Manufacturer", "is_contained": True},
        "substance": {"class_name": "Substance", "is_contained": True},
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
        identifier: "Identifier" = None,
        status: "str" = None,
        _for: list["Reference"] = None,
        role: "CodeableConcept" = None,
        function: list["CodeableConcept"] = None,
        allergenicIndicator: "bool" = None,
        manufacturer: list["Manufacturer"] = None,
        substance: "Substance" = None,
    ):

        self.resourceType = "Ingredient"

        self.id = id
        self.meta = meta
        self.implicitRules = implicitRules
        self.language = language
        self.text = text
        self.contained = contained or []
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.identifier = identifier
        self.status = status
        self._for = _for or []
        self.role = role
        self.function = function or []
        self.allergenicIndicator = allergenicIndicator
        self.manufacturer = manufacturer or []
        self.substance = substance

    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        return super().from_dict(data)

    @classmethod
    def from_obj(self, obj: object) -> "Ingredient":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()
