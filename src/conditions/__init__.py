import os
import importlib

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    instance = importlib.import_module("."+module[:-len(".py")], "conditions")
    obj = instance.Condition(None, None)
    dict[obj.id] = instance.Condition

del module
