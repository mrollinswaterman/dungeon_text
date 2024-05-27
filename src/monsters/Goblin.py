#Goblin mob file
import random
import mob, global_commands

stats = {
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
    "damage": 4,
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
    
    def trigger(self):
        """
        Conditions that trigger the mob's special
        move. 

        For the Goblin, if the player has more gold than
        it does.
        """
        return self._player.gold >= self._loot["gold"]

    def special(self) -> bool:
        """
        Rob: Steals a random amount of gold from the player if they fail a dex check
        """
        if self.trigger():
            self.spend_ap(1)
            global_commands.type_with_lines(f"The {self._id} makes a grab at your gold pouch.\n")
            if self._player.roll_a_check("dex") >= self.roll_attack():
                global_commands.type_text(" It missed.")
            else:
                prospective = random.randrange(1,20)
                actual = self._player.lose_gold(prospective)
                global_commands.type_text(f"The {self._id} stole {actual} gold from you!")
                self._loot["gold"] += actual
            return True
        return False

object = Goblin
