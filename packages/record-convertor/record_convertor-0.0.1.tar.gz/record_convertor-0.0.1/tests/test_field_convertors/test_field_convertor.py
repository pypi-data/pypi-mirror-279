"""Module to test the field converter class from the record convertor module"""

from copy import deepcopy
from datetime import date, datetime, timedelta

import pytest
from data.data_field_convertor_tests import (
    BASE_PARAMS_SELECT_FROM_LIST,
    PARAMS_ADD_DATA_FROM_DICT,
    PARAMS_ADD_KEY_VALUE_FROM_FIELD,
    PARAMS_ADD_KEY_VALUE_FROM_FIELD2,
    PARAMS_ADD_VALUE_FROM_FIELD,
    PARAMS_ADD_VALUE_FROM_NETSED_FIELD,
    PARAMS_ALPHA3_TO_ISO3116,
    PARAMS_CHANGE_KEY_NAME,
    PARAMS_CHANGE_KEY_NAME_NESTED,
    PARAMS_COUNTRY_CODE_FROM_INVALID_PHONE_NUMBER,
    PARAMS_COUNTRY_CODE_FROM_PHONE_NUMBER,
    PARAMS_DATE_OF_TODAY,
    PARAMS_DAYS_AGO_TO_DATE,
    PARAMS_DAYS_AGO_TO_DATE_INVALID,
    PARAMS_DIVIDE_BY,
    PARAMS_DIVIDE_BY_STR,
    PARAMS_DIVIDE_STR,
    PARAMS_FIXED_VALUE,
    PARAMS_INSERT_KEY,
    PARAMS_INVALID_STR_TO_DICT,
    PARAMS_LIST_TO_DICT,
    PARAMS_MULTIPLY_BY,
    PARAMS_MULTIPLY_BY_STR,
    PARAMS_MULTIPLY_STR,
    PARAMS_POST_FIX,
    PARAMS_PRE_FIX,
    PARAMS_REMOVE,
    PARAMS_REMOVE_NESTED_FIELD,
    PARAMS_SELECT_FROM_LIST_VALUE_NOT_FOUND,
    PARAMS_SELECT_FROM_LIST_WITH_NO_LIST,
    PARAMS_SELECT_FROM_LIST_WITH_NON_DICT_ENTRIES,
    PARAMS_STR_TO_DICT,
    PARAMS_TO_LOWER_STR,
    PARAMS_TO_STR,
    PARAMS_TO_UPPER_STR,
    URL_PARAMS,
    URL_PARAMS_WITH_CONDITION,
)

from record_convertor.field_convertors import BaseFieldConvertor

convertor = BaseFieldConvertor()


def test_remove_params_from_url_conversion_1():
    """test request params are removed from url"""
    converted_record = convertor.convert_field(**deepcopy(URL_PARAMS))
    assert converted_record["url"] == "www.test.com/"


def test_convert_condition_met():
    """test conversion is exectued when given condition is met"""
    converted_record = convertor.convert_field(**deepcopy(URL_PARAMS_WITH_CONDITION))
    assert converted_record["url"] == "www.test.com/"


def test_convert_condition_not_met():
    """test is_a_str method evaluates to True with a string as value"""
    convertor_params = deepcopy(URL_PARAMS_WITH_CONDITION)
    convertor_params["conversion_rule"]["condition"] = {"equals": "other str"}
    converted_record = convertor.convert_field(**convertor_params)
    assert not (converted_record["url"] == "www.test.com/")


def test_select_from_list():
    """test selecting value from list succesfull"""
    converted_record = convertor.convert_field(**deepcopy(BASE_PARAMS_SELECT_FROM_LIST))
    assert converted_record["list_key_name"] == {"item2": 2, "selector": 2}


def test_select_from_list_when_value_not_found():
    """test selecting value from list returns none when value not found"""
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_SELECT_FROM_LIST_VALUE_NOT_FOUND)
    )
    assert converted_record["list_key_name"] == {}


def test_select_from_list_with_non_dict_entries():
    """test selecting value from list returns none when value not found"""
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_SELECT_FROM_LIST_WITH_NON_DICT_ENTRIES)
    )
    assert converted_record["list_key_name"] == {}


def test_select_from_list_without_a_list():
    """
    test selecting value from list returns none when givem `list` is actually
    not a list
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_SELECT_FROM_LIST_WITH_NO_LIST)
    )
    assert converted_record["list_key_name"] == {}


def test_country_code_from_phone_nunber():
    """
    test selecting value from list returns none when givem `list` is actually
    not a list
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_COUNTRY_CODE_FROM_PHONE_NUMBER)
    )
    assert converted_record["country_code"] == "NL"


def test_country_code_from_invalid_phone_nunber():
    """
    test selecting value from list returns none when givem `list` is actually
    not a list
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_COUNTRY_CODE_FROM_INVALID_PHONE_NUMBER)
    )
    assert converted_record["country_code"] is None


def test_days_ago_to_date():
    """
    test days ago to date method returning yesterdays date
    """
    yesterday = datetime.now() - timedelta(1)
    converted_record = convertor.convert_field(**deepcopy(PARAMS_DAYS_AGO_TO_DATE))
    assert converted_record["days_ago"] == datetime.strftime(yesterday, "%Y-%m-%d")


def test_days_ago_to_date_with_invalid_field():
    """
    test days ago to date method returning none with invalid nr of
    days ago field
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_DAYS_AGO_TO_DATE_INVALID)
    )
    assert converted_record["days_ago"] is None


def test_to_str():
    """
    test to str method turns an int into a strt
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_TO_STR))
    assert isinstance(converted_record["conversion_field"], str)


def test_to_lower_str():
    """
    test to_lower_str method turns str into lowercase
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_TO_LOWER_STR))
    assert converted_record["to_lower"] == "lowercase"


def test_to_upper_str():
    """
    test to_upper_str method turns str into uppercase
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_TO_UPPER_STR))
    assert converted_record["to_upper"] == "UPPERCASE"


def test_str_to_dict():
    """
    test str_to_dict returns correct dict
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_STR_TO_DICT))
    assert isinstance(converted_record["to_dict"], dict)
    assert converted_record["to_dict"] == {"key": "value"}


def test_invalid_str_to_dict():
    """
    test str_to_dict returns empty dict when given invalid input
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_INVALID_STR_TO_DICT))
    assert converted_record["to_dict"] == dict()


def test_add_pre_fix():
    """
    test add_prefix returns string `abc` with prefix `123`
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_PRE_FIX))
    assert converted_record["string"] == "123abc"


def test_add_post_fix():
    """
    test add_postfix returns string `abc` with prefix `def`
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_POST_FIX))
    assert converted_record["string"] == "abcdef"


def test_insert_key():
    """
    test add a field from another field.
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_INSERT_KEY))
    assert converted_record["from_field"] == {"inserted_field": "abc"}


def test_from_field():
    """
    test add a field from another field.
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_ADD_VALUE_FROM_FIELD))
    assert converted_record["to_field"] == {"nested": "abc"}


def test_add_data_from_dict():
    """
    test add a antries from a dict to another field
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_ADD_DATA_FROM_DICT))  # type: ignore # NOQA: E501
    assert converted_record["to_field"] == {"1": 1, "2": 2, "0": 0}


def test_add_key_value_from_field():
    """
    test add a field from another field.
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_ADD_KEY_VALUE_FROM_FIELD)
    )
    assert converted_record["to_field"] == {"from_field": "abc"}


def test_add_key_value_from_field2():
    """
    test add a field from another field.
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_ADD_KEY_VALUE_FROM_FIELD2)
    )
    assert converted_record["to_field"] == {
        "field2": "def",
        "from_field": "abc",
    }


def test_from_nested_field():
    """
    test add a field from another field.
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_ADD_VALUE_FROM_NETSED_FIELD)
    )
    assert converted_record["to_field"] == "abc"


def test_from_fixed_value():
    """
    test add a field with a fixed value
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_FIXED_VALUE))
    assert converted_record["new_field"] == "new value"


def test_date_of_today():
    """
    test add a field with date of today
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_DATE_OF_TODAY))
    assert converted_record["today"] == str(date.strftime(date.today(), "%Y-%m-%d"))


def test_change_key_name():
    """
    test changing a field name in the record
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_CHANGE_KEY_NAME))
    assert converted_record["new_name"] == {"nested": "abc"}
    assert converted_record.get("from_field", None) is None


def test_change_nested_key_name():
    """
    test changing a nested field name in the record
    """
    converted_record = convertor.convert_field(
        **deepcopy(PARAMS_CHANGE_KEY_NAME_NESTED)
    )
    assert converted_record["parent_field"]["new_nested"] == "abc"
    assert converted_record["parent_field"].get("nested", None) is None


def test_list_to_dict():
    """
    test changing list in a field to a dict
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_LIST_TO_DICT))
    assert converted_record["list"] == {"a": "b", "c": "d"}


def test_remove_field():
    """
    test removing a field
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_REMOVE))
    assert converted_record.get("removed_field", None) is None


def test_remove_nested_field():
    """
    test removing a field
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_REMOVE_NESTED_FIELD))  # type: ignore # NOQA: E501
    assert converted_record["nested"].get("removed_field", None) is None


def test_convert_cc_alpha_to_iso():
    """
    test conversion of ALPHA 3 country code to iso3116 country code
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_ALPHA3_TO_ISO3116))
    assert converted_record["cc"] == "FR"


def test_convert_divide_by():
    """
    test conversion dividing a value by a given devider
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_DIVIDE_BY))
    assert converted_record["tx"] == 12.3


def test_convert_divide_by_str():
    """
    test conversion dividing by an str raises an exception
    """
    with pytest.raises(TypeError):
        convertor.convert_field(**deepcopy(PARAMS_DIVIDE_BY_STR))


def test_convert_divide_str():
    """
    test conversion dividing a str returns None
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_DIVIDE_STR))
    assert converted_record == {"tx": None}


def test_convert_mulitply_by():
    """
    test conversion multiply a value by a given multiplier
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_MULTIPLY_BY))
    assert converted_record["tx"] == 12.3


def test_convert_multiply_by_str():
    """
    test conversion multiplying by an str raises an exception
    """
    with pytest.raises(TypeError):
        convertor.convert_field(**deepcopy(PARAMS_MULTIPLY_BY_STR))


def test_convert_multiply_str():
    """
    test conversion multiplying a str returns None
    """
    converted_record = convertor.convert_field(**deepcopy(PARAMS_MULTIPLY_STR))
    assert converted_record == {"tx": None}
