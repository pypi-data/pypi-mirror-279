from typing import Any

from record_convertor.package_settings import (
    ProcessArgsMustBeOfTypeDict,
    ProcessArgsMustBeOfTypeList,
)


def process_args_is_list(process_args: Any) -> list:
    if isinstance(process_args, list):
        return process_args
    raise ProcessArgsMustBeOfTypeList(process_args)


def process_args_is_dict(process_args: Any) -> dict:
    if isinstance(process_args, dict):
        return process_args
    raise ProcessArgsMustBeOfTypeDict(process_args)
