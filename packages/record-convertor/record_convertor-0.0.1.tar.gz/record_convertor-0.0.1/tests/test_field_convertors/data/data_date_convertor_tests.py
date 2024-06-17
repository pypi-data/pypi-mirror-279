BASE_PARAMS = {
    "record": {"date": "21-02-2021"},
    "conversion_rule": {"date_field": "date", "format": "DD-MM-YYYY"},
}

BASE_PARAMS_YYYY_MM_DD = {
    "record": {"date": "2021-02-21"},
    "conversion_rule": {"date_field": "date", "format": "YYYY-MM-DD"},
}

BASE_PARAMS_DOTTED = {
    "record": {"date": "21.02.2021"},
    "conversion_rule": {"date_field": "date", "format": "DD.MM.YYYY"},
}

BASE_PARAMS_NESTED_DATE_FIELD = {
    "record": {"date": {"nested_date": "21-02-2021"}},
    "conversion_rule": {"date_field": "date.nested_date", "format": "DD-MM-YYYY"},
}

BASE_PARAMS_YYYY_MM_DD = {
    "record": {"date": "2021-02-21"},
    "conversion_rule": {"date_field": "date", "format": "YYYY-MM-DD"},
}

BASE_PARAMS_YYYY_MM_DD_UNDERSCORE = {
    "record": {"date": "2021_02_21"},
    "conversion_rule": {"date_field": "date", "format": "YYYY_MM_DD"},
}

BASE_PARAMS_YYYY_MM_DD_Time = {
    "record": {"date": "2021-02-21 16:01:15.436202"},
    "conversion_rule": {"date_field": "date", "format": "YYYY_MM_DD:Time"},
}

BASE_PARAMS_UNIX_DT_STAMP = {
    "record": {"date": "1613916129"},
    "conversion_rule": {"date_field": "date", "format": "UNIX_DT_STAMP"},
}

BASE_PARAMS_NONE_DATE = {
    "record": {"date": None},
    "conversion_rule": {"date_field": "date", "format": "UNIX_DT_STAMP"},
}
