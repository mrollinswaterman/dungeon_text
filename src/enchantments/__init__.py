import os
import importlib

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    file = importlib.import_module("."+module[:-len(".py")], "enchantments")
    instance = file.Effect(None, None)
    dict[instance.id] = file.Effect

del module
