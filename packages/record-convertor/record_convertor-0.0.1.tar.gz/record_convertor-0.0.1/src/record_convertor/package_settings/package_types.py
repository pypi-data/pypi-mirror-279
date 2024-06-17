from typing import Literal, Optional, TypedDict, Union

from .conditions import ConditionsDict

__all__ = [
    "RecConvKeys",
    "BaseRuleDict",
    "RulesDict",
    "BaseConvertorKeys",
    "FormatDateRuleDict",
    "FormatDateConvKeys",
    "SkipConvKeys",
    "SkipRuleDict",
    "DataClassRuleKeys",
    "DataClassRuleDict",
]


class RecConvKeys:
    SKIP: Literal["$skip"] = "$skip"
    CONVERT: Literal["$convert"] = "$convert"


class BaseConvertorKeys:
    CONDITION: Literal["condition"] = "condition"
    FIELDNAME: Literal["fieldname"] = "fieldname"
    ACTIONS: Literal["actions"] = "actions"
    ACTIONTYPE: Literal["action_type"] = "action_type"
    ACTIONVALUE: Literal["action_value"] = "action_value"
    ACTIONTARGET: Literal["target_field_name"] = "target_field_name"


class FormatDateConvKeys:
    CONDITION: Literal["condition"] = "condition"
    FORMAT: Literal["format"] = "format"
    DATEFIELD: Literal["date_field"] = "date_field"


class SkipConvKeys:
    CONDITION: Literal["condition"] = "condition"
    FIELDNAME: Literal["fieldname"] = "fieldname"


class DataClassRuleKeys:
    NAME: Literal["data_class_name"] = "data_class_name"
    RECORD_CONVERSION_ARGUMENTS: Literal["params"] = "params"
    METHODS: Literal["methods"] = "methods"


class BaseRuleDict(TypedDict):
    condition: Optional[ConditionsDict]
    format: Optional[str]  # used by date convertor
    fieldname: str
    actions: Optional[dict]
    action_type: Optional[str]  # tbd if these are still needed
    action_value: Union[str, dict]  # tbd if these are still needed


class FormatDateRuleDict(TypedDict):
    condition: Optional[ConditionsDict]
    format: str
    date_field: str


class SkipRuleDict(TypedDict):
    condition: ConditionsDict
    fieldname: str


class DataClassRuleDict(TypedDict):
    data_class_name: str
    params: dict
    methods: list[dict]


RulesDict = Union[
    BaseRuleDict,
    FormatDateRuleDict,
    SkipRuleDict,
    DataClassRuleDict,
    dict[
        str,
        Union[
            str,
            dict,
            BaseRuleDict,
            FormatDateRuleDict,
            SkipRuleDict,
            DataClassRuleDict,
        ],
    ],
]
