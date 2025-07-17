import importlib
import os

TABLE_HANDLERS = {}

current_dir = os.path.dirname(__file__)
handler_files = [
    f[:-3] for f in os.listdir(current_dir) if f.endswith(".py") and f != "__init__.py"
]

for module_name in handler_files:
    mod = importlib.import_module(f"kinesis_consumer.handler.{module_name}")
    handler_func = getattr(mod, "handle", None)
    if handler_func:
        if module_name == "default":
            TABLE_HANDLERS["__default__"] = handler_func
        else:
            TABLE_HANDLERS[module_name] = handler_func
