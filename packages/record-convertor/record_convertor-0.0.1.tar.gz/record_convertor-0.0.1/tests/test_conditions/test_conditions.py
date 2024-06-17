from datetime import datetime

import pytest

from record_convertor.package_settings import EvaluateConditions


@pytest.fixture
def conditions():
    return EvaluateConditions()


def test_empty_condtions_instance(conditions):
    """test that an empty conditions class evaluates to True"""
    assert conditions.evaluate()


def test_non_existing_condition_raises_exception(conditions):
    """test is_a_str method evaluates to True with a string as value"""
    conditions.provided_conditions = {"not_existing": None}
    conditions.value = "a string"
    with pytest.raises(NotImplementedError):
        conditions.evaluate()


def test_is_a_str_method_with_a_str(conditions):
    """test is_a_str method evaluates to True with a string as value"""
    conditions.provided_conditions = {"is_a_string": None}
    conditions.value = "a string"
    assert conditions.evaluate()


def test_is_a_str_method_with_an_(conditions):
    """test is_a_str method evaluates to False with an int"""
    conditions.provided_conditions = {"is_a_string": None}
    conditions.value = 1
    assert conditions.evaluate() is False


def test_is_not_a_str_method_with_a_str(conditions):
    """test is_a_str method evaluates to True with a string as value"""
    conditions.provided_conditions = {"is_not_a_string": None}
    conditions.value = "a string"
    assert conditions.evaluate() is False


def test_is_not_a_str_method_with_an_(conditions):
    """test is_a_str method evaluates to False with an int"""
    conditions.provided_conditions = {"is_not_a_string": None}
    conditions.value = 1
    assert conditions.evaluate()


def test_in_list(conditions):
    """test in_list method evaluates true with correct value"""
    conditions.provided_conditions = {"in_list": ["01", "02"]}
    conditions.value = "01"
    assert conditions.evaluate()


def test_in_list_and_does_not_equal_true(conditions):
    """
    test in_list and does_not_equal methods evaluates true with correct value.
    """
    conditions.provided_conditions = {"in_list": ["01", "02"], "does_not_equal": "02"}
    conditions.value = "01"
    assert conditions.evaluate()


def test_in_list_and_does_not_equal_false(conditions):
    """
    test in_list and does_not_equal methods evaluates false with incorrect
    value.
    """
    conditions.provided_conditions = {"in_list": ["01", "02"], "does_not_equal": "01"}
    conditions.value = "01"
    assert conditions.evaluate() is False


def test_in_list_false(conditions):
    """test in_list method evaluates true with correct value"""
    conditions.provided_conditions = {"in_list": ["01", "02"]}
    conditions.value = "03"
    assert conditions.evaluate() is False


def test_str_length_method_true_condition(conditions):
    """test str_length method evaluates to True"""
    conditions.provided_conditions = {"str_length": 1}
    conditions.value = "a"
    assert conditions.evaluate()


def test_str_length_method_false_condition(conditions):
    """test str_length method evaluates to False"""
    conditions.provided_conditions = {"str_length": 1}
    conditions.value = "aa"
    assert conditions.evaluate() is False


def test_str_length_method_with_an_int(conditions):
    """
    test str_length method evaluates to True with a int with length as number
    of digits
    """
    conditions.provided_conditions = {"str_length": 2}
    conditions.value = 12
    assert conditions.evaluate()


def test_field_does_not_exist(conditions):
    """
    test field_does_not_exist method evaluates to True if value is None
    """
    conditions.provided_conditions = {"field_does_not_exist": ""}
    conditions.value = None
    assert conditions.evaluate()


def test_field_does_exist(conditions):
    """
    test field_does_exist method evaluates to True if value is not None
    """
    conditions.provided_conditions = {"field_does_exist": ""}
    conditions.value = "Not None"
    assert conditions.evaluate()


def test_field_does_exist_false(conditions):
    """
    test field_does_not_exist method evaluates to True if value is None
    """
    conditions.provided_conditions = {"field_does_exist": ""}
    conditions.value = None
    assert conditions.evaluate() is False


def test_field_does_not_exist_false(conditions):
    """
    test field_does_not_exist method evaluates to False if value is not None
    """
    conditions.provided_conditions = {"field_does_not_exist": ""}
    conditions.value = "Not None"
    assert conditions.evaluate() is False


def test_is_null_with_arg_true_1(conditions):
    """
    test is_null method evaluates to True with arg True and value None
    """
    conditions.provided_conditions = {"is_null": True}
    conditions.value = None
    assert conditions.evaluate()


def test_is_null_with_arg_true_2(conditions):
    """
    test is_null method evaluates to False with arg True and value not None
    """
    conditions.provided_conditions = {"is_null": True}
    conditions.value = "not None"
    assert conditions.evaluate() is False


def test_is_null_with_arg_false_1(conditions):
    """
    test is_null method evaluates to False with arg False and value None
    """
    conditions.provided_conditions = {"is_null": False}
    conditions.value = None
    assert conditions.evaluate() is False


def test_is_null_with_arg_false_2(conditions):
    """
    test is_null method evaluates to True with arg False and value not None
    """
    conditions.provided_conditions = {"is_null": False}
    conditions.value = "not None"
    assert conditions.evaluate()


def test_equals_true(conditions):
    """
    test equals method evaluates to True
    """
    conditions.provided_conditions = {"equals": "equal_value"}
    conditions.value = "equal_value"
    assert conditions.evaluate()


def test_equals_false(conditions):
    """
    test equals method evaluates to True
    """
    conditions.provided_conditions = {"equals": "value"}
    conditions.value = "other_value"
    assert conditions.evaluate() is False


def test_does_not_equal_true(conditions):
    """
    test does_not_equal method evaluates to True
    """
    conditions.provided_conditions = {"does_not_equal": "equal_value"}
    conditions.value = "equal_value"
    assert conditions.evaluate() is False


def test_does_not_equal_false(conditions):
    """
    test doen_not_equal method evaluates to True
    """
    conditions.provided_conditions = {"does_not_equal": "value"}
    conditions.value = "other value"
    assert conditions.evaluate()


def test_contains_true(conditions):
    """
    test contains method evaluates to True
    """
    conditions.provided_conditions = {"contains": "test"}
    conditions.value = "test_value"
    assert conditions.evaluate()


def test_contains_false(conditions):
    """
    test contains method evaluates to False
    """
    conditions.provided_conditions = {"contains": "test"}
    conditions.value = "other_value"
    assert conditions.evaluate() is False


def test_does_not_contain_true(conditions):
    """
    test does_not_contain method evaluates to True if value does contain
    provided arg
    """
    conditions.provided_conditions = {"does_not_contain": "test"}
    conditions.value = "other_value"
    assert conditions.evaluate()


def test_does_not_contain_false(conditions):
    """
    test does_not_contain method evaluates to False if value does contain
    provided arg
    """
    conditions.provided_conditions = {"does_not_contain": "test"}
    conditions.value = "test_value"
    assert conditions.evaluate() is False


def test_date_not_today_returns_false_with_today_value(conditions):
    """
    test does_not_contain method evaluates to False if value does contain
    provided arg
    """
    conditions.provided_conditions = {"date_not_today": None}
    conditions.value = datetime.today().strftime("%Y-%m-%d")
    assert conditions.evaluate() is False
