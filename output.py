@mqtt
@pytest.mark.parametrize('stage_attributes', [{'data_format': 'DELIMITED', 'parse_nulls': False},
                                              {'data_format': 'DELIMITED', 'parse_nulls': True}])
def test_parse_nulls(sdc_builder, sdc_executor, stage_attributes):
	INPUT_DATA = [['header1', 'header2', 'header3'], ['Field11', 'Field12', 'Field13'], ['Field21', 'Field22','Field23']]
	INPUT_DATA_STR = '\n'.join([','.join(line) for line in INPUT_DATA])
	EXPECTED_OUTPUT_NONE = OrderedDict([('header1', None), ('header2', 'Field22'), ('header3', 'Field23')])
	EXPECTED_OUTPUT = OrderedDict([('header1', 'Field21'), ('header2', 'Field22'), ('header3', 'Field23')])
	if stage_attributes['parse_nulls']:
		stage_attributes.update({'null_constant': 'Field21'})
	if stage_attributes['parse_nulls']:
		assert records[1] == EXPECTED_OUTPUT_NONE
	else:
		assert records[1] == EXPECTED_OUTPUT