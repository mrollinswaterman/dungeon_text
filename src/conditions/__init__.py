import os
import importlib

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    condition = importlib.import_module("."+module[:-len(".py")], "conditions")
    instance = condition.object(None, None)
    dict[instance.id] = condition.object

del module
