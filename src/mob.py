import random
import global_commands
from game_object import Game_Object, Conditions_Handler

default = {
    "level": 1,
    "level_range": (1, 20),
    "hit_dice": 8,
    "str": 10,
    "dex": 10,
    "con": 10,
    "int": 10,
    "wis": 10,
    "cha": 10,
    "base_evasion": 9,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 1,
    "max_mp": 0,
    "armor": 0,
    "damage": "1d6",
    "dc": 10,
}

class Mob(Game_Object):

    def __init__(self, id:str="Anonymous_Mob", stat_dict:dict=default):
        #identification
        super().__init__(id)
        self.conditions:Conditions_Handler = Conditions_Handler(self)
        self.stats.copy(stat_dict)
        self.level = random.randrange(self.stats.level_range[0], self.stats.level_range[1])
        self.stats.level = self.level

        self.retreating = False
        self.load()

    #properties
    @property
    def caster_level(self) -> int:
        return max(1, self.level // 5)

    @property
    def evasion(self) -> int:
        return self.stats.base_evasion + self.bonus("dex")

    @property
    def can_act(self) -> bool:
        return self.ap > 0 and not self.dead

    @property
    def can_cast(self) -> bool:
        return self.mp > 0

    @property
    def can_full_round(self) -> bool:
        return self.ap == self.stats.max_ap

    @property
    def flee_threshold(self) -> float:
    #Percent current %HP threshold at which the enemy tries to flee (higher==more cowardly)"""
        return 10

    @property
    def fleeing(self) -> bool:
        return self.flee_check() or self.retreating

    @property
    def target(self) -> Game_Object:
        import global_variables
        return global_variables.PLAYER

    #methods
    def flee_check(self):
        """Checks if the mob's health is low enough to attempt a flee"""
        if self.hp <= self.stats.max_hp * (self.flee_threshold/100) and self.roll_a_check("cha") < 13:
            self.retreating = True
            return self.retreating
        return False

    #ROLLS
    def roll_damage(self) -> int:
        """Rolls damage (damage dice)"""
        dmg = global_commands.XdY(self.stats.damage)
        return (dmg + self.bonus("str")) * self.stats.damage_multiplier

    #COMBAT
    def attack(self) -> None:
        super().attack()

    def fumble_table(self) -> bool:
        """Determines if a mob sufferes a negative effect upon rolling a nat 1."""
        return global_commands.probability(50)
        
    def attack_of_oppurtunity(self) -> bool:
        """Rolls an attack of opportuity against the player"""
        if self.roll_to_hit() - 2 >= self.target.evasion:
            return True
        return False

    #ENCHANTMENTS
    def apply_on_attacks(self):
        return None

    def apply_on_hits(self):
        return None

    #NARRATION
    def narrate(self, func, param=None):
        text:list[str] = func()
        if self.prev_narration in text:
            text.remove(self.prev_narration)
        final = random.choice(text)
        self.prev_narration = final
        global_commands.type_text(final)
        return None

    def roll_narration(self) -> list[str]:
        text = [
            f"The {self.id} moves to attack.",
            f"The {self.id} lunges at you.",
            f"The {self.id} prepares to strike..."
        ]
        return text
    
    def hit_narration(self) -> list[str]:
        text = [
            f"You fail to move before the attack hits you.",
            f"A hit.",
            f"The {self.id} hits you.",
            f"Its attack lands.",
            f"You can't dodge this one.",
            f"That's going to leave a mark...",
            f"The {self.id} manages to break your guard."
        ]
        return text
    
    def miss_narration(self) -> list[str]:
        text = [
            f"Its attack goes wide.",
            f"Luck is on your side this time.",
            f"The {self.id} fails.",
            f"You stave off the attack.",
            f"The attack flies right by you.",
            f"You are unscathed.",
            f"The {self.id} doesn't manage to hit you.",
            f"You leap out of harm's way."
        ]
        return text

    def take_damage_narration(self, info) -> list[str]:
        from player import Player
        from item import Item
        taken, source = info
        if taken > 0:
            match source:
                case Player():
                    text = [
                        f"You did {taken} damage to the {self.id}.",
                        f"The {self.id} took {taken} damage.",
                        f"You hit the {self.id} for {taken} damage.",
                        ]    
                case Item():
                    text = [
                        f"Your {source.id} did {taken} damage.",
                        f"The {source.id} dealt {taken} damage to the {self.id}.",
                        f"The {self.id} took {taken} damage from your {source.id}."
                    ]
        else: text = [f"The {self.id} took no damage!"] 
        return text
      
    #LOAD
    def load(self):
        """Updates the mob's loot, stats, and ability scores after level has been assigned"""
        self.gold = 0
        self.xp = 0
        self.stats.max_ap = 1 + (self.level // 5)
        self.ap = self.stats.max_ap
        #calculate stats
        self.calculate_loot()
        self.calculate_hp()
        self.calculate_ability_scores

    def calculate_hp(self) -> None:
        """Re-calculates mob's HP based on current level"""
        self.stats.max_hp = 0
        temp = self.stats.hit_dice + self.bonus("con")
        for _ in range(self.level-1):
            temp += global_commands.d(self.stats.hit_dice) + self.bonus("con")

        self.stats.max_hp = temp
        self.hp = self.stats.max_hp

    def calculate_loot(self):
        """Adds a random extra amount of XP and Gold per level it is above base to the mob"""
        for _ in range(self.level+1):
            xtra_gold = global_commands.d(6) 
            xtra_xp = global_commands.d(6)
            self.gold += xtra_gold * self.level // 3
            self.xp += xtra_xp * max(self.level // 5, 1)

    def calculate_ability_scores(self):
        """Randomly adds extra points to a mob's ability scores, increasing based on level"""
        from global_variables import CORE_STATS
        for _ in range(self.level + 1 // 2):
            stat = random.choice(list(CORE_STATS.keys()))
            self.stats.__dict__[stat] += 1

    #SPECIALs + TRIGGER
    def special(self):
        """Mob's special move"""
        return self.conditions.get("Enraged") is None
    
    def trigger(self):
        """Trigger that determines if the mob should do their special move.
        Mobs can't do specials while under certain effects, and each mob
        runs it's parent trigger function to see if it is able to do it's special
        or if it must attack due to effects."""

        return self.conditions.get("Enraged") is None
