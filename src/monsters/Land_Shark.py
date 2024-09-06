#Land Shark mob file
import mob, global_commands
from stackable import Stackable
from condition import Condition
from effects import ModifyStat, GainTempHP

stats = {
    "level": 1, 
    "level_range": (3, 10),
    "hit_dice": 12,
    "str": 15,
    "dex": 9,
    "con": 16,
    "int": 7,
    "wis": 7,
    "cha": 7,
    "base_evasion": 8,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 3,
    "damage": "1d12",
    "dc": 10,
}

class Burrowed(Condition):

    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = "Burrow"

        increase_evasion = ModifyStat(self, self.target)
        increase_evasion.stat = "base_evasion"
        increase_evasion.potency = 3
        increase_evasion.duration = 10000

        self.active_effects.append(increase_evasion)

        increase_armor = ModifyStat(self, self.target)
        increase_armor.stat = "armor"
        increase_armor.potency = 2
        increase_armor.duration = 10000

        self.active_effects.append(increase_armor)

        #decrease_damage = ModifyStat(self, self.target)
        #decrease_damage.stat = "damage_multiplier"
        #decrease_damage.potency = -0.5
        #decrease_damage.duration = 10000

        #self.active_effects.append(decrease_damage)

        self.start_message = f"The {self.source.id} burrows underground, making itself a difficult target."

class Erupt(Condition):

    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = "Erupt"

        temp_hp = GainTempHP(self, self.target)
        temp_hp.potency = 2 * self.source.bonus("con")

        self.active_effects.append(temp_hp)

        vulnerable = ModifyStat(self, self.target)
        vulnerable.stat = "damage_taken_multiplier"
        vulnerable.potency = 1#makes the land shark take x2 damage
        vulnerable.duration = 3

        self.active_effects.append(vulnerable)

        self.start_message = f"The {self.source.id} erupts from the ground, making itself Vulnerable to attack."
        self.end_message = f"The {self.source.id} is no longer Vulnerable."

class Land_Shark(mob.Mob):
    def __init__(self, id="Land Shark", stat_dict=stats):
        super().__init__(id, stat_dict)
        #base gold & xp
        self.gold += 15
        self.xp += 8

        self.rounds_burrowed = 0
        """if global_commands.probability(10):
            tooth = Stackable("Land Shark Tooth", "Epic")
            tooth.unit_weight = 0.5
            self.pick_up(tooth, True)"""

    @property
    def burrowed(self) -> bool:
        return self.conditions.get("Burrow") is not None

    def trigger(self):
        if not super().trigger():
            return False

        if self.burrowed:
            if global_commands.probability(33 + (2.5 * self.rounds_burrowed)):
                return True
            else: 
                self.rounds_burrowed += 1
                return False

        return True#global_commands.probability(100 - ((self.hp * 100) / self.stats.max_hp))

    def special(self) -> bool:
        if not self.burrowed:
            self.spend_ap(0) #indicates a full round action
            burrow = Burrowed(self, self)
            self.conditions.add(burrow)
            return True
        else:
            self.spend_ap()
            self.conditions.cleanse("Burrow")
            self.rounds_burrowed = 0
            erupt = Erupt(self, self)
            self.conditions.add(erupt)
            return True
   
    def roll_narration(self):
        base = super().roll_narration()        
        me = [
            f"The {self.id} rushes you.",
            f"The {self.id} smells blood and closes in...",
            f"The {self.id} comes at you with intent to kill.",
            f"The {self.id} bares its razor sharp teeth and throws itself towards you.",
            f"The {self.id}'s unfeeling gaze bores through you as it prepares to strike..."
        ]
        return base + me

    def hit_narration(self):
        base = super().hit_narration()
        me = [
            f"The {self.id} proves as agile as it's aquatic counterpart. It hits you.",
            f"Its jagged teeth find your soft flesh.",
            f"The {self.id}'s massive bulk slams into you.",
            f"You are unable to avoid the surprisingly spry behemoth."
        ]
        return base + me

    def miss_narration(self):
        base = super().miss_narration()
        me = [
            f"The {self.id}'s teeth barely miss you.",
            f"You get a face-full of teeth, but manage to keep yourself intact.",
            f"You roll beneath the {self.id}'s thick torso, avoiding its wrath for now.",
            f"The {self.id}'s toothy maw nearly catches you.",
        ]
        return base + me

object = Land_Shark
