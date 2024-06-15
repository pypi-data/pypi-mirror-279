"""
Generated class for ParticipantContactable. 
Time: 2024-06-14 18:56:04
"""
from fhirmodels.fhir_base_model import FhirBaseModel
from fhirmodels.R5.Address import *
from fhirmodels.R5.ContactPoint import *


class ParticipantContactable(FhirBaseModel):
    """ Logical Model: A pattern followed by resources that represent a participant that can be contacted.
    :param ContactPoint telecom: A contact detail for the {{title}}
    :param Address address: An address for the {{title}}
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        "telecom": {"class_name": "ContactPoint", "is_contained": False},
        
        
        "address": {"class_name": "Address", "is_contained": False},
        
        }
    def __init__(self,  telecom:  list['ContactPoint']  = None,  address:  list['Address']  = None, ):
        
        self.telecom = telecom or []
        self.address = address or []
        

    @classmethod
    def from_dict(cls, data: dict) -> "ParticipantContactable":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "ParticipantContactable":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()