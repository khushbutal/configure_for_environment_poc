from utility_functions import get_start_and_end_line_number_of_tc, check_word
import fileinput
import os
import sys
import subprocess
from UserSetiing import DataCollectorPath
from TestCaseBodyCode import Body_code
from pipelineBuilderCode import PipelineBuilderCode
from LibraryImporter import Import
from loggerUtility import logger
from global_variable_initializers.GlobalVariableInitializer import GlobalVariable
from shellExecutor import create_git_branch
from CodeGenerator import generate_imports_and_pipeline_code, generate_data

# maintaining a dictionary for keeping the stage holders that would be passed to the function arguments
marker_holder = {'mqtt': 'mqtt_broker'}


def integrate_test_case(gitbranch, file_name, lines, tc_lines, test_case, get_start_end_lines_of_tc, input_data, parametrize,
                        expected_output, assertion, sa_update):
    file_name_path = f'{DataCollectorPath}/stage/configuration/{file_name}'

    create_git_branch(gitbranch, file_name, test_case)

    tc_lines, test_case_line_num = generate_data(file_name_path, file_name, lines, tc_lines, test_case,
                                                 get_start_end_lines_of_tc, input_data,
                                                 parametrize,
                                                 expected_output, assertion, sa_update)

    generate_imports_and_pipeline_code(file_name_path, test_case, tc_lines, test_case_line_num)
