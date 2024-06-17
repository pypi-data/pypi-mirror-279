"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       provide rules.

usage:
>>> converted_record: dict = \
>>>     RecordConvertor(rules: Rules).convert(record: dict)
"""

from copy import copy
from typing import Any, Optional

import jmespath
from jmespath.exceptions import ParseError

from record_convertor.command_processor import ProcessCommand
from record_convertor.dataclass_processor import DataClassProcessor

from .field_convertors import BaseFieldConvertor, DateFieldConvertor
from .package_settings import (
    DataclassInstance,
    DateFormatProtocol,
    EvaluateConditions,
    FieldConvertorProtocol,
    RecConvKeys,
    RulesDict,
    SkipConvKeys,
    SkipRuleDict,
    keys_in_lower_case,
)
from .package_settings.conditions.condition_settings.condition_types import (
    ConditionsDict,
)
from .rules_generator import RulesFromDict, RulesFromYAML  # NOQA: F401


class RecordConvertor:
    RULE_CLASS = RulesFromYAML
    EVALUATE_CLASS = EvaluateConditions
    DATA_CLASS_PROCESSOR: DataClassProcessor = DataClassProcessor()
    KEYS_IN_LOWER_CASE: bool = False
    DEFAULT_VALUE: dict = {}
    DEFAULT_FIELD_CONVERTOR_CLASS: type[FieldConvertorProtocol] = BaseFieldConvertor
    DEFAULT_DATE_FORMAT_CLASS: type[DateFormatProtocol] = DateFieldConvertor
    COMMAND_CLASS: type[ProcessCommand] = ProcessCommand
    _stored_copy: Optional["RecordConvertor"] = None

    def __init__(
        self,
        rule_source: str,
        field_convertor: Optional[type[FieldConvertorProtocol]] = None,
        date_formatter: Optional[type[DateFormatProtocol]] = None,
        data_classes: Optional[list[type[DataclassInstance]]] = None,
        command_class: Optional[type[ProcessCommand]] = None,
    ):
        self._rules = self.RULE_CLASS(rule_source=rule_source).rules
        # set instance of given or default field convertor class
        self._field_convertor: FieldConvertorProtocol = (
            field_convertor or self.DEFAULT_FIELD_CONVERTOR_CLASS
        )()
        # set instance of given or default date format class
        self._date_formatter: DateFormatProtocol = (
            date_formatter or self.DEFAULT_DATE_FORMAT_CLASS
        )()
        # set the dataclasses attribute as a dict with dataclass name as key and data
        # the dataclass itself as value
        dataclasses = data_classes or []
        self.DATA_CLASS_PROCESSOR.register_data_classes(dataclasses=dataclasses)
        self._command_class = command_class or self.COMMAND_CLASS

    def convert(self, record: dict) -> dict:
        """
        Primary public method to run the actual conversion of the record.

        Args:
            record (dict): input record

        Returns:
            dict: converted record
        """
        output_record: dict = {}
        self._input_record = (
            keys_in_lower_case(record) if self.KEYS_IN_LOWER_CASE else record
        )

        # process all rules (and nested rules)
        for rule in self._rules.items():
            # check if the rule determines that the given record can be skipped
            # if so return default value
            if self._skip_this_record(rule):
                return self.DEFAULT_VALUE

            # check if the rule requires a change on the input record to be done
            # if rule is an input record update rule then proceed with the next rule.
            if self._change_field_in_input_record_if_required(rule=rule):
                continue

            # check if the rule requires a change on the input record to be done
            # if rule is an input record update rule then proceed with the next rule.
            if self._is_dataclass_rule(rule=rule):
                _, dataclass_rule = rule
                return self.DATA_CLASS_PROCESSOR.data_from_dataclass(
                    record=self._input_record,
                    rules=dataclass_rule,  # type: ignore
                    record_convertor=self._copy,
                )

            # All possible command options have been excluded so rule must be a key
            # definition for the new record:
            if self._is_command_rule(rule=rule):
                command, command_args = rule
                return self._command_class(
                    record=self._input_record,
                    process_command=command,
                    process_args=command_args,  # type: ignore
                    record_convertor=self._copy,
                ).get_value()

            output_record_key, output_record_value = rule

            if isinstance(output_record_value, dict):
                nested_record_covertor = self.get_record_convertor_copy_with_new_rules(
                    output_record_value
                )
                output_record[output_record_key] = nested_record_covertor.convert(
                    record=self._input_record
                )
                continue

            if isinstance(output_record_value, str):
                # setup with None needed to allow result_for_key to be 0
                result_for_output_record_key = self._get_field(output_record_value)
                if result_for_output_record_key is not None:
                    output_record[output_record_key] = result_for_output_record_key
                continue

        return output_record

    def get_record_convertor_copy_with_new_rules(
        self, new_rules: RulesDict
    ) -> "RecordConvertor":
        """
        Return a copy of the current record convertor instance with new rules.
        """
        new_record_convertor = self._copy
        new_record_convertor._rules = new_rules
        return new_record_convertor

    @property
    def _copy(self) -> "RecordConvertor":
        # prevent from creating class copy everytime a _copy method is called
        # by storing the first copy in the _stored_copy attribute
        if not self._stored_copy:
            self._stored_copy = copy(self)
        return self._stored_copy

    def _change_field_in_input_record_if_required(self, rule: tuple) -> bool:
        """
        Checks if input record needs to be updated based upon the given.
        If so update is performed.

        Returns True if the rule is an input record update rule and false otherwise.
        """
        # check if the rule triggers a field conversion in the input record
        if self._convert_field_rule(rule):
            _, rule_dict = rule
            self._input_record = self._field_convertor.convert_field(
                record=self._input_record, conversion_rule=rule_dict
            )
            return True

        # check if the rule triggers a field date conversion in the input record
        if self._format_date_rule(rule):
            _, rule_dict = rule
            self._input_record = self._date_formatter.format_date_field(
                record=self._input_record, conversion_rule=rule_dict
            )
            return True

        return False

    def _convert_field_rule(self, rule: tuple) -> bool:
        rule_key, _ = rule
        return "$convert" in rule_key

    def _format_date_rule(self, rule: tuple) -> bool:
        rule_key, _ = rule
        return "$format_date" in rule_key

    def _is_dataclass_rule(self, rule: tuple) -> bool:
        rule_key, _ = rule
        return "$dataclass" in rule_key

    def _is_command_rule(self, rule: tuple) -> bool:
        rule_key, _ = rule
        return rule_key[0] == "$"

    def _skip_this_record(self, rule: tuple) -> bool:
        rule_key, rule_value = rule
        if not rule_key.lower() == RecConvKeys.SKIP:
            return False
        skip_rule: SkipRuleDict = rule_value
        conditions: Optional[ConditionsDict] = skip_rule[SkipConvKeys.CONDITION]
        fieldname: Optional[str] = skip_rule.get(SkipConvKeys.FIELDNAME)
        field_value = self._get_field(fieldname)

        return self.EVALUATE_CLASS(conditions, field_value).evaluate()

    def _get_field(self, key: Optional[str]) -> Any:
        if key:
            # key elemenets in nested keys are surround with "". For exmample
            # key.example-1 becomes "key"."example-1".
            # Needed for jmespath can hande special characters in the keys
            nested_keys = key.split(".")
            nested_key = ".".join(['"' + key + '"' for key in nested_keys])
            try:
                return jmespath.search(nested_key, self._input_record)
            except ParseError:
                pass

        return None


class RecordConvertorWithRulesDict(RecordConvertor):
    RULE_CLASS = RulesFromDict

    def __init__(
        self,
        rule_dict: dict,
        field_convertor: Optional[type[FieldConvertorProtocol]] = None,
        date_formatter: Optional[type[DateFormatProtocol]] = None,
        data_classes: Optional[list[type[DataclassInstance]]] = None,
        command_class: Optional[type[ProcessCommand]] = None,
    ):
        self._rules = self.RULE_CLASS(rule_source=rule_dict).rules
        # set instance of given or default field convertor class
        self._field_convertor: FieldConvertorProtocol = (
            field_convertor or self.DEFAULT_FIELD_CONVERTOR_CLASS
        )()
        # set instance of given or default date format class
        self._date_formatter: DateFormatProtocol = (
            date_formatter or self.DEFAULT_DATE_FORMAT_CLASS
        )()
        # set the dataclasses attribute as a dict with dataclass name as key and data
        # the dataclass itself as value
        dataclasses = data_classes or []
        self.DATA_CLASS_PROCESSOR.register_data_classes(dataclasses=dataclasses)
        self._command_class = command_class or self.COMMAND_CLASS