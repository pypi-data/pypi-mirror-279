"""Module to provide a class to make updates to an input Record

Class:
    BaseFieldConvertor

This class allows you to do a number of conversions on a record. This is
usually done prior to creating a new record from this existing record, thus
ensuring a well formatted record prior to processing.

Conditions can be included and conversions will only be executed if all
conditions comply.

Generic format in the rules_dict:
{ 'conversion_name': {
    'fieldname': <name of field that will be used for output and input of
                  the conversion. In some cases the input value will be taken
                  from a different field. This will be mentioned in the
                  description of the conversion. Ususally the input field
                  will the be defined by the values provided in the action
                  dict>,
    'conditions: {<condition name> : <condition value when needed>},
    'actions': [
        {<name action1>: <values for action1 when needed},
        {<name action2>: ....}
    ]
}

Availale conversion
    - remove_params_from_url:
        Returns the url without the request params
            'actions': [{'remove_params_from_url': None}

    - select_object_from_list:
        Selects the first object from a list that contains field with name
        `key` and value `value`:
            'actions': [{'select_object_from_list': [<key>, <value>]}

    - get_country_code_from_phone_nr:
        Returns the country code for a given phonenumber field:
            'actions': [{
                'get_country_code_from_phone_nr': <phonenumber_field_name>}]

    - days_ago_to_date:
        Returns the date of a given number of days ago:
            actions: [{ "days_ago_to_date": None }]

    - to_str:
        Returns the str represenation of given field:
            actions: [{ "to_str": None }]

    - to_lower_str
        Returns the lower case str represenation of given field:
            actions: [{ "to_lower_str": None }]

    - to_upper_str
        Returns the upper case str represenation of given field:
            actions: [{ "to_uppr_str": None }]

    - str_to_dict
        Converts a string into a dict if possible
            actions: [{ "str_to_dict": None }]

    - add_prefix
        adds a prefix string befor the string in the given fieldname:
            actions: [{ "add_prefix": 'String to be added' }]

    - add_postfix
        adds a postfix string after the string in the given fieldname:
            actions: [{ "add_postfix": 'String to be added' }]

    - add_value_from_field
        retrieves the value from a another field in the record and sets the
        fieldname to it, basically copying an existing field to a new field.
        Fielname to copy from can be nested
            actions: [{ "add_value_from_field": 'fieldname to copy from' }]

    - fixed_value
        sets given field name to a fixed value
            'actions': [{'fixed_value': <fixed value to be used>}]}

    - date_of_today
        sets given field name to teh date of today in format YYYY-MM_DD
            'actions': [{'date_of_today': None}]}

    - change_key_name_to
        renames the field name of given nested field to the given name
            'actions': [{'change_key_name_to': 'new_name'}]}

    - remove
        removes the field defined by the given (nested) field name
            'actions': [{'remove': None}]}

    - alpha3_to_iso3116_cc
        converts a alpha 3 country code to a iso3116 country code
            'actions': [{'alpha3_to_iso3116_cc': None}]}

    - divide_by
        divides a float or int by a given value
            'actions': [{'divide_by': 10}]}

"""

import json
from datetime import date, timedelta
from typing import Any, Optional, Union

import jmespath
import phonenumbers
from jmespath.exceptions import ParseError

from ...package_settings import BaseConvertorKeys, BaseRuleDict, EvaluateConditions
from .base_convertor_helpers import (
    DataFromHTMLSnippet,
    iso3116_from_alpha_3_country_code,
    normalize_string,
)

__all__ = ["BaseFieldConvertor"]


class BaseFieldConvertor:
    """
    Class to perform conversions on a given record and return the updated
    record

    args:
        record (dict): record that needs some conversion action
        conversion_rule (dict) :
            instructions about the conversion. Should at least have
                - fieldname -> which field will be converted
                - actions -> list of actions to be applied
                - conditions (optional) -> conditions required to
                                           run the conversion

    method to convert the record:
        - convert
            args: None
            returns: record (dict) -> the converted record
    """

    def convert_field(
        self, record: dict[str, Any], conversion_rule: BaseRuleDict
    ) -> dict:
        self.record = record
        self.conversion_rule = conversion_rule
        self.field_name = conversion_rule[BaseConvertorKeys.FIELDNAME]

        actions = self.conversion_rule[BaseConvertorKeys.ACTIONS] or {}
        if self.all_conditions_true():
            # loop over all actions
            for action_dict in actions:
                self.field_value = self._get_field(self.field_name)
                # remove any optional target_field from the action as the target_field
                # setting is not an action in itself
                optional_target_field = action_dict.pop(
                    BaseConvertorKeys.ACTIONTARGET, None
                )

                # retrieve single action and action value and execute
                [[action, action_value]] = action_dict.items()
                if action in dir(self):
                    field_value = getattr(self, action)(action_value)
                else:
                    raise NotImplementedError(f"Action {action}")

                # Set the target field of leave the used field_name as is if no
                # target field is defined.
                target_field = optional_target_field or self.field_name
                if action not in ["remove"]:
                    self.set_field_value(value=field_value, target_field=target_field)

        return self.record

    def _get_float_from_field_value(self) -> Optional[float]:
        value = self.field_value
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return None

        if not isinstance(value, (int, float)):
            return None

        return value

    def multiply_by(self, action_value: Union[float, int]) -> Optional[float]:
        """multiplies the given field by given value"""
        if not isinstance(action_value, (int, float)):
            raise TypeError(f"action_value {action_value} is not of type int or float")
        value_to_multiply = self._get_float_from_field_value()
        if value_to_multiply is None:
            return None
        return value_to_multiply * action_value

    def divide_by(self, action_value):
        """divides the given field by given value"""
        value_to_divide = self._get_float_from_field_value()
        if value_to_divide is None:
            return None
        return value_to_divide / action_value

    def join_fields(self, action_value: list) -> str:
        """Joins values from a list of fields."""
        field_values = [self._get_field(field_name) for field_name in action_value]
        return "".join(str(field_values))

    def alpha3_to_iso3116_cc(self, action_value):
        """converts a alpha 3 country code to a iso3116 country code"""
        field_value = self.field_value
        if not isinstance(field_value, str):
            raise TypeError(
                f"filed_value is of type `{type(field_value)}` "
                "but should be of type `str`"
            )
        return iso3116_from_alpha_3_country_code(field_value)

    def remove(self, action_value):
        """change remove a (nested) field"""
        self.pop_nested_field(self.field_name)
        return None

    def list_to_dict(self, action_value) -> dict:
        """turns [[a,b] [c,d]] into {a:b, c:d}"""
        return (
            {}
            if not self.field_value
            else {
                normalize_string(item[0]).replace(" ", "_"): normalize_string(item[1])
                for item in self.field_value
            }
        )

    def change_key_name_to(self, action_value):
        """change the field name of a (nested) field"""
        value = self.pop_nested_field(self.field_name)
        self.field_name = action_value
        return value

    def date_of_today(self, action_value):
        """returns date of today in format  YYYY-MM-DD"""
        return date.strftime(date.today(), "%Y-%m-%d")

    def fixed_value(self, action_value):
        """returns the fixed value defined in the action dict"""
        return action_value

    def insert_key(self, action_value):
        """Returns a retrieved from a field in the record

        fieldname to retrieve from is defined in the action dict
        """
        return {action_value: self.field_value}

    def add_value_from_field(self, action_value):
        """Returns a retrieved from a field in the record

        fieldname to retrieve from is defined in the action dict
        """
        return self._get_field(action_value)

    def add_key_value_from_field(self, action_value):
        """
        Returns a dict with key value pairs where key is given
        and value is the value for that key in the record
        """
        if not isinstance(action_value, list):
            action_value = [action_value]

        return {key: self._get_field(key) for key in action_value}

    def add_data_from_dict(self, action_value):
        """
        Return a an existing dict with all the entries from a second dict
        added
        """
        if self.field_value:
            result = self.field_value.copy()
        else:
            result = {}

        if update_dict := self._get_field(action_value):
            result.update(update_dict)
        return result

    def add_data_from_list_of_dict(self, action_value) -> dict:
        """
        Return a dict with key, value pairs from a list of dicts.
        [{'key': 'a', 'value': 'b'}, {'key': 'c', 'value': 'd'}] =>
        {'a': 'b', 'c': 'd'}
        """
        if not self.field_value:
            return {}

        key_key = action_value.get("key_key")
        value_key = action_value.get("value_key")
        if not (key_key and value_key):
            raise KeyError(f"key_key {key_key} or value_key {value_key} missing")
        result = {}
        for entry in self.field_value:
            key = entry.get(key_key)
            value = entry.get(value_key)
            result.update({key: value})
        return result

    def convert_data_from_html_fragment_to_list(self, action_value) -> list:
        """Returns a list of data elemens found in html snippet."""
        if not self.field_value:
            return []

        return DataFromHTMLSnippet().to_list(self.field_value)

    def add_prefix(self, action_value):
        """return the string with prefix value"""
        return str(action_value) + str(self.field_value)

    def add_postfix(self, action_value):
        """return the string with postfix value"""
        return str(self.field_value) + str(action_value)

    def str_to_dict(self, action_value):
        """returns the string version of provided attribute"""
        if not self.field_value:
            return dict()
        try:
            return json.loads(self.field_value)
        except json.decoder.JSONDecodeError:
            return dict()

    def to_str(self, action_value):
        """returns the string version of provided attribute"""
        return str(self.field_value)

    def to_lower_str(self, action_value):
        """returns the string version of provided attribute in lowercase"""
        return str(self.field_value).lower()

    def to_upper_str(self, action_value):
        """returns the string version of provided attribute in uppercase"""
        return str(self.field_value).upper()

    def days_ago_to_date(self, action_value) -> Optional[str]:
        """returns the date of a given number of days ago

        date is returned in format YYYY-MM-DD
        """
        if not self.field_value:
            return None

        try:
            actual_date = date.today() - timedelta(days=int(self.field_value))
        except ValueError:
            return None

        return date.strftime(actual_date, "%Y-%m-%d")

    def remove_params_from_url(self, action_value):
        """removes all query parameters from a url"""
        if isinstance(self.field_value, str):
            return self.field_value.split("?")[0]

    def select_object_from_list(self, action_value: tuple[str, Any]):
        """
        selects an object from a list if specific key in the object equals a
        given value
        """
        key, value = action_value
        try:
            for obj in self.field_value or []:
                if self._get_field(key, obj) == value:
                    return obj
        except TypeError:
            # in case field_value is None
            pass

        return {}

    def get_country_code_from_phone_nr(self, action_value):
        phone_nr = self._get_field(action_value)
        phone_object = None
        if phone_nr:
            try:
                phone_object = phonenumbers.parse(phone_nr)
            except phonenumbers.phonenumberutil.NumberParseException:
                return None

            if phone_object and phone_object.country_code:
                return phonenumbers.region_codes_for_country_code(
                    phone_object.country_code
                )[0]
            else:
                # ensure the field is empty if no country code can be found
                return None

    def all_conditions_true(self) -> bool:
        """Returns True if all provided conditions are satisfied"""
        if conditions := self.conversion_rule.get(BaseConvertorKeys.CONDITION):
            return EvaluateConditions(
                provided_conditions=conditions, value=self.field_value
            ).evaluate()

        # when no conditions were provided the conversion needs to
        # continue
        return True

    def set_field_value(self, value, target_field: str):
        """
        sets a value to a nested field in the record.

        args:
            - value (str)
                value that will be assigned to the last fieldname in
                field_names

        returns none

        """
        nested_field_names = target_field.split(".")
        first_field_name = nested_field_names.pop(0)
        # if it is not a nested field update first level field name and return
        if not nested_field_names:
            self.record.update({first_field_name: value})
            return

        # if it is a nested field capture the fieldname that needs to be
        # updated (i.e. the last field name in thel list).
        last_field = nested_field_names.pop()

        # find the nested dict in whih the last_field is a (nested) key
        field_value = self.record.get(first_field_name, None)
        if field_value is None:
            return None

        # with the list of nested field name we dig deeper into the
        # structure to get to the dict containing the last field name
        for field_name in nested_field_names:
            field_value = field_value.get(field_name, {})

        # update that value of `last_field` in that dict
        if field_value is not None:
            field_value.update({last_field: value})

    def pop_nested_field(self, field):
        """
        removes a value to a nested field in the record.

        args:
            field (str): nested field name (ex. key.subkey1.subkey2 etc)

        returns
            - the content of the popped key
            - None if this field is not found
        """
        nested_field_names = field.split(".")
        first_field_name = nested_field_names.pop(0)
        # if it is not a nested field update first level field name and return
        if not nested_field_names:
            return self.record.pop(first_field_name, None)

        # if it is a nested field capture the fieldname that needs to be
        # popped (i.e. the last field name in the list).
        last_field = nested_field_names.pop()

        # find the nested dict in which the last_field is a (nested) key
        if not (field_value := self.record.get(first_field_name, None)):
            return None

        # with the list of nested field name we dig deeper into the
        # structure to get to the dict containing the last field name
        for field_name in nested_field_names:
            field_value = field_value.get(field_name, {})

        # update that value of `last_field` in that dict
        if field_value and isinstance(field_value, dict):
            return field_value.pop(last_field, None)

    def _get_field(self, key: str, rec: Optional[dict] = None):
        """
        returns a value from a nested field in the record.
        nested field names should be seperated by `__`
        """
        # initially used '__' as key seperator but migrating to using
        # `.` as seperator. This line to allow old conversion yaml files
        # not to fail
        record = rec or self.record
        if key:
            nested_field_names = key.replace("__", ".")
            # key elemenets in nested keys are surround with "". For exmample
            # key.example-1 becomes "key"."example-1".
            # Needed for jmespath can hande special characters in the keys
            nested_keys = nested_field_names.split(".")
            nested_key = ".".join(['"' + key + '"' for key in nested_keys])
            try:
                return jmespath.search(nested_key, record)
            except ParseError:
                pass

        return None
