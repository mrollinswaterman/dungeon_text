#Land Shark mob file
import game_objects
import globals
import effects

class Land_Shark(game_objects.Mob):
    def __init__(self):
        super().__init__(id="Land Shark")
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
        return self.monitor.get("Burrow") is not None

    def trigger(self):
        if not super().trigger():
            return False

        if self.burrowed:
            if globals.probability(33 + (2.5 * self.rounds_burrowed)):
                return True
            else: 
                self.rounds_burrowed += 1
                return False

        return True#global_commands.probability(100 - ((self.hp * 100) / self.stats.max_hp))

    def special(self) -> None:
        if not self.burrowed:
            self.spend_ap(0) #indicates a full round action
            #burrow = Burrowed(self)
            #self.conditions.add(burrow)
        else:
            self.spend_ap()
            self.conditions.cleanse("Burrow")
            self.rounds_burrowed = 0
            #erupt = Erupt(self)
            #self.conditions.add(erupt)
        return None
   
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

"""
class Burrowed(effects.Status_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.id = "Burrow"

        dodge = effects.ModifyStat(self)
        dodge.stat = "base_evasion"
        dodge.potency = 3
        dodge.duration = "100000000"

        armor = effects.ModifyStat(self)
        armor.stat = "armor"
        armor.potency = 2
        armor.duration = dodge.duration

        self._effect = [dodge, armor]

        self.start_message = f"The {self.source.id} burrows underground, making itself a difficult target."

class Erupt(effects.Status_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.id = "Erupt"

        temp_hp = effects.GainTempHP(self)
        temp_hp.potency = 2 * self.source.bonus("con")

        self.active_effects.append(temp_hp)

        vulnerable = effects.ModifyStat(self)
        vulnerable.stat = "damage_taken_multiplier"
        vulnerable.potency = 1#makes the land shark take x2 damage
        vulnerable.duration = 3

        self.active_effects.append(vulnerable)

        self.start_message = f"The {self.source.id} erupts from the ground, making itself Vulnerable to attack."
        self.end_message = f"The {self.source.id} is no longer Vulnerable."
"""

object = Land_Shark
