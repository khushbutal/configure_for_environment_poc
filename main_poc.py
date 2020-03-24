import get_stage_attributes
import read_input_data
import sys
from utility_functions import get_start_and_end_line_number_of_tc
import integrate_functions
from UserSetiing import DataCollectorPath

print()

# Reading test case file name and arguments from command line
git_branch, file_name, test_case = sys.argv[1], sys.argv[2], sys.argv[3]
file_path = f'{DataCollectorPath}/stage/configuration/{file_name}'
with open(file_path, 'r') as f:
    lines = f.readlines()
get_start_end_lines_of_tc_in_lines = get_start_and_end_line_number_of_tc(lines, test_case)
_, start_line_no_of_tc_in_lines, end_line_no_of_tc_in_lines = get_start_end_lines_of_tc_in_lines
# Extracting the required lines of test case from the entire file.
tc_lines = lines[start_line_no_of_tc_in_lines:end_line_no_of_tc_in_lines]
len_tc_lines = len(tc_lines)
while len_tc_lines > 0:
    if tc_lines[len_tc_lines-1] == '\n':
        tc_lines.pop(len_tc_lines-1)
    else:
        break
    len_tc_lines -= 1

# Extracting the stage attributes from the parametrize statements.
unique_attributes = get_stage_attributes.get_stage_attributes(tc_lines, test_case, "@pytest.mark.parametrize('stage_attributes'")

doc_string, input_data, parametrize, expected_output, assertion, sa_update = read_input_data.read_input_data_from_json_file(
    'data/input_data.json', test_case, unique_attributes)
integrate_functions.integrate_test_case(git_branch, file_name, lines, tc_lines, test_case,
                                        get_start_end_lines_of_tc_in_lines,
                                        doc_string, input_data, parametrize, expected_output,
                                        assertion, sa_update)