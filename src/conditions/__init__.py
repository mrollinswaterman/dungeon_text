import os
import importlib

dict:dict= {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    trick = importlib.import_module("."+module[:-len(".py")], "conditions")
    id = trick.__name__[len("conditions."):]
    dict[id] = trick.object

del module
