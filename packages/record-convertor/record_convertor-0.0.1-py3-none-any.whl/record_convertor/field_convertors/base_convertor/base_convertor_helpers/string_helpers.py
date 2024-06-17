"""
Module to provide method to process, clean etc strings.

Methods
    - normalize_string
"""

import unidecode

__all__ = ["normalize_string"]


def normalize_string(accented_string):
    """
    remove special characters form string and make lower case
    """
    accented_string = accented_string.replace('"', "")
    unaccented_string = unidecode.unidecode(accented_string)
    normalized_string = unaccented_string.lower().strip()
    return normalized_string
