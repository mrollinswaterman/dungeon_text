import os
import importlib
#import controller

dict = {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    trick = importlib.import_module("."+module[:-len(".py")], "combat_tricks")
    id = trick.__name__[len("combat_tricks."):]
    dict[id] = trick.object

del module
