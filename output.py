@rabbitmq
@pytest.mark.parametrize('char_length', [2, 1024])
@pytest.mark.parametrize('stage_attributes', [{'data_format': 'JSON'}])
def test_max_object_length_in_chars(sdc_builder, sdc_executor, stage_attributes, rabbitmq, char_length):
	x = {"name": "John", "age": 30, "city": "New York"}
	input_data = json.dumps(x)
	expected_data = [{'name': 'John', 'age': 30, 'city': 'New York'}]
		rabbitmq_consumer.max_object_length_in_chars = char_length
		if char_length == 2:
			assert sdc_executor.get_stage_errors(consumer_origin_pipeline, rabbitmq_consumer)[0].error_code == \
				   'RABBITMQ_04'
		else:
			output_records = [record.field for record in snapshot[rabbitmq_consumer.instance_name].output]
			assert expected_data == output_records