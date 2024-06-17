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

from typing import Any, Optional

from record_convertor.field_convertors.base_convertor.base_convertor_helpers import (
    DataFromHTMLSnippet,
    normalize_string,
)

from .base_convertor_helpers import _BaseConvertorClass

__all__ = ["DataStructureConversions"]


class DataStructureConversions(_BaseConvertorClass):
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
