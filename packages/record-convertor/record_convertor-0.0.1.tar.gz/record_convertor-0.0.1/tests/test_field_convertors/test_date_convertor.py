"""Module to test the field converter class from the record convertor module"""

from data.data_date_convertor_tests import (
    BASE_PARAMS,
    BASE_PARAMS_DOTTED,
    BASE_PARAMS_NESTED_DATE_FIELD,
    BASE_PARAMS_NONE_DATE,
    BASE_PARAMS_UNIX_DT_STAMP,
    BASE_PARAMS_YYYY_MM_DD,
    BASE_PARAMS_YYYY_MM_DD_UNDERSCORE,
    BASE_PARAMS_YYYY_MM_DD_Time,
)

from record_convertor.field_convertors import DateFieldConvertor


def test_convert_yyyy_mm_dd():
    """test conversion from YYYY_DD_MM to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS_YYYY_MM_DD)["date"] == "2021-02-21"  # type:ignore # NOQA: E501


def test_nested_convert_dd_mm_yyyy():
    """test conversion from DD_MM_YYYY to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_NESTED_DATE_FIELD)["date"][
            "nested_date"
        ]
        == "2021-02-21"
    )


def test_convert_dd_mm_yyyy():
    """test conversion from DD_MM_YYYY to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS)["date"] == "2021-02-21"  # type:ignore # NOQA: E501


def test_convert_dd_mm_yyyy_dotted():
    """test conversion from DD.MM.YYYY to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS_DOTTED)["date"] == "2021-02-21"  # type:ignore # NOQA: E501


def test_convert_yyyy_mm_dd_underscore():
    """test conversion from YYYY_MM_DD to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_YYYY_MM_DD_UNDERSCORE)["date"]  # type:ignore # NOQA: E501
        == "2021-02-21"
    )


def test_convert_yyyy_mm_dd_time():
    """test conversion from YYYY_MM_DD:Time to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_YYYY_MM_DD_Time)["date"]  # type:ignore # NOQA: E501
        == "2021-02-21"
    )


def test_convert_unix_date_time_stamp():
    """test conversion from YYYY_MM_DD:Time to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_UNIX_DT_STAMP)["date"] == "2021-02-21"  # type:ignore # NOQA: E501
    )


def test_convert_no_date_field():
    """test conversion where input field is None also returns None"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS_NONE_DATE)["date"] is None
