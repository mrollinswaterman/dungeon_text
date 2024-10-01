"""import global_commands
#from enchantments import Weapon_Enchantment
from game_object import Game_Object
from item import Item
from conditions import On_Fire

class Flaming(Weapon_Enchantment):

    def __init__(self, parent: Game_Object | Item) -> None:
        super().__init__(parent)

        self.active_effects["hit"] = [On_Fire.object(self.parent)]

    def apply(self, effect_type: str):
        if global_commands.probability(100): #35 + level??
            return super().apply(effect_type)"""
