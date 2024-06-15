# SETTINGS
DEFAULT_OUTPUT_DIR = "models"
TEMPLATE_DIR = "templates"
STRUC_DEF_TEMPLATE_NAME: str = "structure_definition_model.j2"
MODEL_TEMPLATE_NAME: str = "model_init.j2"

# FHIR
FHIR_VERSION_PACKAGE_URLS = {
    "R4": "https://hl7.org/fhir/R4/hl7.fhir.r4.core.tgz",
    "R4B": "https://hl7.org/fhir/R4B/hl7.fhir.r4b.core.tgz",
    "R5": "https://hl7.org/fhir/hl7.fhir.r5.core.tgz",
}
DOMAIN_RESOURCE_STRUC_DEF_URL = "http://hl7.org/fhir/StructureDefinition/DomainResource"

# RESOURCE TYPES
ACCOUNT = "Account"
ACTIVITYDEFINITION = "ActivityDefinition"
ADVERSEEVENT = "AdverseEvent"
ALLERGYINTOLERANCE = "AllergyIntolerance"
APPOINTMENT = "Appointment"
APPOINTMENTRESPONSE = "AppointmentResponse"
AUDITEVENT = "AuditEvent"
BASIC = "Basic"
BIOLOGICALLYDERIVEDPRODUCT = "BiologicallyDerivedProduct"
BODYSTRUCTURE = "BodyStructure"
CAPABILITYSTATEMENT = "CapabilityStatement"
CAREPLAN = "CarePlan"
CARETEAM = "CareTeam"
CATALOGENTRY = "CatalogEntry"
CHARGEITEM = "ChargeItem"
CHARGEITEMDEFINITION = "ChargeItemDefinition"
CLAIM = "Claim"
CLAIMRESPONSE = "ClaimResponse"
CLINICALIMPRESSION = "ClinicalImpression"
CODESYSTEM = "CodeSystem"
COMMUNICATION = "Communication"
COMMUNICATIONREQUEST = "CommunicationRequest"
COMPARTMENTDEFINITION = "CompartmentDefinition"
COMPOSITION = "Composition"
CONCEPTMAP = "ConceptMap"
CONDITION = "Condition"
CONSENT = "Consent"
CONTRACT = "Contract"
COVERAGE = "Coverage"
COVERAGEELIGIBILITYREQUEST = "CoverageEligibilityRequest"
COVERAGEELIGIBILITYRESPONSE = "CoverageEligibilityResponse"
DETECTEDISSUE = "DetectedIssue"
DEVICE = "Device"
DEVICEDEFINITION = "DeviceDefinition"
DEVICEMETRIC = "DeviceMetric"
DEVICEREQUEST = "DeviceRequest"
DEVICEUSESTATEMENT = "DeviceUseStatement"
DIAGNOSTICREPORT = "DiagnosticReport"
DOCUMENTMANIFEST = "DocumentManifest"
DOCUMENTREFERENCE = "DocumentReference"
EFFECTEVIDENCESYNTHESIS = "EffectEvidenceSynthesis"
ENCOUNTER = "Encounter"
ENDPOINT = "Endpoint"
ENROLLMENTREQUEST = "EnrollmentRequest"
ENROLLMENTRESPONSE = "EnrollmentResponse"
EPISODEOFCARE = "EpisodeOfCare"
EVENTDEFINITION = "EventDefinition"
EVIDENCE = "Evidence"
EVIDENCEVARIABLE = "EvidenceVariable"
EXAMPLESCENARIO = "ExampleScenario"
EXPLANATIONOFBENEFIT = "ExplanationOfBenefit"
FAMILYMEMBERHISTORY = "FamilyMemberHistory"
FLAG = "Flag"
GOAL = "Goal"
GRAPHDEFINITION = "GraphDefinition"
GROUP = "Group"
GUIDANCERESPONSE = "GuidanceResponse"
HEALTHCARESERVICE = "HealthcareService"
IMAGINGSTUDY = "ImagingStudy"
IMMUNIZATION = "Immunization"
IMMUNIZATIONEVALUATION = "ImmunizationEvaluation"
IMMUNIZATIONRECOMMENDATION = "ImmunizationRecommendation"
IMPLEMENTATIONGUIDE = "ImplementationGuide"
INSURANCEPLAN = "InsurancePlan"
INVOICE = "Invoice"
LIBRARY = "Library"
LINKAGE = "Linkage"
LIST = "List"
LOCATION = "Location"
MEASURE = "Measure"
MEASUREREPORT = "MeasureReport"
MEDIA = "Media"
MEDICATION = "Medication"
MEDICATIONADMINISTRATION = "MedicationAdministration"
MEDICATIONDISPENSE = "MedicationDispense"
MEDICATIONKNOWLEDGE = "MedicationKnowledge"
MEDICATIONREQUEST = "MedicationRequest"
MEDICATIONSTATEMENT = "MedicationStatement"
MEDICINALPRODUCT = "MedicinalProduct"
MEDICINALPRODUCTAUTHORIZATION = "MedicinalProductAuthorization"
MEDICINALPRODUCTCONTRAINDICATION = "MedicinalProductContraindication"
MEDICINALPRODUCTINDICATION = "MedicinalProductIndication"
MEDICINALPRODUCTINGREDIENT = "MedicinalProductIngredient"
MEDICINALPRODUCTINTERACTION = "MedicinalProductInteraction"
MEDICINALPRODUCTMANUFACTURED = "MedicinalProductManufactured"
MEDICINALPRODUCTPACKAGED = "MedicinalProductPackaged"
MEDICINALPRODUCTPHARMACEUTICAL = "MedicinalProductPharmaceutical"
MEDICINALPRODUCTUNDESIRABLEEFFECT = "MedicinalProductUndesirableEffect"
MESSAGEDEFINITION = "MessageDefinition"
MESSAGEHEADER = "MessageHeader"
MOLECULARSEQUENCE = "MolecularSequence"
NAMINGSYSTEM = "NamingSystem"
NUTRITIONORDER = "NutritionOrder"
OBSERVATION = "Observation"
OBSERVATIONDEFINITION = "ObservationDefinition"
OPERATIONDEFINITION = "OperationDefinition"
OPERATIONOUTCOME = "OperationOutcome"
ORGANIZATION = "Organization"
ORGANIZATIONAFFILIATION = "OrganizationAffiliation"
PATIENT = "Patient"
PAYMENTNOTICE = "PaymentNotice"
PAYMENTRECONCILIATION = "PaymentReconciliation"
PERSON = "Person"
PLANDEFINITION = "PlanDefinition"
PRACTITIONER = "Practitioner"
PRACTITIONERROLE = "PractitionerRole"
PROCEDURE = "Procedure"
PROVENANCE = "Provenance"
QUESTIONNAIRE = "Questionnaire"
QUESTIONNAIRERESPONSE = "QuestionnaireResponse"
RELATEDPERSON = "RelatedPerson"
REQUESTGROUP = "RequestGroup"
RESEARCHDEFINITION = "ResearchDefinition"
RESEARCHELEMENTDEFINITION = "ResearchElementDefinition"
RESEARCHSTUDY = "ResearchStudy"
RESEARCHSUBJECT = "ResearchSubject"
RESOURCE = "Resource"
RISKASSESSMENT = "RiskAssessment"
RISKEVIDENCESYNTHESIS = "RiskEvidenceSynthesis"
SCHEDULE = "Schedule"
SEARCHPARAMETER = "SearchParameter"
SERVICEREQUEST = "ServiceRequest"
SLOT = "Slot"
SPECIMEN = "Specimen"
SPECIMENDEFINITION = "SpecimenDefinition"
STRUCTUREDEFINITION = "StructureDefinition"
STRUCTUREMAP = "StructureMap"
SUBSCRIPTION = "Subscription"
SUBSTANCE = "Substance"
SUBSTANCENUCLEICACID = "SubstanceNucleicAcid"
SUBSTANCEPOLYMER = "SubstancePolymer"
SUBSTANCEPROTEIN = "SubstanceProtein"
SUBSTANCEREFERENCEINFORMATION = "SubstanceReferenceInformation"
SUBSTANCESOURCEMATERIAL = "SubstanceSourceMaterial"
SUBSTANCESPECIFICATION = "SubstanceSpecification"
SUPPLYDELIVERY = "SupplyDelivery"
SUPPLYREQUEST = "SupplyRequest"
TASK = "Task"
TERMINOLOGYCAPABILITIES = "TerminologyCapabilities"
TESTREPORT = "TestReport"
TESTSCRIPT = "TestScript"
VALUESET = "ValueSet"
VERIFICATIONRESULT = "VerificationResult"
VISIONPRESCRIPTION = "VisionPrescription"

# PYTHON
PYTHON_KEYWORDS = [
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]
FHIR_PRIMITIVES_TO_PYTHON_MAP = {
    "base64Binary": str,
    "boolean": bool,
    "canonical": str,
    "code": str,
    "date": str,
    "dateTime": str,
    "decimal": float,
    "id": str,
    "instant": str,
    "integer": int,
    "integer64": int,
    "markdown": str,
    "oid": str,
    "positiveInt": int,
    "string": str,
    "time": str,
    "unsignedInt": int,
    "uri": str,
    "url": str,
    "uuid": str,
    "xhtml": str,
}
FHIR_PRIMITIVE_EXPANSION_MAP = {
    "http://hl7.org/fhirpath/System.String": "string",
    "http://hl7.org/fhirpath/System.Boolean": "boolean",
    "http://hl7.org/fhirpath/System.Integer": "integer",
    "http://hl7.org/fhirpath/System.Decimal": "decimal",
    "http://hl7.org/fhirpath/System.DateTime": "dateTime",
    "http://hl7.org/fhirpath/System.Date": "date",
    "http://hl7.org/fhirpath/System.Time": "time",
}
