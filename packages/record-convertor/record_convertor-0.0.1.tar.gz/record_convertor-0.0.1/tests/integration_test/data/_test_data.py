import json

path = "tests/integration_test/data/"


def itterator_test_data(test_file_name: str):
    """Method to provide an itterator over a list of test_data in a json file

    Test data dicts are to be used for integration tests of ConvertRecord
    module/
    Args:
        test_file_name (str): name and path of json file with test data

    Yields:
        dict: dict containing test data with input, ouput and conversion rules
    """
    with open(path + test_file_name) as json_file:
        data = json.loads(json_file.read())
        for test in data["tests"]:
            yield {
                "input_record": test["input_record"],
                "rules": test["rules"],
                "output_record": test["output_record"],
            }
