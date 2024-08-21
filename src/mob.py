import random
import global_commands
import status_effect

default = {
    "base_level": 1,
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

    def __init__(self, id:str="Anonymous_Mob", level:tuple=(1, 20), statblock=None):
        #identification
        import global_variables
        import player
        import status_effect

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
        
        self._temp_hp = None

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

        self._status_effects: dict[str: status_effect.Status_Effect] = {}

        self._retreating = False
        self._my_effect_id = ""
        self._prev_narration = ""

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
    def can_full_round(self) -> bool:
        return self._ap == self.max_ap
    @property
    def flee_threshold(self) -> float:
        return self._flee_threshold
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
        if self._hp <= self.max_hp * self._flee_threshold and self.roll_a_check("cha") < 13:
            self._retreating = True
            return self._retreating
        return False

    #ACTIONS
    def attack(self) -> None:
        import global_variables
        player = global_variables.PLAYER

        roll = self.roll_to_hit()
        self.spend_ap()
        self.narrate(self.roll_text)
        match roll:
            case 0:
                return self.crit()
            case 1:
                return self.crit_fail()
            case _:
                pass
        if roll >= player.evasion:
            self.narrate(self.hit_text)
            taken = player.take_damage(self.roll_damage(), self)
            return None

        self.narrate(self.miss_text)

        #check if player is riposting
        if player.riposting is True: # and player.evasion - roll >= (self._player.bonus("dex") - 5)
            taken = self.roll_damage()
            self.take_damage(max(1, taken//2), "your riposte")

        return None

    def crit(self) -> bool:
        import global_variables
        player = global_variables.PLAYER

        global_commands.type_text(f"A critical hit! Uh oh.")
        self._stats["damage_multiplier"] += 1
        taken = player.take_damage(self.roll_damage(), self)
        self._stats["damage_multiplier"] -= 1
        return None
    
    def crit_fail(self) -> None:
        global_commands.type_text("It critically failed!")
        if self.fumble_table():
            taken = self.take_damage(self.roll_damage(), self)
        else:
            global_commands.type_text("It missed.")
        return None

    def fumble_table(self) -> bool:
        """
        Determines if a mob sufferes a negative effect upon rolling a nat 1.
        """
        return global_commands.probability(50)
        
    def attack_of_oppurtunity(self) -> bool:
        """
        Rolls an attack of opportuity against the player
        """
        if self.roll_to_hit() - 2 >= self._player.evasion:
            return True
        return False

    #NARRATION
    def narrate(self, func) -> None:
        text:list = func()
        if self._prev_narration in text:
            text.remove(self._prev_narration)
        final = random.choice(text)
        self._prev_narration = final
        global_commands.type_text(final)
        return None

    def roll_text(self) -> list[str]:
        text = [
            f"The {self.id} moves to attack.",
            f"The {self.id} lunges at you.",
            f"The {self.id} prepares to strike..."
        ]
        return text
    
    def hit_text(self) -> list[str]:
        text = [
            f"You fail to move before the attack hits you.",
            f"A hit.",
            f"The {self.id} hits you.",
            f"It's attack lands.",
            f"You can't dodge this one.",
            f"You take a hit.",
            f"The {self.id} manages to break your guard."
        ]
        return text
    
    def miss_text(self) -> list[str]:
        text = [
            f"It's attack goes wide.",
            f"Luck is on your side this time.",
            f"The {self.id} fails.",
            f"You stave off the attack.",
            f"The attack flies right by you.",
            f"You are unscathed.",
            f"The {self.id} doesn't manage to hit you.",
            f"You leap out of harm's way."
        ]
        return text

    #ROLLS
    def roll_to_hit(self) -> int:
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
    
    def take_damage(self, taken:int, attacker, armor_piercing=False) -> int:
        """
        Takes a given amount of damage, reduced by armor

        taken: the amount of damage
        attacker: a str or class object that determines the narration
        text of the damage (ie 'your sword' vs 'the boulder')

        """
        import status_effect
        import items
        import global_variables

        dmg_type = "Physical"
        src = attacker
        if type(attacker) is status_effect.Status_Effect or type(attacker) is items.Consumable:
            attacker:status_effect.Status_Effect | items.Item = attacker
            src = "the " + attacker.damage_header
            dmg_type = attacker.damage_type

        taken *= self.damage_taken_multiplier
        if armor_piercing or  dmg_type != "Physical":
            self.lose_hp(taken)
            if attacker == self._player:
                global_commands.type_text(f"You did {taken} damage to the {self._id}.")
            else:
                global_commands.type_text(f"The {self._id} took {taken} damage from {src}.")
            return taken
        else:
            if (taken - self.armor) <= 0:
                if attacker == self._player:
                    global_commands.type_text(f"You did no damage to the {self._id}.")
                else:
                    global_commands.type_text(f"The {self._id} took no damage from {src}.")
                return 0
            else:
                self.lose_hp(taken - self.armor)
                if attacker == self._player:
                    global_commands.type_text(f"You did {taken - self.armor} damage to the {self._id}.")
                else:
                    global_commands.type_text(f"The {self._id} took {taken - self.armor} damage from {src}.")
                return taken - self.armor


    #RESOURCES
    def lose_hp(self, num:int) -> None:
        if self._temp_hp is not None:
            self._temp_hp -= num
            self._hp -= abs(self._temp_hp) if self._temp_hp < 0 else 0
            self._temp_hp = None if self._temp_hp <= 0 else self._temp_hp
        else:
            self._hp -= num
        return None

    def heal(self, num:int) -> None:
        #heals for the given amount up to max hp value
        prev = self._hp
        self._hp = self._hp + num if (self._hp + num <= self.max_hp) else self.max_hp
        global_commands.type_text(f"The {self._id} healed {self._hp - prev} HP.")
    
    def gain_temp_hp(self, num:int) -> None:
        """
        Gain a set amount of temp hp. Temp hp is removed before 
        actual hp during damage calculations. temp hp cannot be
        healed, and is removed (set back to None) if it ever drops below 0.
        """
        if self._temp_hp is None:
            self._temp_hp = num
        else: self._temp_hp += num
        return None
    
    def remove_temp_hp(self, num:int) -> None:
        """
        Removes a set amount of temp hp, resetting it to None
        if it drops below 0 as a result. 
        """
        if self._temp_hp is None:
            return None
        
        self._temp_hp -= num
        self._temp_hp = None if self._temp_hp <= 0 else self._temp_hp
        return None

    def spend_ap(self, num:int=1) -> None:
        if num == 0:#spend_ap(0) indicates a full round action, uses all AP
            self._ap = 0
            return None
        if self.can_act is True:
            self._ap -= 1
        else:
            raise ValueError("No AP to spend")
        
    def reset_ap(self):
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
    
    #SETTERS
    def set_flee_threshold(self, num:float):
        self._flee_threshold == num
    
    #STATUS EFFECTS
    def add_status_effect(self, effect:status_effect.Status_Effect) -> None:
        """
        Adds a status effect to the mob
        """
        if effect.id in self._status_effects:
            #if we have the effect already, run the effect's additional_effect function and kick out
            applied:status_effect.Status_Effect = self._status_effects[effect.id]
            applied.additional_effect(effect)
            return None
        self._status_effects[effect.id] = effect
        effect.apply()

    def remove_status_effect(self, effect:status_effect.Status_Effect) -> None:
        """
        Removes a status effect from the mob
        """
        del self._status_effects[effect.id]
        effect.cleanse()
        return None

    #UPDATES
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

    def initialize(self):
        from global_variables import STATS

        level_mod = self.level - self._stats["base_level"] // 2

        for i in range(level_mod):
            stat = random.choice(list(STATS.keys()))
            stat += 1

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
            effect:status_effect.Status_Effect = self._status_effects[entry]
            effect.update()
            if effect.active is False:
                inactive.append(effect)
        for effect in inactive:
            self.remove_status_effect(effect)
        inactive = []       

    #SPECIAL
    def special(self):
        """
        Mob's special move
        """
        if "Enraged" in self._status_effects:
            return False
        return True
    
    def trigger(self):
        """
        Trigger that determines if the mob should do their special move.
        Mobs can't do specials while under certain effects, and each mob
        runs it's parent trigger function to see if it is able to do it's special
        or if it must attack due to effects.
        """
        return "Enraged" in self._status_effects
