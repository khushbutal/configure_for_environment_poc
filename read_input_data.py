import json


def read_input_data_from_json_file(filename, test_case, unique_attributes):
    input_data, parametrize, expected_output, assertion, sa_update = "", "", "", "", ""
    run_only_once = True
    with open(filename, "r") as input_file:
        json_data = json.load(input_file)
        if test_case in json_data:
            for df in sorted(list(unique_attributes['data_format'])):
                if df in json_data[test_case]:
                    input_data_tmp = json_data[test_case][df]['input_data']
                    expected_output_tmp = json_data[test_case][df]['expected_output'] if 'expected_output' in json_data[test_case][df] else ""
                    assertion_tmp = json_data[test_case][df]['assertion'] if 'assertion' in json_data[test_case][df] else ""
                    sa_update_tmp = json_data[test_case][df]['sa_update'] if 'sa_update' in json_data[test_case][df] else ""

                    input_data += input_data_tmp
                    if run_only_once:
                        doc_string = json_data[test_case][df]['doc_string']
                        parametrize = json_data[test_case][df]['parametrize'] if 'parametrize' in json_data[test_case][df] else ""
                        run_only_once = False
                    expected_output += expected_output_tmp
                    assertion += assertion_tmp
                    sa_update += sa_update_tmp
            return doc_string, input_data, parametrize, expected_output, assertion, sa_update
        else:
            raise ValueError(f'Test case {test_case} is not found in input file')
