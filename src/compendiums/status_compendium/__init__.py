import os
import importlib

dict:dict= {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    status = importlib.import_module("."+module[:-len(".py")], "compendiums.status_compendium")
    id = status.__name__[len("compendiums.status_compendium."):]
    dict[id] = status.object

del module
