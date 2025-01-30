import os
import importlib

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py' or module != "Boulder.py":
        continue
    scenario = importlib.import_module("."+module[:-len(".py")], "compendiums.event_compendium")
    print(scenario)
    instance = scenario.object()
    dict[instance.id] = scenario.object

del module

#del dict["Trap Room"]
