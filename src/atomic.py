
class Atomic_Effect():

    def __init__(self, target, src):
        from player import Player
        from mob import Mob
        from items import Item
        from status_effect import Status_Effect
        self.target:Player | Mob | Item = target
        self.src: Item | Mob = src
        self.id = "None"

        self.effects: set[Status_Effect] = set()

        self.methods = {
            "deal_damage":self.deal_damage,
            "heal":self.heal,
            "self_heal": self.self_heal,
            "drain": self.drain,
            "apply_an_effect":self.apply_an_effect,
            "gain_temp_hp":self.gain_temp_hp,
            "damage_an_item":self.damage_an_item,
            "steal_an_item":self.steal_an_item,
            "execute":self.execute,
        }

    #Effects
    def deal_damage(self, value:int):
        self.target.take_damage(value, self.src)

    def heal(self, value:int):
        self.target.heal(value)

    def self_heal(self, value:int):
        self.src.heal(value)

    def drain(self, damage:int, drain_percentage:int):
        self.self_heal(damage * (drain_percentage/100))

    def gain_temp_hp(self, value:int):
        self.target.gain_temp_hp(value)

    def apply_an_effect(self, effect=None):
        self.target.add_status_effect(effect)

    def damage_an_item(self, value):
        self.target.lose_durability(value)

    def steal_an_item(self):
        from player import Player
        owner:Player = self.target.owner
        owner.drop(self.target)
        self.src.loot["drops"].append(self.target)

    def execute(self):
        self.target.die()

    #Triggers
    def on_hit(self) -> None:
        return None
    
    def on_attack(self) -> None:
        return None
    
    def on_use(self) -> None:
        return None