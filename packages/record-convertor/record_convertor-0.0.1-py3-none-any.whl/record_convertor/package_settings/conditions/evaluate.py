"""Module to define Conditions class.

Classes:
    - EvaluateConditions
"""

from datetime import datetime
from typing import Optional, Union

from .condition_settings import ConditionsDict, ConditionValue

__all__ = ["EvaluateConditions", "ConditionsDict", "ConditionValue"]


class EvaluateConditions:
    """
    Evaluates a set of conditions against a provided value.

    This class allows for evaluating various conditions such as type checks,
    string operations, and date comparisons against a given value. It supports
    a flexible definition of conditions through a dictionary where each key
    represents a specific condition to be evaluated.

    Parameters:
        provided_conditions (Optional[ConditionsDict]): A dictionary of conditions
            to be evaluated against the value. Each key in the dictionary is a string
            that corresponds to a condition method within this class, and its value
            is the expected condition value or parameter. Defaults to None, which
            results in an empty condition set.
        value (Optional[ConditionValue]): The value to be evaluated against the
            provided conditions. Can be a string, integer, float, or None. Defaults
            to None.

    Methods:
        evaluate() -> bool:
            Evaluates all provided conditions against the value and returns True
            if all conditions are met, otherwise False.

    Supported Conditions:
        - is_a_string:
            Checks if the value is a string.
        - is_not_a_string:
            Checks if the value is not a string.
        - is_null:
            Checks if the value is None, based on a boolean argument.
        - date_not_today:
            Verifies that a date string (YYYY-MM-DD) does not represent today's date.
        - str_length:
            Checks if the value's string representation has a specific length.
        - field_does_not_exist:
            Returns True if the value is None (field does not exist).
        - field_does_exist:
            Returns True if the value is not None (field exists).
        - equals:
            Checks if the value equals a specified value.
        - in_list:
            Verifies if the value exists within a provided list.
        - does_not_equal:
            Checks if the value does not equal a specified value.
        - contains:
            Determines if a substring exists within the value.
        - does_not_contain:
            Determines if a substring does not exist within the value.

    Raises:
        NotImplementedError:
            If a provided condition does not match any supported condition method.
        ValueError:
            If conditions 'contains' or 'does_not_contain' are provided None as input.

    Example:
        >>> conditions = {"is_a_string": True, "str_length": 5}
        >>> evaluator = EvaluateConditions(
        ...     provided_conditions=conditions, value="Hello"
        ... )
        >>> evaluator.evaluate()
        True

    Note:
        The 'date_not_today' condition does not validate the format of the input date
        string.
    """

    def __init__(
        self,
        provided_conditions: Optional[ConditionsDict] = None,
        value: Optional[ConditionValue] = None,
    ):
        self.provided_conditions: Union[ConditionsDict, dict] = (
            provided_conditions or {}
        )
        self.value = value

    def evaluate(self) -> bool:
        """Evaluetes the given conditions with the given value

        Returns:
            Boolean: Returns true if all conditions are met for given
                     value. If not all conditions are met False is returned

        """
        # be default evaluate method returns True unless one of the given
        # conditions is no met
        all_conditions_are_true = True

        for condition in self.provided_conditions:
            if condition in dir(self):
                all_conditions_are_true = (
                    all_conditions_are_true and getattr(self, condition)()
                )
            else:
                raise NotImplementedError(f"Condition {condition}")

        return all_conditions_are_true

    def date_not_today(self) -> bool:
        return not (datetime.today().strftime("%Y-%m-%d") == self.value)

    def is_not_a_string(self) -> bool:
        return not isinstance(self.value, str)

    def is_a_string(self) -> bool:
        return isinstance(self.value, str)

    def str_length(self) -> bool:
        return len(str(self.value)) == self.provided_conditions["str_length"]

    def field_does_not_exist(self) -> bool:
        return self.value is None

    def field_does_exist(self) -> bool:
        return self.value is not None

    def is_null(self) -> bool:
        """
        check if value is None or not None depending on value of condition field
        'is_null'
        """
        return (self.value is None) == self.provided_conditions["is_null"]

    def equals(self) -> bool:
        return self.value == self.provided_conditions["equals"]

    def in_list(self) -> bool:
        if not isinstance(self.provided_conditions["in_list"], list):
            return False

        return self.value in self.provided_conditions["in_list"]

    def does_not_equal(self) -> bool:
        return self.value != self.provided_conditions["does_not_equal"]

    def contains(self) -> bool:
        if self.provided_conditions["contains"] is None:
            raise ValueError("Condition 'contains' can not have None as input value.")
        if not isinstance(self.value, (list, str)):
            return False
        return self.provided_conditions["contains"] in self.value

    def does_not_contain(self) -> bool:
        if self.provided_conditions["does_not_contain"] is None:
            raise ValueError(
                "Condition 'does_not_contain' can not have None as input value."
            )
        if not isinstance(self.value, (list, str)):
            return False

        return self.provided_conditions["does_not_contain"] not in self.value
