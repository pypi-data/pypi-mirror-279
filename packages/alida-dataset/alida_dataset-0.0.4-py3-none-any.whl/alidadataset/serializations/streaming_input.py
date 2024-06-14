from ..utils import input_or_output, get_asset_property
from kafka import KafkaConsumer
import json


class Consumer(KafkaConsumer):
    def __init__(self, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)

    def read_message(self):
        for element in self:
            yield json.loads(element.value.decode('utf-8'))
        

def load(name) -> Consumer:
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"
    
    
    if storage_type == "kafka":
        consumer = Consumer(
            get_asset_property(asset_name=name),
            bootstrap_servers=get_asset_property(asset_name=name, property="kafka_brokers").split(",")
        )
    
        return consumer
