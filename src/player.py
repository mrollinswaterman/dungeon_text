import random, time, os, csv
import global_commands
from items import Item, Consumable, Weapon, Armor
from status_effect import Status_Effect
from conditions import Stat_Buff_Debuff as sbd

class Player():

    def __init__(self, id:str="Player", name:str="New Player"):
        import status_effect

        self._id = id
        self._name = name
        self._level = 1

        self._stats = {
            "str": 12,
            "dex": 12,
            "con": 12,
            "int": 12,
            "wis": 12,
            "cha": 12,
            "base_evasion": 9,
            "damage_taken_multiplier": 1,
            "damage_multiplier": 1,
            "max_hp": 0,
            "max_ap": 1 + (self._level // 5)
        }

        self._stats["max_hp"] = 10 + self.bonus("con")
        self._hp = self.max_hp
        self._ap = self.max_ap
        
        #xp/gold/items
        self._xp = 0
        self._gold = 0
        self._inventory:dict[str, Item] = {}
        self._status_effects:dict[str: status_effect.Status_Effect] = {}

        #equipment
        w:Weapon = None
        a:Armor = None
        self._equipped:dict[str, Weapon, Armor] = {
            "Weapon": w, 
            "Armor": a
        }

        #statuses
        self._riposting = False

    #properties
    @property
    def dead(self) -> bool:
        return self._hp <= 0
    @property
    def stats(self) -> int:
        return self._stats
    @property
    def level(self) -> int:
        return self._level
    @property
    def caster_level(self) -> int:
        return 1 + (self.level // 5)
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def max_hp(self):
        return self._stats["max_hp"]
    @property
    def max_ap(self):
        return self._stats["max_ap"]
    @property
    def xp(self):
        return self._xp
    @property
    def armor(self) -> Armor:
        return self._equipped["Armor"]
    @property
    def weapon(self) -> Weapon:
        return self._equipped["Weapon"]
    @property
    def evasion(self):
        return self._stats["base_evasion"] + self.bonus("dex")
    @property
    def carrying_capacity(self) -> int:
        return int(5.5 * self._stats["str"])
    @property
    def available_carrying_capacity(self) -> int:
        return self.carrying_capacity - self.carrying
    @property
    def needs_healing(self):
        return self._hp < self.max_hp
    @property
    def riposting(self) -> bool:
        return self._riposting
    @property
    def damage_type(self) -> str:
        return "Physical"
    @property
    def carrying(self) -> int:
        total_weight = 0
        for entry in self._inventory:
            if self._inventory[entry] is not None:#check to make sure the entry is valid
                held_item:Item = self._inventory[entry]
                total_weight += held_item.weight
        for item in self._equipped:
            if self._equipped[item] is not None: #check to make sure an item is equipped, add its weight to the total if it is
                held_item:Item = self._equipped[item]
                total_weight += held_item.weight
        return total_weight
    @property
    def gold(self):
        return self._gold
    @property
    def inventory(self) -> dict:
        return self._inventory
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def damage_taken_multiplier(self):
        return self._stats["damage_taken_multiplier"]
    @property
    def damage_multiplier(self):
        return self._stats["damage_multiplier"]
    @property
    def max_hp(self):
        return self._stats["max_hp"]
    @property
    def threat(self):
        """
        Returns the player's current threat level which effect mob spawns
        """
        if int(self._level * 1.5) == 1:
            return 2
        return int(self._level * 1.5)
    @property
    def can_level_up(self):
        """
        Checks if the player has enough XP to level up
        """
        return self.xp >= (15 * self._level)
    @property
    def status_effects(self):
        return self._status_effects
    @property
    def equipped(self):
        return self._equipped
    @property
    def ap(self) -> None:
        return self._ap
    @property
    def can_act(self) -> bool:
        """
        Checks if the player can act (ie AP > 0)
        """
        return self._ap > 0 and not self.dead

    #STATUS
    def bonus(self, stat:str) -> int:
        if stat == "dex":
            armor:Armor = self.equipped["Armor"] if self.equipped["Armor"] is not None else None
            if armor is not None and armor.max_dex_bonus is not None:
                return min(global_commands.bonus(self._stats[stat]), armor.max_dex_bonus)
        return global_commands.bonus(self._stats[stat])
    
    def die(self) -> None:
        """
        Kils the player. Lose gold and inventory on death
        """
        self._gold = 0
        self._inventory = []
        #other stuff to be added

    def set_level(self, num:int) -> None:
        self._level = num

    #ACTIONS
    def attack(self) -> None:
        import player_commands, controller
        enemy = controller.SCENE.enemy

        roll = 10000 if player_commands.GOD_MODE else self.roll_to_hit()
        self.spend_ap()
        processed = self.process_roll(roll)
        self.roll_narration(processed)

        match roll:
            case 0:
                return self.crit()
            case 1:
                return self.crit_fail()
            case _:
                pass

        if roll >= controller.SCENE.enemy.evasion:
            self.hit_narration()
            dmg = 10000 if player_commands.GOD_MODE else self.roll_damage()
            taken = enemy.take_damage(dmg, self)
            return None

        self.miss_narration()
        return None

    def process_roll(self, roll) -> None | str:
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

    def crit(self) -> None:
        import controller
        enemy = controller.SCENE.enemy

        #global_commands.type_text("A critical hit!")
        no_weapon = True if self.weapon.broken else False

        if no_weapon:
            self._stats["damage_multiplier"] += 1
        else:
            self._stats["damage_multiplier"] += (self.weapon.crit-1)

        taken = enemy.take_damage(self.roll_damage(), self)

        if no_weapon:
            self._stats["damage_multiplier"] -= 1
        else:
            self._stats["damage_multiplier"] -= (self.weapon.crit-1)
        return None
    
    def crit_fail(self) -> None:
        global_commands.type_text("You critically failed!")
        return None
    
    def use(self, item:Item):
        """
        If the item is consumable, use it. If equippable, equip it.
        Anything else, return False
        """
        if item is None: return False

        if item.is_consumable:
            import player_commands
            player_commands.use_an_item(item, self)
            self.reset_ap()
        elif item.type != "Item":
            self.equip(item)
        else:
            return False
        
        return True
    
    #NARRATION --> prints statements based on given situation
    def roll_narration(self, roll_text):
        import controller as c
        enemy = c.SCENE.enemy
        text = [
            f"You heft your {self.weapon.id} and attack the {enemy.id}, ",
            f"You charge the {enemy.id}, ",
            f"You swing your {self.weapon.id}, ",
            f"Brandishing your {self.weapon.id}, you prepare to strike... ",
        ]
        global_commands.type_text(random.choice(text) + f"{roll_text}")
        return None

    def hit_narration(self) -> None:
        import controller as c
        enemy = c.SCENE.enemy
        text = [
            f"A hit.",
            f"The {enemy.id} didn't get out of the way in time.",
            f"You hit the {enemy.id}.",
            f"Your attack lands.",
            f"Your {self.weapon.id} strikes true.",
            f"The {enemy.id} wasn't able to dodge this one.",
            f"Sucess."
        ]
        global_commands.type_text(random.choice(text))
        return None

    def miss_narration(self) -> None:
        import controller as c
        enemy = c.SCENE.enemy
        text = [
            f"You missed.",
            f"No luck this time.",
            f"The {enemy.id} deftly dodges your attack.",
            f"Your attack whizzes past the {enemy.id}, missing by a hair.",
            f"You don't crack the {enemy.id}'s defenses this time.",
            f"It leaps out of the way in the nick of time.",
            f"A miss.",
            f"The {enemy.id} ducks your strike.",
            f"The {enemy.id} manages to weather your onslaught for now."
        ]
        global_commands.type_text(random.choice(text))
        return None

    #COMBAT TRICKS
    def power_attack(self) -> int:
        import controller
        enemy = controller.SCENE.enemy

        global_commands.type_text(f"You wind up for a powerful attack...")
        roll = self.roll_to_hit()
        self.spend_ap()

        self._stats["damage_multiplier"] += self.weapon.crit if roll == 0 else 0

        if roll != 0:
            roll -= self.bonus("dex")

        hit_text = f"A critical hit!" if roll == 0 else f"You hit the {enemy.id}."
        if roll >= enemy.evasion or roll == 0:
            global_commands.type_text(hit_text)
            dmg = max(self.roll_damage(), self.roll_damage())
            dmg += (self.bonus("str") // 2) * self.damage_multiplier
            taken = enemy.take_damage(dmg, self)
            self._stats["damage_multiplier"] -= 1 if roll == 0 else 0
            return None
        else:
            global_commands.type_text("No luck.")
    
    def feint(self) -> None:
        import controller
        from conditions import Stat_Buff_Debuff
        enemy = controller.SCENE.enemy

        global_commands.type_text("You attempt a feint...")
        roll = self.roll_a_check("cha")
        self.spend_ap()

        if roll >= enemy.roll_a_check("cha"):
            global_commands.type_text(f"You faked out the {enemy.id}!")
            def_bonus = Stat_Buff_Debuff.Stat_Buff(self, self)
            def_bonus.set_stat("base_evasion")
            def_bonus.set_duration(2)
            def_bonus.set_potency(max(2, self.bonus("cha")))
            self.add_status_effect(def_bonus)
        else:
            global_commands.type_text(f"The {enemy.id} spots your trick.")

        return None
    
    def riposte(self) -> None:
        from conditions import Stat_Buff_Debuff

        global_commands.type_text("You ready yourself to repel any oncoming attacks...")

        self.spend_ap(2)

        if not self._riposting:
            print("no riposte, adding...")
            rip_bonus = Stat_Buff_Debuff.Stat_Buff(self, self)
            rip_bonus.set_id("Riposte")
            rip_bonus.set_stat("base_evasion")
            rip_bonus.set_duration(1000000)
            rip_bonus.set_potency(2)
            #rip_bonus.set_cleanse_message("")
            self.add_status_effect(rip_bonus)

            self._riposting = True

    def end_riposte(self) -> None:
        self._riposting = False

        if self.get_se_by_id("Riposte") is not None:
            self.remove_status_effect(self.get_se_by_id("Riposte"))

        return None

    #ROLLS
    def roll_to_hit(self) -> int:
        """
        Returns an attack roll (d20 + dex bonus + BAB + weapon attack bonus)
        """
        weapon:Weapon = self._equipped["Weapon"]
        if weapon.broken is True:
            raise ValueError("Weapon is broken")
        roll = global_commands.d(20)
        match roll:
            case 1:
                return 1
            case _:
                #checks if the roll is a crit or not. Crits result in a return of 0
                #attack roll formula: roll + dex bonus + BaB + weapon att bonus
                return 0 if roll >= self.weapon.crit_range else roll + self.bonus("dex") + self.level // 5 + weapon.attack_bonus
            
    def roll_damage(self) -> int:
        """
        Returns a damage roll (weapon dice + str bonus)
        """
        weapon:Weapon = self._equipped["Weapon"]
        if weapon.broken:
            global_commands.type_text(f"You can't use a broken {weapon.id}, so your hands will have to do.")
            return (global_commands.d(4) + self.bonus("str")) * self.damage_multiplier
        
        weapon.lose_durability()
        return (weapon.roll_damage() + self.bonus("str")) * self.damage_multiplier

    def roll_a_check(self, stat: str) -> int:
        """
        Returns a check with a given stat (d20 + stat bonus)
        """
        roll = global_commands.d(20)
        match roll:
            case 1:
                return 1
            case 20:
                return 0
            case _:
                return roll + self.bonus(stat)
    
    def take_damage(self, taken: int, src, armor_piercing=False) -> int:
        """
        Reduces the players hp by a damage amount, reduced by armor
        """
        import magic
        import mob
        import player_commands

        #make sure incoming damage is in integer form
        taken *= self.damage_taken_multiplier
        taken = int(taken)

        #
        src:magic.Spell | mob.Mob | Status_Effect | Item = src

        #Ignores armor (Magic damage or Armor Piercing)
        if armor_piercing is True:
            self._hp -= taken
            strings = [
            f"You took {taken} damage from the {src.damage_header}.",
            f"The {src.damage_header} dealt {taken} damage to you."]
            global_commands.type_text(random.choice(strings))
            if self.dead:
                player_commands.end_game()
                return None
            return taken

        #Physical damage (everything else)
        armor:Armor = self._equipped["Armor"]
        if src.damage_type == "Physical" or src.damage_type is None:
            if armor.broken is False:
                armor.lose_durability()
                if (taken - self.armor.armor_value) <= 0:
                    strings = [
                        f"You took no damage from the {src.damage_header}!",
                        f"The {src.damage_header} did no damage to you!"]
                    global_commands.type_text(random.choice(strings))
                    return 0 
                else:
                    self._hp -= taken - self.armor.armor_value
                    strings = [
                        f"You took {taken - self.armor.armor_value} damage from the {src.damage_header}.",
                        f"The {src.damage_header} dealt {taken - self.armor.armor_value} damage to you."]
                    global_commands.type_text(random.choice(strings))
                    if self.dead:
                        player_commands.end_game()
                        return None
                    return taken - self.armor.armor_value
            else:
                global_commands.type_text(f"Broken {armor.id} does you no good...")

        #No armor (broken/not equipped)
        self._hp -= taken
        strings = [
            f"You took {taken} damage from the {src.damage_header}.",
            f"The {src.damage_header} dealt {taken} damage to you."]
        global_commands.type_text(random.choice(strings))
        if self.dead:
            player_commands.end_game()
            return None
        return taken

    def lose_hp(self, num:int) -> None:
        import player_commands

        num = int(num)

        self._hp -= num
        if self.dead:
            player_commands.end_game()
        return None

    #RESOURCES
    def level_up(self, stat: str) -> None:
        """
        Levels up a given stat
        """
        self._stats[stat] += 1
        self._xp -= 15 * self._level
        self._level += 1
        prev_max = self.max_hp
        self._stats["max_hp"] += (global_commands.d(10) + self.bonus("con"))
        if self._hp == prev_max:# ie, you were full HP before level up
            self._hp = self.max_hp
        if self._hp < (prev_max * .5): #if you were under 1/2 HP, heal to 1/2 HP
            self._hp = (self.max_hp * 0.5)

    def gain_xp(self, xp:int) -> None:
        """
        Increases player XP by a given amount
        """
        if xp <= 0:
            return None
        global_commands.type_text(f"{xp} XP earned.")
        self._xp += xp
    
    def gain_gold(self, gold:int, silently:bool=False) -> None:
        """
        Increases player gold by a given amount
        """
        if gold <= 0:
            return None
        if silently is False:
            global_commands.type_text(f"{gold} Gold gained.")
        self._gold += gold

    def spend_gold(self, gold:int) -> bool:
        """
        Reduces player gold by a given amount
        Throws a value error if the player doesnt have enough gold to spend
        """
        if gold > self.gold:   
            return False
        self._gold -= gold
        global_commands.type_text(f"{gold} gold spent. {self._gold} gold remaining.")
        return True

    def lose_gold(self, amount:int) -> None:
        """
        Takes a certain amount of gold from the player, if the player doesnt
        have sufficient gold, sets gold to 0
        """
        if self._gold - amount >= 0:
            self._gold -= amount
            return amount
        else:
            all_i_have = self._gold
            self._gold = 0
            return all_i_have

    def spend_ap(self, num=1) -> None:
        """
        Spends Action points equal to num
        """
        self.end_riposte()
        if num == 0:
            self._ap = 0
        elif self.can_act:
            self._ap -= num
        else:
            raise ValueError(f"You don't have {num} AP to spend.")
        return None

    def reset_ap(self) -> None:
        self._ap = self._stats["max_ap"]

    def change_name(self, name:str) -> None:
        self._name = name

    def heal(self, healing: int) -> None:
        """
        Heals the player for a given amount
        """
        if self._hp <= (self.max_hp - healing):
            self._hp += healing
            global_commands.type_text(f"You healed {healing} HP.")
            return None
        if self._hp + healing > self.max_hp:
            self._hp = self.max_hp
            if self.max_hp == self._hp:#if you were already full HP, say nothing
                return None
            global_commands.type_text(f"You only healed {self.max_hp - self._hp} HP.")
            return None

    #INVENTORY STUFF
    def pick_up(self, item: Item | Consumable, silently:bool = False) -> bool:
        """
        Picks up an item if the player has inventory space for it
        """
        if item is None:
            return False

        if self.can_carry(item):
            if self.has_item(item)and item.is_consumable:
                held_item:Consumable = self.get_item_by_id(item.id)
                held_item.increase_quantity(item.quantity)
                if not silently:
                    global_commands.type_text(item.pickup_message)
                return True
            self._inventory[item.id] = item
            item.set_owner(self)
            if not silently:
                global_commands.type_text(item.pickup_message)
            return True
        else:
            if not silently:
                global_commands.type_text("Not enough inventory space.")
        
    def drop(self, item: Item) -> None:
        """
        Drops an item out of the player's inventory
        """
        if item.id in self._inventory:
            del self._inventory[item.id]
            item.set_owner(None)
        else:
            raise ValueError("Can't drop an item you don't have.")

    def equip(self, item: Item, silently=False) -> bool:
        """
        Equips the player with a given weapon
        """
        if item.type in self._equipped:
            prev:Item = self._equipped[item.type]
            if prev is not None and prev.id != item.id:#if its not none and not the same item, swap it to inventory
                self._inventory[prev.id] = prev
            if item.id in self._inventory and item == self._inventory[item.id]:
                del self._inventory[item.id]
            if silently is False:
                global_commands.type_text(f"{item.name} equipped.")
            self._equipped[item.type] = item
            return True
        return False

    def can_carry(self, item:Item) -> bool:
        """
        Checks if the player can carry item 

        Returns True if they can, False if not
        """
        return self.carrying + item.weight <= self.carrying_capacity

    def has_item(self, item: Item) -> bool:
        """
        Checks if a player has an item in their inventory

        Return the item if its there and False if not
        """
        if item is None:
            return False

        if item.id in self._inventory:
            if item.is_consumable:
                return True    
            try:
                return item == self._inventory[item.id]
            except KeyError:
                return False

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
        """
        Prints the players inventory, line-by-line
        """
        import items
        last = False
        idx = 0
        mx = max(3, len(self._inventory))
        while(idx < mx):
            if idx % 2 == 0 and idx != 0:
                time.sleep(0.05)
                print("\n")

            weapon = list(self._equipped["Weapon"].format().values()) if idx == 0 else []
            w_header = f"1. {weapon[0]}" if idx == 0 else " "

            armor = list(self._equipped["Armor"].format().values()) if idx == 2 else []
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

    def recieve_reward(self, reward:dict) -> None:
        for entry in reward:
            match entry:
                case "gold":
                    self.gain_gold(reward[entry])
                case "xp":
                    self.gain_xp(reward[entry])
                case "drops":
                    for item in reward[entry]:
                        self.pick_up(item)        
        return None

    #STATUS EFFECTS / MODIFY STAT FUNCTIONS
    def modify_stat(self, stat, num):
        self._stats[stat] += num

    def add_status_effect(self, effect: Status_Effect, silent=False) -> None:
        """
        Adds a status effect to the player's status effect list and applies it
        """
        if effect.id in self._status_effects:#if effect already in status_effects
            applied:Status_Effect = self._status_effects[effect.id]
            applied.additional_effect(effect)#...apply the effect's additional_effect function
        else:
            self._status_effects[effect.id] = effect
            effect.apply()
        return None

    def remove_status_effect(self, effect:"Status_Effect") -> bool:
        if effect.id in self._status_effects:
            del self._status_effects[effect.id]
            effect.cleanse()
            return True
        else:
            return False

    def update(self) -> None:
        removed = []
        self.reset_ap()
        for entry in self._status_effects:
            effect:Status_Effect = self._status_effects[entry]
            effect.update()
            if effect.active is False:
                removed.append(effect)

        if not self._riposting:
            self.end_riposte()

        for effect in removed:
            self.remove_status_effect(effect)

    def cleanse_all(self):
        inactive = []
        for entry in self._status_effects:
            inactive.append(self._status_effects[entry])
        
        for effect in inactive:
            self.remove_status_effect(effect)

    #GETTERS
    def get_item_by_id(self, id:str) -> Item:
        """
        Get an item in the player's inventory by it's id
        Returns the item, None if not found
        """
        try:
            return self._inventory[id]
        except KeyError:
            return None
    
    def get_item_by_index(self, idx:int) -> Item:
        """
        Gets an item by index. Returns None if no item at that index
        """
        try:
            return list(self._inventory.values())[idx]
        except IndexError:
            return None
    
    def get_se_by_index(self, idx:int) -> Status_Effect | None:
        """
        Same as items but for status effects (se)
        """
        try:
            return list(self._status_effects.values())[idx]
        except IndexError:
            return None

    def get_se_by_id(self, id:str) -> Status_Effect | None:
        """
        Same as items but for status effects (se)
        """
        try: 
            return self._status_effects[id]
        except KeyError:
            return None

    ##MISC.
    def save_to_dict(self) -> dict:
        for entry in self._status_effects:
            effect:Status_Effect = self._status_effects[entry]
            if effect.src == self:
                self.remove_status_effect(effect)
        player_tod = {
            "name": self._name,
            "level": self._level
        }
        for stat in self._stats:
            player_tod[stat] = self._stats[stat]
        player_tod["hp"] = self._hp
        player_tod["xp"] = self._xp
        player_tod["gold"] = self._gold 

        return player_tod
    
    def load(self, stats_file, inventory_file) -> None:
        #first check if save file is empty
        empty_check = True if os.stat(stats_file).st_size == 0 else False
        if empty_check: return None
        #if it's not, set values to save file values
        with open(stats_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self._name = row["name"]
                self._level = int(row["level"])
                for i in range(2, 13):#magic number, the range of 
                #loaded values that corresponds to the player's stats dictionary
                    key = list(row.keys())[i]
                    self._stats[key] = int(row[key])
                self._hp = int(row["hp"])
                self._xp = int(row["xp"])
                self._gold = int(row["gold"])
                self.reset_ap()
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
