#Hobgoblin mob file
import random
import mob, player, global_commands

class Hobgoblin(mob.Mob):
    def __init__(self, id="Hobgoblin", level = (1,5)):
        super().__init__(id, level)

        self._stats = {
            "str": 12,
            "dex": 12,
            "con": 12,
            "int": 9,
            "wis": 7,
            "cha": 14,
            "evasion": 8,
            "damage-taken-multiplier": 1
        }
        self._max_hp = 6 + self.bonus("con")
        self._damage = 5
        self._armor = 1
        self._dc = 12 + self.bonus("cha")

        self._loot = {
            "gold": 8,
            "xp": 6,
            "drops": None
        }

    def trigger(self):
        """
        Conditions that trigger the mob's special
        move. 

        For Hobgoblin's it's if the player's evasion is over
        10, and that the Hobgoblin has not recently applied a
        status effect 
        """
        return self._player.evasion > 10 and len(self._applied_status_effects) == 0

    def special(self) -> bool:
        """
        Taunt: Reduces the player's evasion by 2 points for 2 turns if they fail a charisma check
        """
        if self.trigger():
            self.spend_ap(1)
            global_commands.type_with_lines(f" The {self.id} hurls enraging insults at you.\n")

            if self._player.roll_a_check("cha") >= self.dc:
                global_commands.type_text(f" Your mind is an impenetrable fortess. The {self.id}'s words have no effect.")

            else:
                global_commands.type_text(f" The {self.id}'s insults distract you, making you an easier target.\n")
                taunt = player.Status_Effect("Taunt", self, "evasion", self._player)
                taunt.set_duration(3)
                taunt.set_power(-2)
                taunt.set_message(f" Your Evasion has been redcued by 2 by the {self.id}'s Taunt!")
                self._player.add_status_effect(taunt)
                self._applied_status_effects.add(taunt)
            return True
        return False 

object = Hobgoblin()
