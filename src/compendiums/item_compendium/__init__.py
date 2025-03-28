import os
import importlib

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    item = importlib.import_module("."+module[:-len(".py")], "compendiums.item_compendium")
    instance = item.object()
    dict[instance.__class__.__name__] = item.object

del module
