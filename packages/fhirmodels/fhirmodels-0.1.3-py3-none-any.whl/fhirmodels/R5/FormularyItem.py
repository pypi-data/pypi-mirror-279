"""
Generated class for FormularyItem. 
Time: 2024-06-14 18:56:04
"""
from fhirmodels.R5.CodeableConcept import *
from fhirmodels.R5.DomainResource import *
from fhirmodels.R5.Extension import *
from fhirmodels.R5.Identifier import *
from fhirmodels.R5.Meta import *
from fhirmodels.R5.Narrative import *
from fhirmodels.R5.Resource import *


class FormularyItem(DomainResource):
    """ This resource describes a product or service that is available through a program and includes the conditions and constraints of availability.  All of the information in this resource is specific to the inclusion of the item in the formulary and is not inherent to the item itself.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    :param Narrative text: Text summary of the resource, for human interpretation
    :param Resource contained: Contained, inline Resources
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored
    :param Identifier identifier: Business identifier for this formulary item
    :param CodeableConcept code: Codes that identify this formulary item
    :param str status: active | entered-in-error | inactive
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "meta": {"class_name": "Meta", "is_contained": False},
        
        
        
        
        "text": {"class_name": "Narrative", "is_contained": False},
        
        
        "contained": {"class_name": "Resource", "is_contained": False},
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        "identifier": {"class_name": "Identifier", "is_contained": False},
        
        
        "code": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        }
    def __init__(self,  id:  'str'  = None,  meta:  'Meta'  = None,  implicitRules:  'str'  = None,  language:  'str'  = None,  text:  'Narrative'  = None,  contained:  list['Resource']  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  identifier:  list['Identifier']  = None,  code:  'CodeableConcept'  = None,  status:  'str'  = None, ):
        
        self.resourceType = "FormularyItem"
        
        self.id = id 
        self.meta = meta 
        self.implicitRules = implicitRules 
        self.language = language 
        self.text = text 
        self.contained = contained or []
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.identifier = identifier or []
        self.code = code 
        self.status = status 
        

    @classmethod
    def from_dict(cls, data: dict) -> "FormularyItem":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "FormularyItem":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()