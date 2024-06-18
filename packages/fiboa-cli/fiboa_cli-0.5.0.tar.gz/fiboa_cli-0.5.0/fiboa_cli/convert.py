import importlib
import os
from .util import log

IGNORED_DATASET_FILES = ["__init__.py", "template.py"]

def convert(dataset, output_file, cache = None, source_coop_url = None, collection = False, compression = None):
    if dataset in IGNORED_DATASET_FILES:
        raise Exception(f"'{dataset}' is not a converter")
    try:
        converter = read_converter(dataset)
    except ImportError as e:
        raise Exception(f"Converter for '{dataset}' not available or faulty: {e}")

    if hasattr(converter, "DATA_ACCESS") and not cache:
        log("Data access is restricted. You need to manually get the data from the source.", "warning")
        log("Instructions for data access:", "warning")
        log(converter.DATA_ACCESS.strip(), "info")
        raise Exception("Provide the folder that contains the downloaded files through the `-c` parameter.")

    converter.convert(output_file, cache = cache, source_coop_url = source_coop_url, collection = collection, compression = compression)

def list_all_converter_ids():
    datasets = importlib.import_module(".datasets", package="fiboa_cli")
    files = os.listdir(datasets.__path__[0])
    return [f[:-3] for f in files if f.endswith(".py") and f not in IGNORED_DATASET_FILES]

def list_all_converters(keys):
    converters = {}
    for id in list_all_converter_ids():
        obj = {}
        try:
            converter = read_converter(id)
            for key in keys:
                value = getattr(converter, key)

                if key == "SOURCES":
                    if isinstance(value, str):
                        value = tuple([value])
                    elif isinstance(value, dict):
                        value = value.keys()
                elif key == "LICENSE" and isinstance(value, dict):
                    value = value["href"]

                obj[key] = value

            converters[id] = obj
        except ImportError:
            pass
    return converters

def read_converter(id):
    module_name = f".datasets.{id}"
    return importlib.import_module(module_name, package="fiboa_cli")
