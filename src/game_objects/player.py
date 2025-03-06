import time, os, csv
from compendiums import combat_trick_compendium
import controllers.player_turn
import globals
import game_objects
import items
import controllers
import game
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import compendiums.combat_trick_compendium as combat_trick_compendium

class playerHeader(game_objects.Header):

    def __init__(self, parent):
        super().__init__(parent)
        self.combat_trick = None
        self._bonus_crit_range = None

    @property
    def default(self):
        return "you"
    
    @property
    def action(self):
        return "you are"
    
    @property
    def ownership(self):
        return "your"

class Player(game_objects.Game_Object):

    def __init__(self):
        super().__init__("Player")
        #self.conditions:"game_objects.Conditions_Handler" = game_objects.Conditions_Handler(self)
        self.level = 1
        self.stats.max_ap = 1 + (self.level // 5)

        self.header = playerHeader(self)

        self.armor:items.Armor = None
        self.weapon:items.Weapon = None
        
        self._bonus_crit_range = 0
        self.combat_trick:mechanics.Combat_Trick | None = None

    #properties
    @property
    def armor_value(self) -> int:
        if self.armor.broken: return 0
        return self.armor.armor_value

    @property
    def available_carrying_capacity(self) -> float:
        return self.carrying_capacity - self.carrying

    @property
    def bonus_crit_range(self) -> int:
        #bonus crit capped +4 (ie, min roll you can ever crit on is like a 14 with the correct weapon)
        return min(4, self._bonus_crit_range)

    @property
    def can_level_up(self) -> bool:
        """Checks if the player has enough XP to level up"""
        return self.xp >= (15 * self.level)

    @property
    def carrying_capacity(self) -> float:
        return 5.5 * self.stats.str
    
    @property
    def carrying(self) -> float:
        total_weight = 0
        for entry in self.inventory:
            if self.inventory[entry] is not None:#check to make sure the entry is valid
                held_item:"items.Item" = self.inventory[entry]
                total_weight += held_item.weight
        if self.armor is not None: total_weight += self.armor.weight
        if self.weapon is not None: total_weight += self.weapon.weight
        return total_weight

    @property
    def target(self):
        return game.SCENE.enemy

    #methods
    def update(self) -> None:
        super().update()
        if self.combat_trick is not None: self.combat_trick.update()

    def bonus(self, stat:str) -> int:
        match stat:
            case "dex":
                if self.armor is not None and self.armor.max_dex_bonus is not None:
                    return min(super().bonus("dex"), self.armor.max_dex_bonus)
            case _:
                return super().bonus(stat)

    def die(self) -> None:
        self.gold = 0
        self.inventory = {}
        #other stuff to be added

    #ROLLS
    def roll_to_hit(self) -> int:
        """Returns an attack roll (d20 + dex bonus + BAB + weapon attack bonus)"""
        if controllers.player_turn.GOD_MODE: return 999
        if self.weapon.broken is True:
            raise ValueError("Weapon is broken")

        roll = globals.d(20)
        match roll:
            case 1:
                return 1
            case _:
                #checks if the roll is a crit or not. Crits result in a return of 0
                #attack roll formula: roll + dex bonus + BaB + weapon att bonus
                if roll >= self.weapon.crit_range - self.bonus_crit_range:
                    return 0
                else: return roll + self.bonus("dex") + self.base_attack_bonus + self.weapon.attack_bonus
            
    def roll_damage(self) -> "mechanics.DamageInstance":
        """Returns a damage instance """
        if controllers.player_turn.GOD_MODE: return mechanics.DamageInstance(self.weapon, 999)#999
        if self.weapon.broken:
            globals.type_text(f"You can't use a broken {self.weapon.id}, so your hands will have to do.")
            amount = (globals.d(4) + self.bonus("str")) * self.stats.damage_multiplier
            return mechanics.DamageInstance(self, amount)
        
        self.weapon.lose_durability()
        amount = (self.weapon.roll_damage() + self.bonus("str")) * self.stats.damage_multiplier
        return mechanics.DamageInstance(self.weapon, amount)

    #MODIFY RESOURCES
    def lose_hp(self, num:int) -> None:
        super().lose_hp(num)
        if self.dead:
            controllers.player_turn.end_game()
        return None

    def level_up(self, stat: str) -> None:
        """Levels up a given stat"""
        self.stats.modify(stat, 1)
        self.xp -= 15 * self.level
        self.level += 1
        prev_max = self.stats.max_hp
        self.stats.max_hp += (globals.d(self.stats.hit_die) + self.bonus("con"))
        if self.hp == prev_max:# ie, you were full HP before level up
            self.hp = self.stats.max_hp
        if self.hp < (prev_max * .5): #if you were under 1/2 HP, heal to 1/2 HP
            self.hp = (self.stats.max_hp * 0.5)

    def gain_xp(self, xp:int) -> None:
        """Increases player XP by a given amount"""
        if xp <= 0:
            return None
        globals.type_text(f"{xp} XP earned.")
        self.xp += xp
    
    def gain_gold(self, num:int, silently:bool=False) -> None:
        """Increases player gold by a given amount"""
        if num <= 0:
            return None
        if silently is False:
            globals.type_text(f"{num} Gold gained.")
        self.gold += num

    def spend_gold(self, num:int) -> bool:
        """Reduces player gold by a given amount. Return False if the player doesnt have enough gold to spend"""
        if num > self.gold:   
            return False
        self.gold -= num
        globals.type_text(f"{num} gold spent. {self.gold} gold remaining.")
        return True

    #COMBAT
    def attack(self) -> None:
        super().attack()
        self._bonus_crit_range = 0
    
    def use(self, item:"items.Item"):
        if super().use(item) is False:
            base = globals.get_type(item)
            match base:
                case "Equipment": 
                    self.equip(item)
                    return True
            globals.error_message(None, f"You can't use an item of type '{base}'. Please try again.")
            return False
        return True
    
    #ENCHANTMENTS
    def apply_on_attacks(self):
        return None

    def apply_on_hits(self):
        return None
    
    def apply_on_misses(self):
        return None

    #CRITS
    def critical_hit(self) -> None:
        crit = 2 if self.weapon.broken or self.weapon is None else self.weapon.crit
        self.stats.damage_multiplier = crit
        taken = self.target.take_damage(self.roll_damage())
        self.apply_on_hits()
        self.stats.damage_multiplier = 1
        return None

    #NARRATION
    def roll_narration(self, roll):
        roll_text = self.process_roll(roll)
        text = [
            f"You heft your {self.weapon.id} and attack the {self.target.id},",
            f"You charge the {self.target.id},",
            f"You swing your {self.weapon.id},",
            f"Brandishing your {self.weapon.id}, you prepare to strike...",
        ]
        for idx, entry in enumerate(text):
            entry = entry + " " + roll_text
            text[idx] = entry
        return text

    def hit_narration(self) -> None:
        text = [
            f"A hit.",
            f"The {self.target.id} didn't get out of the way in time.",
            f"You hit the {self.target.id}.",
            f"Your attack lands.",
            f"Your {self.weapon.id} strikes true.",
            f"The {self.target.id} wasn't able to dodge this one.",
            f"Success."
        ]
        return text

    def miss_narration(self) -> None:
        text = [
            f"You missed.",
            f"No luck this time.",
            f"The {self.target.id} deftly dodges your attack.",
            f"Your attack whizzes past the {self.target.id}, missing by a hair.",
            f"You don't crack the {self.target.id}'s defenses this time.",
            f"It leaps out of the way in the nick of time.",
            f"No dice.",
            f"A miss.",
            f"The {self.target.id} ducks your strike.",
            f"The {self.target.id} manages to weather your onslaught for now."
        ]
        return text
    
    def take_damage_narration(self, damage:"mechanics.DamageInstance"):
        taken = f"{damage.amount} damage"
        if damage.amount <= 0: 
            damage.amount = 0
            taken = "no damage"
        source = f"{damage.header.damage}"
        text = [
            f"You took {taken} from {source}.",
            f"{source} dealt {taken} to you.",
            f"{source} did {taken}.",  
            ]

        #if source isnt a GameObject, don't add "hit you for..." text to final list, else do
        match source:
            case game_objects.Game_Object():
                text.append(f"{source} hit you for {taken}.")
        return text
    
    def heal_narration(self, num: int) -> list[str]:
        globals.type_text(f"You healed {num} HP.")

    def process_roll(self, roll) -> str:
        vowel = f"rolling an {roll}."
        match roll:
            case 0:
                return f"rolling a critical hit!"
            case 1:
                return "rolling a natural 1!"
            case 8:
                return vowel
            case 11:
                return vowel
            case 18:
                return vowel
            case _:
                return f"rolling a {roll}."

    #TRICKS
    def power_attack(self) -> int:
        self.combat_trick = combat_trick_compendium.dict["Power_Attack"](self)
        self.combat_trick.start()

    def feint(self) -> None:
        self.combat_trick = combat_trick_compendium.dict["Feint"](self)
        self.combat_trick.start()
    
    def riposte(self) -> None:
        pass

    def total_defense(self):
        self.combat_trick = combat_trick_compendium.dict["Total_Defense"](self)
        self.combat_trick.start()

    def all_out(self):
        self.combat_trick = combat_trick_compendium.dict["All_Out"](self)
        self.combat_trick.start()

    def study_weakness(self):
        self.combat_trick = combat_trick_compendium.dict["Study_Weakness"](self)
        self.combat_trick.start()

    #INVENTORY STUFF
    def pick_up(self, item: items.Item | items.Stackable, silent:bool=False) -> bool:
        if self.can_carry(item):
            return super().pick_up(item, silent)
        else:
            return False

    def equip(self, item: "items.Item", silent=False) -> bool:
        """Equips the player with a given equipment"""
        match item:
            case items.Weapon():
                prev = self.weapon
                self.pick_up(prev, True)
                self.drop(item)
                self.weapon = item
            case items.Armor():
                prev = self.armor
                self.pick_up(prev, True)
                self.drop(item)
                self.armor = item
            case _:
                return False
        if not silent: globals.type_text(f"{item.id} equipped.")
        item.owner = self
        return True

    #Add an unequip function

    def can_carry(self, item:items.Item | None) -> bool:
        """Checks if the player can carry item. Returns True if they can, False if not"""
        if item is None: return False
        else: return self.carrying + item.weight <= self.carrying_capacity

    def print_inventory(self) -> None:
        line_len = 30
        globals.type_with_lines()
        print(f'{line_len * " "}Inventory:{line_len * " "}\t\t\tEquipped:\n')
        self.display_inventory()
        print(f"Gold: {self.gold}g", end='')
        time.sleep(0.05)
        print(f"\t Carrying Capacity: {self.carrying}/{self.carrying_capacity}\n")
        globals.type_with_lines()

    def display_items(self, start:int, equipment:"items.Item"):
        """Processes an item's format property and feeds it to globals.print_line_by_line
            to be printed"""
        index = start
        item_1 = [""]
        item_2 = [""]
        equip_format = [""]
        if self.get_item(index + 1) is not None:
            item_1 = self.get_item(index).format
            item_1[0] = f"{index+1}. {item_1[0]}"

            item_2 = self.get_item(index + 1).format
            item_2[0] = f"{index+2}. {item_2[0]}"
        elif self.get_item(index) is not None:
            item_1 = self.get_item(index).format
            item_1[0] = f"{index+1}. {item_1[0]}"

        if equipment is not None:
            equip_format = equipment.format
            equipment_index = 1 if index == 0 else index
            equip_format[0] = f"{equipment_index}. {equip_format[0]}"

        globals.print_line_by_line([item_1, item_2, equip_format])

    def display_inventory(self):
        """Formats and prints the players inventory, line-by-line"""
        item_index = 0

        while(item_index < len(self.inventory) + 4):
            equipment = None
            if item_index == 0:
                equipment = self.weapon
            elif item_index == 2:
                equipment = self.armor
            self.display_items(item_index, equipment)
            item_index += 2
            print("\n")

    def receive_loot(self):
        self.gain_xp(self.target.xp)
        self.gain_gold(self.target.gold)
        for entry in self.target.inventory:
            self.pick_up(self.target.inventory[entry])

    ##MISC.
    def save(self) -> dict:
        self.monitor.cleanse_all()

        player_tod = {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "xp":self.xp,
            "gold":self.gold
        }

        for entry in self.stats.__dict__:
            player_tod[entry] = self.stats.__dict__[entry]

        return player_tod
    
    def load(self, stats_file, inventory_file) -> None:
        #first check if save file is empty
        empty_check = True if os.stat(stats_file).st_size == 0 else False
        if empty_check: return None
        #if it's not, set values to save file values
        with open(stats_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.name = row["name"]
                self.level = int(row["level"])
                self.hp = int(row["hp"])
                self.xp = int(row["xp"])
                self.gold = int(row["gold"])
                self.reset_ap()

                self.stats.load(stats_file)
            file.close()
                
        self.load_inventory(inventory_file)
    
    def load_inventory(self, filename) -> None:
        #check if inventory file is emtpty
        empty_check = True if os.stat(filename).st_size == 0 else False
        if empty_check: return None
        size = 0
        self.inventory = {}
        self.weapon = None
        self.armor = None
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                size += 1
            file.close()
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                item = globals.create_item(row)
                if idx >= size - 2:
                    self.equip(item, True)
                else:
                    self.pick_up(item, True)
            file.close()

"""
# arush wrote this while drunk, he won't let me delete it
class bitch(event.Event):
    def __init__(self, num_bitches: int):
        var: str = "bitch"
        self.bitches = num_bitches
        return f"miles has {self.bitches} {var}s"
"""
