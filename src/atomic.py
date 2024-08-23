
class Atomic_Effect():

    def __init__(self, target, src):
        from player import Player
        from mob import Mob
        from items import Item
        self.target:Player | Mob | Item = target
        self.src: Item | Mob = src

    def damage(self, value:int, AP:bool = False):
        self.target.take_damage(value, self.src, AP)

    def heal(self, value:int):
        self.target.heal(value)

    def gain_temp_hp(self, value:int):
        self.target.gain_temp_hp(value)

    def apply_effect(self, effect):
        from status_effect import Status_Effect
        effect:Status_Effect = effect
        self.target.add_status_effect(effect)

    def damage_an_item(self, value):
        self.target.lose_durability(value)