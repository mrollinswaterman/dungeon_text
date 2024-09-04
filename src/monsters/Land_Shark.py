#Land Shark mob file
import mob, global_commands
from stackable import Stackable

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

class Land_Shark(mob.Mob):
    def __init__(self, id="Land Shark", stat_dict=stats):
        super().__init__(id, stat_dict)
        #base gold & xp
        self.gold += 15
        self.xp += 8

        """if global_commands.probability(10):
            tooth = Stackable("Land Shark Tooth", "Epic")
            tooth.unit_weight = 0.5
            self.pick_up(tooth, True)"""

        self.burrowed = False

    @property
    def applied(self) -> bool:
        return self.conditions.get("Vulnerable") is not None

    def trigger(self):
        if not super().trigger():
            return False
        if self.burrowed is True and not self.applied and global_commands.probability(33):
            return True
        
        if global_commands.probability(100 - ((self.hp * 100) / self.stats.max_hp)):
            # %HP determines directly determines burrow chance
            return True
        
        return len(self.status_effects.effects) >= 2 and self.burrowed is False#if I have status effects and not burrowed, burrow

    def special(self) -> bool:
        """
        Burrow: increases evasion and armor temporarily
        Erupt: can only be used when 'burrowed',
        doubles all damage done and taken after use, reverts evasion
        changes made by burrow
        """
        if not self.burrowed:
            self.spend_ap(0) #indicates a full round action
            global_commands.type_text(f"The {self.id} burrows underground, making itself harder to hit.")
            self.stats.base_evasion += 3
            self.stats.armor += 2
            self.burrowed = True
            return True
        else:
            self.spend_ap()
            global_commands.type_text(f"The {self.id} erupts from the ground.")
            self.stats.base_evasion -= 3
            self.stats.armor -= 2
            #vul:status_effect.Status_Effect = Vulnerable.Condition(self, self)#double all damage taken for 3 turns
            #vul.set_duration(3)
            #self.status_effects.add(vul)
            self.burrowed = False
            return True
    
    def roll_narration(self):
        base = super().roll_narration()        
        me = [
            f"The {self.id} rushes you.",
            f"The {self.id} smells blood and closes in...",
            f"The {self.id} comes at you with intent to kill.",
            f"The {self.id} bares its razor sharp teeth and throws itself towards you."
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
