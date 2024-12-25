import os
import importlib

dict:dict= {}

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-len(".py"):] != '.py':
        continue
    enchantment = importlib.import_module("."+module[:-len(".py")], "compendiums.enchantment_compendium")
    id = enchantment.__name__[len("compendiums.enchantment_compendium."):]
    dict[id] = enchantment.object

del module
