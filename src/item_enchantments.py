import random
from atomic import Atomic_Effect
import conditions.On_Fire


CONDITION_CODES = {
    "On Fire": {"hit": "Flaming", "attack": "Molten"},
    "Debuff": {"hit": "Weakening", "attack": None},
    "Entangled": {"hit": None, "attack": None},
    "Buff": {"hit": None, "attack": None},
    "Poisoned": {"hit": "Poisoning", "attack": "Noxious"},
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
        print("randomizing...")
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
        #get the str code associated with the randomly selected on_attack and on_hit effects
        for entry in self.methods:
            if self.methods[entry] == self.on_hit:
                hit_str = entry
            if self.methods[entry] == self.on_attack:
                attack_str = entry

        if attack_str == "apply_an_effect":
            self.generate_effect("attack")
        if hit_str == "apply_an_effect":
            self.generate_effect("hit")

    def generate_effect(self, catagory:str, effect=None):
        if effect is None:
            import conditions, status_effect
            effect:status_effect.Status_Effect = random.choice(list(conditions.dict.values()))(self.src, self.target)

        self.effects[catagory].add(effect)

        if effect.id in CONDITION_CODES and CONDITION_CODES[effect.id][catagory] is not None:
            self.id = f"{self.id} {CONDITION_CODES[effect.id][catagory]}"
            self.id = self.id.strip()

new = Enchantment(None, None)

new.randomize()