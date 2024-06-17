from typing import Any, Optional, TypedDict, Union

__all__ = ["ConditionsDict", "ConditionValue"]


class ConditionsDict(TypedDict):
    date_not_today: Optional[Any]
    is_not_a_string: Optional[Any]
    is_a_string: Optional[Any]
    str_length: Optional[int]
    field_does_not_exist: Optional[Any]
    field_does_exist: Optional[Any]
    is_null: Optional[bool]
    equals: Optional[Any]
    does_not_equal: Optional[Any]
    in_list: Optional[list]
    contains: Optional[Any]
    does_not_contain: Optional[Any]


ConditionValue = Union[str, int, float, list[Any]]
