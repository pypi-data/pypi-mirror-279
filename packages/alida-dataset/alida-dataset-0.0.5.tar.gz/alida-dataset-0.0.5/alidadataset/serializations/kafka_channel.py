from ..utils import input_or_output, get_asset_property
from kafka import KafkaConsumer, KafkaProducer
import typing



def load(name):
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"
    
    
    if storage_type == "kafka":
            
        if input_or_output(name=name) == "input":
            consumer = KafkaConsumer(
                get_asset_property(asset_name=name), 
                bootstrap_servers=get_asset_property(asset_name=name, property="kafka_brokers").split(",")
            )
            return typing.cast(KafkaConsumer, consumer)

        elif input_or_output(name=name) == "output":
            producer = KafkaProducer(
                bootstrap_servers=get_asset_property(asset_name=name, property="kafka_brokers").split(",")
            )
            return typing.cast(KafkaProducer, producer)
