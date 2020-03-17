def check_word(lines, word, is_print):
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
        print('test case starting line number: ', start_line_no, lines[start_line_no])
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
    except:
        pass
