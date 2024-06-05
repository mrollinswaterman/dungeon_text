import os
import importlib

scenarios = []

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    scenario = importlib.import_module("."+module[:-len(".py")], "events")
    scenarios.append(scenario.object)

del module
