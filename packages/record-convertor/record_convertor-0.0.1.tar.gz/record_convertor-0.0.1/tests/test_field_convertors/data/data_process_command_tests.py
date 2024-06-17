import jmespath
from jmespath.exceptions import ParseError

from record_convertor.command_processor import ProcessCommand


class AbstractCommand:
    def __init__(self, record, rules):
        self.rules = rules
        self.record = record

    def convert(self):
        raise NotImplementedError

    def _get_field(self, key, rec=None):
        record = rec or self.record
        if key:
            try:
                return jmespath.search(key, record)
            except ParseError:
                pass

        return None


class GetReverseTest(AbstractCommand):
    """test class to test injecting custom field process commands.

    In this example the value for self.rules key field_name will be returned
    im reversed order if it is a string.
    """

    def convert(self):
        value = self._get_field(self.rules["field_name"])
        if isinstance(value, str):
            return value[::-1]
        return None


class ConvertRecordTest(AbstractCommand):
    """
    Test Convert record classm to allow for a single level of recursiveness.

    To be used in tests where the command rule and command args require 0 or 1
    recursive level of record conversion.
    """

    command_class = ProcessCommand

    def convert(self):
        result = {}
        for key, value in self.rules.items():
            if key[0] == "$":
                return self.command_class(
                    record=self.record,
                    process_command=key,
                    process_args=value,
                    record_convertor=ConvertRecordTest(self.record, self.rules),
                ).get_value()

            if isinstance(value, str):
                # setup with None needed to allow result_for_key to be 0
                result_for_key = self._get_field(value)
                if result_for_key is not None:
                    result[key] = result_for_key
                continue
        return result


BASE_PARAMS = {
    "record": {"field1": "a"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$fixed_value",
    "process_args": "the fixed value",
}


PARAMS_GET_FIXED_VALUE = {
    "record": {"field1": "a"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$fixed_value",
    "process_args": "the fixed value",
}


PARAMS_SET_TO_NONE_VALUE = {
    "record": {"field1": "a"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$set_to_none_value",
    "process_args": {},
}

PARAMS_ALLOW_NONE_VALUE_NONE = {
    "record": {"field1": "a"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$allow_none_value",
    "process_args": {"field_name": "non_existing_field"},
}

PARAMS_ALLOW_NONE_VALUE_WITH_VALUE = {
    "record": {"field1": "existing value"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$allow_none_value",
    "process_args": {"field_name": "field1"},
}


PARAMS_NON_EXIST_COMM = {
    "record": {"field1": "a"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$non_existing",
    "process_args": "the fixed value",
}

PARAMS_ADD_COMMANDS = {
    "record": {"field1": "abcdef"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$$reverse",
    "process_args": {"field_name": "field1"},
    "add_process_commands": {"reverse": GetReverseTest},
}

PARAMS_SPLIT_FIELD = {
    "record": {"field1": "index0_index1"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$split_field",
    "process_args": {"field_name": "field1", "seperator": "_", "index": 1},
}

PARAMS_SPLIT_FIELD_NONE = {
    "record": {"field1": "index0_index1"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$split_field",
    "process_args": {"field_name": "field1", "seperator": "_", "index": 3},
}

PARAMS_INT_FROM_STRING = {
    "record": {"field1": "123 456.01 EUR"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$int_from_string",
    "process_args": {"field_name": "field1", "seperators": [" "]},
}

PARAMS_JOIN = {
    "record": {"field1": "abc", "field2": "def"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join",
    "process_args": ["field1", "field2"],
}

PARAMS_JOIN_WITH_SEPERATOR = {
    "record": {"field1": "abc", "field2": "def"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join",
    "process_args": ["$seperator_", "field1", "field2"],
}

PARAMS_JOIN_WITH_SEPERATOR_AND_NONE = {
    "record": {"field1": None, "field2": "def"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join",
    "process_args": ["$seperator ", "field1", "field2"],
}


PARAMS_JOIN_WITH_FIXED_VALUE = {
    "record": {"field1": "abc", "field2": "def"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join",
    "process_args": ["field1", "field2", "$ghij"],
}

PARAMS_JOIN_ERROR = {
    "record": {"field1": "abc", "field2": "def"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join",
    "process_args": "field1",
}

PARAMS_NORM_ADDRESS = {
    "record": {
        "address1": "teding v berkhoutlaan 17",
        "zipcode": "2111ZA",
        "city": "aerdenhout",
        "country": "NL",
    },
    "record_convertor": ConvertRecordTest,
    "process_command": "$normalized_address",
    "process_args": {
        "address": "address1",
        "zip_code": "zipcode",
        "city": "city",
        "iso3116_country_code": "country",
    },
}

PARAMS_NORM_ADDRESS_ERROR = {
    "record": {"zipcode": "2111ZA", "city": "aerdenhout", "country": "NL"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$normalized_address",
    "process_args": {
        "address": "address1",
        "zip_code": "zipcode",
        "city": "city",
        "iso3116_country_code": "country",
    },
}

PARAMS_POINT = {
    "record": {"latitude": "5.1", "longitude": "40.1"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$point",
    "process_args": {"lat": "latitude", "lon": "longitude"},
}

PARAMS_POINT_ERROR1 = {
    "record": {"latitude": "5.1", "longitude": "40.1"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$point",
    "process_args": {"wrong_key": "latitude", "lon": "longitude"},
}

PARAMS_POINT_ERROR2 = {
    "record": {"wrong_key": "5.1", "longitude": "40.1"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$point",
    "process_args": {"lat": "latitude", "lon": "longitude"},
}

PARAMS_FULL_RECORD = {
    "record": {"field1": {"nested_field": {"a": 1}}, "field2": "2"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$full_record",
    "process_args": {},
}

PARAMS_JOIN_KEY_VALUE = {
    "record": {"field1": "key", "field2": "value"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join_key_value",
    "process_args": {
        "key": "field1",
        "value": "field2",
    },
}

PARAMS_JOIN_KEY_VALUE2 = {
    "record": {
        "field1": "key",
        "field1a": "_join",
        "field2": "value",
        "field2a": "_join",
    },
    "record_convertor": ConvertRecordTest,
    "process_command": "$join_key_value",
    "process_args": {
        "key": {"$join": ["field1", "field1a"]},
        "value": {"$join": ["field2", "field2a"]},
    },
}

PARAMS_JOIN_KEY_VALUE_ERROR1 = {
    "record": {"field1": "key", "field2": "value"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join_key_value",
    "process_args": {
        "wrong arg": "field1",
        "value": "field2",
    },
}

PARAMS_JOIN_KEY_VALUE_ERROR2 = {
    "record": {"field2": "value"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join_key_value",
    "process_args": {
        "key": "field1",
        "value": "field2",
    },
}

PARAMS_JOIN_KEY_VALUE_ERROR3 = {
    "record": {"field1": {"test": 1}, "field2": "value"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$join_key_value",
    "process_args": {
        "key": "field1",
        "value": "field2",
    },
}

PARAMS_GET_COORDINATES = {
    "record": {
        "address1": "Teding van Berkhoutlaan",
        "address2": "17",
        "zipcode": "2111ZA",
        "city": "aerdenhout",
        "country": "NL",
    },
    "record_convertor": ConvertRecordTest,
    "process_command": "$get_coordinates",
    "process_args": {
        "address_keys": ["address1", "address2"],
        "zip_code": "zipcode",
        "country_code": "country",
    },
}


PARAMS_TO_LIST = {
    "record": {"field1": 1, "field2": 2},
    "record_convertor": ConvertRecordTest,
    "process_command": "$to_list",
    "process_args": ["field1", "field2"],
}

PARAMS_TO_INT_STRIP_LIST = {
    "record": {"field1": "10.000 eur"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$to_int",
    "process_args": {"field_name": "field1", "strip": ["eur", " ", "."]},
}

PARAMS_TO_INT_STRIP_STR = {
    "record": {"field1": "10.000 eur"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$to_int",
    "process_args": {"field_name": "field1", "strip": "eur"},
}

PARAMS_TO_LIST_DYNAMIC = {
    "record": {"field1": "10.000 eur", "field2": {"nested_field": "9.000 eur"}},
    "record_convertor": ConvertRecordTest,
    "process_command": "$to_list_dynamic",
    "process_args": [{"price1": "field1"}, {"price2": "field2.nested_field"}],
}

PARAMS_FIRST_ITEM_FROM_LIST = {
    "record": {
        "field1": [{"field2": "item1"}, {"field2": "item2"}, {"field2": "item3"}]
    },
    "record_convertor": ConvertRecordTest,
    "process_command": "$first_item_from_list",
    "process_args": {"list_field_name": "field1", "result": "field2"},
}

PARAMS_FIRST_ITEM_FROM_LIST_NONE_RESULT = {
    "record": {
        "field1": [{"field2": "item1"}, {"field2": "item2"}, {"field2": "item3"}]
    },
    "record_convertor": ConvertRecordTest,
    "process_command": "$first_item_from_list",
    "process_args": {"list_field_name": "field1", "result": "field3"},
}

PARAMS_FROM_LIST = {
    "record": {"list1": [{"field1": 1, "field2": 2}, {"field1": 2, "field2": 3}]},
    "record_convertor": ConvertRecordTest,
    "process_command": "$from_list",
    "process_args": {
        "list_field_name": "list1",
        "target_field1": "field1",
        "target_field2": "field2",
    },
}

PARAMS_GET_TIMEZONE = {
    "record": {"loc": {"lat": 52, "lon": 4}},
    "record_convertor": ConvertRecordTest,
    "process_command": "$get_time_zone_from_coordinates",
    "process_args": {
        "lat": "loc.lat",
        "lon": "loc.lon",
    },
}

PARAMS_CURRENT_YEAR = {
    "record": {"field1": "a"},
    "record_convertor": ConvertRecordTest,
    "process_command": "$current_year",
    "process_args": {},
}
