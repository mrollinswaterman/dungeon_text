import os
import importlib

dict:dict= {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    trick = importlib.import_module("."+module[:-len(".py")], "compendiums.condition_compendium")
    id = trick.__name__[len("compendiums.condition_compendium."):]
    dict[id] = trick.object

del module
