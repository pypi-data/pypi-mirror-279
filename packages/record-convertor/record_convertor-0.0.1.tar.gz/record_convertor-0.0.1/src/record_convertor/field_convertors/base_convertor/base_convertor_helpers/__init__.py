from typing import Any, Optional

import jmespath
from jmespath.exceptions import ParseError

from record_convertor.package_settings.conditions.evaluate import EvaluateConditions
from record_convertor.package_settings.package_types import (
    BaseConvertorKeys,
    BaseRuleDict,
)

from .countries import *  # NOQA
from .html_parser import *  # NOQA
from .string_helpers import *  # NOQA


class _BaseConvertorClass:
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

    def convert_field(
        self, record: dict[str, Any], conversion_rule: BaseRuleDict
    ) -> dict:
        self.record = record
        self.conversion_rule = conversion_rule
        self.field_name = conversion_rule[BaseConvertorKeys.FIELDNAME]

        actions = self.conversion_rule[BaseConvertorKeys.ACTIONS] or {}
        if self.all_conditions_true():
            # loop over all actions
            for action_dict in actions:
                self.field_value = self._get_field(self.field_name)
                # remove any optional target_field from the action as the target_field
                # setting is not an action in itself
                optional_target_field = action_dict.pop(
                    BaseConvertorKeys.ACTIONTARGET, None
                )

                # retrieve single action and action value and execute
                [[action, action_value]] = action_dict.items()
                if action in dir(self):
                    field_value = getattr(self, action)(action_value)
                else:
                    raise NotImplementedError(f"Action {action}")

                # Set the target field of leave the used field_name as is if no
                # target field is defined.
                target_field = optional_target_field or self.field_name
                if action not in ["remove"]:
                    self.set_field_value(value=field_value, target_field=target_field)

        return self.record

    def all_conditions_true(self) -> bool:
        """Returns True if all provided conditions are satisfied"""
        if conditions := self.conversion_rule.get(BaseConvertorKeys.CONDITION):
            return EvaluateConditions(
                provided_conditions=conditions, value=self.field_value
            ).evaluate()

        # when no conditions were provided the conversion needs to
        # continue
        return True

    def set_field_value(self, value, target_field: str):
        """
        sets a value to a nested field in the record.

        args:
            - value (str)
                value that will be assigned to the last fieldname in
                field_names

        returns none

        """
        nested_field_names = target_field.split(".")
        first_field_name = nested_field_names.pop(0)
        # if it is not a nested field update first level field name and return
        if not nested_field_names:
            self.record.update({first_field_name: value})
            return

        # if it is a nested field capture the fieldname that needs to be
        # updated (i.e. the last field name in thel list).
        last_field = nested_field_names.pop()

        # find the nested dict in whih the last_field is a (nested) key
        field_value = self.record.get(first_field_name, None)
        if field_value is None:
            return None

        # with the list of nested field name we dig deeper into the
        # structure to get to the dict containing the last field name
        for field_name in nested_field_names:
            field_value = field_value.get(field_name, {})

        # update that value of `last_field` in that dict
        if field_value is not None:
            field_value.update({last_field: value})

    def pop_nested_field(self, field):
        """
        removes a value to a nested field in the record.

        args:
            field (str): nested field name (ex. key.subkey1.subkey2 etc)

        returns
            - the content of the popped key
            - None if this field is not found
        """
        nested_field_names = field.split(".")
        first_field_name = nested_field_names.pop(0)
        # if it is not a nested field update first level field name and return
        if not nested_field_names:
            return self.record.pop(first_field_name, None)

        # if it is a nested field capture the fieldname that needs to be
        # popped (i.e. the last field name in the list).
        last_field = nested_field_names.pop()

        # find the nested dict in which the last_field is a (nested) key
        if not (field_value := self.record.get(first_field_name, None)):
            return None

        # with the list of nested field name we dig deeper into the
        # structure to get to the dict containing the last field name
        for field_name in nested_field_names:
            field_value = field_value.get(field_name, {})

        # update that value of `last_field` in that dict
        if field_value and isinstance(field_value, dict):
            return field_value.pop(last_field, None)

    def _get_field(self, key: str, rec: Optional[dict] = None):
        """
        returns a value from a nested field in the record.
        nested field names should be seperated by `__`
        """
        # initially used '__' as key seperator but migrating to using
        # `.` as seperator. This line to allow old conversion yaml files
        # not to fail
        record = rec or self.record
        if key:
            nested_field_names = key.replace("__", ".")
            # key elemenets in nested keys are surround with "". For exmample
            # key.example-1 becomes "key"."example-1".
            # Needed for jmespath can hande special characters in the keys
            nested_keys = nested_field_names.split(".")
            nested_key = ".".join(['"' + key + '"' for key in nested_keys])
            try:
                return jmespath.search(nested_key, record)
            except ParseError:
                pass

        return None
