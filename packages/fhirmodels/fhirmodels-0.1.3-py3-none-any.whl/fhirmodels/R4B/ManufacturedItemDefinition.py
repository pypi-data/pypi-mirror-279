"""
Generated class for ManufacturedItemDefinition. 
Time: 2024-06-14 18:55:59
"""
from fhirmodels.R4B.Attachment import *
from fhirmodels.R4B.BackboneElement import *
from fhirmodels.R4B.CodeableConcept import *
from fhirmodels.R4B.DomainResource import *
from fhirmodels.R4B.Extension import *
from fhirmodels.R4B.Identifier import *
from fhirmodels.R4B.Meta import *
from fhirmodels.R4B.Narrative import *
from fhirmodels.R4B.Quantity import *
from fhirmodels.R4B.Reference import *
from fhirmodels.R4B.Resource import *


class Property(FhirBaseModel):
    """ General characteristics of this item.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param CodeableConcept type: A code expressing the type of characteristic
    :param CodeableConcept valueCodeableConcept: A value for the characteristic
    :param Quantity valueQuantity: A value for the characteristic
    :param str valueDate: A value for the characteristic
    :param bool valueBoolean: A value for the characteristic
    :param Attachment valueAttachment: A value for the characteristic
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        "type": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "valueCodeableConcept": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "valueQuantity": {"class_name": "Quantity", "is_contained": False},
        
        
        
        
        "valueAttachment": {"class_name": "Attachment", "is_contained": False},
        
        }
    def __init__(self,  id:  'str'  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  type:  'CodeableConcept'  = None,  valueCodeableConcept:  'CodeableConcept'  = None,  valueQuantity:  'Quantity'  = None,  valueDate:  'str'  = None,  valueBoolean:  'bool'  = None,  valueAttachment:  'Attachment'  = None, ):
        self.id = id 
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.type = type 
        self.valueCodeableConcept = valueCodeableConcept 
        self.valueQuantity = valueQuantity 
        self.valueDate = valueDate 
        self.valueBoolean = valueBoolean 
        self.valueAttachment = valueAttachment 
        

    @classmethod
    def from_dict(cls, data: dict) -> "ManufacturedItemDefinition":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "ManufacturedItemDefinition":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class ManufacturedItemDefinition(DomainResource):
    """ The definition and characteristics of a medicinal manufactured item, such as a tablet or capsule, as contained in a packaged medicinal product.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    :param Narrative text: Text summary of the resource, for human interpretation
    :param Resource contained: Contained, inline Resources
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored
    :param Identifier identifier: Unique identifier
    :param str status: draft | active | retired | unknown
    :param CodeableConcept manufacturedDoseForm: Dose form as manufactured (before any necessary transformation)
    :param CodeableConcept unitOfPresentation: The “real world” units in which the quantity of the item is described
    :param Reference manufacturer: Manufacturer of the item (Note that this should be named "manufacturer" but it currently causes technical issues)
    :param CodeableConcept ingredient: The ingredients of this manufactured item. Only needed if these are not specified by incoming references from the Ingredient resource
    :param Property property: General characteristics of this item
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "meta": {"class_name": "Meta", "is_contained": False},
        
        
        
        
        "text": {"class_name": "Narrative", "is_contained": False},
        
        
        "contained": {"class_name": "Resource", "is_contained": False},
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        "identifier": {"class_name": "Identifier", "is_contained": False},
        
        
        
        "manufacturedDoseForm": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "unitOfPresentation": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "manufacturer": {"class_name": "Reference", "is_contained": False},
        
        
        "ingredient": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "property": {"class_name": "Property", "is_contained": True},
        
        }
    def __init__(self,  id:  'str'  = None,  meta:  'Meta'  = None,  implicitRules:  'str'  = None,  language:  'str'  = None,  text:  'Narrative'  = None,  contained:  list['Resource']  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  identifier:  list['Identifier']  = None,  status:  'str'  = None,  manufacturedDoseForm:  'CodeableConcept'  = None,  unitOfPresentation:  'CodeableConcept'  = None,  manufacturer:  list['Reference']  = None,  ingredient:  list['CodeableConcept']  = None,  property:  list['Property']  = None, ):
        
        self.resourceType = "ManufacturedItemDefinition"
        
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
        self.manufacturedDoseForm = manufacturedDoseForm 
        self.unitOfPresentation = unitOfPresentation 
        self.manufacturer = manufacturer or []
        self.ingredient = ingredient or []
        self.property = property or []
        

    @classmethod
    def from_dict(cls, data: dict) -> "ManufacturedItemDefinition":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "ManufacturedItemDefinition":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()