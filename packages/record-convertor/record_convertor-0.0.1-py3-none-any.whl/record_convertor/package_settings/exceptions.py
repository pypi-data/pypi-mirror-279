"""
Module to define customer excpetions for record_convertor package

exceptions
- ProcessArgsMustBeOfTypeList
"""

from typing import Any


class ProcessArgsMustBeOfTypeList(Exception):
    def __init__(self, process_args: Any):
        super().__init__(
            f"process_args must be of <type> list but is of type `{type(process_args)}"
        )


class ProcessArgsMustBeOfTypeDict(Exception):
    def __init__(self, process_args: Any):
        super().__init__(
            f"process_args must be of type <dict> but is of type `{type(process_args)}"
        )


class FormatNotImplementedException(Exception):
    def __init__(self, format: str):
        super().__init__(f"Requested format {format} not implememted.")


class NoDateFieldException(Exception):
    def __init__(self):
        super().__init__("No input for dateformat provided in the ruleset.")
