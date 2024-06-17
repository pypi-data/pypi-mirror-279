from dataclasses import Field
from typing import Any, ClassVar, Protocol

from .package_types import BaseRuleDict, FormatDateRuleDict, RulesDict

__all__ = [
    "RecordConvertorProtocol",
    "FieldConvertorProtocol",
    "DateFormatProtocol",
    "DataclassInstance",
]


class RecordConvertorProtocol(Protocol):
    def convert(self, record: dict) -> dict: ...

    def get_record_convertor_copy_with_new_rules(
        self, new_rules: RulesDict
    ) -> "RecordConvertorProtocol": ...


class FieldConvertorProtocol(Protocol):
    def convert_field(self, record: dict, conversion_rule: BaseRuleDict) -> dict: ...


class DateFormatProtocol(Protocol):
    def format_date_field(
        self, record: dict, conversion_rule: FormatDateRuleDict
    ) -> dict: ...


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]
