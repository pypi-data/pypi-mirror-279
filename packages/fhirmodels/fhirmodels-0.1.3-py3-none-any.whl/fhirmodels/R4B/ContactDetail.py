"""
Generated class for ContactDetail. 
Time: 2024-06-14 18:55:59
"""
from fhirmodels.fhir_base_model import FhirBaseModel
from fhirmodels.R4B.ContactPoint import *
from fhirmodels.R4B.Extension import *


class ContactDetail(FhirBaseModel):
    """ Base StructureDefinition for ContactDetail Type: Specifies contact information for a person or organization.
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param str name: Name of an individual to contact
    :param ContactPoint telecom: Contact details for individual or organization
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        
        "telecom": {"class_name": "ContactPoint", "is_contained": False},
        
        }
    def __init__(self,  id:  'str'  = None,  extension:  list['Extension']  = None,  name:  'str'  = None,  telecom:  list['ContactPoint']  = None, ):
        
        self.id = id 
        self.extension = extension or []
        self.name = name 
        self.telecom = telecom or []
        

    @classmethod
    def from_dict(cls, data: dict) -> "ContactDetail":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "ContactDetail":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()