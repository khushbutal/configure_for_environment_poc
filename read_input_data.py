##For reading input data and assertion from the json file.
import json
import get_stage_attributes

# data_formats = ['LOG', 'DELIMITED', 'TEXT', 'JSON', 'SDC_JSON', 'PROTOBUF']

def read_input_data_from_json_file(filename, test_case, unique_attributes):
    with open(filename, "r") as input_file:
        json_data = json.load(input_file)
        for df in unique_attributes['data_format']:
            if df in json_data[test_case]:
                # print('got the data from input file')
                # print(json_data[test_case][df]['input_data'])
                pass
