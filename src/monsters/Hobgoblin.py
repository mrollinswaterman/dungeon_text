#Hobgoblin mob file
import mob, global_commands
import status_effects

stats = {
    "str": 12,
    "dex": 12,
    "con": 12,
    "int": 9,
    "wis": 7,
    "cha": 14,
    "base_evasion": 8,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 1,
    "damage": "1d8",
    "dc": 10,
    "hit_dice": 10,
    "loot": {
        "gold": 10,
        "xp": 5,
        "drops": []
    }
}

class Hobgoblin(mob.Mob):
    def __init__(self, id="Hobgoblin", level=(1,5), statblock=stats):
        super().__init__(id, level, statblock)

        self._stats["dc"] = 24 + self.bonus("cha")#12 + cha

    def trigger(self):
        """
        For Hobgoblins it's if the player's evasion is >= 10, 
        and the player is not currently suffering from a Hobgoblin's taunt
        """
        return self._player.evasion >= 10 and not self.applied


    def special(self) -> None:
        """
        Taunt: Reduces the player's evasion by 2 points for 2 turns if they fail a charisma check
        """
        self.spend_ap()
        global_commands.type_text(f"The {self.id} hurls enraging insults at you.")

        if self._player.roll_a_check("cha") >= self.dc:
            global_commands.type_text(f"Your mind is an impenetrable fortess. The {self.id}'s words have no effect.")

        else:
            global_commands.type_text(f"The {self.id}'s insults distract you, making you an easier target.")
            taunt = status_effects.Stat_Debuff(self, self._player)
            self._my_effect_id = taunt.id
            taunt.set_duration(3)
            taunt.set_potency(2)
            taunt.set_stat("base_evasion")
            self._player.add_status_effect(taunt)
        return None

object = Hobgoblin