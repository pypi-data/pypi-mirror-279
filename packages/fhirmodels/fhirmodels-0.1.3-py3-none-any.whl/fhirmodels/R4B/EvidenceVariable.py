"""
Generated class for EvidenceVariable. 
Time: 2024-06-14 18:55:59
"""
from fhirmodels.R4B.Annotation import *
from fhirmodels.R4B.BackboneElement import *
from fhirmodels.R4B.CodeableConcept import *
from fhirmodels.R4B.ContactDetail import *
from fhirmodels.R4B.DomainResource import *
from fhirmodels.R4B.Expression import *
from fhirmodels.R4B.Extension import *
from fhirmodels.R4B.Identifier import *
from fhirmodels.R4B.Meta import *
from fhirmodels.R4B.Narrative import *
from fhirmodels.R4B.Quantity import *
from fhirmodels.R4B.Range import *
from fhirmodels.R4B.Reference import *
from fhirmodels.R4B.RelatedArtifact import *
from fhirmodels.R4B.Resource import *
from fhirmodels.R4B.UsageContext import *


class TimeFromStart(FhirBaseModel):
    """ Indicates duration, period, or point of observation from the participant's study entry.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param str description: Human readable description
    :param Quantity quantity: Used to express the observation at a defined amount of time after the study start
    :param Range range: Used to express the observation within a period after the study start
    :param Annotation note: Used for footnotes or explanatory notes
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        
        "quantity": {"class_name": "Quantity", "is_contained": False},
        
        
        "range": {"class_name": "Range", "is_contained": False},
        
        
        "note": {"class_name": "Annotation", "is_contained": False},
        
        }
    def __init__(self,  id:  'str'  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  description:  'str'  = None,  quantity:  'Quantity'  = None,  range:  'Range'  = None,  note:  list['Annotation']  = None, ):
        self.id = id 
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.description = description 
        self.quantity = quantity 
        self.range = range 
        self.note = note or []
        

    @classmethod
    def from_dict(cls, data: dict) -> "EvidenceVariable":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "EvidenceVariable":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


  
    
    

class Characteristic(FhirBaseModel):
    """ A characteristic that defines the members of the evidence element. Multiple characteristics are applied with "and" semantics.:param str characteristicCombination: intersection | union
    :param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param str description: Natural language description of the characteristic
    :param Reference definitionReference: What code or expression defines members?
    :param str definitionCanonical: What code or expression defines members?
    :param CodeableConcept definitionCodeableConcept: What code or expression defines members?
    :param Expression definitionExpression: What code or expression defines members?
    :param CodeableConcept method: Method used for describing characteristic
    :param Reference device: Device used for determining characteristic
    :param bool exclude: Whether the characteristic includes or excludes members
    :param TimeFromStart timeFromStart: Observation time from study start
    :param str groupMeasure: mean | median | mean-of-mean | mean-of-median | median-of-mean | median-of-median
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        
        "definitionReference": {"class_name": "Reference", "is_contained": False},
        
        
        
        "definitionCodeableConcept": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "definitionExpression": {"class_name": "Expression", "is_contained": False},
        
        
        "method": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "device": {"class_name": "Reference", "is_contained": False},
        
        
        
        "timeFromStart": {"class_name": "TimeFromStart", "is_contained": True},
        
        
        }
    def __init__(self,  characteristicCombination:  'str'  = None,  id:  'str'  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  description:  'str'  = None,  definitionReference:  'Reference'  = None,  definitionCanonical:  'str'  = None,  definitionCodeableConcept:  'CodeableConcept'  = None,  definitionExpression:  'Expression'  = None,  method:  'CodeableConcept'  = None,  device:  'Reference'  = None,  exclude:  'bool'  = None,  timeFromStart:  'TimeFromStart'  = None,  groupMeasure:  'str'  = None, ):
        self.characteristicCombination = characteristicCombination 
        self.id = id 
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.description = description 
        self.definitionReference = definitionReference 
        self.definitionCanonical = definitionCanonical 
        self.definitionCodeableConcept = definitionCodeableConcept 
        self.definitionExpression = definitionExpression 
        self.method = method 
        self.device = device 
        self.exclude = exclude 
        self.timeFromStart = timeFromStart 
        self.groupMeasure = groupMeasure 
        

    @classmethod
    def from_dict(cls, data: dict) -> "EvidenceVariable":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "EvidenceVariable":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


    
    

class Category(FhirBaseModel):
    """ A grouping (or set of values) described along with other groupings to specify the set of groupings allowed for the variable.:param str id: Unique id for inter-element referencing
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored even if unrecognized
    :param str name: Description of the grouping
    :param CodeableConcept valueCodeableConcept: Definition of the grouping
    :param Quantity valueQuantity: Definition of the grouping
    :param Range valueRange: Definition of the grouping
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        
        "valueCodeableConcept": {"class_name": "CodeableConcept", "is_contained": False},
        
        
        "valueQuantity": {"class_name": "Quantity", "is_contained": False},
        
        
        "valueRange": {"class_name": "Range", "is_contained": False},
        
        }
    def __init__(self,  id:  'str'  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  name:  'str'  = None,  valueCodeableConcept:  'CodeableConcept'  = None,  valueQuantity:  'Quantity'  = None,  valueRange:  'Range'  = None, ):
        self.id = id 
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.name = name 
        self.valueCodeableConcept = valueCodeableConcept 
        self.valueQuantity = valueQuantity 
        self.valueRange = valueRange 
        

    @classmethod
    def from_dict(cls, data: dict) -> "EvidenceVariable":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "EvidenceVariable":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()


class EvidenceVariable(DomainResource):
    """ The EvidenceVariable resource describes an element that knowledge (Evidence) is about.
    :param str id: Logical id of this artifact
    :param Meta meta: Metadata about the resource
    :param str implicitRules: A set of rules under which this content was created
    :param str language: Language of the resource content
    :param Narrative text: Text summary of the resource, for human interpretation
    :param Resource contained: Contained, inline Resources
    :param Extension extension: Additional content defined by implementations
    :param Extension modifierExtension: Extensions that cannot be ignored
    :param str url: Canonical identifier for this evidence variable, represented as a URI (globally unique)
    :param Identifier identifier: Additional identifier for the evidence variable
    :param str version: Business version of the evidence variable
    :param str name: Name for this evidence variable (computer friendly)
    :param str title: Name for this evidence variable (human friendly)
    :param str shortTitle: Title for use in informal contexts
    :param str subtitle: Subordinate title of the EvidenceVariable
    :param str status: draft | active | retired | unknown
    :param str date: Date last changed
    :param str description: Natural language description of the evidence variable
    :param Annotation note: Used for footnotes or explanatory notes
    :param UsageContext useContext: The context that the content is intended to support
    :param str publisher: Name of the publisher (organization or individual)
    :param ContactDetail contact: Contact details for the publisher
    :param ContactDetail author: Who authored the content
    :param ContactDetail editor: Who edited the content
    :param ContactDetail reviewer: Who reviewed the content
    :param ContactDetail endorser: Who endorsed the content
    :param RelatedArtifact relatedArtifact: Additional documentation, citations, etc.
    :param bool actual: Actual or conceptual
    :param str characteristicCombination: intersection | union
    :param Characteristic characteristic: What defines the members of the evidence element
    :param str handling: continuous | dichotomous | ordinal | polychotomous
    :param Category category: A grouping for ordinal or polychotomous variables
    """
    # needed for complex properties where the element name is different from the class name
    property_class_info = {
        
        
        "meta": {"class_name": "Meta", "is_contained": False},
        
        
        
        
        "text": {"class_name": "Narrative", "is_contained": False},
        
        
        "contained": {"class_name": "Resource", "is_contained": False},
        
        
        "extension": {"class_name": "Extension", "is_contained": False},
        
        
        "modifierExtension": {"class_name": "Extension", "is_contained": False},
        
        
        
        "identifier": {"class_name": "Identifier", "is_contained": False},
        
        
        
        
        
        
        
        
        
        
        "note": {"class_name": "Annotation", "is_contained": False},
        
        
        "useContext": {"class_name": "UsageContext", "is_contained": False},
        
        
        
        "contact": {"class_name": "ContactDetail", "is_contained": False},
        
        
        "author": {"class_name": "ContactDetail", "is_contained": False},
        
        
        "editor": {"class_name": "ContactDetail", "is_contained": False},
        
        
        "reviewer": {"class_name": "ContactDetail", "is_contained": False},
        
        
        "endorser": {"class_name": "ContactDetail", "is_contained": False},
        
        
        "relatedArtifact": {"class_name": "RelatedArtifact", "is_contained": False},
        
        
        
        
        "characteristic": {"class_name": "Characteristic", "is_contained": True},
        
        
        
        "category": {"class_name": "Category", "is_contained": True},
        
        }
    def __init__(self,  id:  'str'  = None,  meta:  'Meta'  = None,  implicitRules:  'str'  = None,  language:  'str'  = None,  text:  'Narrative'  = None,  contained:  list['Resource']  = None,  extension:  list['Extension']  = None,  modifierExtension:  list['Extension']  = None,  url:  'str'  = None,  identifier:  list['Identifier']  = None,  version:  'str'  = None,  name:  'str'  = None,  title:  'str'  = None,  shortTitle:  'str'  = None,  subtitle:  'str'  = None,  status:  'str'  = None,  date:  'str'  = None,  description:  'str'  = None,  note:  list['Annotation']  = None,  useContext:  list['UsageContext']  = None,  publisher:  'str'  = None,  contact:  list['ContactDetail']  = None,  author:  list['ContactDetail']  = None,  editor:  list['ContactDetail']  = None,  reviewer:  list['ContactDetail']  = None,  endorser:  list['ContactDetail']  = None,  relatedArtifact:  list['RelatedArtifact']  = None,  actual:  'bool'  = None,  characteristicCombination:  'str'  = None,  characteristic:  list['Characteristic']  = None,  handling:  'str'  = None,  category:  list['Category']  = None, ):
        
        self.resourceType = "EvidenceVariable"
        
        self.id = id 
        self.meta = meta 
        self.implicitRules = implicitRules 
        self.language = language 
        self.text = text 
        self.contained = contained or []
        self.extension = extension or []
        self.modifierExtension = modifierExtension or []
        self.url = url 
        self.identifier = identifier or []
        self.version = version 
        self.name = name 
        self.title = title 
        self.shortTitle = shortTitle 
        self.subtitle = subtitle 
        self.status = status 
        self.date = date 
        self.description = description 
        self.note = note or []
        self.useContext = useContext or []
        self.publisher = publisher 
        self.contact = contact or []
        self.author = author or []
        self.editor = editor or []
        self.reviewer = reviewer or []
        self.endorser = endorser or []
        self.relatedArtifact = relatedArtifact or []
        self.actual = actual 
        self.characteristicCombination = characteristicCombination 
        self.characteristic = characteristic or []
        self.handling = handling 
        self.category = category or []
        

    @classmethod
    def from_dict(cls, data: dict) -> "EvidenceVariable":
        return super().from_dict(data)
    
    @classmethod
    def from_obj(self, obj: object) -> "EvidenceVariable":
        return super().from_obj(obj)

    def as_dict(self) -> dict:
        return super().as_dict()