# keep the python package and codegen package separate
import json
import os


def read_input_data_from_json_file(filename, test_case):
    input_data_values = {'doc_string': '', 'input_data': '', 'parametrize': '', 'expected_output': '',
                         'assertion': '', 'sa_update': ''}
    with open(filename, "r") as input_file:
        json_data = json.load(input_file)
        if test_case in json_data:
            input_data_values = iterate_json_data(json_data[test_case], input_data_values)
            return input_data_values
        else:
            raise ValueError(f'Test case {test_case} is not found in input file')


def iterate_json_data(json_data, input_data_values):
    for key, value in json_data.items():
        if isinstance(value, dict):
            iterate_json_data(value, input_data_values)
        else:
            if key in input_data_values:
                input_data_values[key] += value
    return input_data_values
