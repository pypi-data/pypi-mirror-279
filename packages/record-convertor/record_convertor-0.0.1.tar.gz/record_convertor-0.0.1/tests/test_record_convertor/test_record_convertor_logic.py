from dataclasses import dataclass
from typing import Optional

from record_convertor import EvaluateConditions, RecordConvertor
from record_convertor.command_processor import ProcessCommand
from record_convertor.dataclass_processor import DataClassProcessor
from record_convertor.package_settings import BaseRuleDict, FormatDateRuleDict

TEST_RULE = {"fieldname": "field1", "actions": []}
SKIP_RULE = {"fieldname": "field1", "condition": {"does_not_equal": "test"}}
TEST_FORMAT_DATE_RULE = {"date_field": "date", "format": "YYYY-MM-DD"}


class EveluateConditionsAlwaysToTrue(EvaluateConditions):
    def evaluate(self) -> bool:
        return True


class EveluateConditionsAlwaysToFalse(EvaluateConditions):
    def evaluate(self) -> bool:
        return False


class RuleConvertorTest:
    RULE_SOURCE_TYPE = str
    DEFAULT_RULE = TEST_RULE

    def __init__(self, rule_source: RULE_SOURCE_TYPE): ...

    @property
    def rules(self) -> dict:
        return self.DEFAULT_RULE


class EmptyRuleConvertorTest(RuleConvertorTest):
    DEFAULT_RULE = {}


class FieldConvertorTest:
    DEFAULT_RESULT: dict = {"ouput": "ouptut value"}

    def convert_field(self, record: dict, conversion_rule: BaseRuleDict) -> dict:
        return self.DEFAULT_RESULT


class DateFormatTest:
    DEFAULT_RESULT: dict = {"date1": "formatted_date"}

    def format_date_field(
        self, record: dict, conversion_rule: FormatDateRuleDict
    ) -> dict:
        return self.DEFAULT_RESULT


def basic_test_convertor(
    rule_class: type[RuleConvertorTest] = RuleConvertorTest,
    evaluate_class: type[EvaluateConditions] = EveluateConditionsAlwaysToTrue,
    field_convertor_class: type[FieldConvertorTest] = FieldConvertorTest,
    date_format_class: type[DateFormatTest] = DateFormatTest,
    data_classes: Optional[list[type]] = None,
    default_value: Optional[dict] = None,
) -> RecordConvertor:
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = rule_class
        EVALUATE_CLASS = evaluate_class
        DEFAULT_VALUE = default_value or {}
        _input_record = {}

    data_classes = data_classes or []
    return RecordConvertorTest(
        rule_source="test",
        field_convertor=field_convertor_class,
        date_formatter=date_format_class,
        data_classes=data_classes,
    )


def test_record_convertor_class_exits():
    """
    Tests the existence of the `RecordConvertor` class to ensure it is correctly
    defined and importable.
    """
    assert RecordConvertor


def test_record_convertor_sets_rules_source():
    """
    Tests that instances (subclasses of) `RecordConvertor` class correctly sets and
    utilizes the `_rules` attribute.
    """
    record_covertor = basic_test_convertor(rule_class=RuleConvertorTest)
    assert isinstance(record_covertor, RecordConvertor)
    assert basic_test_convertor()._rules == RuleConvertorTest(rule_source="").rules


def test_record_convertor_sets_field_convertor():
    """
    Tests that the `RecordConvertorTest` class correctly sets and utilizes the `_rules`
    attribute.
    """

    class TestFieldConvertor: ...  # NOQA : E701

    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        DEFAULT_FIELD_CONVERTOR_CLASS: type[TestFieldConvertor] = TestFieldConvertor

    assert isinstance(
        RecordConvertorTest(rule_source="test")._field_convertor, TestFieldConvertor
    )


################################################
# Test the set record keys to lower case logic #
################################################


def test_record_convert_sets_keys_to_lower_case():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest
        KEYS_IN_LOWER_CASE = True

    record_convertor = RecordConvertorTest(rule_source="test")
    test_record = {"KEY1": 1}
    record_convertor.convert(record=test_record)
    assert record_convertor._input_record == {"key1": 1}


def test_record_convert_does_not_set_keys_to_lower_case_by_default():
    record_convertor = basic_test_convertor(rule_class=EmptyRuleConvertorTest)
    test_record = {"KEY1": 1}
    record_convertor.convert(record=test_record)
    assert record_convertor._input_record == {"KEY1": 1}


########################################################
# Test flow where nothing hapens with the input record #
########################################################


def test_empty_record_returned_when_no_rules_are_applied():
    rule = {}

    class RuleClass(RuleConvertorTest):
        DEFAULT_RULE = rule

    record_convertor = basic_test_convertor(
        rule_class=RuleClass,
    )
    input_record = {"input value": "something"}

    assert record_convertor.convert(input_record) == {}


##############################
# Test the skip record flow #
##############################


def test_default_value_returned_when_record_skipped():
    rule = {"$SKIP": SKIP_RULE}

    class RuleClass(RuleConvertorTest):
        DEFAULT_RULE = rule

    default_value = {"value": "conversion skipped"}
    record_convertor = basic_test_convertor(
        rule_class=RuleClass, default_value=default_value
    )
    input_record = {"input value": "something"}

    assert record_convertor.convert(input_record) == default_value


###########################################
# Test the _convert_field in record logic #
###########################################


def test_field_convert_method_changes_the_input_record_with_convert_key():
    class TestConvertRuleClass(RuleConvertorTest):
        DEFAULT_RULE = {"$convert1": TEST_RULE}

    record_convertor = basic_test_convertor(rule_class=TestConvertRuleClass)
    input_record = {"input": "input value"}
    record_convertor.convert(input_record)
    assert record_convertor._input_record == FieldConvertorTest.DEFAULT_RESULT


def test_field_convert_method_no_change_of_input_without_convert_key():
    class TestConvertRuleClass(RuleConvertorTest):
        DEFAULT_RULE = {"no_convert": None}

    record_convertor = basic_test_convertor(rule_class=TestConvertRuleClass)
    input_record = {"input": "input value"}
    record_convertor.convert(input_record)
    assert record_convertor._input_record == {"input": "input value"}


def test_format_date_method_changes_input_record_with_format_date_key():
    class TestConvertRuleClass(RuleConvertorTest):
        DEFAULT_RULE = {"$format_date1": TEST_FORMAT_DATE_RULE}

    record_convertor = basic_test_convertor(rule_class=TestConvertRuleClass)
    input_record = {"date1": "date1"}
    record_convertor.convert(input_record)
    assert record_convertor._input_record == {"date1": "formatted_date"}


def test_format_date_method_leaves_input_as_is_without_convert_key():
    class TestConvertRuleClass(RuleConvertorTest):
        DEFAULT_RULE = {"no_format_date1": TEST_FORMAT_DATE_RULE}

    record_convertor = basic_test_convertor(rule_class=TestConvertRuleClass)
    input_record = {"date1": "date1"}
    record_convertor.convert(input_record)
    assert record_convertor._input_record == {"date1": "date1"}


############################################################
# Test the get_record_convertor_copy_with_new_rules method #
############################################################


def test_record_convertor_with_new_rules_from_dict_sets_new_rules():
    """
    Test that the method get_record_convertor_copy_with_new_rules returns
    a record convertor with the rules given by the input argument (in dict).
    """
    record_convertor = basic_test_convertor()
    assert record_convertor._rules == TEST_RULE
    new_record_convertor = record_convertor.get_record_convertor_copy_with_new_rules(
        {"new_rule1": "rule value1"}
    )
    assert new_record_convertor._rules == {"new_rule1": "rule value1"}


def test_rec_convt_with_new_rules_from_dict_sets_leaves_all_other_attributes_as_is():
    """
    Test that the method get_record_convertor_copy_with_new_rules returns a copy of
    the record convertor with only the rules changed to the given new rules
    """
    record_covertor = basic_test_convertor(rule_class=RuleConvertorTest)
    new_record_covertor = record_covertor.get_record_convertor_copy_with_new_rules(
        {"new_rule1": "rule value1"}
    )
    assert new_record_covertor._date_formatter == record_covertor._date_formatter
    assert new_record_covertor._field_convertor == record_covertor._field_convertor
    assert new_record_covertor.RULE_CLASS == record_covertor.RULE_CLASS
    assert new_record_covertor.KEYS_IN_LOWER_CASE == record_covertor.KEYS_IN_LOWER_CASE


#############################
# Test the data class logic #
#############################


def test_data_class_attribute_exist_if_no_dataclasses_provided():
    record_convertor = basic_test_convertor()
    assert isinstance(record_convertor.DATA_CLASS_PROCESSOR, DataClassProcessor)


def test_data_class_processer_has_attribute_with_dataclass_name_in_snake_case_as_key():
    @dataclass
    class DataClassOne:
        pass

    @dataclass
    class DataClassTwo:
        pass

    record_convertor = basic_test_convertor(data_classes=[DataClassOne, DataClassTwo])
    assert "data_class_one" in dir(record_convertor.DATA_CLASS_PROCESSOR)
    assert "data_class_two" in dir(record_convertor.DATA_CLASS_PROCESSOR)


def test_record_convertor_retrieves_result_from_data_class_processor():
    class DataClassTestProcessor:
        def data_from_dataclass(self, **kwargs) -> dict:
            return {"test": "result"}

    record_convertor = basic_test_convertor()
    record_convertor.DATA_CLASS_PROCESSOR = DataClassTestProcessor()  # type: ignore
    record_convertor._rules = {  # type: ignore
        "dataclass_result": {
            "$dataclass": {"data_class_name": "test", "params": {}, "method": []}
        }
    }

    assert record_convertor.convert(record={}) == {
        "dataclass_result": {"test": "result"}
    }


#####################################
# Test the command class conversion #
#####################################


def test_command_class_attribute_exists():
    record_convertor = basic_test_convertor()
    assert issubclass(record_convertor._command_class, ProcessCommand)


def test_record_convertor_runs_command_processor():
    class CommandTestProcessor:
        def __init__(self, **kwargs):
            pass

        def get_value(self, **kwargs) -> str:
            return "test result command processor"

    record_convertor = basic_test_convertor()
    record_convertor._command_class = CommandTestProcessor  # type: ignore
    record_convertor._rules = {  # type: ignore
        "command_processor_result": {"$any_command": "any_value"}
    }

    assert record_convertor.convert(record={}) == {
        "command_processor_result": "test result command processor"
    }
