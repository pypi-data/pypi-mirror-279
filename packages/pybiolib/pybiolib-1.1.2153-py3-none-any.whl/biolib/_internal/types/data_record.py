from .typing import Dict, List, Optional, TypedDict


class DataRecordValidationRuleDict(TypedDict):
    path: str
    type: str
    rule: Dict


class DataRecordTypeDict(TypedDict):
    name: str
    validation_rules: List[Dict]


class DataRecordSlimDict(TypedDict):
    pass


class DataRecordDetailedDict(DataRecordSlimDict):
    type: Optional[DataRecordTypeDict]
