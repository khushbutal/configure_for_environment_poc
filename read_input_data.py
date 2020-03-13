import json

def read_input_data_from_json_file(filename, test_case, unique_attributes):
    with open(filename, "r") as input_file:
        json_data = json.load(input_file)
        for df in unique_attributes['data_format']:
            if df in json_data[test_case]:
                return json_data[test_case][df]['input_data'], json_data[test_case][df]['expected_output'], json_data[test_case][df]['assertion'], \
                       json_data[test_case][df]['sa_update']
