import os
import importlib

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    importlib.import_module("."+module[:-len(".py")], "conditions")

del module
