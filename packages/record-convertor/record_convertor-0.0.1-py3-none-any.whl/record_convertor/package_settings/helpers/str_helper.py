import re

__all___ = ["class_name_in_snake_case"]


def class_name_in_snake_case(name: str) -> str:
    """
    Transfrom class name to python variable (snake case) format.

    i.e MyTestClass -> my_test_class
    """
    name = re.sub(
        "(.)([A-Z][a-z]+)", r"\1_\2", name
    )  # Before each capital letter except the first one, if it's at the beginning.
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
