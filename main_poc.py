import get_stage_attributes
import read_input_data
from loggerUtility import logger
from utility_functions import get_start_and_end_line_number_of_tc
import integrate_functions
from UserSetiing import DataCollectorPath
import argparse

# Reading test case file name and arguments from command line
# only run if below modules are the entry point to the program. Restricting access to other module
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gitBranch', help='GitBranch , please provide git branch ')
    parser.add_argument('fileName', help='StageName , please provide file name')
    parser.add_argument('testCaseName', help='TestCaseName , please provide test case name')
    args = parser.parse_args()
    git_branch = args.gitBranch
    file_name = args.fileName
    test_case = args.testCaseName
    file_path = f'{DataCollectorPath}/stage/configuration/{file_name}'
    check_error_flag = False
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
    except Exception as error:
        # if any exception occurs above (such as file not found) then this flag will be set to True
        check_error_flag = True
        logger.error(error)
    if not check_error_flag:

        # Extracting the stage attributes from the parametrize statements.
        unique_attributes = get_stage_attributes.get_stage_attributes(tc_lines, test_case, "@pytest.mark.parametrize('stage_attributes'")

        output_from_read_input_data_from_json_file = read_input_data.read_input_data_from_json_file(
            'data/input_data.json', test_case, unique_attributes)
        integrate_functions.integrate_test_case(git_branch, file_name, lines, tc_lines, test_case,
                                                get_start_end_lines_of_tc_in_lines,
                                                output_from_read_input_data_from_json_file)
    else:
        logger.info(f'code generation process did not start.GIT branch {git_branch} is not created.')
