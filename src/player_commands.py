import time, sys
import global_commands
from item import Item
from stackable import Consumable

GOD_MODE = False

def turn():
    """Runs the player's turn"""
    import global_variables
    import controller
    from command_dict import commands

    actions = commands["actions"]
    combat_tricks = commands["combat_tricks"]

    global_variables.PLAYER.update()

    if global_variables.PLAYER.dead:
        end_game()
        return None

    while global_variables.PLAYER.can_act:
        turn_options()
        done = False
        while not done:
            code = global_commands.get_cmd()

            #check if code is an action
            if code in actions:
                actions[code]()
                done = True
            else:
                #check if code is item hotkey
                try: 
                    code = int(code)
                    item = global_variables.PLAYER.get_item(code-1)
                    use_an_item(item)
                    done = True
                except ValueError:
                    #check if code is combat trick hotkey
                    if code in combat_tricks:
                        combat_tricks[code]()
                        done = True
            
            #if none of the above, throw an error
            response = global_commands.error_message(code) if not done else None
        
        if controller.SCENE.enemy.dead:
            global_variables.PLAYER.reset_ap()
            global_variables.RUNNING = False
            controller.SCENE.end()
            return None
        
        if global_variables.PLAYER.can_act:
            global_commands.type_with_lines()
    
    if global_variables.RUNNING:
        global_commands.type_with_lines()#shorthand, just prints the '=' signs
        controller.SCENE.turn_order.go()
        return None

    return None

def cancel():
    return None

def turn_options():
    """Prints the player's stat info and turn options"""
    import global_variables

    header = f"What would you like to do?"
    global_commands.type_text(header, None, False)
    b_e = global_variables.PLAYER.stats.base_evasion
    stats = {
        "hp": f'HP: {"[" + "/"*global_variables.PLAYER.hp+" "*(global_variables.PLAYER.stats.max_hp-global_variables.PLAYER.hp) + "]"}',
        "ap": f"AP: {global_variables.PLAYER.ap}/{global_variables.PLAYER.stats.max_ap}",
        "gold": f"Gold: {global_variables.PLAYER.gold}g",
        "xp": f"XP: {global_variables.PLAYER.xp}/{15 * global_variables.PLAYER.level}",
        "eva": f"Base Evasion: {b_e}"
    }
    print("\t", end="")
    for stat in stats:
        print(stats[stat] + " \t", end="")
    print("\n")

    options = [
        "Attack - (a)", "Combat Tricks - (ct)",
        "Status Effects - (e)", "Inventory - (i)",
        "Wait - (w)", "Retreat - (r)"
    ]
    print("\t", end="")
    for item in options:
        print(item + " | ", end="")
    print("\n")

def combat_tricks():
    from command_dict import commands
    ct = commands["combat_tricks"]

    global_commands.type_text("Select a trick to use -OR- Cancel - (c)")
    options = [
        "Power Attack - (p)",
        "Feint - (f)",
        "Riposte - (ri)",
        "Total Defense - (t)",
        "All-Out - (all)",
        "Study Weakness - (s)",
    ]
    print("\t", end='')
    for item in options:
        print(item + " | ", end='')
    print("\n")

    done = False
    while not done:
        code = global_commands.get_cmd()
        if code in ct:
            done = True
            ct[code]()
        else:
            global_commands.error_message(code)
    
    return None

def cleanse_a_condition():
    """Attempts to cleanse a chosen condition"""
    import global_variables
    from condition import Condition
    from command_dict import commands
    effects = commands["cleanse_an_effect"]

    global_commands.type_text("Select an effect to cleanse -OR- Cancel - (c)")
    for idx, condition in enumerate(global_variables.PLAYER.conditions.list):
        string = f"{idx+1}. {condition.id}"
        if idx % 2 == 0 and idx != 0:
            time.sleep(0.05)
            print("\n")
        
        print(string + 2*"\t", end='')

    if len(global_variables.PLAYER.conditions.list) > 0:
        print("\n")

    done = False
    while not done:
        code = global_commands.get_cmd()
        if code in effects:
            done = True
            effects[code]()
        else:
            try:
                num = int(code)
                selected = global_variables.PLAYER.conditions.get(num-1)
                if selected is not None:
                    global_variables.PLAYER.spend_ap()
                    selected.cleanse_check()
                    done = True
                    return None
            except TypeError:
                raise Exception
            global_commands.error_message(code)

def show_inventory() -> None:
    import global_variables
    global_variables.PLAYER.print_inventory()
    item_select()

def item_select() -> None:
    """Lets the player select an inventory item to use"""
    import global_variables
    import controller
    from command_dict import commands
    item_selection = commands["item_select"]

    global_commands.type_text("Enter an Item's number to use it -OR- Cancel - (c)")

    done = False
    while not done:
        code = global_commands.get_cmd()
        if code in item_selection:
            done = True
            item_selection[code]()
        else:
            try:
                num = int(code)
                item = global_variables.PLAYER.get_item(num-1)
                if item is not None:
                    done = True
                    return use_an_item(item)
                else:
                    global_commands.error_message(None, f"Invalid item number '{code}'. Please try again.")
            except ValueError:
                global_commands.error_message(code)

def use_an_item(item:Item | Consumable) -> bool:
    """Uses an item if the player has the item in their inventory."""
    import global_variables

    if item is None:
        global_commands.error_message(None, "Invalid item selected. Please try again.")
        return False

    item = global_variables.PLAYER.get_item(item.id)

    if global_variables.PLAYER.use(item):
        match item:
            case Consumable(): item.remove_quantity()
        return True
    else: 
        global_commands.error_message(None, f"You can't use that {item.id}. Please try again.")
        return False

def flee() -> None:
    """Attempts to run away from the current encounter"""
    import global_variables
    import narrator
    import controller

    if global_variables.PLAYER.conditions.get("Enraged") is not None:
        global_commands.type_text("You cannot flee while Enraged.")
        return None
    
    global_variables.RUNNING = False
    global_commands.type_text("You attempt to flee...")
    
    if global_commands.probability(90 - int((global_variables.PLAYER.hp / global_variables.PLAYER.stats.max_hp) * 100)):
        #higher HP == lower chase chance
        stop_flee_attempt()
        return None
    else:
        global_commands.type_text(f"The {controller.SCENE.enemy.id} lets you go.")
        global_variables.PLAYER.spend_ap(0)
        narrator.continue_run()
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

#META FUNCTIONS
def end_game():
    """End game message"""
    import global_variables
    #smth else
    global_commands.type_with_lines("You have died.", 2)
    global_variables.RUNNING = False
    reset()
    sys.exit()

def load():
    """Loads the player.csv save file"""
    import global_variables
    global_variables.PLAYER.load("player.csv", "inventory.csv")

def reset():
    """Wipes the player.csv and inventory.csv files"""
    import global_variables
    with open('player.csv', "r+") as file:
        file.truncate(0)
        file.close()

    with open('inventory.csv', "r+") as file:
        file.truncate(0)
        file.close()

    global_variables.RUNNING = False
    sys.exit()
