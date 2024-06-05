import random
import global_commands
import status_effects

default = {
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
    "armor": 0,
    "damage": "1d6",
    "dc": 10,
    "loot": {
        "gold": 0,
        "xp": 0,
        "drops": []
    }
}

class Mob():

    def __init__(self, id:str="Anonymous_Mob", level:tuple= (1, 20), statblock=None):
        #identification
        import global_variables
        import player
        import status_effects

        self._id = id
        self._name = self._id
        self._level = random.randrange(min(level), max(level)+1)
        self._range = level

        self._stats = {}
        self._stats["max_mp"] = 0

        #if no statblock, use default
        if not statblock:
            print("No statblock given.\n")
            statblock = default

        #copy statblock items to self._stats
        for entry in statblock:
            self._stats[entry] = statblock[entry]

        #copy loot info to self._stats
        self._loot = {}
        for item in self._stats["loot"]:
            self._loot[item] = self._stats["loot"][item]

        #calculate stats
        self.calculate_hp()
        self._stats["max_ap"] = 1 + (self._level // 5)
        self._ap = self.max_ap

        # percent current HP threshold at which the enemy tries to flee (higher==more cowardly)
        self._flee_threshold = 0.2
        self._player:player.Player = global_variables.PLAYER

        self._status_effects: dict[str: status_effects.Status_Effect] = {}

        self._retreating = False
        self._my_effect_id = ""

        self.update()
        self.calculate_loot()

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def damage_header(self) -> str:
        return self._id
    @property
    def damage_type(self) -> str:
        return "Physical"
    @property
    def dead(self) -> bool:
        return self.hp <= 0
    @property
    def level(self) -> int:
        return self._level
    @property
    def caster_level(self) -> int:
        return max(1, self.level // 5)
    @property
    def damage(self) -> int:
        return self._stats["damage"]
    @property
    def evasion(self) -> int:
        return self._stats["base_evasion"] + self.bonus("dex")
    @property
    def armor(self) -> int:
        return self._stats["armor"]
    @property
    def max_mp(self) -> str:
        return self._stats["max_mp"]
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def loot(self) -> dict:
        return self._loot
    @property
    def name(self) -> str:
        return self._name
    @property
    def damage_multiplier(self) -> int:
        return self._stats["damage_multiplier"]
    @property
    def damage_taken_multiplier(self) -> int:
        return self._stats["damage_taken_multiplier"]
    @property
    def dc(self) -> int:
        return self._stats["dc"]
    @property
    def max_hp(self) -> int:
        return self._stats["max_hp"]
    @property
    def max_ap(self) -> int:
        return self._stats["max_ap"]
    @property
    def ap(self) -> int:
        return self._ap
    @property
    def can_act(self) -> bool:
        return self._ap > 0 and not self.dead
    @property
    def can_cast(self) -> bool:
        return self._mp > 0
    @property
    def fleeing(self) -> bool:
        return self.flee_check() or self._retreating
    @property
    def range(self) -> int:
        return self._range
    @property
    def stats(self) -> dict:
        return self._stats
    @property
    def applied(self) -> bool:
        return self._my_effect_id in self._player.status_effects

    #MISC.
    def bonus(self, stat:str) -> int:
        """
        Returns the numerical bonus of the given stat
        """
        return global_commands.bonus(self._stats[stat])
    
    def calculate_hp(self) -> None:
        """
        Re-calculates mob's HP based on current level,
        then sets stats['hp'] and self._hp variables appropriately
        """
        self._stats["max_hp"] = 0
        temp = self._stats["hit_dice"] + self.bonus("con")
        for _ in range(self._level-1):
            temp += global_commands.d(self._stats["hit_dice"]) + self.bonus("con")

        self._stats["max_hp"] = temp
        self._hp = self.max_hp

    def flee_check(self):
        """
        Checks the enemy should be fleeing
        """
        if self._hp <= self.max_hp * self._flee_threshold and self.roll_a_check("cha") > 10:
            self._retreating = True
            return self._retreating
        return False

    #ROLLS
    def roll_attack(self) -> int:
        """
        Rolls an attack (d20)
        """
        roll = global_commands.d(20)

        if roll == 1:
            return 1
        if roll == 20:
            return 0
        
        return roll + self.bonus("dex") + (self._level // 5)

    def roll_a_check(self, stat:str):
        """
        Rolls a check with a given stat
        """
        return global_commands.d(20) + self.bonus(stat)
    
    def roll_damage(self) -> int:
        """
        Rolls damage (damage dice)
        """
        dmg = global_commands.XdY(self.damage)
        return (dmg + self.bonus("str")) * self.damage_multiplier
    
    def take_damage(self, taken:int, src, armor_piercing=False) -> int:
        """
        Takes a given amount of damage, reduced by armor
        """
        import status_effects
        import items

        src:status_effects.Status_Effect | items.Item = src

        taken *= self.damage_taken_multiplier
        if armor_piercing:
            self._hp -= taken
            if src == self._player:
                global_commands.type_text(f"You did {taken} damage to the {self._id}.")
            else:
                global_commands.type_text(f"The {self._id} took {taken} damage from the {src.damage_header}.")
            return taken

        if src.damage_type == "Physical":
            if (taken - self.armor) <= 0:
                if src == self._player:
                    global_commands.type_text(f"You did no damage to the {self._id}.")
                else:
                    global_commands.type_text(f"The {self._id} took no damage from the {src.damage_header}.")
                return 0
            else:
                self._hp -= taken - self.armor
                if src == self._player:
                    global_commands.type_text(f"You did {taken - self.armor} damage to the {self._id}.")
                else:
                    global_commands.type_text(f"The {self._id} took {taken - self.armor} damage from the {src.damage_header}.")
                return taken - self.armor
        else:
            self._hp -= taken
            if src == self._player:
                global_commands.type_text(f"You did {taken} damage to the {self._id}.")
            else:
                global_commands.type_text(f"The {self._id} took {taken} damage from the {src.damage_header}.")
            return taken

        
    def fumble_table(self) -> bool:
        """
        Determines if a mob sufferes a negative effect upon rolling a nat 1.
        """
        return global_commands.probability(50)
        
    def attack_of_oppurtunity(self) -> bool:
        """
        Rolls an attack of opportuity against the player
        """
        if self.roll_attack() - 2 >= self._player.evasion:
            return True
        return False
    
    #Resources
    def heal(self, num:int) -> None:
        #heals for the given amount up to max hp value
        prev = self._hp
        self._hp = self._hp + num if (self._hp + num <= self.max_hp) else self.max_hp
        global_commands.type_text(f"The {self._id} healed {self._hp - prev} HP.")

    def spend_ap(self, num:int=1) -> None:
        """
        Spends an amount of AP
        """
        if num == 0:#spend_ap(0) indicates a full round action, uses all AP
            self._ap = 0
            return None
        if self.can_act is True:
            self._ap -= 1
        else:
            raise ValueError("No AP to spend")
        
    def reset_ap(self):
        """
        Resets mob's AP to max value
        """
        self._ap = self.max_ap

    def spend_mp(self, num:int=1) -> bool:
        if num == 0:
            self._mp = 0
            return False
        
        if self._mp >= num:
            self._mp -= num
            return True
        return False
    
    def regain_mp(self, num:int=None):
        if num is None:
            self._mp = self.max_mp
            return True
        self._mp += num
        return True
    
    #STATUS EFFECTS
    def add_status_effect(self, effect:status_effects.Status_Effect) -> None:
        """
        Adds a status effect to the mob
        """
        if effect.id in self._status_effects:
            #if we have the effect already, run the effect's additional_effect function and kick out
            applied = self._status_effects[effect.id]
            applied.additional_effect(effect)
            return None
        self._status_effects[effect.id] = effect
        effect.apply()

    def remove_status_effect(self, effect:status_effects.Status_Effect) -> None:
        """
        Removes a status effect from the mob
        """
        del self._status_effects[effect.id]
        effect.cleanse()
        return None

    #Updates
    def calculate_loot(self):
        """
        Adds a random extra amount of XP and Gold per level it is above base
        to the mob's loot pool
        """
        for _ in range(self._range[0], self._level+1):
            x_gold = global_commands.d(6) 
            x_xp = global_commands.d(6)
            self._loot["gold"] += x_gold * self._level // 3
            self._loot["xp"] += x_xp * max(self._level // 5, 1)

    def update(self):
        """
        Updates all relevant stats when a mob's level is changed,
        updates status effects and removes them when their duration
        expires. 
        """
        self.reset_ap()
    
        #update all status effects
        inactive = []
        for entry in self._status_effects:
            effect:status_effects.Status_Effect = self._status_effects[entry]
            effect.update()
            if effect.active is False:
                inactive.append(effect)
        for effect in inactive:
            self.remove_status_effect(effect)
        inactive = []

    def special(self):
        """
        Mob's special move
        """
        raise NotImplementedError
    
    def trigger(self):
        """
        Trigger that determines if the mob should do their special move
        """
        return False
