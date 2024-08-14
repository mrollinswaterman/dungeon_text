#Goblin mob file
import random
import mob, global_commands

stats = {
    "base_level": 1,
    "str": 10,
    "dex": 16,
    "con": 10,
    "int": 9,
    "wis": 7,
    "cha": 6,
    "base_evasion": 9,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 0,
    "damage": "1d6",
    "dc": 10,
    "hit_dice": 10,
    "loot": {
        "gold": 10,
        "xp": 5,
        "drops": []
    }
}

class Goblin(mob.Mob):
    def __init__(self, id="Goblin", level=(1,3), statblock=stats):
        super().__init__(id, level, statblock)

        self._flee_threshold = 0.25
        self._stolen = False

    @property
    def retreat(self):
        return self._loot["gold"] >= (1.5 * self._player.gold) and self._stolen
    
    def trigger(self):
        """
        Returns True if the player has more gold than the goblin, 
        or if the goblin has x1.5 the player's gold
        """
        if not super().trigger():
            return False
        return self._loot["gold"] < self._player.gold or self.retreat

    def special(self) -> None:
        """
        Rob: Steals a random amount of gold from the player if they fail a dex check
        """
        if not self.retreat:
            self.spend_ap()
            global_commands.type_text(f"The {self._id} makes a grab at your gold pouch.")
            save = self._player.roll_a_check("dex")
            attack = self.roll_to_hit()
            if save >= attack:
                global_commands.type_text("It missed.")
            else:
                prospective = global_commands.d(10) + (attack - save)#adjust gold stolen based on how bad the player got beat
                actual = self._player.lose_gold(prospective)
                global_commands.type_text(f"The {self._id} stole {actual} gold from you!")
                self._loot["gold"] += actual
                self._stolen = actual > 0
            return None
        else:
            self._flee_threshold = 1.01
        return None
    
    def roll_text(self):
        base = super().roll_text()    
        me = [
            f"The {self.id} jabs its dagger towards you.",
            f"The {self.id} jumps at you.",
            f"The {self.id} slashes at your legs.",
        ]
        return base + me

    def hit_text(self):
        base = super().hit_text()
        me = [
            f"The {self.id}'s dagger finds a chink in your armor.",
            f"The {self.id}'s small frame slips past your guard."
        ]
        return base + me

    def miss_text(self):
        base = super().miss_text()
        me = [
            f"You easily dodge the {self.id}'s wild swing.",
            f"It's dagger bounces off your own weapon.",
            f"The {self.id} stabs the spot you were just stading in.",
            f"The {self.id}'s small stature means you can easily parry it's frontal assault."
        ]
        return base + me

object = Goblin
