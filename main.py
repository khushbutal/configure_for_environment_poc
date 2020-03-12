import get_stage_attributes
import read_input_data
import sys

try:
    print()
    file_name = sys.argv[1]
    test_case = sys.argv[2]
    with open(file_name, 'r') as f:
        lines = f.readlines()
    unique_attributes = get_stage_attributes.all_fns_in_one_fn(lines, test_case)
except:
    pass


# Integrating the input data
# print(read_input_data.read_input_data_from_json_file('input_data.json', test_case))
read_input_data.read_input_data_from_json_file("input_data.json", test_case, unique_attributes)