#Goblin mob file
import random
import globals, game_objects

class Goblin(game_objects.Mob):
    def __init__(self):
        super().__init__(id="Goblin")
        self.stolen = False
        #base xp & gold
        self.gold += 10
        self.xp += 5
    
    @property
    def flee_threshold(self) -> float:
        return 30
    @property
    def retreat(self):
        return self.gold >= (1.5 * self.target.gold) and self.stolen
    
    def trigger(self):
        """Returns True if the player has more gold than the goblin, or if the goblin has x1.5 the player's gold"""
        if not super().trigger():
            return False
        return self.gold < self.target.gold or self.retreat

    def special(self) -> None:
        """Rob: Steals a random amount of gold from the player if they fail a dex check"""
        if not self.retreat:
            self.spend_ap()
            globals.type_text(f"The {self.id} makes a grab at your gold pouch.")
            save = self.target.roll_a_check("dex")
            attack = self.roll_to_hit()
            if save >= attack:
                globals.type_text("It missed.")
            else:
                prospective = globals.d(10) + (attack - save)#adjust gold stolen based on how bad the player got beat
                actual = self.target.lose_gold(prospective)
                globals.type_text(f"The {self.id} stole {actual} gold from you!")
                self.gold += actual
                self.stolen = actual > 0
        else:
            self.flee_threshold = 100
        return None
    
    def roll_narration(self):
        base = super().roll_narration()    
        me = [
            f"The {self.id} jabs its dagger towards you.",
            f"The {self.id} jumps at you.",
            f"The {self.id} slashes at your legs.",
        ]
        return base + me

    def hit_narration(self):
        base = super().hit_narration()
        me = [
            f"The {self.id}'s dagger finds a chink in your armor.",
            f"The {self.id}'s small frame slips past your guard."
        ]
        return base + me

    def miss_narration(self):
        base = super().miss_narration()
        me = [
            f"You easily dodge the {self.id}'s wild swing.",
            f"It's dagger bounces off your own weapon.",
            f"The {self.id} stabs the spot you were just stading in.",
            f"The {self.id}'s small stature means you can easily parry it's frontal assault."
        ]
        return base + me

object = Goblin
