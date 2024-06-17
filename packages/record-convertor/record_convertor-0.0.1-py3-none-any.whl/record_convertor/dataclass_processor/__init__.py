"""
This module provides functionality for using a dataclasses to generate a dict by using
an input record and a set of rules. The rules determine how the input record will be
convertod so that the dataclass instance can be generated. The dataclass might hold
internal methods that can be called based upon the rules with arguments also based upon
the rules.

The class support regestering custom dataclasses to be used.

The class uses an injected record convertor to process the input record bases upon the
provided rules.
"""

from dataclasses import asdict, is_dataclass
from typing import Any, Type

from pydantic import BaseModel

from ..package_settings import (
    DataclassInstance,
    DataClassRuleDict,
    DataClassRuleKeys,
    RecordConvertorProtocol,
    class_name_in_snake_case,
)


def _is_dataclass(dataclass: type) -> bool:
    """
    Helper method to check if a class is a dataclass.
    Returns True for default python dataclasses and Pydantic dataclasse.
    Returns False in al other cases.
    """
    if is_dataclass(dataclass):
        return True
    if issubclass(dataclass, BaseModel):
        return True
    return False


def _asdict(dataclass) -> dict:
    if is_dataclass(dataclass):
        return asdict(dataclass)
    if isinstance(dataclass, BaseModel):
        return dataclass.model_dump()
    raise TypeError(f"Class {dataclass.__name__} is not a dataclass of a Pydantic c")


class DataClassProcessor:
    """
    Processes dataclasses by applying a set of rules and converting dictionaries to
    dataclass instances.

    This class provides methods to register dataclasses, apply conversion and
    transformation rules, and generate dataclass instances from dictionaries.
    It is designed to work with a customizable set of rules and leverages a protocol
    for converting records to dataclass-compatible formats.
    """

    def data_from_dataclass(
        self,
        record: dict,
        rules: DataClassRuleDict,
        record_convertor: RecordConvertorProtocol,
    ) -> dict:
        """
        Uses a record as input to return a dict created by a dataclass. The dataclass in
        socpe is defined in the rules dict as well as how to convert the input record
        to be converted before is used to create the dataclass instance.

        Args:
            record (dict):
                The input dict used to create the dataclass instance (after conversion).
            rules (DataClassRuleDict):
                The rules to apply during the conversion of the input dict and the
                creation of the dataclass instance.
            record_convertor (RecordConvertorProtocol):
                The record convertor to use for data preparation.

        Returns:
            dict: The converted dataclass instance as a dictionary.
        """
        self._record = record
        self._record_covertor = record_convertor
        self._prepare_dataclass_settings(rules=rules)
        return self._create_return_dict()

    def register_dict_of_data_classes(
        self, dataclasses: dict[str, Type[DataclassInstance]]
    ):
        """
        Registers multiple dataclasses provided in a dictionary where keys are the
        dataclass names.

        Args:
            dataclasses (dict[str, Type[DataclassInstance]]):
                A dictionary of dataclass names to dataclass types.
        """
        for dataclass_name, dataclass in dataclasses.items():
            self._register_dataclass(dataclass_name=dataclass_name, dataclass=dataclass)

    def register_data_classes(self, dataclasses: list[Type[DataclassInstance]]):
        """
        Registers a list of dataclasses.

        Args:
            dataclasses (list[Type[DataclassInstance]]):
                A list of dataclass types to register.
        """
        for dataclass in dataclasses:
            self.register_dataclass(dataclass=dataclass)

    def register_dataclass(self, dataclass: Type[DataclassInstance]):
        """
        Registers a single dataclass.

        Args:
            dataclass (Type[DataclassInstance]): The dataclass type to register.
        """
        data_class_name_snake_case = class_name_in_snake_case(dataclass.__name__)
        self._register_dataclass(
            dataclass_name=data_class_name_snake_case, dataclass=dataclass
        )

    def _register_dataclass(
        self, dataclass_name: str, dataclass: Type[DataclassInstance]
    ):
        """
        Registers a dataclass by setting it as an attribute of the processor instance.

        Args:
            dataclass_name (str): The name of the dataclass to register.
            dataclass (Type[DataclassInstance]): The dataclass type.

        Raises:
            ValueError: If the provided class is not a dataclass.
        """
        if not _is_dataclass(dataclass):
            raise ValueError(f"class '{dataclass.__name__}' is not a dataclass")
        setattr(self, dataclass_name, dataclass)

    def _prepare_dataclass_settings(self, rules: DataClassRuleDict):
        """
        Prepares settings for dataclass processing being
        - rule set
        - arguments for the intial record conversion
        - methods and arguments to be run on the dataclass instance
        """
        self._set_dataclass_to_use(rules)
        self._set_record_covertor_arguments(rules)
        self._set_dataclass_methods(rules)

    def _set_record_covertor_arguments(self, rules: DataClassRuleDict):
        """Set arguments for the intial record conversion."""
        self._record_convertor_args: dict = rules.get(
            DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS, {}
        )

    def _set_dataclass_methods(self, rules: DataClassRuleDict):
        """
        Set methods and their arguments to be used after the dataclass has been created.
        """
        self._data_class_methods: list[dict[str, Any]] = (
            rules.get(
                DataClassRuleKeys.METHODS  # type: ignore
            )
            or []
        )

    def _set_dataclass_to_use(self, rules: DataClassRuleDict):
        """Select the dataclass to be used from the registered dataclasses."""
        data_class_name = rules[DataClassRuleKeys.NAME]
        try:
            self._dataclass_to_be_used: Type = getattr(self, data_class_name)
        except AttributeError:
            raise ValueError(f"Unknown dataclass '{data_class_name}' defined in rules")

    def _get_dataclass_content(self) -> dict:
        """Convert input record into dict that can be be used byu the dataclass."""
        dataclass_content_creator = (
            self._record_covertor.get_record_convertor_copy_with_new_rules(
                new_rules=self._record_convertor_args
            )
        )
        return dataclass_content_creator.convert(record=self._record)

    def _create_return_dict(self) -> dict:
        """Create dict record to be returned."""
        dataclass_content = self._get_dataclass_content()
        dataclass_instance = self._get_dataclass_instance(dataclass_content)
        return _asdict(dataclass_instance)

    def _get_dataclass_instance(self, dataclass_content: dict) -> DataclassInstance:
        """Create the dataclass instance and initiate the methods to be run."""
        dataclass_instance = self._dataclass_to_be_used(**dataclass_content)
        dataclass_instance = self._update_dataclass_with_provided_methods(
            dataclass_instance
        )
        return dataclass_instance

    def _update_dataclass_with_provided_methods(
        self, dataclass_instance: DataclassInstance
    ) -> DataclassInstance:
        """Execute each method on the data class."""
        for method_dict in self._data_class_methods:
            [[method, method_argument_rules]] = method_dict.items()
            method_arguments = self._get_method_arguments(method_argument_rules)
            for method_argument in method_arguments:
                getattr(dataclass_instance, method)(**method_argument)  # type: ignore
        return dataclass_instance

    def _get_method_arguments(
        self, method_argument_rules: dict
    ) -> list[dict[str, Any]]:
        """Retrieve method arguments from the method rules."""
        method_arguments = (
            self._record_covertor.get_record_convertor_copy_with_new_rules(
                new_rules=method_argument_rules
            ).convert(self._record)
        )
        return (
            method_arguments
            if isinstance(method_arguments, list)
            else [method_arguments]
        )
