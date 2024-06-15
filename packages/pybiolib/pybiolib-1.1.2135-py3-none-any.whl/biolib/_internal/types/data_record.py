from .typing import Dict, List, TypedDict


class DataRecordValidationRuleDict(TypedDict):
    path: str
    type: str
    rule: Dict


class DataRecordTypeDict(TypedDict):
    name: str
    validation_rules: List[Dict]
