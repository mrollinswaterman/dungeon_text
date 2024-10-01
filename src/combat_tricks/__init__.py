import os
import importlib

#Note to self: Most combat tricks work by replacing some of the player's default functions like damage rolls
#or attack rolls (etc) with their own version of that function that gets called instead. all function changes are then reverted to 
#normal once the combat trick's duration has run out

dict:dict= {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    trick = importlib.import_module("."+module[:-len(".py")], "combat_tricks")
    id = trick.__name__[len("combat_tricks."):]
    dict[id] = trick.object

del module
