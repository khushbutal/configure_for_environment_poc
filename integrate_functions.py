def integrate_test_case(file_name, tc_lines, input_data, expected_output, assertion, sa_update):
    test_case_annotation = file_name.split('/')[-1].split('_')[1]
    for line_num in range(len(tc_lines)):
        if tc_lines[line_num] == '@stub\n':
            tc_lines[line_num] = f'@{test_case_annotation}\n'
        elif tc_lines[line_num] == '    pass\n':
            tc_lines[line_num] = input_data.rstrip()
    tc_lines.append(expected_output)
    tc_lines.append(sa_update)
    tc_lines.append(assertion)
    with open('output.py', 'w') as output_file:
        for item in tc_lines:
            output_file.write("%s" % item)