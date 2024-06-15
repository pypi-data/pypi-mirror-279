import pytest

from fhirmodels.models.R4.Annotation import Annotation
from fhirmodels.models.R4.CodeableConcept import CodeableConcept
from fhirmodels.models.R4.Condition import Condition, Evidence, Stage
from fhirmodels.models.R4.Identifier import Identifier
from fhirmodels.models.R4.Meta import Meta
from fhirmodels.models.R4.Narrative import Narrative
from fhirmodels.models.R4.Reference import Reference

# Sample data to be used in tests
sample_condition_dict = {
    "resourceType": "Condition",
    "id": "example",
    "meta": {"versionId": "1", "lastUpdated": "2021-05-25T12:30:50.150+00:00"},
    "text": {"status": "generated", "div": "<div>Condition Text</div>"},
    "identifier": [{"system": "http://example.org", "value": "12345"}],
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "problem-list-item",
                }
            ]
        }
    ],
    "severity": {
        "coding": [
            {"system": "http://snomed.info/sct", "code": "255604002", "display": "Mild"}
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "386661006",
                "display": "Fever",
            }
        ]
    },
    "bodySite": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "38266002",
                    "display": "Entire body",
                }
            ]
        }
    ],
    "subject": {"reference": "Patient/example"},
    "encounter": {"reference": "Encounter/example"},
    "onsetDateTime": "2021-05-25T12:30:50.150+00:00",
    "abatementDateTime": "2021-05-30T12:30:50.150+00:00",
    "recordedDate": "2021-05-25",
    "recorder": {"reference": "Practitioner/example"},
    "asserter": {"reference": "Practitioner/example"},
    "stage": [
        {
            "summary": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "261665006",
                        "display": "Stage I",
                    }
                ]
            },
            "assessment": [{"reference": "Observation/example"}],
        }
    ],
    "evidence": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "428341000124106",
                        "display": "Suspected diagnosis",
                    }
                ]
            },
            "detail": [{"reference": "Observation/example"}],
        }
    ],
    "note": [
        {
            "authorString": "Dr. Smith",
            "time": "2021-05-25T12:30:50.150+00:00",
            "text": "Patient is doing well.",
        }
    ],
}


# Test conversion from dictionary to Condition object
def test_condition_from_dict():
    condition = Condition.from_dict(sample_condition_dict)
    assert condition.resourceType == "Condition"
    assert condition.id == "example"
    assert isinstance(condition.meta, Meta)
    assert condition.meta.versionId == "1"
    assert isinstance(condition.text, Narrative)
    assert condition.text.div == "<div>Condition Text</div>"
    assert isinstance(condition.identifier[0], Identifier)
    assert condition.identifier[0].value == "12345"
    assert isinstance(condition.clinicalStatus, CodeableConcept)
    assert condition.clinicalStatus.coding[0].code == "active"
    assert isinstance(condition.verificationStatus, CodeableConcept)
    assert condition.verificationStatus.coding[0].code == "confirmed"
    assert isinstance(condition.category[0], CodeableConcept)
    assert condition.category[0].coding[0].code == "problem-list-item"
    assert isinstance(condition.severity, CodeableConcept)
    assert condition.severity.coding[0].code == "255604002"
    assert isinstance(condition.code, CodeableConcept)
    assert condition.code.coding[0].code == "386661006"
    assert isinstance(condition.bodySite[0], CodeableConcept)
    assert condition.bodySite[0].coding[0].code == "38266002"
    assert isinstance(condition.subject, Reference)
    assert condition.subject.reference == "Patient/example"
    assert isinstance(condition.encounter, Reference)
    assert condition.encounter.reference == "Encounter/example"
    assert condition.onsetDateTime == "2021-05-25T12:30:50.150+00:00"
    assert condition.abatementDateTime == "2021-05-30T12:30:50.150+00:00"
    assert condition.recordedDate == "2021-05-25"
    assert isinstance(condition.recorder, Reference)
    assert condition.recorder.reference == "Practitioner/example"
    assert isinstance(condition.asserter, Reference)
    assert condition.asserter.reference == "Practitioner/example"
    assert isinstance(condition.stage[0], Stage)
    assert condition.stage[0].summary.coding[0].code == "261665006"
    assert isinstance(condition.stage[0].assessment[0], Reference)
    assert condition.stage[0].assessment[0].reference == "Observation/example"
    assert isinstance(condition.evidence[0], Evidence)
    assert condition.evidence[0].code.coding[0].code == "428341000124106"
    assert isinstance(condition.evidence[0].detail[0], Reference)
    assert condition.evidence[0].detail[0].reference == "Observation/example"
    assert isinstance(condition.note[0], Annotation)
    assert condition.note[0].authorString == "Dr. Smith"
    assert condition.note[0].time == "2021-05-25T12:30:50.150+00:00"
    assert condition.note[0].text == "Patient is doing well."


# Test conversion from Condition object to dictionary
def test_condition_as_dict():
    condition = Condition.from_dict(sample_condition_dict)
    condition_dict = condition.as_dict()
    assert condition_dict == sample_condition_dict


# Test conversion from an object implementing as_dict() method to Condition object
def test_condition_from_obj():
    class MockConditionObject:
        def as_dict(self):
            return sample_condition_dict

    condition = Condition.from_obj(MockConditionObject())
    assert condition.resourceType == "Condition"
    assert condition.id == "example"
    assert isinstance(condition.meta, Meta)
    assert condition.meta.versionId == "1"
    assert isinstance(condition.text, Narrative)
    assert condition.text.div == "<div>Condition Text</div>"
    assert isinstance(condition.identifier[0], Identifier)
    assert condition.identifier[0].value == "12345"
    assert isinstance(condition.clinicalStatus, CodeableConcept)
    assert condition.clinicalStatus.coding[0].code == "active"
    assert isinstance(condition.verificationStatus, CodeableConcept)
    assert condition.verificationStatus.coding[0].code == "confirmed"
    assert isinstance(condition.category[0], CodeableConcept)
    assert condition.category[0].coding[0].code == "problem-list-item"
    assert isinstance(condition.severity, CodeableConcept)
    assert condition.severity.coding[0].code == "255604002"
    assert isinstance(condition.code, CodeableConcept)
    assert condition.code.coding[0].code == "386661006"
    assert isinstance(condition.bodySite[0], CodeableConcept)
    assert condition.bodySite[0].coding[0].code == "38266002"
    assert isinstance(condition.subject, Reference)
    assert condition.subject.reference == "Patient/example"
    assert isinstance(condition.encounter, Reference)
    assert condition.encounter.reference == "Encounter/example"
    assert condition.onsetDateTime == "2021-05-25T12:30:50.150+00:00"
    assert condition.abatementDateTime == "2021-05-30T12:30:50.150+00:00"
    assert condition.recordedDate == "2021-05-25"
    assert isinstance(condition.recorder, Reference)
    assert condition.recorder.reference == "Practitioner/example"
    assert isinstance(condition.asserter, Reference)
    assert condition.asserter.reference == "Practitioner/example"
    assert isinstance(condition.stage[0], Stage)
    assert condition.stage[0].summary.coding[0].code == "261665006"
    assert isinstance(condition.stage[0].assessment[0], Reference)
    assert condition.stage[0].assessment[0].reference == "Observation/example"
    assert isinstance(condition.evidence[0], Evidence)
    assert condition.evidence[0].code.coding[0].code == "428341000124106"
    assert isinstance(condition.evidence[0].detail[0], Reference)
    assert condition.evidence[0].detail[0].reference == "Observation/example"
    assert isinstance(condition.note[0], Annotation)
    assert condition.note[0].authorString == "Dr. Smith"
    assert condition.note[0].time == "2021-05-25T12:30:50.150+00:00"
    assert condition.note[0].text == "Patient is doing well."


# Test for invalid input to from_obj()
def test_invalid_input_to_from_obj():
    with pytest.raises(ValueError):
        Condition.from_obj("invalid_input")


# Test with missing optional fields
def test_condition_missing_optional_fields():
    minimal_condition_dict = {"resourceType": "Condition", "id": "example"}
    condition = Condition.from_dict(minimal_condition_dict)
    assert condition.resourceType == "Condition"
    assert condition.id == "example"
    assert condition.meta is None
    assert condition.text is None
    assert condition.identifier == []
    assert condition.clinicalStatus is None
    assert condition.verificationStatus is None
    assert condition.category == []
    assert condition.severity is None
    assert condition.code is None
    assert condition.bodySite == []
    assert condition.subject is None
    assert condition.encounter is None
    assert condition.onsetDateTime is None
    assert condition.abatementDateTime is None
    assert condition.recordedDate is None
    assert condition.recorder is None
    assert condition.asserter is None
    assert condition.stage == []
    assert condition.evidence == []
    assert condition.note == []


if __name__ == "__main__":
    pytest.main()
