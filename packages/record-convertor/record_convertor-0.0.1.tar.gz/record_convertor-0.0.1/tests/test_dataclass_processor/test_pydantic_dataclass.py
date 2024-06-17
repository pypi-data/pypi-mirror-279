from copy import deepcopy
from typing import Optional

from pydantic import BaseModel

from record_convertor.dataclass_processor import DataClassProcessor
from record_convertor.package_settings import DataClassRuleDict, DataClassRuleKeys

from ..test_record_convertor.test_record_convertor_logic import basic_test_convertor


class DataClassTest(BaseModel): ...  # noqa: E701


class DataClassTestWithMethod(BaseModel):
    value: Optional[int] = None

    def multiply_by(self, multiplier: int):
        if self.value:
            self.value = self.value * multiplier


base_data_class_rule: DataClassRuleDict = {
    DataClassRuleKeys.NAME: "data_class_name",
    DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS: {"field1": "field2"},
    DataClassRuleKeys.METHODS: [
        {"rule_key1": "rule_value1", "rule_key2": "rule_value2"}
    ],
}


def test_private_register_pydantic_dataclass_method_adds_a_dataclass_to_the_class():
    """
    Test the private method _register_dataclass adds an attribute holding the
    dataclass to the dataclass processor.
    """
    data_class_processor = DataClassProcessor()
    data_class_processor._register_dataclass("test_class", DataClassTest)
    assert "test_class" in dir(data_class_processor)
    assert getattr(data_class_processor, "test_class") is DataClassTest  # noqa: B009


def test_data_class_return_without_method():
    data_class_processor = DataClassProcessor()
    data_class_processor.register_dataclass(DataClassTestWithMethod)
    rule = deepcopy(base_data_class_rule)
    rule[DataClassRuleKeys.NAME] = "data_class_test_with_method"
    rule[DataClassRuleKeys.METHODS] = []
    rule[DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS] = {"value": "input_value"}
    result = data_class_processor.data_from_dataclass(
        record={"input_value": 3}, rules=rule, record_convertor=basic_test_convertor()
    )
    assert result == {"value": 3}


def test_data_class_return_with_method():
    input_value = 4
    input_multiplier = 2
    data_class_processor = DataClassProcessor()
    data_class_processor.register_dataclass(DataClassTestWithMethod)
    rule = deepcopy(base_data_class_rule)
    rule[DataClassRuleKeys.NAME] = "data_class_test_with_method"
    rule[DataClassRuleKeys.METHODS] = [
        {"multiply_by": {"multiplier": "input_multiplier"}}
    ]
    rule[DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS] = {"value": "input_value"}
    result = data_class_processor.data_from_dataclass(
        record={"input_value": input_value, "input_multiplier": input_multiplier},
        rules=rule,
        record_convertor=basic_test_convertor(),
    )
    assert result == {"value": input_value * input_multiplier}
