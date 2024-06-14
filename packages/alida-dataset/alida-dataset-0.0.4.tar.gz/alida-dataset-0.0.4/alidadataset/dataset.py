import importlib.util
from .utils import input_or_output, get_asset_property
import logging
import importlib
# from alidadataset.serializations

def load(name, load_as="path"):
    
    module = importlib.import_module("alidadataset.serializations." + load_as)
    loading_func = getattr(module, "load")

    return loading_func(name)


