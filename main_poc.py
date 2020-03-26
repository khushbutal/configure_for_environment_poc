import get_stage_attributes
import read_input_data
from loggerUtility import logger
from utility_functions import get_start_and_end_line_number_of_tc
import integrate_functions
from UserSetiing import DataCollectorPath
import sys
import json

# Reading test case file name and arguments from command line
# only run if below modules are the entry point to the program. Restricting access to other module
if __name__ == '__main__':
    git_branch = sys.argv[1]
    file_name = sys.argv[2]
    test_cases = sys.argv[3:]

    # Finding valid test cases i.e. test case should present in the both stage file and input_file.json
    with open('data/input_data.json', "r") as input_file:
        json_data = json.load(input_file)

    invalid_test_cases = list(set(test_cases) - set(list(json_data.keys())))
    if len(invalid_test_cases) > 0:
        logger.info(f'Below test cases are not implemented in input file')
        print(invalid_test_cases)

    valid_test_cases = list(set(test_cases).intersection(set(list(json_data.keys()))))
    # print(valid_test_cases)
    test_cases = valid_test_cases

    file_path = f'{DataCollectorPath}/stage/configuration/{file_name}'
    run_only_once = True
    for test_case in test_cases:
        try:
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
            unique_attributes = get_stage_attributes.get_stage_attributes(tc_lines, test_case,
                                                                          "@pytest.mark.parametrize('stage_attributes'")

            output_from_read_input_data_from_json_file = read_input_data.read_input_data_from_json_file(
                'data/input_data.json', test_case, unique_attributes)
            integrate_functions.integrate_test_case(run_only_once, git_branch, file_name, lines, tc_lines,
                                                    test_case,
                                                    get_start_end_lines_of_tc_in_lines,
                                                    output_from_read_input_data_from_json_file)
        except Exception as error:
            # if any exception occurs above (such as file not found) then this flag will be set to True
            logger.error(error)
            logger.info(f'code generation process did not start. Git branch {git_branch} is not created.')

        run_only_once = False
