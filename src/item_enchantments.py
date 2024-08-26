import random
from atomic import Atomic_Effect


CONDITICODES = {
    "On_Fire": {"hit": "Flaming", "attack": "Molten"},
    "Debuff": {"hit": "Weakening", "attack": None},
    "Entangled": {"hit": None, "attack": None},
    "Buff": {"hit": None, "attack": None},
    "Poisoned": {"hit": "Poison", "attack": "Noxious"},
    "Slowed": {"hit": "Freezing", "attack": "Glacial"},
    "Enraged": {"hit": None, "attack": None},
    "Vulnerable": {"hit": "Acidic", "attack": "Corrosive"}
}

class Enchantment(Atomic_Effect):

    def __init__(self, target, src):
        super().__init__(target, src)

        self.on_attack = None
        self.on_hit = None

    
    def randomize(self):
        import global_commands

        #75% chance of an item having an on-hit ability
        if global_commands.probability(75):
            self.on_hit = random.choice(list(self.methods.values()))
            #then, 5% chance of an item having both on_hit and on_attack
            if global_commands.probability(5):
                self.on_attack = random.choice(list(self.methods.values()))
        #if no on_hit, give it an on_attack, with a 5% chance of on_hit as well
        else:
            self.on_attack = random.choice(list(self.methods.values()))
            if global_commands.probability(5):
                self.on_hit = random.choice(list(self.methods.values()))

        hit_str = None
        attack_str = None
        for entry in self.methods:
            if self.methods[entry] == self.on_hit:
                hit_str = entry
            if self.methods[entry] == self.on_attack:
                attack_str = entry

        if attack_str or hit_str == "apply_an_effect":
            self.generate_effect()



        
