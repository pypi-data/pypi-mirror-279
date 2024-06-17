BASE_PARAMS = {
    "record": {"url": "www.test.com/?test_params=1"},
    "conversion_rule": {
        "fieldname": "url",
        "actions": [{"remove_params_from_url": None}],
    },
}

URL_PARAMS = {
    "record": {"url": "www.test.com/?test_params=1"},
    "conversion_rule": {
        "fieldname": "url",
        "actions": [{"remove_params_from_url": None}],
    },
}

URL_PARAMS_WITH_CONDITION = {
    "record": {"url": "www.test.com/?test_params=1"},
    "conversion_rule": {
        "fieldname": "url",
        "condition": {"field_does_exist": None},
        "actions": [{"remove_params_from_url": None}],
    },
}

BASE_PARAMS_SELECT_FROM_LIST = {
    "record": {
        "list_key_name": [
            {"item1": 1, "selector": 1},
            {"item2": 2, "selector": 2},
        ]
    },
    "conversion_rule": {
        "fieldname": "list_key_name",
        "actions": [{"select_object_from_list": ["selector", 2]}],
    },
}

PARAMS_SELECT_FROM_LIST_VALUE_NOT_FOUND = {
    "record": {
        "list_key_name": [
            {"item1": 1, "selector": 1},
            {"item2": 2, "selector": 2},
        ]
    },
    "conversion_rule": {
        "fieldname": "list_key_name",
        "actions": [{"select_object_from_list": ["selector", 3]}],
    },
}

PARAMS_SELECT_FROM_LIST_WITH_NON_DICT_ENTRIES = {
    "record": {"list_key_name": [1, 2, "item1", "item2"]},
    "conversion_rule": {
        "fieldname": "list_key_name",
        "actions": [{"select_object_from_list": ["selector", 3]}],
    },
}

PARAMS_SELECT_FROM_LIST_WITH_NO_LIST = {
    "record": {"list_key_name": 1},
    "conversion_rule": {
        "fieldname": "list_key_name",
        "actions": [{"select_object_from_list": ["selector", 3]}],
    },
}

PARAMS_COUNTRY_CODE_FROM_PHONE_NUMBER = {
    "record": {"phonenumber": "+31612341234"},
    "conversion_rule": {
        "fieldname": "country_code",
        "actions": [{"get_country_code_from_phone_nr": "phonenumber"}],
    },
}

PARAMS_COUNTRY_CODE_FROM_INVALID_PHONE_NUMBER = {
    "record": {"phonenumber": "124"},
    "conversion_rule": {
        "fieldname": "country_code",
        "actions": [{"get_country_code_from_phone_nr": "phonenumber"}],
    },
}

PARAMS_DAYS_AGO_TO_DATE = {
    "record": {"days_ago": "1"},
    "conversion_rule": {
        "fieldname": "days_ago",
        "actions": [{"days_ago_to_date": None}],
    },
}

PARAMS_DAYS_AGO_TO_DATE_INVALID = {
    "record": {"days_ago": "invalid days ago field"},
    "conversion_rule": {
        "fieldname": "days_ago",
        "actions": [{"days_ago_to_date": None}],
    },
}

PARAMS_TO_STR = {
    "record": {"conversion_field": 1},
    "conversion_rule": {"fieldname": "conversion_field", "actions": [{"to_str": None}]},
}

PARAMS_TO_LOWER_STR = {
    "record": {"to_lower": "LOWERCASE"},
    "conversion_rule": {"fieldname": "to_lower", "actions": [{"to_lower_str": None}]},
}

PARAMS_TO_UPPER_STR = {
    "record": {"to_upper": "uppercase"},
    "conversion_rule": {"fieldname": "to_upper", "actions": [{"to_upper_str": None}]},
}

PARAMS_STR_TO_DICT = {
    "record": {"to_dict": '{"key": "value"}'},
    "conversion_rule": {"fieldname": "to_dict", "actions": [{"str_to_dict": None}]},
}

PARAMS_INVALID_STR_TO_DICT = {
    "record": {"to_dict": "abc"},
    "conversion_rule": {"fieldname": "to_dict", "actions": [{"str_to_dict": None}]},
}

PARAMS_PRE_FIX = {
    "record": {"string": "abc"},
    "conversion_rule": {"fieldname": "string", "actions": [{"add_prefix": 123}]},
}

PARAMS_POST_FIX = {
    "record": {"string": "abc"},
    "conversion_rule": {"fieldname": "string", "actions": [{"add_postfix": "def"}]},
}

PARAMS_ADD_VALUE_FROM_FIELD = {
    "record": {"from_field": {"nested": "abc"}},
    "conversion_rule": {
        "fieldname": "to_field",
        "actions": [{"add_value_from_field": "from_field"}],
    },
}

PARAMS_ADD_KEY_VALUE_FROM_FIELD = {
    "record": {"from_field": "abc"},
    "conversion_rule": {
        "fieldname": "to_field",
        "actions": [{"add_key_value_from_field": "from_field"}],
    },
}


PARAMS_ADD_DATA_FROM_DICT = {
    "record": {"from_field": {"abc": {"1": 1, "2": 2}}, "to_field": {"0": 0}},
    "conversion_rule": {
        "fieldname": "to_field",
        "actions": [{"add_data_from_dict": "from_field.abc"}],
    },
}

PARAMS_ADD_KEY_VALUE_FROM_FIELD2 = {
    "record": {"from_field": "abc", "field2": "def"},
    "conversion_rule": {
        "fieldname": "to_field",
        "actions": [{"add_key_value_from_field": ["from_field", "field2"]}],
    },
}

PARAMS_INSERT_KEY = {
    "record": {"from_field": "abc"},
    "conversion_rule": {
        "fieldname": "from_field",
        "actions": [{"insert_key": "inserted_field"}],
    },
}


PARAMS_ADD_VALUE_FROM_NETSED_FIELD = {
    "record": {"from_field": {"nested": "abc"}},
    "conversion_rule": {
        "fieldname": "to_field",
        "actions": [{"add_value_from_field": "from_field.nested"}],
    },
}

PARAMS_FIXED_VALUE = {
    "record": {},
    "conversion_rule": {
        "fieldname": "new_field",
        "actions": [{"fixed_value": "new value"}],
    },
}

PARAMS_DATE_OF_TODAY = {
    "record": {},
    "conversion_rule": {"fieldname": "today", "actions": [{"date_of_today": None}]},
}

PARAMS_CHANGE_KEY_NAME = {
    "record": {"from_field": {"nested": "abc"}},
    "conversion_rule": {
        "fieldname": "from_field",
        "actions": [{"change_key_name_to": "new_name"}],
    },
}

PARAMS_CHANGE_KEY_NAME_NESTED = {
    "record": {"parent_field": {"nested": "abc"}},
    "conversion_rule": {
        "fieldname": "parent_field.nested",
        "actions": [{"change_key_name_to": "parent_field.new_nested"}],
    },
}

PARAMS_LIST_TO_DICT = {
    "record": {"list": [["a", "b"], ["c", "d"]]},
    "conversion_rule": {"fieldname": "list", "actions": [{"list_to_dict": None}]},
}

PARAMS_REMOVE = {
    "record": {"field": "abc", "removed_field": "def"},
    "conversion_rule": {"fieldname": "removed_field", "actions": [{"remove": None}]},
}


PARAMS_REMOVE_NESTED_FIELD = {
    "record": {"field": "abc", "nested": {"removed_field": "def"}},
    "conversion_rule": {
        "fieldname": "nested.removed_field",
        "actions": [{"remove": None}],
    },
}

PARAMS_ALPHA3_TO_ISO3116 = {
    "record": {"cc": "FRA"},
    "conversion_rule": {"fieldname": "cc", "actions": [{"alpha3_to_iso3116_cc": None}]},
}

PARAMS_DIVIDE_BY = {
    "record": {"tx": 123},
    "conversion_rule": {"fieldname": "tx", "actions": [{"divide_by": 10}]},
}

PARAMS_DIVIDE_BY_STR = {
    "record": {"tx": 123},
    "conversion_rule": {"fieldname": "tx", "actions": [{"divide_by": "str"}]},
}

PARAMS_DIVIDE_STR = {
    "record": {"tx": "str"},
    "conversion_rule": {"fieldname": "tx", "actions": [{"divide_by": 10}]},
}

PARAMS_MULTIPLY_BY = {
    "record": {"tx": 1.23},
    "conversion_rule": {"fieldname": "tx", "actions": [{"multiply_by": 10}]},
}

PARAMS_MULTIPLY_BY_STR = {
    "record": {"tx": 123},
    "conversion_rule": {"fieldname": "tx", "actions": [{"multiply_by": "str"}]},
}

PARAMS_MULTIPLY_STR = {
    "record": {"tx": "str"},
    "conversion_rule": {"fieldname": "tx", "actions": [{"multiply_by": 10}]},
}
