"""Module to provide DateFieldConvertor class.

This class allows you to do a number of date conversions on a record. This is
usually done prior to creating a new record from this existing record, thus
ensuring a well formatted record prior to processing.

Conditions can be included and conversions will only be executed if all
conditions comply.

Availale conversion commands
    - $fixed_value
        Returns the fixed value given in the arguments
    -  $split_field
        Splits a field based upon a given seperator and return a given entry
        (index) from the resulting split list
        Args: field_name (str), seperator (str), index (int)
    - $int_from_string
        returns a numerical value (as a string) from the input string based
        upon the first sequence of numerical charraters found in the string.
        Characters can be removed first by adding them to the list in the
        `seperators` argument.
        '123 456.00 EUR' can be converted to '123456' with seperators arg [' ']
        Args: field_name (str), seperators (list of str)
    - $join
        return a joined set of fields and optionally fixed values with
        optionally a seperator in between the fields
        Args: [list of str] where str's are
            - `$seperatorX' where X is the seperator. Field is optional
               but if used should always be at index 0 of the list
            - <field_name> value will be retrieved from entry in record with
              `field_name`
            - <$fixed_value> value `fixed_value` will be used
    - $normalized_address
        returns a normalized address as string using an external Geo API
        Args: address (str), zip_code (str), city (str),
              iso3116_country_code (str)
            -> all mandatory, representing the (nestred) field in the
               record where the actual values are to be retrieved
    - $point
        returns a geojson Point dict
        Args: lat (str), lon (str)
            ->  all mandatory, representing the (nested) field in the record
                where the actual values are to be retrieved
    - $full_record
        returns the full record
        Args: none
    - $join_key_value
        returns a key value pair from two record field defined in the args.
        If with retrieved values no key value pair can be made None is returned
        Args: key(str), value(str)
            ->  both mandatory, representing the (nested) field in the record
                where the actual values are to be retrieved
    - $get_coordinates
        returns a geoJson point dict representing the address in lon, lat.
        Args: address_keys(list of str), zip_code(str), city (str),
              iso3116_country_code (str)
            -> all are optional representing the (nested) field in the record
               where the actual values are to be retrieved
            -> address field is created by joining the different values for
               retrieved with the list of address_keys
    - $from_list
        returns a list of dicts created from specific fields in a list of dicts
        provided by the record. This method can be used to transform a list
        of dicts into the correct format.
        Args: list_field_name (str) -> key retrieve the input list of dicts
              <keys> (str) -> keys to be used in new list of dicts. Value for
                              this key is retrieved with the value of this key
                              i.e. 'target_field1': 'field1' will result in
                              'target_field1': list_item['field1']
    - $to_list
        returns a list with values retrieved from the record. None values are
        skipped.
        Args: List of keys (str) for which the values need to be returned in
              the return list
    - $to_list_dynamic
        returns a list with the results of the rule sets provided in the input
        list. This allows to create a list of more complex objects
        Args: List of rule dicts that result in the required data objects
              when processed against the input record. Each rule dict will
              result in a single entry in the list
     - $to_int
        returns a string from the record with all strings removed indiacted by
        the `skip` list in the arguments.
        Args: field_name (str) -> field name from where to retrieve the string
              skip (list of str or str) -> strings that need to be removed from
                                           the input string
    - $set_to_none_value
        return a None value

    - $allow_none_value
        retrieves a value from the record but if not found leaves a None value
        instead of skipping the field

    - $current_year
        sets the field value to the current year as a str
"""

import re
from datetime import datetime
from typing import Union

import jmespath
from jmespath.exceptions import ParseError

from .command_helper import (
    lat_lon_to_geojson_point,
    process_args_is_dict,
    process_args_is_list,
)

__all__ = ["ProcessCommand"]


class ProcessCommand:
    """
    Class to create a value for the output record, mostly based upon one or
    more fields from the input record.

    args:
        record (dict): record that needs some conversion action
        process_command (str) : process command to be executed to obtain the
                                correct value from the record
        process_args (str, dict) : arguments needed to run the process command
        add_process_commands (dict) : dict with process names and custom
                                      lambda's


    returns:
        value (dict, list, str, int, float): output of teh conversion
    """

    def __init__(
        self,
        record: dict,
        process_command: str,
        process_args: Union[dict, list, str],
        record_convertor,
        add_process_commands=None,
    ):
        self.record = record
        # remove the `$` from the command
        self.process_command = process_command[1:]
        self.process_args = process_args
        self.record_convertor = record_convertor
        self.add_process_commands = add_process_commands or {}

    def current_year(self):
        """Returns current year in 4 decimals"""
        return str(datetime.now().year)

    def set_to_none_value(self):
        """Returns None value"""
        return None

    def allow_none_value(self):
        """Returns value for field and None if no field can be found"""
        process_args = process_args_is_dict(self.process_args)

        return self._get_field(process_args.get("field_name"), None)

    def to_list(self):
        """
        retrieve the values for a list of fields and returns them as a list
        """
        process_args = process_args_is_list(self.process_args)
        return list(
            filter(
                None,
                [self._get_field(field_name) for field_name in process_args],
            )
        )

    def to_int(self):
        """turn a string into an int"""
        process_args = process_args_is_dict(self.process_args)
        field_name = process_args.get("field_name")
        amount = self._get_field(field_name)
        if not amount:
            return None
        remove_list = process_args.get("strip", None)
        if isinstance(remove_list, (str, int)):
            remove_list = [str(remove_list)]
        for item in remove_list:
            amount = amount.replace(item, "")
        return amount

    def first_item_from_list(self):
        items_from_list = self.from_list()
        if items_from_list:
            return items_from_list[0]
        return None

    def from_list(self):
        """
        converts a list of dicts from the input record to a new cleaned list of
        dicts
        """
        process_args = process_args_is_dict(self.process_args)

        rules = process_args.copy()
        obj_list = self._get_field(rules.pop("list_field_name"))

        if not (obj_list and isinstance(obj_list, list)):
            return []

        return list(
            filter(
                None,
                [
                    self.record_convertor(rules=rules, record=obj).convert()
                    for obj in obj_list
                ],
            )
        )

    def to_list_dynamic(self):
        return list(
            filter(
                None,
                [
                    self.record_convertor(rules=rule, record=self.record).convert()
                    for rule in self.process_args
                ],
            )
        )

    def join_key_value(self):
        process_args = process_args_is_dict(self.process_args)
        key_key = process_args.get("key", False)
        value_key = process_args.get("value", False)
        if not (key_key and value_key):
            raise KeyError("Missing `key` or `value` argument")

        # check if key value needs to be composed
        if isinstance(key_key, dict):
            key = self.record_convertor(rules=key_key, record=self.record).convert()
        else:
            key = self._get_field(key_key)

        # check if value value needs to be composed
        if isinstance(value_key, dict):
            value = self.record_convertor(rules=value_key, record=self.record).convert()
        else:
            value = self._get_field(value_key)

        if key and value:
            try:
                return {key: value}
            except (TypeError, KeyError):
                return None

    def key_value(self):
        process_args = process_args_is_dict(self.process_args)

        key = process_args.get("key", False)
        value = process_args.get("value", False)
        if not (key and value):
            raise KeyError("Missing `key` or `value` argument")
        return {key: self._get_field(value)}

    def full_record(self):
        """returns the full record"""
        return self.record

    def point(self):
        """
        Retrieves lat, lon fields from record and returns them in point format.
        """
        process_args = process_args_is_dict(self.process_args)

        # check if lat and lon field names are provided in the value
        lat_field = process_args.get("lat", False)
        lon_field = process_args.get("lon", False)
        if not (lat_field and lon_field):
            raise ValueError("Both lat and lon field required for Point Field")

        # get the lattitude and longitude from the record and return point
        # field
        lat = self._get_field(lat_field)
        lon = self._get_field(lon_field)
        return lat_lon_to_geojson_point(latitude=lat, longitude=lon)

    def join(self):
        """
        joins the record values for the list of keys to a single string
        """

        def join_value(key):
            """
            Return the actual value (string) that belongs to the given key
            """
            # check if fixed value needs to be returned
            if key[0] == "$":
                return key[1:]
            # if not fixed value then return the value that belongs to the
            # given (nested) key(s)
            res = self._get_field(key)
            return "" if res is None else str(res)

        if not isinstance(self.process_args, list):
            raise ValueError("provided list of keys is not of type list")

        seperator = ""
        # set seperator if defined and remove it from the list of keys
        if "$seperator" in self.process_args[0]:
            seperator = self.process_args.pop(0)[-1]

        try:
            return seperator.join(
                [join_value(key) for key in self.process_args]
            ).strip()
        except KeyError:
            return None

    def int_from_string(self):
        """
        returns the value represented in a string in a string format
        """
        process_args = process_args_is_dict(self.process_args)

        seperators = process_args.get("seperators", False)
        field_name = process_args.get("field_name", False)
        if not (seperators and field_name):
            return None

        field_value = self._get_field(field_name)
        if not isinstance(field_value, str):
            return None

        for seperator in seperators:
            field_value = field_value.replace(seperator, "")
        match = re.search(r"\d+", field_value)
        return match.group() if match else None

    def split_field(self):
        """
        Split the requested field and returns a specific entry from the split
        result
        """
        process_args = process_args_is_dict(self.process_args)

        seperator = process_args.get("seperator", False)
        field_name = process_args.get("field_name", False)
        index = process_args.get("index", False)
        if not (seperator and field_name and (index is not False)):
            return None
        field_value = self._get_field(field_name)

        if field_value is None:
            return None

        try:
            return field_value.split(seperator)[index]
        except (IndexError, AttributeError):
            return None

    def fixed_value(self):
        """return the (fixed) value given in the conversion args"""
        return self.process_args

    def get_value(self):
        """calls the actual process command

        first command is looked up in default commands.
        If not found there it is looked up in custom commands

        """
        if self.process_command in dir(self):
            return getattr(self, self.process_command)()

        cust_command = self.process_command[1:]
        cust_comm_class = self.add_process_commands.get(cust_command, None)

        if cust_comm_class:
            return cust_comm_class(self.record, self.process_args).convert()

        raise NotImplementedError(f"Field conversion command `{self.process_command}`")

    def _get_field(self, key, rec=None):
        record = rec or self.record

        if key:
            # key elemenets in nested keys are surround with "". For exmample
            # key.example-1 becomes "key"."example-1".
            # Needed for jmespath can hande special characters in the keys
            nested_keys = key.split(".")
            nested_key = ".".join(['"' + key + '"' for key in nested_keys])
            try:
                return jmespath.search(nested_key, record)
            except ParseError:
                pass

        return None
