import os
from CodeGenerator import generate_imports_and_pipeline_code, generate_data
from loggerUtility import logger
from utility_functions import create_git_branch
from UserSetiing import DataCollectorPath


def integrate_test_case(run_only_once, gitbranch, file_name, lines, tc_lines, test_case, get_start_end_lines_of_tc_in_lines,
                        output_from_read_input_data_from_json_file):
    file_name_path = f'{DataCollectorPath}/stage/configuration/{file_name}'

    tc_lines, test_case_line_num_in_tc_lines = generate_data(file_name_path, file_name, lines, tc_lines,
                                                             test_case, get_start_end_lines_of_tc_in_lines,
                                                             output_from_read_input_data_from_json_file)
    if run_only_once:
        generate_imports_and_pipeline_code(file_name_path, test_case, tc_lines, test_case_line_num_in_tc_lines)
