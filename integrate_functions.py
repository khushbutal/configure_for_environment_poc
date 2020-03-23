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

# maintaining a dictionary for keeping the stage holders that would be passed to the function arguments
marker_holder = {'mqtt': 'mqtt_broker'}


def integrate_test_case(gitbranch, file_name, lines, tc_lines, test_case, get_start_end_lines_of_tc, input_data, parametrize,
                        expected_output, assertion, sa_update):
    file_name_path = f'{DataCollectorPath}/stage/configuration/{file_name}'
    test_case_marker = file_name.split('/')[-1].split('_')[1]

    os.chdir(f'{DataCollectorPath}')
    logger.info(f'creating a git branch {gitbranch}')
    print(os.getcwd())
    cmd1 = 'git checkout master'
    cmd2 = f'git checkout -b {gitbranch}'
    subprocess.call(cmd1, shell=True)
    subprocess.call('git reset --hard origin/master', shell=True)
    subprocess.call('git pull', shell=True)
    result = subprocess.call(cmd2, shell=True)
    if not result:
        logger.info(f'successfully created git branch {gitbranch}')
        logger.info("generating code")
        # generate_code(gitbranch, file_name, test_case)

    # Remove the original test case lines
    # print(get_start_end_lines_of_tc)
    test_case_line_num, start_line_no_of_tc, end_line_no_of_tc = get_start_end_lines_of_tc
    del lines[start_line_no_of_tc:end_line_no_of_tc]

    if len(parametrize) > 0:
        extra_arguments = [line.split('(')[1].split(',')[0][1:-1] for line in parametrize.split('\n')]
        extra_arguments_comma_sepa = f", {', '.join(extra_arguments)}"
        parametrize = f'{parametrize}\n'
    else:
        extra_arguments_comma_sepa = ""

    # print('trtttttttttttttttttttttttttttttttttttttttttttttttttttt')
    # print(tc_lines)
    # print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    test_case_line_num = get_start_and_end_line_number_of_tc(tc_lines, test_case)[0]

    marker_test_case_argument = marker_holder[test_case_marker] if test_case_marker in marker_holder else test_case_marker
    # Updating the test case function with the required arguments
    tc_lines[test_case_line_num] = f"{tc_lines[test_case_line_num].split('):')[0]}, {marker_test_case_argument}{extra_arguments_comma_sepa}):\n"

    # Replacing the default test case lines with the updated code.
    for line_num in range(len(tc_lines)):
        if tc_lines[line_num] == '@stub\n':
            tc_lines[line_num] = f'@{test_case_marker}\n{parametrize}'
        elif tc_lines[line_num] == '    pass\n':
            tc_lines[line_num] = input_data.rstrip()
    tc_lines.append(expected_output)
    tc_lines.append(sa_update)
    # generates body code inside test case
    body_code_object = Body_code(file_name, tc_lines[test_case_line_num])
    body_code = body_code_object.get_body_code()
    body_code_lines = body_code.split('\n')
    finally_line_num = check_word(body_code_lines, '    finally:', False)[1][0]
    # print(finally_line_num)
    body_code_lines[finally_line_num] = assertion + '\n' + body_code_lines[finally_line_num]
    body_code = '\n'.join(body_code_lines)
    tc_lines.append(body_code)
    # tc_lines.append(assertion)

    # Adding modified tc_lines into the lines(original)
    final_tc_lines = lines[:start_line_no_of_tc] + tc_lines + ['\n\n\n'] + lines[start_line_no_of_tc:]
    # print(final_tc_lines)

    with open(file_name_path, 'w') as output_file:
        for item in final_tc_lines:
            output_file.write("%s" % item)

    build_pipeline_code = ''
    import_object = Import(file_name)
    import_library = import_object.import_library()
    for line in fileinput.FileInput(file_name_path, inplace=1):
        # import all libraries
        if 'import pytest' in line:
            line = line.rstrip()
            line = line.replace(line, f'{import_library}')
            # not writing if line is equal to specified one .Already handled during library import
        if line.strip("\n") != "from streamsets.testframework.decorators import stub":
            sys.stdout.write(line)
    # opening the file in append mode to append pipeline builder code to the file
    with open(file_name_path, 'a+') as f:
        pipeline_builder_object = PipelineBuilderCode(file_name, tc_lines[test_case_line_num])
        build_pipeline = pipeline_builder_object.build_pipeline()
        build_pipeline_code = build_pipeline
        f.write(build_pipeline_code)
    # setting global variable at the top if the test case or file need to set it
    global_object = GlobalVariable(file_name_path, test_case, file_name)
    global_object.set_global_variable()
    logger.info("successfully generated code ")
