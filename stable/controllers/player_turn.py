##Required Modules: globals, controllers, narrator, items

import time, sys
import game
import globals
import items
import narrator

GOD_MODE = True

def turn():
    """Runs the player's turn"""

    actions = game.COMMANDS["actions"]
    combat_tricks = game.COMMANDS["combat_tricks"]

    game.PLAYER.update()

    if game.PLAYER.dead:
        end_game()
        return None

    while game.PLAYER.can_act:
        turn_options()
        done = False
        while not done:
            code = globals.get_cmd()

            #check if code is an action
            if code in actions:
                actions[code]()
                done = True
            else:
                #check if code is item hotkey
                try: 
                    code = int(code)
                    item = game.PLAYER.get_item(code-1)
                    use_an_item(item)
                    done = True
                except ValueError:
                    #check if code is combat trick hotkey
                    if code in combat_tricks:
                        combat_tricks[code]()
                        done = True
            
            #if none of the above, throw an error
            response = globals.error_message(code) if not done else None
        
        if game.SCENE.enemy.dead:
            game.PLAYER.reset_ap()
            game.RUNNING = False
            game.SCENE.end()
            return None
        
        if game.PLAYER.can_act:
            globals.type_with_lines()
    
    if game.RUNNING:
        globals.type_with_lines()#shorthand, just prints the '=' signs
        game.SCENE.turn_order.go()
        return None

    return None

def cancel():
    return None

def turn_options():
    """Prints the player's stat info and turn options"""
    import game

    header = f"What would you like to do?"
    globals.type_header(header, None, False)
    stats = {
        "lvl": f"Lvl: {game.PLAYER.level}",
        "hp": f'HP: {"[" + "/"*game.PLAYER.hp+" "*(game.PLAYER.stats.max_hp-game.PLAYER.hp) + "]"}',
        "ap": f"AP: {game.PLAYER.ap}/{game.PLAYER.stats.max_ap}",
        "gold": f"Gold: {game.PLAYER.gold}g",
        "xp": f"XP: {game.PLAYER.xp}/{15 * game.PLAYER.level}",
        "evasion": f"AC: {game.PLAYER.evasion()}"
    }
    print("\t", end="")
    for stat in stats:
        print(f"{stats[stat]} \t", end="")
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
    ct = game.COMMANDS["combat_tricks"]

    globals.type_text("Select a trick to use -OR- Cancel - (c)")
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
        code = globals.get_cmd()
        if code in ct:
            done = True
            ct[code]()
        else:
            globals.error_message(code)
    
    return None

def cleanse_a_condition():
    """Attempts to cleanse a chosen condition"""
    effects = game.COMMANDS["cleanse_an_effect"]

    globals.type_text("Select an effect to cleanse -OR- Cancel - (c)")
    for idx, condition in enumerate(game.PLAYER.conditions.list):
        string = f"{idx+1}. {condition.id}"
        if idx % 2 == 0 and idx != 0:
            time.sleep(0.05)
            print("\n")
        
        print(string + 2*"\t", end='')

    if len(game.PLAYER.conditions.list) > 0:
        print("\n")

    done = False
    while not done:
        code = globals.get_cmd()
        if code in effects:
            done = True
            effects[code]()
        else:
            try:
                num = int(code)
                selected = game.PLAYER.conditions.get(num-1)
                if selected is not None:
                    game.PLAYER.spend_ap()
                    selected.cleanse_check()
                    done = True
                    return None
            except TypeError:
                raise Exception
            globals.error_message(code)

def show_inventory() -> None:
    import game
    game.PLAYER.print_inventory()
    item_select()

def item_select() -> None:
    """Lets the player select an inventory item to use"""
    item_selection = game.COMMANDS["item_select"]

    globals.type_text("Enter an Item's number to use it -OR- Cancel - (c)")

    done = False
    while not done:
        code = globals.get_cmd()
        if code in item_selection:
            done = True
            item_selection[code]()
        else:
            try:
                num = int(code)
                item = game.PLAYER.get_item(num-1)
                if item is not None:
                    done = True
                    return use_an_item(item)
                else:
                    globals.error_message(None, f"Invalid item number '{code}'. Please try again.")
            except ValueError:
                globals.error_message(code)

def use_an_item(item:"items.Item | items.Consumable") -> bool:
    """Uses an item if the player has the item in their inventory."""
    if item is None:
        globals.error_message(None, "Invalid item selected. Please try again.")
        return False

    return game.PLAYER.use(game.PLAYER.get_item(item.id))

def flee() -> None:
    """Attempts to run away from the current encounter"""
    if game.PLAYER.conditions.get("Enraged") is not None:
        globals.type_text("You cannot flee while Enraged.")
        return None
    
    game.RUNNING = False
    globals.type_text("You attempt to flee...")
    
    if globals.probability(90 - int((game.PLAYER.hp / game.PLAYER.stats.max_hp) * 100)):
        #higher HP == lower chase chance
        stop_flee_attempt()
        return None
    else:
        globals.type_text(f"The {game.SCENE.enemy.id} lets you go.")
        game.PLAYER.spend_ap(0)
        narrator.continue_run()
        return None

def stop_flee_attempt() -> None:
    """
    Checks to see if an enemy is able to successfuly interrupt
    a player's attempt to flee
    """
    import narrator

    globals.type_text(f"The {game.SCENE.enemy.id} attempts to stop you!")
    if game.SCENE.enemy.attack_of_oppurtunity() is True:
        globals.type_text("It caught up with you! You escape but not unscathed.")
        #game.PLAYER.lose_some_items
    else:
        globals.type_text("It failed. You've escaped.")
    
    narrator.continue_run()
    return None

#META globals
def end_game():
    """End game message"""
    #smth else
    globals.type_with_lines("You have died.", 2)
    game.RUNNING = False
    reset()
    sys.exit()

def load():
    """Loads the player.csv save file"""
    game.PLAYER.load("player.csv", "inventory.csv")

def reset():
    """Wipes the player.csv and inventory.csv files"""
    with open('player.csv', "r+") as file:
        file.truncate(0)
        file.close()

    with open('inventory.csv', "r+") as file:
        file.truncate(0)
        file.close()

    game.RUNNING = False
    sys.exit()
