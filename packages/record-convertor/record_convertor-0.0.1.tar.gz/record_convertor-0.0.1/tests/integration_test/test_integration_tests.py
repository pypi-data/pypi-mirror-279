from typing import Optional

from data._test_data import itterator_test_data

from record_convertor import (
    BaseFieldConvertor,
    DateFieldConvertor,
    EvaluateConditions,
    RecordConvertor,
    RulesFromDict,
)


def basic_test_convertor(
    rule_source: str,
    rule_class: type[RulesFromDict] = RulesFromDict,
    evaluate_class: type[EvaluateConditions] = EvaluateConditions,
    field_convertor_class: type[BaseFieldConvertor] = BaseFieldConvertor,
    date_format_class: type[DateFieldConvertor] = DateFieldConvertor,
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
        rule_source=rule_source,
        field_convertor=field_convertor_class,
        date_formatter=date_format_class,
        data_classes=data_classes,
    )


def test_integtation_test():
    for test in itterator_test_data("base_test.json"):
        convertor = basic_test_convertor(test["rules"])
        assert convertor.convert(test["input_record"]) == test["output_record"]
