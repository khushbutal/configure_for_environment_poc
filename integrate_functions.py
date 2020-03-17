from utility_functions import get_start_and_end_line_number_of_tc

marker_holder = {'mqtt': 'mqtt_broker'}


def integrate_test_case(file_name, tc_lines, test_case, input_data, parametrize, expected_output, assertion, sa_update):
    test_case_marker = file_name.split('/')[-1].split('_')[1]
    if len(parametrize) > 0:
        extra_arguments = [line.split('(')[1].split(',')[0][1:-1] for line in parametrize.split('\n')]
        extra_arguments_comma_sepa = f", {', '.join(extra_arguments)}"
        parametrize = f'{parametrize}\n'
    else:
        extra_arguments_comma_sepa = ""

    get_start_end_tc_lines = get_start_and_end_line_number_of_tc(tc_lines, test_case)
    test_case_line_num = get_start_end_tc_lines[0]

    marker_test_case_argument = marker_holder[test_case_marker] if test_case_marker in marker_holder else test_case_marker
    # Updating the test case function with the required arguments
    tc_lines[test_case_line_num] = f"{tc_lines[test_case_line_num].split('):')[0]}, {marker_test_case_argument}{extra_arguments_comma_sepa}):\n"

    for line_num in range(len(tc_lines)):
        if tc_lines[line_num] == '@stub\n':
            tc_lines[line_num] = f'@{test_case_marker}\n{parametrize}'
        elif tc_lines[line_num] == '    pass\n':
            tc_lines[line_num] = input_data.rstrip()
    tc_lines.append(expected_output)
    tc_lines.append(sa_update)
    tc_lines.append(assertion)
    with open('output.py', 'w') as output_file:
        for item in tc_lines:
            output_file.write("%s" % item)