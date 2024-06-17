"""
Module to provide a YAML reader including validation.

Classes:
    RulesFromDict: Creates a rule dictionary from a dict
"""

from typing import Dict, Union


class RulesFromDict:
    """
    Class to create a rule dictionary from a YAML file.

    This class reads a YAML file and converts it into a dictionary. It includes
    error handling for YAML syntax issues and provides access to the resulting
    dictionary through a property.

    Attributes:
        RULE_SOURCE_TYPE (str): Type hint for the rule source file name.

    Parameters:
        rule_source (RULE_SOURCE_TYPE): The filename, including path, of the YAML file.

    Raises:
        ValueError: If trying to access the rules property when the YAML file
                    has been invalidated due to an exception.

    Properties:
        rules (dict): Returns a dictionary representation of the YAML file.
    """

    RULE_SOURCE_TYPE = dict

    def __init__(self, rule_source: Union[str, dict]):
        """
        Initializes the RulesFromYAML object with a YAML file source.

        Args:
            rule_source (str):
                The filename, including path, of the YAML file.
        """
        if type(rule_source) is not self.RULE_SOURCE_TYPE:
            raise TypeError(f"rule_source not of type {self.RULE_SOURCE_TYPE}")

        self._rule_source = rule_source
        self._dict: Dict = {}
        self._error: Union[bool, str] = False
        self._convert_rule_source_to_rule_dict()

    @property
    def rules(self) -> dict:
        """
        Gets the dictionary formed from the YAML file.

        This property provides access to the dictionary representation of the
        YAML file, ensuring that the file has been successfully parsed without
        errors.

        Returns:
            dict: The dictionary containing the rules from the YAML file.

        Raises:
            ValueError: If the YAML file contains errors or cannot be parsed.
        """
        if self._error:
            raise ValueError(
                "Attempting to access rules property failed due to an error ",
                f" in the YAML file: {self._error}",
            )

        return self._dict

    def _convert_rule_source_to_rule_dict(self) -> None:
        """
        Converts the YAML file to a dictionary.

        This method attempts to parse the YAML file specified by the rule_source
        attribute and convert it into a dictionary. If the YAML file cannot be
        parsed, the _error attribute is set with the error message.
        """
        self._dict = dict(self._rule_source)
