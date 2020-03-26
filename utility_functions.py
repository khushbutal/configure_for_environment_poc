import os
import subprocess
from loggerUtility import logger
from UserSetiing import DataCollectorPath


def create_git_branch(gitbranch):
    cwd_path = os.getcwd()
    os.chdir(f'{DataCollectorPath}')
    logger.info(f'creating a git branch {gitbranch}')
    cmd1 = 'git checkout master'
    cmd2 = f'git checkout -b {gitbranch}'
    subprocess.call(cmd1, shell=True)
    # subprocess.call('git reset --hard origin/master', shell=True)
    # subprocess.call('git pull', shell=True)
    result = subprocess.call(cmd2, shell=True)
    if not result:
        logger.info(f'successfully created git branch {gitbranch}')
        # Restoring to cwd path
        os.chdir(cwd_path)
    else:
        raise Exception(f'git branch {gitbranch} already exist')


def check_word(lines, word):
    is_word_found = False
    occurrences = []
    occurrence_lines = []
    line_count = 0
    try:
        for line in lines:
            if word in line:
                is_word_found = True
                occurrences.append(line_count)
                occurrence_lines.append(line)
            line_count += 1
        return is_word_found, occurrences, occurrence_lines
    except Exception as error:
        logger.exception(error)


def get_start_and_end_line_number_of_tc(lines, test_case):
    try:
        if len(check_word(lines, test_case)[1]) == 0:
            return 'skip_test_case'
        start_line_no = check_word(lines, test_case)[1][0]
        intial_start_line_no = start_line_no
        # print('test case starting line number: ', start_line_no, lines[start_line_no])
        # For starting line go up(decrement)
        # print(lines[start_line_no])
        while True:
            # print(lines[start_line_no])
            # Check '    pass\n' in above lines, if found it then stop going up
            if (lines[start_line_no] != '\n' and lines[start_line_no-1] == '\n' and lines[start_line_no-2] == '\n') or \
                    lines[start_line_no-2] == '    pass\n':
                break
            start_line_no -= 1
        end_line_no = intial_start_line_no+1
        # print('end_line_no ', end_line_no)
        # start_line_no += 1
        # print(lines[-5:])

        # Finding ending line
        while True:
            # print(lines[end_line_no])
            # print(lines[end_line_no])

            if end_line_no + 1 == len(lines):
                break
            # lines[end_line_no] = lines[end_line_no].rstrip()
            # print(lines[end_line_no])
            # if lines[end_line_no] != '\n' and lines[end_line_no + 1] == '\n':
            #     break
            if lines[end_line_no] == '@stub\n' or \
                    lines[end_line_no][:len('@pytest.mark')] == '@pytest.mark' or \
                    lines[end_line_no][:len('def test_')] == 'def test_' or \
                    lines[end_line_no][:len('@')] == '@':
                break
            end_line_no += 1

        # print(start_line_no, end_line_no)
        return intial_start_line_no, start_line_no, end_line_no
    except Exception as error:
        logger.exception(error)


def create_doc_string(file_name, test_case, doc_string, pipeline_lines):
    stage_name_doc_string = file_name[5:][:-3].replace('_', ' ')
    test_case_name_doc_string = test_case[5:].replace('_', ' ')
    doc_string_first_line = f'check {stage_name_doc_string} can honour {test_case_name_doc_string} configuration.\n\n\t'
    doc_string_updated = doc_string.replace('"""', '"""' + doc_string_first_line, 1)
    doc_string_final = '\t"' + doc_string_updated[2:].replace('"""', '\n\tpipeline looks like \n\t\t'+ pipeline_lines + '"""', 1)
    return doc_string_final
