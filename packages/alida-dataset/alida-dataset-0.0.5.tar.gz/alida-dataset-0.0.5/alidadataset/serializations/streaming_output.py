from ..utils import input_or_output, get_asset_property
from kafka import KafkaProducer
import json


class Producer(KafkaProducer):
    def __init__(self, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)

    def set_out_channel(self, channel):
        self.alida_out_channel = channel
        
    def send_message(self, value, *args, **kwargs):
        self.send(topic=self.alida_out_channel, value=json.dumps(value).encode('utf-8'), *args, **kwargs)


def load(name) -> Producer:
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"
    
    
    if storage_type == "kafka":
        producer = Producer(
            bootstrap_servers=get_asset_property(asset_name=name, property="kafka_brokers").split(",")
        )
        producer.set_out_channel(get_asset_property(asset_name=name))
        
        return producer
