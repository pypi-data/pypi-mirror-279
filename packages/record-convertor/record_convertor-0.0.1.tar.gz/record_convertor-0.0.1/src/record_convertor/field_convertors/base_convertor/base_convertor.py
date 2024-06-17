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

from .data_structure_conversions import DataStructureConversions
from .generic_conversions import GenericConversions
from .in_place_basic_conversions import InPlaceBasicConversions
from .key_values import KeyValueConversions

__all__ = ["BaseFieldConvertor"]


class BaseFieldConvertor(
    DataStructureConversions,
    GenericConversions,
    InPlaceBasicConversions,
    KeyValueConversions,
): ...  # NOQA: E701
