from kafka import KafkaProducer
from json import dumps
import time

producer = KafkaProducer(acks=0,
                         compression_type='gzip',
                         bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

data = {"schema": {"type": "struct", "fields": [{"type": "int32", "optional": "false", "field": "id"},
                                                {"type": "string", "optional": "false", "field": "user_id"},
                                                {"type": "string", "optional": "false", "field": "name"}
                                                ], "optional": "false", "name": "users"},
        "payload": {"id": 4, "user_id": "test5" , "name": "test_test5"}}
producer.send("skuser42_exam_topic_users", data)
time.sleep(1)
producer.flush()
