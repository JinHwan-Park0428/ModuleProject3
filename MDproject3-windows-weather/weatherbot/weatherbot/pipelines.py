from kafka import KafkaProducer
from json import dumps
import time


class WeatherbotPipeline:
    def __init__(self):
        self.producer = KafkaProducer(acks=0,
                                      compression_type='gzip',
                                      bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

    def process_item(self, item, spider):
        item = dict(item)
        item["temper"] = int(item["temper"])
        item["high_temp"] = int(item["high_temp"])
        item["low_temp"] = int(item["low_temp"])
        data = {"schema": {"type": "struct", "fields": [{"type": "int32", "optional": "false", "field": "temper"},{"type": "string", "optional": "false", "field": "humid"}, {"type": "int32", "optional": "false", "field": "high_temp"},{"type": "int32", "optional": "false", "field": "low_temp"},{"type": "string", "optional": "false", "field": "title"},{"type": "string", "optional": "false", "field": "wind"},{"type": "string", "optional": "false", "field": "weather"},{"type": "int64", "optional": "true","name": "org.apache.kafka.connect.data.Timestamp","version": 1, "field": "search_time"}], "optional": "false","name": "weather"},"payload": {"temper": item["temper"], "humid": item["humid"], "high_temp": item["high_temp"],"low_temp": item["low_temp"], "title": item["title"], "wind": item["wind"], "weather": item["weather"], "search_time": int(time.time() * 1000)}}
        self.producer.send("my_project_weather", data)
        self.producer.flush()


