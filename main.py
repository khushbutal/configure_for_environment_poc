import get_stage_attributes
import read_input_data
import sys
from utility_functions import get_start_and_end_line_number_of_tc
import integrate_functions

try:
    print()

    # Reading test case file name and arguments from command line
    file_name = sys.argv[1]
    test_case = sys.argv[2]
    with open(file_name, 'r') as f:
        lines = f.readlines()
    get_start_end_lines = get_start_and_end_line_number_of_tc(lines, test_case)
    test_case_line_num, start_line_no, end_line_no = get_start_end_lines
    # Extracting the required lines of test case from the entire file.
    tc_lines = lines[start_line_no: end_line_no]
    len_tc_lines = len(tc_lines)
    while  len_tc_lines > 0:
        if tc_lines[len_tc_lines-1] == '\n':
            tc_lines.pop(len_tc_lines-1)
        else:
            break
        len_tc_lines -= 1
    unique_attributes = get_stage_attributes.get_stage_attributes(tc_lines, test_case, "@pytest.mark.parametrize('stage_attributes'")
    print(unique_attributes)
except:
    pass

input_data, parametrize, expected_output, assertion, sa_update = read_input_data.read_input_data_from_json_file("input_data.json", test_case, unique_attributes)

integrate_functions.integrate_test_case(file_name, tc_lines, test_case, input_data, parametrize, expected_output, assertion, sa_update)