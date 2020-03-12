import re, ast
def check_word(lines, word, is_print):
    # print(lines)
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
        if not is_word_found and is_print:
            print(f'\t\x1b[1;31m{word} \x1b[0mis not found')
        return is_word_found, occurrences, occurrence_lines
    except:
        pass


def get_start_and_end_line_number_of_tc(lines, test_case):
    try:
        # print(test_case)
        # If test case name is not found in the file just return
        # print(check_word(lines, test_case, False))
        if len(check_word(lines, test_case, False)[1]) == 0:
            return 'skip_test_case'
        start_line_no = check_word(lines, test_case, False)[1][0]
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
        return start_line_no, end_line_no
    except:
        pass


def check_stage_attribute_lines_should_not_modified(tc_lines, test_case, word):
    stage_attribute_lines = []
    try:
        if True:
            # print(check_word(tc_lines, 'pytest.mark.parametrize', False))
            pytest_mark_parametrize_lines = check_word(tc_lines, word, False)
            # print(pytest_mark_parametrize_lines)
            if len(pytest_mark_parametrize_lines[1]) > 1:
                start_sa, end_sa = pytest_mark_parametrize_lines[1][:2]
                stage_attribute_lines = [line.rstrip() for line in tc_lines[start_sa: end_sa]]
                if stage_attribute_lines[len(stage_attribute_lines) - 1] == '':
                    stage_attribute_lines = stage_attribute_lines[:len(stage_attribute_lines) - 1]
                # print(stage_attribute_lines)
                # final_stage_attribute_lines = stage_attribute_lines
                # print(len(stage_attribute_lines))
            elif len(pytest_mark_parametrize_lines[1]) == 1:
                # print(check_word(tc_lines, test_case, False))
                test_case_def_line_num = check_word(tc_lines, test_case, False)[1][0]
                start_sa, end_sa = pytest_mark_parametrize_lines[1][0], test_case_def_line_num
                # print(start_sa, end_sa)
                stage_attribute_lines = [line.rstrip() for line in tc_lines[start_sa: end_sa]]
                # print(stage_attribute_lines)

            # print(stage_attribute_lines)
            # print(len(stage_attribute_lines))
            stage_attribute_lines = ''.join(stage_attribute_lines)
            start_stage_attributes = stage_attribute_lines.find('[')
            end_stage_attributes = [i.start() for i in re.finditer(']', stage_attribute_lines)][-1]
            sa_line = stage_attribute_lines[start_stage_attributes:end_stage_attributes+1]
            sa_line = ast.literal_eval(sa_line)
            # print(sa_line)
            unique_attributes = {}
            for sa in sa_line:
                if 'data_format' not in unique_attributes:
                    unique_attributes['data_format'] = set()
                    unique_attributes['data_format'].add(sa['data_format'])
                else:
                    unique_attributes['data_format'].add(sa['data_format'])
            return unique_attributes
            # print(type(stage_attribute_lines[start_stage_attributes:end_stage_attributes+1]))


    except:
        # print('in except')
        pass


def all_fns_in_one_fn(lines, test_case):
    try:
        get_start_end_lines = get_start_and_end_line_number_of_tc(lines, test_case)
        # print('starting')
        if get_start_end_lines == 'skip_test_case':
            return
        start_line_no, end_line_no = get_start_end_lines
        # Extract test case lines from all the lines
        tc_lines = lines[start_line_no:end_line_no]
        # print(lines[start_line_no], lines[end_line_no])
        # print(start_line_no, end_line_no)
        # print(tc_lines)
        ###### Some fields should not be changed   Ex: stage_attributes in test case
        return check_stage_attribute_lines_should_not_modified(tc_lines, test_case, "@pytest.mark.parametrize('stage_attributes'")
    except:
        pass