import random, time, os, csv, enum
import global_commands
from game_object import Game_Object
from items import Item, Consumable, Weapon, Armor

class Stance(enum.Enum):
    NONE = 0
    RIPOSTE = 1
    TOTAL_DEFENSE = 2
    ALL_OUT = 3

class Player(Game_Object):

    def __init__(self, id="Player"):
        super().__init__(id)
        self.level = 1
        self.statblock.max_ap = 1 + (self.level // 5)

        #stances
        self.stance = Stance(0)

    #PROPERTIES
    @property
    def carrying_capacity(self) -> int:
        return int(5.5 * self.statblock.str)

    @property
    def available_carrying_capacity(self) -> int:
        return self.carrying_capacity - self.carrying

    @property
    def carrying(self) -> int:
        total_weight = 0
        for entry in self._inventory:
            if self._inventory[entry] is not None:#check to make sure the entry is valid
                held_item:Item = self._inventory[entry]
                total_weight += held_item.weight
        total_weight += self.weapon.weight + self.armor.weight
        return total_weight

    @property
    def can_level_up(self):
        """Checks if the player has enough XP to level up"""
        return self.xp >= (15 * self.level)

    @property
    def target(self):
        import controller
        return controller.SCENE.enemy

    #METHODS
    def bonus(self, stat:str) -> int:
        match stat:
            case "dex":
                if self.armor is not None and self.armor.max_dex_bonus is not None:
                    return min(super().bonus("dex"), self.armor.max_dex_bonus)
            case _:
                return super().bonus(stat)
    
    def die(self) -> None:
        self._gold = 0
        self._inventory = []
        #other stuff to be added

    #ROLLS
    def roll_to_hit(self) -> int:
        """Returns an attack roll (d20 + dex bonus + BAB + weapon attack bonus)"""
        if self.weapon.broken is True:
            raise ValueError("Weapon is broken")
        roll = global_commands.d(20)
        match roll:
            case 1:
                return 1
            case _:
                #checks if the roll is a crit or not. Crits result in a return of 0
                #attack roll formula: roll + dex bonus + BaB + weapon att bonus
                return 0 if roll >= self.weapon.crit_range else roll + self.bonus("dex") + (self.level // 5) + self.weapon.attack_bonus
            
    def roll_damage(self) -> int:
        """Returns a damage roll (weapon dice + str bonus)"""
        if self.weapon.broken:
            global_commands.type_text(f"You can't use a broken {self.weapon.id}, so your hands will have to do.")
            return (global_commands.d(4) + self.bonus("str")) * self.statblock.damage_multiplier
        
        self.weapon.lose_durability()
        return (self.weapon.roll_damage() + self.bonus("str")) * self.statblock.damage_multiplie

    #MODIFY RESOURCES
    def lose_hp(self, num:int) -> None:
        import player_commands
        super().lose_hp(num)
        if self.dead:
            player_commands.end_game()
        return None

    def level_up(self, stat: str) -> None:
        """Levels up a given stat"""
        self.statblock.dict[stat] += 1
        self.xp -= 15 * self.level
        self.level += 1
        prev_max = self.statblock.max_hp
        self.statblock.max_hp += (global_commands.d(self.statblock.hit_dice) + self.bonus("con"))
        if self._hp == prev_max:# ie, you were full HP before level up
            self._hp = self.statblock.max_hp
        if self._hp < (prev_max * .5): #if you were under 1/2 HP, heal to 1/2 HP
            self._hp = (self.statblock.max_hp * 0.5)

    def gain_xp(self, xp:int) -> None:
        """Increases player XP by a given amount"""
        if xp <= 0:
            return None
        global_commands.type_text(f"{xp} XP earned.")
        self.xp += xp
    
    def gain_gold(self, num:int, silently:bool=False) -> None:
        """Increases player gold by a given amount"""
        if num <= 0:
            return None
        if silently is False:
            global_commands.type_text(f"{num} Gold gained.")
        self.gold += num

    def spend_gold(self, num:int) -> bool:
        """Reduces player gold by a given amount. Return False if the player doesnt have enough gold to spend"""
        if num > self.gold:   
            return False
        self._gold -= num
        global_commands.type_text(f"{num} gold spent. {self.gold} gold remaining.")
        return True

    #COMBAT
    def attack(self) -> None:
        import player_commands

        if not player_commands.GOD_MODE:
            return super().attack()
        else:
            pass

    def take_damage(self, taken: int, source) -> int:
        if self.armor is None:
            self.armor = 0
        
        super().take_damage(taken, source)
    
    def use(self, item):
        pass
    
    #ENCHANTMENTS
    def apply_on_attacks(self):
        pass

    def apply_on_hits(self):
        pass
    
    #CRITS
    def critical_hit(self) -> None:
        crit = 2 if self.weapon.broken or self.weapon is None else self.weapon.crit
        self.statblock.damage_multiplier = crit
        taken = self.target.take_damage(self.roll_damage(), self)
        self.apply_on_hits()
        self.statblock.damage_multiplier = 1
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
        for entry in text:
            entry = f"{entry} {roll_text}"
        return text

    def hit_narration(self) -> None:
        text = [
            f"A hit.",
            f"The {self.target.id} didn't get out of the way in time.",
            f"You hit the {self.target.id}.",
            f"Your attack lands.",
            f"Your {self.weapon.id} strikes true.",
            f"The {self.target.id} wasn't able to dodge this one.",
            f"Sucess."
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
            f"A miss.",
            f"The {self.target.id} ducks your strike.",
            f"The {self.target.id} manages to weather your onslaught for now."
        ]
        return text
    
    def take_damage_narration(self, info:tuple[int, Game_Object]):
        taken, source = info
        if taken > 0:
            text = [
                f"You took {taken} damage from the {source.id}.",
                f"The {source.id} dealt {taken} damage to you.",
                f"The {source.id} did {taken} damage.",
                f"The {source.id} hit you for {taken} damage."
                ]
        else:
            text = [
                f"You took no damage from the {source.id}!",
                f"The {source.id} did no damage to you!",
                f"The {source.id} hit you for no damage.",
                ]
        return text
    
    def heal_narration(self, num: int) -> list[str]:
        return super().heal_narration(num)

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
        global_commands.type_text(f"You wind up for a powerful attack...")
    
    def feint(self) -> None:
        from conditions import Stat_Buff

        global_commands.type_text("You attempt a feint...")
        roll = self.roll_a_check("cha")
        self.spend_ap()

        if roll >= self.target.roll_a_check("cha"):
            global_commands.type_text(f"You faked out the {self.target.id}!")
            def_bonus = Stat_Buff.Condition(self, self)
            def_bonus.set_stat("base_evasion")
            def_bonus.set_duration(2)
            def_bonus.set_potency(max(2, self.bonus("cha")))
            self.add_status_effect(def_bonus)
        else:
            global_commands.type_text(f"The {self.target.id} spots your trick.")

        return None
    
    def riposte(self) -> None:
        from conditions import Stat_Buff

        global_commands.type_text("You ready yourself to repel any oncoming attacks...")

        self.spend_ap(2)
        rip_bonus = Stat_Buff.Condition(self, self)
        rip_bonus.set_id("Riposte")
        rip_bonus.set_cleanse_message("Your Riposte has ended.")
        rip_bonus.set_stat("base_evasion")
        rip_bonus.set_duration(1000000)
        rip_bonus.set_potency(2)
        self.add_status_effect(rip_bonus)

        self._stance = Stance(1)
        self._riposting = True

    def end_riposte(self) -> None:
        self._riposting = False

        if self.get_status_effect("Riposte") is not None:
            self.remove_status_effect(self.get_status_effect("Riposte"))

        return None

    #INVENTORY STUFF
    def pick_up(self, item: Item | Consumable, silent:bool=False) -> bool:
        if self.can_carry(item):
            return super().pick_up(item, silent)
        else:
            return False

    def equip(self, item: Item, silent=False) -> bool:
        """Equips the player with a given equipment"""
        match item:
            case Weapon():
                prev = self.weapon
                self.pick_up(prev)
                self.drop(item)
                self.weapon = item
            case Armor():
                prev = self.armor
                self.pick_up(prev)
                self.drop(item)
                self.armor = item
            case _:
                return False
        if not silent: global_commands.type_text(f"{item.name} equipped.")
        return True

    def can_carry(self, item:Item) -> bool:
        """Checks if the player can carry item. Returns True if they can, False if not"""
        return self.carrying + item.weight <= self.carrying_capacity

    def print_inventory(self, line_len=25) -> None:
        line_len = 25
        global_commands.type_with_lines()
        print(f'{line_len * " "} Inventory: {line_len * " "} \t \t\t Equipped:\n')
        
        self.format_inventory()
        
        print("\n")
        print(f"Gold: {self.gold}g", end='')
        time.sleep(0.05)
        print(f"\t Carrying Capacity: {self.carrying}/{self.carrying_capacity}\n")
        global_commands.type_with_lines()

    def format_inventory(self, line_len=25):
        """Formats and prints the players inventory, line-by-line"""
        import items
        last = False
        idx = 0
        mx = max(3, len(self._inventory))
        while(idx < mx):
            if idx % 2 == 0 and idx != 0:
                time.sleep(0.05)
                print("\n")
            weapon = list(self.weapon.format().values()) if idx == 0 else []
            w_header = f"1. {weapon[0]}" if idx == 0 else " "
            armor = list(self.armor.format().values()) if idx == 2 else []
            a_header = f"2. {armor[0]}" if idx == 2 else " "
            first = second = []
            header1 = header2 = " "
            if idx < len(self._inventory):
                #creates a list of the current item's format dictionary values 
                first = list(list(self._inventory.values())[idx].format().values())
                try:
                    #checks if this is the last item in the inventory or not
                    second = list(list(self._inventory.values())[idx + 1].format().values())
                except IndexError:
                    last = True
                    second = first
                #sets the items' headers (ex. "1. Greatsword (Uncommon)     2. Plated Steelcaps (Rare)")
                header1 = f"{idx+1}. {first[0]}"
                header2 = f"{idx+2}. {second[0]}" if not last else " "
            headers = (header1, header2, w_header, a_header)
            header1, header2, w_header, a_header = global_commands.match(headers, line_len)
            #sets header for equipped item, first weapon, then armor
            equipped_header = w_header if idx == 0 else a_header
            #print headers (first two item ids + weapon id)
            print(f" {header1} \t {header2} \t\t {equipped_header}")
            #finds longest necessary iteration length (ie longest item.format dictionary)
            long = max(len(first), len(second), len(weapon), len(armor))
            for i in range(1, long):
                #sets whats going to be printed on the current line
                str1 = first[i] if i < len(first) else " "
                #if the item.format dictionary doesn't go past the current index, print " "
                str2 = second[i] if i < len(second) and not last else " "
                #ditto, but for equipped items
                w = weapon[i] if idx == 0 and i < len(weapon) else " "
                a = armor[i] if idx == 2 and i < len(armor) else " "
                string = str1, str2, w, a
                str1, str2, w, a = global_commands.match(string, line_len)
                equipped = w if idx == 0 else a
                #prints current line
                print(f" {str1} \t {str2} \t\t {equipped}")
            #if there's 2 or more items left, increment index by 2, else 1
            idx += 2 if len(self._inventory) - idx >= 2 else 1

    ##MISC.
    def update(self) -> None:
        self.reset_ap()
        self.status_effects.update()

    def save(self) -> dict:
        self.status_effects.cleanse_all()

        player_tod = {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "xp":self.xp,
            "gold":self.gold
        }

        for entry in self.statblock.dict:
            player_tod[entry] = self.statblock.dict[entry]

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

                self.statblock.load(stats_file)
            file.close()
                
        self.load_inventory(inventory_file)
    
    def load_inventory(self, filename) -> None:
        import items
        #check if inventory file is emtpty
        empty_check = True if os.stat(filename).st_size == 0 else False
        if empty_check: return None
        size = 0
        self._inventory = {}
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                size += 1
            file.close()
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                item = items.load_item(row["type"], row)
                if idx >= size -2:
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
