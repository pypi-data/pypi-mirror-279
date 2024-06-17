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

import phonenumbers

from record_convertor.field_convertors.base_convertor.base_convertor_helpers import (
    iso3116_from_alpha_3_country_code,
)

from .base_convertor_helpers import _BaseConvertorClass

__all__ = ["GenericConversions"]


class GenericConversions(_BaseConvertorClass):
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

    def remove(self, action_value):
        """change remove a (nested) field"""
        self.pop_nested_field(self.field_name)
        return None

    def alpha3_to_iso3116_cc(self, action_value):
        """converts a alpha 3 country code to a iso3116 country code"""
        field_value = self.field_value
        if not isinstance(field_value, str):
            raise TypeError(
                f"filed_value is of type `{type(field_value)}` "
                "but should be of type `str`"
            )
        return iso3116_from_alpha_3_country_code(field_value)
