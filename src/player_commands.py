import random, time, csv
import sys
import global_commands
import global_variables
import mob
import items
import narrator
import status_effects

GOD_MODE = False
TEST = None
PLAYER = global_variables.PLAYER

ENEMY:mob.Mob = None
ENEMY_TURN = None

END_SCENE = None
NEXT_SCENE = None

def start_turn():
    """
    Runs the player's turn
    """
    PLAYER.update()

    while PLAYER.can_act:
        turn_options()

        command = input(">> ").lower()
        print("")

        if command == "exit":
            global_variables.RUNNING = False
            global_commands.exit()
        if command == "reset":
            reset()
            sys.exit()
        try:
            command = int(command)
            try:
                item = list(PLAYER.inventory.values())[command - 1]
            except IndexError:
                item = None
            use_an_item(item, ENEMY)
        except ValueError:
            pass
        match command:
            case "a": #attack
                attack()
            case "c": #combat tricks
                combat_tricks()
            case "i": #show inventory
                show_inventory()
            case "test": #test suite
                print(PLAYER.evasion)
            case "p": #pass the turn
                PLAYER.spend_ap(0)
            case "s": #cleanse an effect
                cleanse_an_effect()
            case "f": #attempt to flee
                global_variables.RUNNING = False
                flee()

        if ENEMY.dead:
            PLAYER.reset_ap()
            global_variables.RUNNING = False
            END_SCENE()
            return None
        
        if PLAYER.can_act:
            global_commands.type_with_lines("")
    
    if global_variables.RUNNING:
        global_commands.type_with_lines("")#shorthand, just prints the #s
        ENEMY_TURN()
        return None
    
    return None

def turn_options():
    """
    Prints the player's stat info and turn options
    """
    header = f"What would you like to do? \t"
    hp = f"HP: {"[" + "/"*PLAYER.hp+" "*(PLAYER.max_hp-PLAYER.hp) + "]"} \t"
    ap = f"AP: {PLAYER.ap}/{PLAYER.max_ap} \t"
    gold = f"Gold: {PLAYER.gold}g \t"
    xp = f"XP: {PLAYER.xp}/{15 * PLAYER.level} \t"
    global_commands.type_text(header, 0.03, False)
    print(hp + ap + gold + xp + "\n")
    options = "\t Attack - (a) | Combat Tricks - (c) | Attempt to Cleanse a Status Effect - (s) | Inventory - (i) | Pass Turn - (p) | Flee - (f)"
    print(options)

def cleanse_an_effect():
    """
    Attempts to cleanse a chosen status effect
    """
    global_commands.type_text("Select an effect to cleanse OR Cancel - (c)")
    for idx, entry in enumerate(PLAYER.status_effects):
        effect: status_effects.Status_Effect = PLAYER.status_effects[entry.id]
        string = f"{idx+1}. {effect.id}"
        if idx % 2 == 0 and idx != 0:
            time.sleep(0.05)
            print("\n")
        
        print(string + 2*"\t", end='')

    if len(PLAYER.status_effects) > 0:
        print("\n")

    while True:
        cmd = input(">> ").lower()
        print("")
        match cmd:
            case "exit":
                global_commands.exit()
            case "c":
                return None
            case _:
                try:
                    num = int(cmd)
                    try: 
                        effect: status_effects.Status_Effect = list(PLAYER.status_effects.values())[num-1]
                        PLAYER.spend_ap()
                        effect.attempt_cleanse(PLAYER.roll_a_check(effect.cleanse_stat))
                        return None
                    except KeyError:
                        global_commands.type_text(f"Invalid effect number '{cmd}'. Please try again.")
                except ValueError:
                    global_commands.type_text(f"Invalid effect number '{cmd}'. Please try again.")

def combat_tricks():
    pass

def attack() -> None:
    """
    Runs the player attack action
    """
    if GOD_MODE is True:
        attack = 1000000
    else:
        attack = PLAYER.roll_attack() if TEST is False else 1
        PLAYER.spend_ap()

    if attack == 0:#CRITICAL HIT DETECTION
        global_commands.type_text(f"You attack the {ENEMY.id}, rolling a natural 20!")
    else:
        global_commands.type_text(f"You attack the {ENEMY.id}, rolling a {attack}.")

    if attack == 0:#CRITICAL HIT DETECTION
        global_commands.type_text("Critical Hit!")
        PLAYER.stats["damage_multiplier"] += (PLAYER.weapon.crit - 1)#math thing
        taken = ENEMY.take_damage(PLAYER.roll_damage(), PLAYER)
        PLAYER.stats["damage_multiplier"] -= (PLAYER.weapon.crit - 1)#math thing
        return None
    elif attack == 1:
        global_commands.type_text("Crtical Fail!")
    elif attack >= ENEMY.evasion:
        if GOD_MODE is True:
            taken = ENEMY.take_damage(1000, PLAYER, True)
        else:
            taken = ENEMY.take_damage(PLAYER.roll_damage(), PLAYER)
        return None
    global_commands.type_text("You missed.")
    return None

def show_inventory() -> None:
    """
    Prints the player's inventory
    """
    global_commands.type_with_lines("")
    PLAYER.print_inventory()
    select_an_item()

def select_an_item() -> None:
    """
    Lets the player select an inventory item to use
    """
    global_commands.type_text("Enter an Item's number to use it | Go Back - (b)")
    
    while True:
        cmd = input(">> ").lower()
        print("")
        match cmd:
            case "exit":
                global_commands.exit()
            case "b":
                return None
            case _:
                try:
                    cmd = int(cmd)
                    try:
                        item = list(PLAYER.inventory.values())[cmd - 1]
                        return use_an_item(item, ENEMY)
                    except IndexError:
                        global_commands.type_text("Please enter a valid item number.")
                except ValueError:
                    global_commands.type_text("Please enter a valid command.")


def use_an_item(item: items.Consumable, target=None) -> None:
    """
    Uses an item if the player has the item in their inventory
    """
    if item is None:
        global_commands.type_text("Invalid item selected. Please try again.")
        return None

    if PLAYER.has_item(item) is True:#check the player has the item
        if item.is_consumable is True:
            item = PLAYER.inventory[item.id]
            held_item:items.Consumable = item
            if held_item.quantity == 0: #if the items quantity is 0, remove it
                PLAYER.drop(held_item)
                global_commands.type_text(f"No {item.name} avaliable!")
                select_an_item()
                return None
            if held_item.use(target):
                PLAYER.spend_ap()
            return None
        else:
            global_commands.type_text(f"{item.name} is not a consumable.")
            select_an_item()
            return None
    else:
        global_commands.type_text(f"No {item.name} avaliable!")
        select_an_item()
        return None

def stop_flee_attempt() -> None:
    """
    Checks to see if an enemy is able to successfuly interrupt
    a player's attempt to flee
    """
    global_commands.type_text(f"The {ENEMY.id} attempts to stop you!")
    if ENEMY.attack_of_oppurtunity() is True:
        global_commands.type_text("It caught up with you! You escape but not unscathed.")
        #player.lose_some_items
    else:
        global_commands.type_text("It failed. You've escaped.")
    
    narrator.continue_run(NEXT_SCENE)
    return None

def flee() -> None:
    """
    Attempts to run away from the current encounter
    """
    global_commands.type_text("You attempt to flee...")
    
    if global_commands.probability(90 - int((PLAYER.hp / PLAYER.max_hp) * 100)):
        #higher HP == lower chase chance
        stop_flee_attempt()
        return None
    else:
        global_commands.type_text(f"The {ENEMY.id} lets you go.")
        PLAYER.spend_ap(0)
        narrator.continue_run(NEXT_SCENE)
        return None

def end_game():
    """
    End game message
    """
    #smth else
    global_commands.type_with_lines("You have died.", 2)
    global_variables.RUNNING = False
    reset()
    global_commands.exit()

def load():
    """
    Loads the player.csv save file
    """
    PLAYER.load("player.csv", "inventory.csv")

def reset():
    """
    Wipes the player.csv and inventory.csv files
    """
    with open('player.csv', "r+") as file:
        file.truncate(0)
        file.close()

    with open('inventory.csv', "r+") as file:
        file.truncate(0)
        file.close()