#Land Shark mob file
import random
import mob, player, global_commands
import status_effects
import items

stats = {
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
    "damage": 10,
    "dc": 10,
    "hit_dice": 12,
    "loot": {
        "gold": 15,
        "xp": 8,
        "drops": []
    }
}

class Land_Shark(mob.Mob):
    def __init__(self, id="Land Shark", level = (3,10), statblock=stats):
        super().__init__(id, level, statblock)

        if global_commands.probability(10):
            tooth = items.Item("Land Shark Tooth", "Epic")
            tooth.set_weight(0.5)
            self._loot["drops"] = [tooth]

        self._burrowed = False

    @property
    def applied(self):
        return self._my_effect_id in self._status_effects

    def trigger(self):
        """
        Conditions that trigger the mob's special
        move. 

        For Hobgoblin's it's if the player's evasion is over
        10, and that the Hobgoblin has not recently applied a
        status effect 
        """
        if self._burrowed is True and not self.applied and global_commands.probability(33):
            return True
        
        if global_commands.probability(100 - ((self._hp * 100) / self.max_hp)):
            # %HP determines directly determines burrow chance
            return True
        
        return len(self._status_effects) >= 2 and self._burrowed is False#if I have status effects and not burrowed, burrow

    def special(self) -> bool:
        """
        Burrow: increases evasion temporarily

        Erupt: can only be used when 'burrowed',
        doubles all damage done and taken after use, reverts evasion
        changes made by burrow 
        """
        if not self._burrowed:
            self.spend_ap(0) #indicates a full round action
            global_commands.type_text(f"The {self._id} burrows underground, making itself harder to hit.")
            self._stats["base_evasion"] += 3
            self._burrowed = True
            return True
        else:
            self.spend_ap()
            global_commands.type_text(f"The {self._id} erupts from the ground.")
            self._stats["base_evasion"] -= 3
            vul = status_effects.Vulnerable(self, self)#double all damage taken for 3 turns
            self._my_effect_id = vul.id
            vul.set_duration(3)
            self.add_status_effect(vul)
            self._burrowed = False
            return True

object = Land_Shark
