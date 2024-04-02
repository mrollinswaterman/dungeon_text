#Land Shark mob file
import random
import mob, player, global_commands
import status_effects
import items

class Land_Shark(mob.Mob):
    def __init__(self, id="Land Shark", level = (3,10)):
        super().__init__(id, level)
        self._stats = {
            "str": 15,
            "dex": 9,
            "con": 16,
            "int": 7,
            "wis": 7,
            "cha": 7,
        }

        self._max_hp = 10 + self.bonus("con")
        self._hp = self._max_hp
        self._stats["evasion"] = 8

        self._damage = 8
        self._armor = 3

        self._loot = {
            "gold": 15,
            "xp": 12,
            "drops": None
        }

        if global_commands.probability(3):
            tooth = items.Item("Land Shark Tooth", "Epic")
            tooth.set_weight(0.5)
            self._loot["drops"] = tooth

        self._burrowed = False

        self.update()

    def trigger(self):
        """
        Conditions that trigger the mob's special
        move. 

        For Hobgoblin's it's if the player's evasion is over
        10, and that the Hobgoblin has not recently applied a
        status effect 
        """


    def special(self) -> bool:
        """
        Burrow: increases evasion temporarily

        Erupt: can only be used when 'burrowed'  
        """

        if self.trigger() is True:
            self.spend_ap()
            if self._burrowed is False:
                global_commands.type_with_lines(f"The {self._id} burrows underground, increasing it's evasion by 3.\n")
                self._evasion += 3
                self._burrowed = True
                return None
            else:
                global_commands.type_with_lines(f"The {self._id} erupts from the ground.")
                self._evasion -= 3
                #double all damage done for 2 turns 
                damage_buff = status_effects.Stat_Buff(self, self)
                damage_buff.set_stat("damage-multiplier")
                damage_buff.set_duration(2)
                damage_buff.set_potency(2)
                self.add_status_effect(damage_buff)
                vul = status_effects.Vulnerable
                vul.set_duration(3)
                
        

object = Land_Shark()
