import os
import importlib

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    mob = importlib.import_module("."+module[:-len(".py")], "compendiums.monster_manual")
    instance = mob.object()
    dict[instance.id] = mob.object

del module
