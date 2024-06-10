import os
import importlib

master = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    item_file = importlib.import_module("."+module[:-len(".py")], "item_compendium")
    master[module[:-len(".py")]] = item_file.object

del module
