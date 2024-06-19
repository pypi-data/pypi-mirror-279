"""metadata for imported datasets, containe the protected attributes
and the privileged classes
"""
ADULT_METADATA = {
    "protected_attributes": ["sex", "race"],
    "privileged_classes": {"sex": "Male", "race": "White"}
}

BANK_MARKETING_METADATA = {
    "protected_attributes": ["age"],
    "privileged_classes": {"age": "x>25"}
}

KDD_CENSUS_METADATA = {
    "protected_attributes": ["sex", "race"],
    "privileged_classes": {"sex": "Male", "race": "White"}
}

ACS_METADATA = {
    "protected_attributes": ["SEX", "RAC1P"],
    "privileged_classes": {"SEX": "Male", "RAC1P": "White"}
}
