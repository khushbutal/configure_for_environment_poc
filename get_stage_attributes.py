import re, ast
from utility_functions import check_word


def get_stage_attributes(tc_lines, test_case, word):
    stage_attribute_lines = []
    try:
        pytest_mark_parametrize_lines = check_word(tc_lines, word, False)
        if len(pytest_mark_parametrize_lines[1]) > 1:
            start_sa, end_sa = pytest_mark_parametrize_lines[1][:2]
            stage_attribute_lines = [line.rstrip() for line in tc_lines[start_sa: end_sa]]
            if stage_attribute_lines[len(stage_attribute_lines) - 1] == '':
                stage_attribute_lines = stage_attribute_lines[:len(stage_attribute_lines) - 1]
        elif len(pytest_mark_parametrize_lines[1]) == 1:
            test_case_def_line_num = check_word(tc_lines, test_case, False)[1][0]
            start_sa, end_sa = pytest_mark_parametrize_lines[1][0], test_case_def_line_num
            stage_attribute_lines = [line.rstrip() for line in tc_lines[start_sa: end_sa]]
        stage_attribute_lines = ''.join(stage_attribute_lines)
        start_stage_attributes = stage_attribute_lines.find('[')
        end_stage_attributes = [i.start() for i in re.finditer(']', stage_attribute_lines)][-1]
        sa_line = stage_attribute_lines[start_stage_attributes:end_stage_attributes+1]
        sa_line = ast.literal_eval(sa_line)
        unique_attributes = {}
        for sa in sa_line:
            if 'data_format' not in unique_attributes:
                unique_attributes['data_format'] = set()
                unique_attributes['data_format'].add(sa['data_format'])
            else:
                unique_attributes['data_format'].add(sa['data_format'])
        return unique_attributes
    except:
        pass
