#Evil Eye mob file
import mob, global_commands
from spells import Magic_Missile

stats = {
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
        return self._mp >= 2 and self._player.hp < self._player.max_hp // 2
    @property
    def death_ray_damage(self) -> str:
        return "2d6"

    def trigger(self):
        """
        Returns True if you have more than 5 MP or player is below 50% HP
        """
        if self._mp > 5 or self._player.hp < self._player.max_hp // 2:
            return True
        #if player not below execute threshold, and less than half MP, 70% of just magic missiling again
        elif global_commands.probability(70) and self._mp > 0:
            return True
        return False

    def spell(self):
        self.spend_ap()
        spell:Magic_Missile.magic.Spell = Magic_Missile.Magic_Missile(self)
        spell.cast(self._player)
        del spell
        return None

    def death_ray(self):
        import player_commands

        self.spend_ap(0)
        self._mp -= 3

        global_commands.type_text(f"The {self._id} begins charging its Death Ray...")

        roll = self.roll_attack()

        self._stats["damage_multiplier"] += 1 if roll == 0 else 0
        hit_text = "A critical hit. Uh oh..." if roll == 0 else "The magic beam hit you."

        if roll > self._player.evasion or roll == 0:
            global_commands.type_text(hit_text)
            dmg = global_commands.XdY(self.death_ray_damage)
            dmg = (dmg + self.bonus("int")) * self.damage_multiplier
            taken = self._player.take_damage(dmg, self)
            self._stats["damage_multiplier"] -= 1 if roll == 0 else 0
        else:
            global_commands.type_text("It missed.")
            return None
        
        if self.execute_trigger:
            missing_hp = self._player.max_hp - self._player.hp
            percent_missing = (missing_hp * 100) / self._player.max_hp
            #execute chance is a magic number but it increases with missing HP
            execute_chance = percent_missing * (0.1 + (percent_missing / 10))
            if global_commands.probability(execute_chance):
                global_commands.type_text("The Evil Eye attempts to execute you...")
                if self._player.roll_a_check("con") >= self.dc:
                    global_commands.type_text("It failed.")
                else:
                    global_commands.type_text("You were executed by the Evil Eye's dark magic!")
                    player_commands.end_game()
        return None

    def special(self) -> bool:
        """
        Picks which magic attack the Evil Eye uses
        """
        if self._player.hp < self._player.max_hp // 2 and self._mp > 3:
            self.death_ray()
        elif self._mp > 0:
            self.spell()
        else:#if no MP, must attack
            return False
        return True

object = Evil_Eye
