"""
Generated class for Resource. 
Time: 2024-06-14 18:55:42
"""
from fhirmodels.fhir_base_model import FhirBaseModel
from fhirmodels.R4.Meta import *


class Resource(FhirBaseModel):
    """ This is the base resource type for everything.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "meta": {"class_name": "Meta", "is_contained": False},
        
        
        
        }
    def __init__(self,  id:  'str'  = None,  meta:  'Meta'  = None,  implicitRules:  'str'  = None,  language:  'str'  = None, ):
        
        self.id = id 
        self.meta = meta 
        self.implicitRules = implicitRules 
        self.language = language 
        

    @classmethod
    def from_dict(cls, data: dict) -> "Resource":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "Resource":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()