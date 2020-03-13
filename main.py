import get_stage_attributes
import read_input_data
import sys
from utility_functions import get_start_and_end_line_number_of_tc

try:
    print()
    file_name = sys.argv[1]
    test_case = sys.argv[2]
    with open(file_name, 'r') as f:
        lines = f.readlines()
    get_start_end_lines = get_start_and_end_line_number_of_tc(lines, test_case)
    # if get_start_end_lines == 'skip_test_case':
    #     return
    start_line_no, end_line_no = get_start_end_lines
    # Extract test case lines from all the lines
    tc_lines = lines[start_line_no: end_line_no]
    unique_attributes = get_stage_attributes.get_stage_attributes(tc_lines, test_case, "@pytest.mark.parametrize('stage_attributes'")
    print(unique_attributes)
except:
    pass


# Integrating the input data
# print(read_input_data.read_input_data_from_json_file('input_data.json', test_case))
# print('mainnnnnnnnnnnnnnn')
read_input_data.read_input_data_from_json_file("input_data.json", test_case, unique_attributes)