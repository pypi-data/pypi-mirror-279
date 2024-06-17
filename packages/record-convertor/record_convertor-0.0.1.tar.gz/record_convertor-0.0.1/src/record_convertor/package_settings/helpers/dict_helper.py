"""
This module provides utility functions for manipulating dictionaries and lists,
particularly focusing on case normalization and cleaning of data structures. It includes
functions for recursively converting dictionary keys to lowercase, even within nested
dictionaries and lists, and for removing entries from dictionaries where values are
None.

Functions:
    - list_in_lower_case:
        Recursively converts all dictionary keys within a list to lower case, including
        keys in nested structures.
    - keys_in_lower_case:
        Recursively converts all keys in a dictionary to lower case, including keys in
        nested dictionaries and lists.
    - dict_without_non_values:
        Removes key-value pairs from a dictionary where the value is None, cleaning up
        the dictionary.

The module aims to facilitate the handling of data structures that are commonly used in
data parsing, preprocessing, and transformation tasks, ensuring consistency in key
naming conventions and eliminating null entries from dictionaries.
"""

from typing import Any, Dict, List

__all__ = [
    "list_in_lower_case",
    "keys_in_lower_case",
    "dict_without_non_values",
]


def list_in_lower_case(input_record: List[Any]) -> List[Any]:
    """
    Recursively converts all dictionary keys within a list to lower case, including
    nested dictionaries and lists.

    Args:
        input_record (List[Any]):
            A list potentially containing dictionaries, lists, and other data types.

    Returns:
        List[Any]:
            A new list with dictionary keys in lower case within any nested structures.
    """
    result: List[Any] = []
    for item in input_record:
        if isinstance(item, list):
            result.append(list_in_lower_case(item))
        elif isinstance(item, dict):
            result.append(keys_in_lower_case(item))
        else:
            result.append(item)
    return result


def keys_in_lower_case(input_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively converts all keys in a dictionary to lower case, including keys in
    nested dictionaries and lists.

    Args:
        input_record (Dict[str, Any]):
            The dictionary to be processed, potentially containing nested dictionaries
            and lists.

    Returns:
        Dict[str, Any]:
            A new dictionary with all keys in lower case, including within nested
            structures.
    """
    dict_result: Dict[str, Any] = {}
    for key, value in input_record.items():
        if isinstance(value, list):
            dict_result[key.lower()] = list_in_lower_case(value)
        elif isinstance(value, dict):
            dict_result[key.lower()] = keys_in_lower_case(value)
        else:
            dict_result[key.lower()] = value
    return dict_result


def dict_without_non_values(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Removes key-value pairs from a dictionary where the value is None.

    Args:
        input_dict (Dict[str, Any]): The dictionary to be processed.

    Returns:
        Dict[str, Any]: A new dictionary with all None values removed.
    """
    return {k: v for k, v in input_dict.items() if v is not None}
