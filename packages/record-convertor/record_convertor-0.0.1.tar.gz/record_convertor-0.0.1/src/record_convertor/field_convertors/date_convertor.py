"""Module to provide DateFieldConvertor class.

This class allows you to do a number of date conversions on a record. This is
usually done prior to creating a new record from this existing record, thus
ensuring a well formatted record prior to processing.

Conditions can be included and conversions will only be executed if all
conditions comply.

Generic format in the rules_dict:
{
    'date_field': <name of date field that needs to be converted>,
    'conditions: {<condition name> : <condition value when needed>},
    'format': <format name that is used in date_field>
}

Availale date formats (from which to convert to YYYY-MM-DD)
    - DD-MM-YYYY
    - DD.MM.YYYY
    - YYYY_MM_DD
    - YYYY_MM_DD:Time
    - UNIX_DT_STAMP
    - YYYY-MM-DD
"""

from datetime import datetime
from typing import Dict, Literal

import jmespath
from jmespath.exceptions import ParseError

from ..package_settings import (
    EvaluateConditions,
    FormatDateConvKeys,
    FormatDateRuleDict,
    FormatNotImplementedException,
)

__all__ = ["DateFieldConvertor"]


DATE_METHOD_NAME = Literal[
    "day_month_year",
    "day_month_year_dotted",
    "year_month_day",
    "year_month_day_time",
    "unix_dt_stamp",
    "year_month_date",
]


CONV_METHODS: Dict[str, DATE_METHOD_NAME] = {
    "DD-MM-YYYY": "day_month_year",
    "DD.MM.YYYY": "day_month_year_dotted",
    "YYYY_MM_DD": "year_month_day",
    "YYYY_MM_DD:Time": "year_month_day_time",
    "UNIX_DT_STAMP": "unix_dt_stamp",
    "YYYY-MM-DD": "year_month_date",
}


class DateFieldConvertor:
    """
    A class dedicated to converting date fields within records according to specified
    conversion rules.

    This class applies a series of predefined actions to transform the format of date
    fields in a given record. It supports both direct and nested fields within the
    record's dictionary structure. The conversion process is contingent upon the
    fulfillment of specified conditions, allowing for versatile date field manipulation.

    Parameters:
    - record (Dict):
        The record containing the date field to be converted. This argument expects a
        dictionary.
    - conversion_rule (FormatDateRuleDict):
        A dictionary specifying the conversion rules. The rules dictionary should
        include the following keys:
            - 'fieldname':
                The name of the field to be converted.
            - 'format':
                The name of the input format.
            - 'conditions' (optional):
                Conditions that must be met for the conversion to proceed.
                If not provided, the conversion is assumed to be unconditional.

    Available Conversions:
    - unix_dt_stamp: Converts Unix timestamp (string) to 'YYYY-MM-DD'.
    - year_month_date: Converts 'YYYY-MM-DD' to 'YYYY-MM-DD' (identity transformation).
    - year_month_day_time: Extracts 'YYYY-MM-DD' from 'YYYY-MM-DD:time'.
    - year_month_day: Converts 'YYYY_MM_DD' to 'YYYY-MM-DD'.
    - day_month_year: Converts 'DD-MM-YYYY' to 'YYYY-MM-DD'.
    - day_month_year_dotted: Converts 'DD.MM.YYYY' to 'YYYY-MM-DD'.

    Methods:
    - convert_date:
        Converts the date field in the record to the 'YYYY-MM-DD' format based on the
        provided conversion rule.
    - all_conditions_true:
        Evaluates if all specified conditions are met for the given date field value.
    - update_field_with_date:
        Updates the specified field in the record with the new date format.
    - _get_field:
        Retrieves the value from a potentially nested field within the record.

    The conversion process supports handling both flat and nested dictionary structures,
    with the ability to navigate through nested fields specified by a dot-separated
    path.

    Example:
        To convert a date field within a record, instantiate the `DateFieldConvertor`
        with the target record and a rule dict outlining the conversion specifics.
        Then, call the `convert_date` method to apply the conversion.
    """

    def format_date_field(
        self, record: dict, conversion_rule: FormatDateRuleDict
    ) -> dict:
        """
        Method to convert a date field in a record into into a
        'YYYY-MM-DD' string date format.

        Args:
            - record (Dict):
                The record containing the date field to be converted.
            - conversion_rule (RuleDict):
                The conversion rules specifying the fieldname, actions, and optional
                conditions.
        """
        self._record = record
        self.date_field_key_name: str = self._get_date_field_key_name(conversion_rule)
        date_formatter_method = self._get_date_formatter_method_name(conversion_rule)
        date_field_value = self._get_field()

        if date_field_value and self.all_conditions_true(
            date_field_value, conversion_rule
        ):
            date_in_new_format = getattr(self, date_formatter_method)(date_field_value)
            self.update_field_with_date(date_in_new_format)

        return self._record

    @staticmethod
    def unix_dt_stamp(unix_dt_stamp: str) -> str:
        """convert Unix date time stamp to YYYY-MM-DD"""
        datetime_date = datetime.fromtimestamp(int(unix_dt_stamp))
        return datetime_date.strftime("%Y-%m-%d")

    @staticmethod
    def year_month_date(date_str: str) -> str:
        """convert YYYY-MM-DD to YYYY-MM-DD"""
        return date_str

    @staticmethod
    def year_month_day_time(date_str: str) -> str:
        """convert YYYY-MM-DD:time to YYYY-MM-DD"""
        return date_str[0:10]

    @staticmethod
    def year_month_day(date_str: str) -> str:
        """convert YYYY-MM-DD to YYYY-MM-DD"""
        datetime_date = datetime.strptime(date_str, "%Y_%m_%d")
        return datetime_date.strftime("%Y-%m-%d")

    @staticmethod
    def day_month_year(date_str: str) -> str:
        """convert DD-MM-YYYY to YYYY-MM-DD"""
        datetime_date = datetime.strptime(date_str, "%d-%m-%Y")
        return datetime_date.strftime("%Y-%m-%d")

    @staticmethod
    def day_month_year_dotted(date_str: str) -> str:
        """convert DD.MM.YYYY to YYYY-MM-DD"""
        datetime_date = datetime.strptime(date_str, "%d.%m.%Y")
        return datetime_date.strftime("%Y-%m-%d")

    def all_conditions_true(
        self, date_field_value: str, conversion_rule: FormatDateRuleDict
    ) -> bool:
        """Returns True if all provided conditions are satisfied."""
        conditions = conversion_rule.get(FormatDateConvKeys.CONDITION)
        if not conditions:
            return True

        return EvaluateConditions(
            provided_conditions=conditions, value=date_field_value
        ).evaluate()

    def update_field_with_date(self, date_in_new_format: str) -> None:
        """
        updates the datefield in the record to date_in_new_format

        args:
            - date_in_new_format (str)
        """
        nested_field_names = self.date_field_key_name.split(".")
        first_field_name = nested_field_names.pop(0)
        # if it is not a nested field update first level field name and return
        if not nested_field_names:
            self._record.update({first_field_name: date_in_new_format})
            return

        # if it is a nested field capture the fieldname that needs to be
        # updated (i.e. the last field name in thel list).
        last_field = nested_field_names.pop()

        # find the nested dict in whih the last_field is a (nested) key
        field_value = self._record.get(first_field_name, None)
        if field_value is None:
            return None

        # with the list of nested field name we dig deeper into the
        # structure to get to the dict containing the last field name
        for field_name in nested_field_names:
            field_value = field_value.get(field_name, {})

        # update that value of `last_field` in that dict
        if field_value is not None:
            field_value.update({last_field: date_in_new_format})

    @staticmethod
    def _get_date_field_key_name(rule: FormatDateRuleDict) -> str:
        date_field_in_record = rule[FormatDateConvKeys.DATEFIELD]
        return date_field_in_record.replace("__", ".")
        # initially used '__' as key seperator but migrating to using
        # `.` as seperator. This line to allow old conversion yaml files
        # not to fail

    def _get_field(self) -> str:
        """
        returns a value from a nested field in the record.
        if value is not found or can not be converted into a string an empty
        string is returned
        """
        # key elemenets in nested keys are surround with "". For exmample
        # key.example-1 becomes "key"."example-1".
        # Needed for jmespath can hande special characters in the keys
        nested_field_names = self.date_field_key_name.split(".")
        nested_key = ".".join(['"' + name + '"' for name in nested_field_names])
        try:
            date_value_from_record = jmespath.search(nested_key, self._record)
        except ParseError:
            return ""

        return str(date_value_from_record) if date_value_from_record else ""

    @staticmethod
    def _get_date_formatter_method_name(
        rule: FormatDateRuleDict,
    ) -> DATE_METHOD_NAME:
        format = rule[FormatDateConvKeys.FORMAT]

        date_formatter_method_name = CONV_METHODS.get(format)
        if not date_formatter_method_name:
            raise FormatNotImplementedException(format)

        return date_formatter_method_name
