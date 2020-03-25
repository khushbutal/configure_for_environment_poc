import os
from CodeGenerator import generate_imports_and_pipeline_code, generate_data
from loggerUtility import logger
from utility_functions import create_git_branch
from UserSetiing import DataCollectorPath


def integrate_test_case(gitbranch, file_name, lines, tc_lines, test_case, get_start_end_lines_of_tc_in_lines, doc_string,
                        input_data, parametrize, expected_output, assertion, sa_update):
    file_name_path = f'{DataCollectorPath}/stage/configuration/{file_name}'

    check_flag = create_git_branch(gitbranch)
    if not check_flag:
        try:
            # Updates test case code(tc_lines) like doc_string, input_data, parametrize, etc..
            tc_lines, test_case_line_num_in_tc_lines = generate_data(file_name_path, file_name, lines, tc_lines, test_case,
                                                         get_start_end_lines_of_tc_in_lines, doc_string, input_data,
                                                         parametrize, expected_output, assertion, sa_update)
            generate_imports_and_pipeline_code(file_name_path, test_case, tc_lines, test_case_line_num_in_tc_lines)
        except Exception as error:
            # Delete the created git branch if any exceptions occurs while generating code
            os.system('git checkout master')
            os.system(f'git branch -D {gitbranch}')
            logger.exception(error)
            logger.info(f'git branch {gitbranch} has been deleted')
