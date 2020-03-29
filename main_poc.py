# keep the python package and codegen package separate
import argparse
import json
import os

import get_stage_attributes
import read_input_data
import integrate_functions
from loggerUtility import logger
from utility_functions import get_start_and_end_line_number_of_tc, check_word
from UserSetiing import DataCollectorPath
from utility_functions import create_git_branch


# Reading test case file name and arguments from command line
# only run if below modules are the entry point to the program. Restricting access to other module
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('git_branch', help='GitBranch, please provide git branch ')
    parser.add_argument('file_name', help='StageName, please provide file name')
    parser.add_argument('test_cases', nargs='*', help='TestCaseNames, please provide test case name')
    args = parser.parse_args()
    git_branch = args.git_branch
    file_name = args.file_name
    test_cases = args.test_cases

    file_path = f'{DataCollectorPath}/stage/configuration/{file_name}'

    # If no test_cases are provided from command line, then script will check for all the test cases in the file.
    if len(test_cases) == 0:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            all_test_cases = check_word(lines, 'def test')[2]
            all_test_cases = ['test_' + tc.split('(')[0][len('def test') + 1:] for tc in all_test_cases]
            test_cases = all_test_cases
    # Finding valid test cases i.e. test case should be present in both the stage file and input_file.json
    with open('data/input_data.json', "r") as input_file:
        json_data = json.load(input_file)
    invalid_test_cases = list(set(test_cases) - set(list(json_data.keys())))
    # This second condition comes in handy when no test cases passed i.e. we need to check for all the test cases,
    # in case number of invalid_test_cases will be many so we are not logging anything.
    if len(invalid_test_cases) > 0 and len(args.test_cases) > 0:
        logger.info(f'Below test cases are not implemented in input file')
        print(invalid_test_cases)

    valid_test_cases = list(set(test_cases).intersection(set(list(json_data.keys()))))
    test_cases = valid_test_cases
    run_only_once = True
    is_error_occurred_in_creation_of_git_branch = True
    try:
        for test_case in test_cases:
            # Create branch only for valid test cases, i.e. calling create_git_branch function in for loop.
            if run_only_once:
                create_git_branch(git_branch)
                is_error_occurred_in_creation_of_git_branch = False
            # Read the stage file name for every test_case.
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
            integrate_functions.integrate_test_case(run_only_once, file_name, lines, tc_lines,
                                                    test_case, get_start_end_lines_of_tc_in_lines,
                                                    output_from_read_input_data_from_json_file)
            run_only_once = False
    except Exception as error:
        # if any exception occurs above (such as file not found) then this flag will be set to True
        logger.error(error)
        # if any exception occurs above, before this any part of the code already write to file name then, delete the
        # git branch.
        if not is_error_occurred_in_creation_of_git_branch:
            os.chdir(f'{DataCollectorPath}')
            os.system('git checkout -- .')
            os.system('git checkout master')
            os.system(f'git branch -D {git_branch}')
            logger.info(f'git branch {git_branch} has been deleted')
