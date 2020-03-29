# keep the python package and codegen package separate
import os
import sys

class Body_code:
    def __init__(self, file_name, function):
        self.file_name = file_name
        self.line = function
        self.input_data = ''

    def get_body_code(self):
        # with open(os.path.join(sys.path[0], 'test_case.txt'), 'r') as f:
        #     name_of_test_case = f.read().splitlines()
        # for line in name_of_test_case:
        #     if line in self.line:
        #         with open(os.path.join(sys.path[0], f'{line}.txt'), 'r') as f:
        #             self.input_data = f.read()

        # if there is stage_attributes we pass the same into pipeline builder function to set it
        # stage_attributes = ', **stage_attributes' if 'stage_attributes' in self.line else ""
        stage_attributes = ', **stage_attributes'
        if self.file_name == 'test_mqtt_subscriber_origin.py':
            defualt_stage_attributes = """
    stage_attributes={'topic_filter':data_topic}"""
            set_attribute = "stage_attributes.update({'topic_filter':[data_topic]})" if 'stage_attributes' in self.line else defualt_stage_attributes
            line = f"""{self.input_data}
    data_topic = 'mqtt_subscriber_topic'
    {set_attribute}
    try:
        mqtt_broker.initialize(initial_topics=[data_topic])
        pipeline ,mqtt_source = get_mqtt_trash_pipeline_and_mqtt_stage(sdc_builder, mqtt_broker{stage_attributes})
        #want to set attribute after configure for environment? set here.
        sdc_executor.add_pipeline(pipeline)
        running_snapshot = sdc_executor.capture_snapshot(pipeline, start_pipeline=True, batches=1, wait=False)

        time.sleep(1)
        mqtt_broker.publish_message(topic=data_topic, payload=payload)
        snapshot = running_snapshot.wait_for_finished().snapshot
        sdc_executor.stop_pipeline(pipeline)
        # write your assertion code here
    finally:
        mqtt_broker.destroy()"""

        if self.file_name == 'test_influxdb_destination.py':

            line = f"""{self.line[0:len(self.line)-3]}, influxdb):
    {self.input_data}
    client = influxdb.client
    measurement = get_random_string(string.ascii_letters, 10)
    raw_dict = [{{'measurement': measurement, 'record': {{'time': 1439897881000, 'butterflies': 12, 'honeybees': 23,
                                                        'location': '1', 'scientist': 'langstroth'}}}}]
    create_db = not any(database['name'] == influxdb.database for database in client.get_list_database())

    try:
        # build pipeline and get the same
        pipeline, destination = get_pipeline_and_destination_stage(raw_dict, sdc_builder, influxdb, create_db{stage_attributes})
        #want to set attribute after configure for env ? set here.
        
    finally:
        if sdc_executor.get_pipeline_status(pipeline).response.json().get('status') == "RUNNING":
            sdc_executor.stop_pipeline(pipeline)
        logger.info('Dropping InfluxDB measurement %s in the database %s ...', measurement, influxdb.database)
        influxdb.drop_measurement(measurement)
        logger.info('Dropping InfluxDB database %s ...', influxdb.database)
        client.drop_database(influxdb.database)"""

        elif self.file_name == 'test_mqtt_publisher_destination.py':

            line = f"""{self.line[0:len(self.line)-3]}, mqtt_broker):
    {self.input_data}       
    data_topic = 'mqtt_subscriber_topic'
    try:
        mqtt_broker.initialize(initial_topics=[data_topic])
        pipeline, mqtt_target, dev_raw_data_source = get_pipeline_and_stages(sdc_builder,data_topic,mqtt_broker{stage_attributes})
        #want to set attribute after configure for environment? set here.
        sdc_executor.add_pipeline(pipeline)
        snapshot = sdc_executor.capture_snapshot(pipeline, start_pipeline=True).snapshot
        sdc_executor.stop_pipeline(pipeline)
        output_records = snapshot[dev_raw_data_source.instance_name].output
        #get message from broker
        # with QOS=2 (default), exactly one message should be received per published message
        # so we should have no trouble getting as many messages as output records from the
        # snapshot
        pipeline_msgs = mqtt_broker.get_messages(data_topic, num=len(output_records))
        #sample assertions. you can modify as per your need
        #for msg in pipeline_msgs:
            #assert msg.payload.decode().rstrip() == raw_str
            #assert msg.topic == data_topic
    finally:
        mqtt_broker.destroy()"""

        elif self.file_name == 'test_mongodb_origin.py':
            line = f"""{self.line[0:len(self.line)-3]}, mongodb):
    try:
        pipeline, mongodb_origin = get_mongodb_to_trash_pipeline_and_stage(sdc_builder, mongodb{stage_attributes})
        # want to set attributes after configure for env? set here
        # MongoDB and PyMongo add '_id' to the dictionary entries e.g. docs_in_database
        # when used for inserting in collection. Hence the deep copy.
        docs_in_database = copy.deepcopy(ORIG_DOCS)
        # Create documents in MongoDB using PyMongo.
        # First a database is created. Then a collection is created inside that database.
        # Then documents are created in that collection.
        logger.info('Adding documents into %s collection using PyMongo...', mongodb_origin.collection)
        mongodb_database = mongodb.engine[mongodb_origin.database]
        mongodb_collection = mongodb_database[mongodb_origin.collection]
        insert_list = [mongodb_collection.insert_one(doc) for doc in docs_in_database]
        assert len(insert_list) == len(docs_in_database)

        # Start pipeline and verify the documents using snaphot.
        sdc_executor.add_pipeline(pipeline)
        snapshot = sdc_executor.capture_snapshot(pipeline=pipeline, start_pipeline=True).snapshot
        sdc_executor.stop_pipeline(pipeline)
        # asserts your expectations 

    finally:
        logger.info('Dropping %s database...', mongodb_origin.database)
        mongodb.engine.drop_database(mongodb_origin.database)"""
        elif self.file_name == "test_redis_consumer_origin.py":
            key_1 = "key_1 = f'extra{pattern_1}extra'"
            sample_input = '' if self.input_data else "raw_dict = dict(name='Jane Smith', zip_code=27023)\n    DATA = json.dumps(raw_dict)"
            default_stage_attributes = """
    stage_attributes={'data_format':'JSON',
                      'max_batch_size_in_records':10,
                      'pattern':[f'*{pattern_1}*']}"""
            set_attribute= "stage_attributes.update({'pattern': [f'*{pattern_1}*'], 'max_batch_size_in_records': 1})" if 'stage_attributes' in self.line else default_stage_attributes
            line = f"""{self.line[0:len(self.line) - 3]}, redis):
    {self.input_data}
    {sample_input}
    pattern_1 = get_random_string()
    {set_attribute}
    try:
        pipeline, redis_consumer =get_redis_origin_to_trash_pipeline(sdc_builder, redis{stage_attributes})
        #want to set stage attribute after configure for env ? set here.
        # pipeline has to be started first to have the Redis channel to be created
        sdc_executor.add_pipeline(pipeline)
        sdc_executor.start_pipeline(pipeline)
        snapshot_command = sdc_executor.capture_snapshot(pipeline, start_pipeline=False, wait=False)
        key_1 = {key_1}
        for _ in range(20):  # 20 records will make 2 batches (each of 10)
            assert redis.client.publish(key_1, DATA) == 1  # 1 indicates pipeline consumer received the raw_data
        snapshot = snapshot_command.wait_for_finished().snapshot
        output_records=snapshot[redis_consumer.instance_name].output
        #assertions
        
    finally:
        sdc_executor.stop_pipeline(pipeline)"""
        elif self.file_name == 'test_rabbitmq_consumer_origin.py':
            default_stage_attributes="""
        stage_attributes={'name':name,'data_format':'TEXT', 
                          'durable':True, 
                          'auto_delete':False, 
                          'bindings':[]}"""
            set_attribute = "stage_attributes.update({'name':name})" if 'stage_attributes' in self.line else default_stage_attributes
            line = f"""{self.input_data}
    name = get_random_string()
    {set_attribute}
    try:
        
        pipeline, rabbitmq = get_pipeline_and_rebbitmq_consumer_stage(sdc_builder, rabbitmq{stage_attributes})
        #want to set attribute after configure for env? set here.
        sdc_executor.add_pipeline(pipeline)
        
        connection = rabbitmq.blocking_connection
        channel = connection.channel()
        
        # About default exchange routing: https://www.rabbitmq.com/tutorials/amqp-concepts.html
        channel.queue_declare(queue=name, durable=True, exclusive=False, auto_delete=False)
        channel.confirm_delivery()
        
        for i in range(5):
            expected_message = INPUT_DATA
            try:
                channel.basic_publish(exchange="",
                                      routing_key=name,  # Routing key has to be same as queue name.
                                      body=expected_message,
                                      properties=pika.BasicProperties(content_type='text/plain', delivery_mode=1),
                                      mandatory=True)
            except:
                logger.warning('Message %s could not be sent.', expected_message)   
        
        snapshot = sdc_executor.capture_snapshot(pipeline, start_pipeline=True).snapshot
        sdc_executor.stop_pipeline(pipeline)
        #assertion logic
    finally:
        channel.close()
        connection.close()
        """
        elif self.file_name == 'test_rabbitmq_producer_destination.py':
            default_stage_attributes = """
                    stage_attributes={'name':name,'data_format':'TEXT', 
                                      'bindings':[dict(name=exchange_name,
                                                    type='DIRECT',
                                                    durable=False,
                                                    autoDelete=True)]}"""
            set_attribute = """
        stage_attributes.update({'name':name,
                                 'bindings':[dict(name=exchange_name, 
                                                  type='DIRECT', 
                                                  durable=False, 
                                                  autoDelete=True)]})""" if 'stage_attributes' in self.line else default_stage_attributes
            line = rf"""{self.line[0:len(self.line) - 3]}, rabbitmq):
            
        name = get_random_string()
        exchange_name = get_random_string()
        {set_attribute}
        try:
            pipeline, rabbitmq_destination = get_pipeline_and_rabbitmq_producer_destination_stage(sdc_builder, rabbitmq{stage_attributes})
            # want to set attributes after configure for env? set here.
            sdc_executor.add_pipeline(pipeline)
            sdc_executor.start_pipeline(pipeline).wait_for_pipeline_batch_count(5)
            sdc_executor.stop_pipeline(pipeline)
            history = sdc_executor.get_pipeline_history(pipeline)
            msgs_sent_count = history.latest.metrics.counter('pipeline.batchOutputRecords.counter').count
            logger.debug('Number of messages ingested into the pipeline = %s', msgs_sent_count)
            
            connection = rabbitmq.blocking_connection
            channel = connection.channel()
            msgs_received = [channel.basic_get(name, False)[2].decode().replace('\n', '')
                         for _ in range(msgs_sent_count)]
            # your assertions
        finally:
            channel.close()
            connection.close()"""

        return line
