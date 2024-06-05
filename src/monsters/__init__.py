import os
import importlib

mobs = []

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    mob = importlib.import_module("."+module[:-len(".py")], "monsters")
    mobs.append(mob.object)

del module
