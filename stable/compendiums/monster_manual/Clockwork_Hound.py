#Clockwork Hound mob file
import random
import game_objects, globals
from items.stackable import Stackable
from items.equipment import Equipment

stats = {
    "level": 1,
    "level_range": (6, 13),
    "hit_dice": 10,
    "str": 16,
    "dex": 14,
    "con": 14,
    "int": 18,
    "wis": 10,
    "cha": 7,
    "base_evasion": 10,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 3,
    "damage": "2d8",
    "dc": 10,
}

class Clockwork_Hound(game_objects.Mob):
    def __init__(self, id="Clockwork Hound", stat_dict=stats):
        super().__init__(id, stat_dict)
        #base gold & xp
        self.gold += 30
        self.xp += 15

        """if globals.probability(50):
            scrap:Stackable = Stackable("Clockwork Scrap", "Uncommon", random.randrange(1, (self.level // 2)))
            scrap.unit_weight = 1.5
            self.pick_up(scrap, True)

        if globals.probability(3):
            heart = Stackable("Clockwork Heart", "Epic")
            heart.unit_weight = 2
            self.pick_up(heart, True)"""
            
    def trigger(self) -> bool:
        if not super().trigger():
            return False
        return self.hp < self.stats.max_hp // 3

    def special(self) -> None:
        self.spend_ap()
        meal:Equipment = self.target.weapon
        if self.target.weapon.durability < self.target.armor.durability:
            meal = self.target.armor
        
        globals.type_text(f"The {self.id} lunges for your {meal.id}.")
        if self.roll_to_hit() >= self.target.evasion():
            globals.type_text(f"It tears off a chunk before darting back to gulp it down.")
            meal.remove_durability(self.bonus("str"))
            self.heal(self.bonus("str"))
        else:
            globals.type_text("It missed.")

        return True
    
    def roll_narration(self):
        base = super().roll_narration()        
        me = [
            f"The {self.id} snarls and dashes towards you.",
            f"The {self.id}'s gears screech and grind as it prepares to tear into you.",
            f"The {self.id}'s clicks and whirs intensify as it readies its attack...",
            f"The {self.id}'s mechanical muscles tense before it leaps towards you.",
            f"The mechanical beast growls and crouches low, ready to pounce.",
            f"The {self.id} gnashes it's teeth and snaps at your midsection.",
        ]
        return base + me

    def hit_narration(self):
        base = super().hit_narration()
        me = [
            f"The {self.id}'s fluid movements are far from mechanical. It catches you.",
            f"It's metal teeth tear through your defenses.",
            f"The {self.id}'s metal claws find your body.",
            f"You feel cold steel on your skin, then a burst of pain.",
        ]
        return base + me

    def miss_narration(self):
        base = super().miss_narration()
        me = [
            f"Just as the {self.id} would have struck you, it's internal machines sputter causing it to fall short.",
            f"The {self.id}'s jerky, robotic motions are easy enough to dodge this time.",
            f"The {self.id}'s targeting systems failed. It misses you completely.",
            f"It's jaws clamp down on the empty space where you once stood.",
            f"Failing to hit you, it skitters to a stop before whipping back around to face you, metal fangs bared.",
        ]
        return base + me

object = Clockwork_Hound
