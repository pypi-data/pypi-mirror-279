"""
Helper module to provide meta data for country regions structure

Methods:
    iso3116_from_alpha_3_country_code
"""

from .data_files.country_codes import ALL_COUNTRY_CODES

__all__ = ["iso3116_from_alpha_3_country_code"]


def iso3116_from_alpha_3_country_code(alpha_3: str) -> str:
    """Returns iso3116 country code from alph3 country code

    Args:
        alpha_3 (str): alpha3 country code

    Returns:
        str: iso3116 country code
    """
    return next(
        (
            country["let2"]
            for country in ALL_COUNTRY_CODES
            if country["let3"] == alpha_3.upper()
        ),
        "",
    )
