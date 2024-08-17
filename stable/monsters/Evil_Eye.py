#Evil Eye mob file
import random
import mob, global_commands
from spells import Magic_Missile as mm

stats = {
    "base_level": 6,
    "str": 9,
    "dex": 14,
    "con": 10,
    "int": 18,
    "wis": 12,
    "cha": 12,
    "base_evasion": 12,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 1,
    "damage": "1d4",
    "dc": 10,
    "hit_dice": 8,
    "loot": {
        "gold": 15,
        "xp": 8,
        "drops": []
    }
}

class Evil_Eye(mob.Mob):
    def __init__(self, id="Evil Eye", level = (6,11), statblock=stats):
        super().__init__(id, level, statblock)

        self.roll_damage()
        self._stats["max_mp"] = 10 + self.bonus("int")
        self._mp = self.max_mp

        #flee threshold scales with missing MP, ie less MP == more likely to flee
        self._flee_threshold = self._flee_threshold + ((1.0 - self.remaining_mp) / 2)

    @property
    def damage_type(self):
        return "Magic" 
    @property
    def remaining_mp(self):
        return (self._mp / self.max_mp)
    @property
    def execute_trigger(self):
        return self._mp >= 3 and self._player.hp < self._player.max_hp // 2
    @property
    def death_ray_damage(self) -> str:
        return "2d6"

    def trigger(self):
        """
        Returns True if the player is low hp or if I can cast, else False
        """
        if not super().trigger():
            return False

        return self.execute_trigger or self.can_cast


    def spell(self):
        self.spend_ap()
        spell:mm.magic.Spell = mm.Magic_Missile(self)
        spell.cast(self._player)
        del spell
        return None

    def death_ray(self):
        import player_commands

        self.spend_ap(0)
        self._mp -= 3

        global_commands.type_text(f"The {self._id} begins charging its Death Ray...")

        roll = self.roll_to_hit()

        match roll:
            case 0:
                global_commands.type_text("A critical hit. Uh oh...")
                self._stats["damage_multiplier"] += 1
                dmg = global_commands.XdY(self.death_ray_damage)
                dmg = (dmg + (self.bonus("int") // 2)) * self.damage_multiplier
                taken = self._player.take_damage(dmg, self)
                self._stats["damage_multiplier"] -= 1
            case 1:
                return self.crit_fail()
            case _:
                if roll > self._player.evasion:
                    global_commands.type_text("The magic beam hit you.")
                    dmg = global_commands.XdY(self.death_ray_damage)
                    dmg = (dmg + (self.bonus("int") // 2)) * self.damage_multiplier
                    taken = self._player.take_damage(dmg, self)
                else:
                    global_commands.type_text("It missed.")
                    return None
        
        if self.execute_trigger:
            missing_hp = self._player.max_hp - self._player.hp
            percent_missing = (missing_hp * 100) / self._player.max_hp
            #execute chance is a magic number but it increases with missing HP
            execute_chance = percent_missing * (0.1 + (percent_missing / 10))
            if global_commands.probability(execute_chance):
                global_commands.type_text(f"The {self.id} attempts to execute you...")
                if self._player.roll_a_check("con") >= self.dc:
                    global_commands.type_text("It failed.")
                else:
                    global_commands.type_text(f"You were executed by the {self.id}'s Death Ray!")
                    player_commands.end_game()
        return None

    def special(self) -> bool:
        """
        Picks which magic attack the Evil Eye uses
        """
        if self.execute_trigger and self.can_full_round:
            self.death_ray()
        else:
            self.spell()
        
        return True

    
    def roll_text(self):
        base = super().roll_text()        
        me = [
            f"",
        ]
        return base + me

    def hit_text(self):
        base = super().hit_text()
        me = [
            f"",
        ]
        return base + me

    def miss_text(self):
        base = super().miss_text()
        me = [
            f"",
        ]
        return base + me

object = Evil_Eye
