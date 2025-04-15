import random
import csv
import globals
import game_objects
import game
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

class Mob(game_objects.Game_Object):

        def __init__(self, id:str="default"):
            #identification
            super().__init__(id)
            self.base_save_dc = 0
            self.retreating = False
            self._flee_threshold = 10
            self.load()

        #properties
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
        def caster_level(self) -> int:
            return max(1, self.level // 5)

        @property
        def fleeing(self) -> bool:
            return self.flee_check() or self.retreating

        @property
        def flee_threshold(self) -> float:
        #Percent current %HP threshold at which the enemy tries to flee (higher ==> more cowardly)
            return self._flee_threshold

        @property
        def target(self) -> "game_objects.Game_Object":
            return game.PLAYER

        #methods
        def flee_check(self):
            """Checks if the mob's health is low enough to attempt a flee"""
            if self.hp <= self.stats.max_hp * (self.flee_threshold/100) and self.roll_a_check("cha") < 13:
                self.retreating = True
                return self.retreating
            return False

        #ROLLS
        def roll_damage(self) -> mechanics.DamageInstance:
            """Rolls damage (damage dice)"""
            dmg = globals.XdY(self.stats.damage)
            dmg += self.bonus("str")

            return mechanics.DamageInstance(self, dmg)

        #COMBAT
        def attack(self) -> None:
            super().attack()

        def fumble_table(self) -> bool:
            """Determines if a mob sufferes a negative effect upon rolling a nat 1."""
            return globals.probability(50)
            
        def attack_of_oppurtunity(self) -> bool:
            """Rolls an attack of opportuity against the player"""
            if self.roll_to_hit() - 2 >= self.target.evasion():
                return True
            return False

        #ENCHANTMENTS
        def apply_on_attacks(self):
            return None

        def apply_on_hits(self):
            return None
        
        def apply_on_misses(self):
            pass

        #NARRATION

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

        def take_damage_narration(self, damage:"mechanics.DamageInstance") -> list[str]:
            taken = f"{damage.amount} damage"
            if damage.amount <= 0:
                damage.amount = 0
                taken = "no damage"
            source = f"{damage.header.damage}"
            text = [
                    f"{source} did {taken} to {self.header.default}.",
                    f"{source} dealt {taken} to {self.header.default}.",
                    f"{self.header.default} took {taken} from {source}."
                    ]

            #if source isnt a GameObject, don't add "hit you for..." text to final list, else do
            match damage.source:
                case game_objects.Game_Object():
                    text.append(f"{source} hit {self.id} for {taken}")
            return text
        
        #LOAD
        def load(self):
            """Loads the mob's info from the csv file"""
            source_stat_block = None

            #find my statblock in the source file
            with open(globals.MOBS_FILEPATH, "r") as file:
                r = csv.DictReader(file)
                for entry in r:
                    if entry["id"] == self.id:
                        source_stat_block = entry
                        break
                file.close()
            
            #throw an error if my id isn't found in the csv file
            if source_stat_block is None: raise ValueError(f"The id '{self.id}' was not found in the monster files.")

            #copy the statblock to my statblock and my own attributes
            self.stats.copy(source_stat_block)
            for entry in source_stat_block:
                if source_stat_block[entry] == "":
                    source_stat_block[entry] = None
                if entry in self.__dict__ and entry != "id":
                    self.__dict__[entry] = source_stat_block[entry]

            #set unqiue stats that require their own class instance (damage type)
            self.resistances = globals.build_damage_type(source_stat_block["resistances"])
            self.immunities = globals.build_damage_type(source_stat_block["immunities"])
            #generate level from my level range
            self.level = random.randrange(self.stats.level_range[0], self.stats.level_range[1])
            self.stats.level = self.level
            #set ap
            self.stats.max_ap = 1 + (self.level // 5)
            self.ap = self.stats.max_ap

            #calculate stats
            self.calculate_loot()
            self.calculate_hp()
            self.calculate_ability_scores()
        
        def calculate_loot(self):
            """Adds a random amount of bonus reward XP and Gold scaling with level"""
            for _ in range(self.level+1):
                xtra_gold = globals.d(6) 
                xtra_xp = globals.d(6)
                self.gold += xtra_gold * self.level // 3
                self.xp += xtra_xp * max(self.level // 5, 1)

        def calculate_hp(self) -> None:
            """Re-calculates mob's HP based on current level"""
            self.stats.max_hp = 0
            temp = self.stats.hit_die + self.bonus("con")
            for _ in range(self.level-1):
                temp += globals.d(self.stats.hit_die) + self.bonus("con")

            self.stats.max_hp = temp
            self.hp = self.stats.max_hp

        def calculate_ability_scores(self):
            """Randomly adds extra points to a mob's ability scores, increasing based on level"""
            for _ in range(self.level + 1 // 2):
                stat = random.choice(list(globals.ABILITY_SCORES.keys()))
                self.stats.__dict__[stat] += 1

        #SPECIALs + TRIGGER
        def special(self):
            """Mob's special move"""
            return self.monitor.get("Enraged") is None
        
        def trigger(self):
            """Trigger that determines if the mob should do their special move."""
            return self.monitor.get("Enraged") is None
