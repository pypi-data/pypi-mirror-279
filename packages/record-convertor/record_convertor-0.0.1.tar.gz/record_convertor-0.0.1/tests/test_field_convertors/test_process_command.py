"""Module to test the process field class from the record convertor module"""

from datetime import datetime

import pytest
from data.data_process_command_tests import (
    BASE_PARAMS,
    PARAMS_ALLOW_NONE_VALUE_NONE,
    PARAMS_ALLOW_NONE_VALUE_WITH_VALUE,
    PARAMS_CURRENT_YEAR,
    PARAMS_FIRST_ITEM_FROM_LIST,
    PARAMS_FIRST_ITEM_FROM_LIST_NONE_RESULT,
    PARAMS_FROM_LIST,
    PARAMS_FULL_RECORD,
    PARAMS_GET_FIXED_VALUE,
    PARAMS_INT_FROM_STRING,
    PARAMS_JOIN,
    PARAMS_JOIN_ERROR,
    PARAMS_JOIN_KEY_VALUE,
    PARAMS_JOIN_KEY_VALUE2,
    PARAMS_JOIN_KEY_VALUE_ERROR1,
    PARAMS_JOIN_KEY_VALUE_ERROR2,
    PARAMS_JOIN_KEY_VALUE_ERROR3,
    PARAMS_JOIN_WITH_FIXED_VALUE,
    PARAMS_JOIN_WITH_SEPERATOR,
    PARAMS_JOIN_WITH_SEPERATOR_AND_NONE,
    PARAMS_NON_EXIST_COMM,
    PARAMS_POINT,
    PARAMS_POINT_ERROR1,
    PARAMS_POINT_ERROR2,
    PARAMS_SET_TO_NONE_VALUE,
    PARAMS_SPLIT_FIELD,
    PARAMS_SPLIT_FIELD_NONE,
    PARAMS_TO_INT_STRIP_LIST,
    PARAMS_TO_INT_STRIP_STR,
    PARAMS_TO_LIST,
    PARAMS_TO_LIST_DYNAMIC,
)

from record_convertor.command_processor import ProcessCommand


def field_processor(params):
    return ProcessCommand(**params)


def test_constructor():
    """Test field_processor method returns ProcessCommand instance."""
    processor = field_processor(BASE_PARAMS)
    assert isinstance(processor, ProcessCommand)


def test_non_existing_process_commands_exception():
    """Test non existing process command results in NonImplementedException"""
    processor = field_processor(PARAMS_NON_EXIST_COMM)
    with pytest.raises(NotImplementedError):
        assert processor.get_value()


def test_fixed_value():
    """Test fixed value method returns the fixed value."""
    processor = field_processor(PARAMS_GET_FIXED_VALUE)
    assert processor.get_value() == "the fixed value"


def test_split_field():
    """test split field method returns the correct value"""
    processor = field_processor(PARAMS_SPLIT_FIELD)
    assert processor.get_value() == "index1"


def test_split_field_wrong_index():
    """test split field method with wrong index returns None"""
    processor = field_processor(PARAMS_SPLIT_FIELD_NONE)
    assert processor.get_value() is None


def test_int_from_string():
    """test create an int from a string"""
    processor = field_processor(PARAMS_INT_FROM_STRING)
    assert processor.get_value() == "123456"


def test_join():
    """test create an int from a string"""
    processor = field_processor(PARAMS_JOIN)
    assert processor.get_value() == "abcdef"


def test_join_with_seperator():
    """test create an int from a string"""
    processor = field_processor(PARAMS_JOIN_WITH_SEPERATOR)
    assert processor.get_value() == "abc_def"


def test_join_with_seperator_and_none_value():
    """test join strings including seperator and None"""
    processor = field_processor(PARAMS_JOIN_WITH_SEPERATOR_AND_NONE)
    assert processor.get_value() == "def"


def test_join_with_error():
    """test create an int from a string"""
    processor = field_processor(PARAMS_JOIN_ERROR)
    with pytest.raises(ValueError):
        processor.get_value()


def test_join_with_fixed_value():
    """test create an int from a string"""
    processor = field_processor(PARAMS_JOIN_WITH_FIXED_VALUE)
    assert processor.get_value() == "abcdefghij"


def test_point(mocker):
    """test create an int from a string"""
    mocked_point = "test123"
    mocker.patch(
        "record_convertor.command_processor.lat_lon_to_geojson_point",
        return_value=mocked_point,
    )
    processor = field_processor(PARAMS_POINT)
    assert processor.get_value() == mocked_point


def test_point_error1():
    """
    test that ValueError is raised if lat or lon field is missing in the
    arguments
    """
    processor = field_processor(PARAMS_POINT_ERROR1)
    with pytest.raises(ValueError):
        processor.get_value()


def test_point_error2():
    """test create an int from a string"""
    processor = field_processor(PARAMS_POINT_ERROR2)
    assert processor.get_value() is None


def test_full_record():
    """test create an int from a string"""
    processor = field_processor(PARAMS_FULL_RECORD)
    assert "field2" in processor.get_value()
    assert processor.get_value()["field1"] == {"nested_field": {"a": 1}}


def test_join_key_value():
    """test join_key_value method success"""
    processor = field_processor(PARAMS_JOIN_KEY_VALUE)
    assert processor.get_value() == {"key": "value"}


def test_join_key_value_with_join():
    """
    test join_key_value method success when join operator is used
    from key and value
    """
    processor = field_processor(PARAMS_JOIN_KEY_VALUE2)
    assert processor.get_value() == {"key_join": "value_join"}


def test_join_key_value_error1():
    """test join_key_value method with wrong args results in None"""
    processor = field_processor(PARAMS_JOIN_KEY_VALUE_ERROR1)
    with pytest.raises(KeyError):
        processor.get_value()


def test_join_key_value_error2():
    """test join_key_value method with wrong args results in None"""
    processor = field_processor(PARAMS_JOIN_KEY_VALUE_ERROR2)
    assert processor.get_value() is None


def test_join_key_value_error3():
    """test join_key_value method with wrong args results in None"""
    processor = field_processor(PARAMS_JOIN_KEY_VALUE_ERROR3)
    assert processor.get_value() is None


def test_from_list():
    """test from_list method success"""
    processor = field_processor(PARAMS_FROM_LIST)
    assert processor.get_value() == [
        {"target_field1": 1, "target_field2": 2},
        {"target_field1": 2, "target_field2": 3},
    ]


def test_to_list():
    """test to_list method success"""
    processor = field_processor(PARAMS_TO_LIST)
    assert processor.get_value() == [1, 2]


def test_to_int_with_strip_list():
    """test to_int method with list of strip arguments success"""
    processor = field_processor(PARAMS_TO_INT_STRIP_LIST)
    assert processor.get_value() == "10000"


def test_to_int_with_strip_str():
    """test to_int with only a str a strip agument method success"""
    processor = field_processor(PARAMS_TO_INT_STRIP_STR)
    assert processor.get_value() == "10.000 "


def test_to_list_dynamic():
    """test to_list_dynamic method success"""
    processor = field_processor(PARAMS_TO_LIST_DYNAMIC)
    assert processor.get_value() == [{"price1": "10.000 eur"}, {"price2": "9.000 eur"}]


def test_first_item_from_list():
    """test first_item_from_list method success"""
    processor = field_processor(PARAMS_FIRST_ITEM_FROM_LIST)
    assert processor.get_value() == {"result": "item1"}


def test_first_item_from_list_none_result():
    """test first_item_from_list returns None when no value is found"""
    processor = field_processor(PARAMS_FIRST_ITEM_FROM_LIST_NONE_RESULT)
    assert processor.get_value() is None


def test_allow_value_to_be_none_with_none():
    """test first_item_from_list method success"""
    processor = field_processor(PARAMS_ALLOW_NONE_VALUE_NONE)
    assert processor.get_value() is None


def test_allow_value_to_be_none_with_value():
    """test first_item_from_list method success"""
    processor = field_processor(PARAMS_ALLOW_NONE_VALUE_WITH_VALUE)
    assert processor.get_value() == "existing value"


def test_set_to_none_value():
    """test set_to_none_value method"""
    processor = field_processor(PARAMS_SET_TO_NONE_VALUE)
    assert processor.get_value() is None


def test_current_year():
    """test current_year"""
    processor = field_processor(PARAMS_CURRENT_YEAR)
    assert processor.get_value() == str(datetime.now().year)
