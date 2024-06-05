import time, sys
import global_commands
import items

GOD_MODE = False

def start_turn():
    """
    Runs the player's turn
    """
    import global_variables
    import enemy_commands
    import controller

    global_variables.PLAYER.update()

    if global_variables.PLAYER.dead:
        end_game()
        return None

    while global_variables.PLAYER.can_act:
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
                item = list(global_variables.PLAYER.inventory.values())[command - 1]
            except IndexError:
                item = None
            use_an_item(item, controller.SCENE.enemy)
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
                print(global_variables.PLAYER.evasion)
            case "p": #pass the turn
                global_variables.PLAYER.spend_ap(0)
            case "s": #cleanse an effect
                cleanse_an_effect()
            case "f": #attempt to flee
                global_variables.RUNNING = False
                flee()

        if controller.SCENE.enemy.dead:
            global_variables.PLAYER.reset_ap()
            global_variables.RUNNING = False
            controller.end_scene()
            return None
        
        if global_variables.PLAYER.can_act:
            global_commands.type_with_lines("")
    
    if global_variables.RUNNING:
        global_commands.type_with_lines("")#shorthand, just prints the #s
        enemy_commands.start_turn()
        return None
    
    return None

def turn_options():
    """
    Prints the player's stat info and turn options
    """
    import global_variables

    header = f"What would you like to do? \t"
    hp = f"HP: {"[" + "/"*global_variables.PLAYER.hp+" "*(global_variables.PLAYER.max_hp-global_variables.PLAYER.hp) + "]"} \t"
    ap = f"AP: {global_variables.PLAYER.ap}/{global_variables.PLAYER.max_ap} \t"
    gold = f"Gold: {global_variables.PLAYER.gold}g \t"
    xp = f"XP: {global_variables.PLAYER.xp}/{15 * global_variables.PLAYER.level} \t"
    global_commands.type_text(header, 0.03, False)
    print(hp + ap + gold + xp + "\n")
    options = "\t Attack - (a) | Combat Tricks - (c) | Attempt to Cleanse a Status Effect - (s) | Inventory - (i) | Pass Turn - (p) | Flee - (f)"
    print(options)

def cleanse_an_effect():
    """
    Attempts to cleanse a chosen status effect
    """
    import global_variables
    import status_effect
    global_commands.type_text("Select an effect to cleanse OR Cancel - (c)")
    for idx, entry in enumerate(global_variables.PLAYER.status_effects):
        effect: status_effect.Status_Effect = global_variables.PLAYER.status_effects[entry]
        string = f"{idx+1}. {effect.id}"
        if idx % 2 == 0 and idx != 0:
            time.sleep(0.05)
            print("\n")
        
        print(string + 2*"\t", end='')

    if len(global_variables.PLAYER.status_effects) > 0:
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
                        effect:status_effect.Status_Effect = list(global_variables.PLAYER.status_effects.values())[num-1]
                        global_variables.PLAYER.spend_ap()
                        effect.attempt_cleanse(global_variables.PLAYER.roll_a_check(effect.cleanse_stat))
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
    import global_variables
    
    global_variables.PLAYER.attack()
    return None

def show_inventory() -> None:
    import global_variables
    global_variables.PLAYER.print_inventory()
    select_an_item()

def select_an_item() -> None:
    """
    Lets the player select an inventory item to use
    """
    import global_variables
    import controller

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
                        item = global_variables.PLAYER.get_item_by_index(cmd-1)
                        return use_an_item(item, controller.SCENE.enemy)
                    except IndexError:
                        global_commands.type_text("Please enter a valid item number.")
                except ValueError:
                    global_commands.type_text("Please enter a valid command.")


def use_an_item(item:items.Item, target=None) -> None:
    """
    Uses an item if the player has the item in their inventory
    """
    import global_variables
    if item is None:
        global_commands.type_text("Invalid item selected. Please try again.")
        return None

    if global_variables.PLAYER.has_item(item) is True:#check the player has the item
        if item.is_consumable is True:
            item = global_variables.PLAYER.inventory[item.id]
            held_item:items.Consumable = item
            if held_item.quantity == 0: #if the items quantity is 0, remove it
                global_variables.PLAYER.drop(held_item)
                global_commands.type_text(f"No {item.name} avaliable!")
                select_an_item()
                return None
            if held_item.use(target):
                global_variables.PLAYER.spend_ap()
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
    import narrator
    import controller

    global_commands.type_text(f"The {controller.SCENE.enemy.id} attempts to stop you!")
    if controller.SCENE.enemy.attack_of_oppurtunity() is True:
        global_commands.type_text("It caught up with you! You escape but not unscathed.")
        #global_variables.PLAYER.lose_some_items
    else:
        global_commands.type_text("It failed. You've escaped.")
    
    narrator.continue_run()
    return None

def flee() -> None:
    """
    Attempts to run away from the current encounter
    """
    import global_variables
    import narrator
    import controller

    global_commands.type_text("You attempt to flee...")
    
    if global_commands.probability(90 - int((global_variables.PLAYER.hp / global_variables.PLAYER.max_hp) * 100)):
        #higher HP == lower chase chance
        stop_flee_attempt()
        return None
    else:
        global_commands.type_text(f"The {controller.SCENE.enemy.id} lets you go.")
        global_variables.PLAYER.spend_ap(0)
        narrator.continue_run()
        return None

def end_game():
    """
    End game message
    """
    import global_variables
    #smth else
    global_commands.type_with_lines("You have died.", 2)
    global_variables.RUNNING = False
    reset()
    sys.exit()

def load():
    """
    Loads the player.csv save file
    """
    import global_variables
    global_variables.PLAYER.load("player.csv", "inventory.csv")

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