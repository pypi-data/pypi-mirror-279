import importlib.util
from .utils import input_or_output, get_asset_property
import logging
import importlib
# from alidadataset.serializations

def load(name, load_as="path"):
    
    module = importlib.import_module("alidadataset.serializations." + load_as)
    loading_func = getattr(module, "load")

    return loading_func(name)

def infer_module(name):
    storage = get_asset_property(name, "storage_type")
    print(storage)
    if storage == "filesystem":
        return "pandas_dataframe"
    elif storage == "kafka":
        if input_or_output(name) == "input":
            return "streaming_input"
        elif input_or_output(name) == "output":
            return "streaming_output"

def auto_load(name):
    return load(name=name, load_as=infer_module(name))