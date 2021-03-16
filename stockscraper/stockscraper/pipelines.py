from kafka import KafkaProducer
from json import dumps
import time


class StockscraperPipeline(object):

    def __init__(self):
        self.producer = KafkaProducer(acks=0,
                                      compression_type='gzip',
                                      bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))

    def process_item(self, item, spider):
        item = dict(item)
        item["Quantity"] = int(item["Quantity"].replace(",", ""))
        item["Price"] = float(item["Price"].replace(",", ""))
        data = {"schema": {"type": "struct", "fields": [{"type": "int64", "optional": "false", "field": "Quantity"},{"type": "float", "optional": "false", "field": "price"},{"type": "string", "optional": "false", "field": "days_range"},{"type": "string", "optional": "false", "field": "title"},{"type": "int64", "optional": "true","name": "org.apache.kafka.connect.data.Timestamp","version": 1, "field": "search_time"}], "optional": "false","name": "md3stock"},"payload": {"Quantity": item["Quantity"], "price": item["Price"], "days_range": item["days_range"], "title": item["title"], "search_time": int(time.time() * 1000)}}
        self.producer.send("my_project_md3stock", data)
        time.time(1)
        self.producer.flush()
