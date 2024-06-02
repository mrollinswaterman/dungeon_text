import time
import sys
import random
import global_commands
import global_variables
import player_commands

SCENE_CHANGE = [
    "You press towards your goal...\n",
    "Your resolve steeled, you continue forwards...\n",
    "Your weary legs carry you on...\n",
    "You venture deeper into the dungeon...\n"
]

EXIT_DUNGEON = [
    "You climb out of the darkness.",
    "You take your first breath of fresh in what feels like an eternity.",
    "Finally, out...",
    "The soft moonlight bathes the world in a gentle glow.",
    "The sky above you seems real enough to touch. You barely remember what it looked like...",
    "As you breathe a sigh of relief, you can't help but wonder if you'll make it out the next time...",
    "The openess of the Overworld is a stark contrast to the confines of the Dungeon.",
    "As you emerge from the Dungeon's darkness, the harsh light of day stings your eyes."
]

ENTER_THE_SHOP = [
    "The Shopkeep eyes you sleepily.",
    "The Shopkeep glances at you warmly.",
    "The Shopkeep glares at you.",
    "The Shopkeep shoots you a friendly look.",
    "The Shopkeep barely notices you.",
    "The Shopkeep seems to look right through you.",
    "The Shopkeep eyes you eagerly.",
    "The Shopkeep grunts at your approach.",
    "The Shopkeep eyes you wearily."
]

EXIT_THE_SHOP = [
    "You go on your way.",
    "Your business is concluded.",
    "You slink out of the Shop.",
    "As you leave, you wonder if you'll see this place again...",
]

def next_scene_options():
    global_commands.type_text("\n" + " " + random.choice(SCENE_CHANGE))
    ominous = f'    ...\n'
    for i in range(4):
        time.sleep(.4)
        print('\t'*i + ominous)
    print("\n")

def level_up_options():
    global_commands.type_with_lines(' You have gained enough XP to level up! Which stat would you like to level up?')
    print("\t Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n")

def event_options():
    global_commands.type_text("Which stat would you like to roll?")
    print("\t Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n")

def continue_run(next):
    global_commands.type_with_lines("Continue? y/n")
    command = input(">> ").lower()
    if command == "y":   
        next_scene_options()
        next()
    elif command == "n":
        exit_the_dungeon()
    elif command == "exit":
        global_commands.exit()
    else:
        global_commands.type_text("Invalid command. Please try again.")
        continue_run(next)

def exit_the_dungeon():
    global_variables.RUNNING = False
    global_commands.type_with_lines(random.choice(EXIT_DUNGEON))
    global_variables.restock_the_shop()
    menu_options()

def buy_something():
    global_commands.type_with_lines("Enter an item's number to purchase it OR (c) - Cancel Order")
    command = input(">> ").lower()

    if command == "exit":
        global_commands.exit()
    elif command == "c":
        shopkeep_options()
    else:
        try:
            stock_num = int(command)
            item = global_variables.SHOPKEEP.inventory[stock_num-1]
        except ValueError:
            print("Invalid option, please try again.\n")
            buy_something()
        if stock_num <= global_variables.SHOPKEEP.stock_size+1:
            print("")#formatting
            if item.is_consumable is False:
                if global_variables.SHOPKEEP.sell(item, global_variables.PLAYER) is False:
                    buy_something()
                else:
                    global_variables.SHOPKEEP.print_inventory()
                    buy_something()
            else:
                def ask_quantity():
                    global_commands.type_text(f"Please enter desired quantity:")
                    command = input(">> ").lower()
                    print("")#newline after... you get the idea
                    if command == "exit":
                        sys.exit()
                    try:
                        if global_variables.SHOPKEEP.sell(item, global_variables.PLAYER, int(command)) is False:
                            buy_something()
                        else:
                            global_variables.SHOPKEEP.print_inventory()
                            buy_something()
                    except TypeError:
                        print(f" Invalid quantity '{command}'. Please enter a valid quantity.")
                        ask_quantity()

                ask_quantity()
        else:
            print(f" Invalid item number '{int(command)}'. Please try again.")
            buy_something()

def leave_the_shop():
    global_commands.type_with_lines(random.choice(EXIT_THE_SHOP))
    menu_options()

def shopkeep_options():
    global_commands.type_with_lines(random.choice(ENTER_THE_SHOP))
    global_commands.type_with_lines("What would you like to do?\n")
    print("\t Buy Something - (b) | Leave - (l) | Sell something - (s) | Inventory - (i)\n")
    command = input(">> ").lower()
    if command == "b":
        global_variables.SHOPKEEP.print_inventory()
        buy_something()
    elif command == "l":
        leave_the_shop()
    elif command == "i":
        check_player_inventory(shopkeep_options)
    elif command == "exit":
        global_commands.exit()
    else: 
        print("Invalid command, please try again")
        shopkeep_options()

def rest():
    global_commands.type_with_lines("Plenty of time to rest when you're dead.")
    menu_options()

def check_player_inventory(next):
    global_commands.type_with_lines("Inventory:\n")
    print(f"Gold: {global_variables.PLAYER.gold}\n")
    global_variables.PLAYER.print_inventory()
    def select_item():
        global_commands.type_with_lines("Enter an item's number to equip it OR (b) - Go Back")
        command = input(">> ").lower()
        if command == "b":
            next()
        elif command == "exit":
            global_commands.exit()
        else:
            try:
                x = int(command)
            except ValueError:
                print("Invalid command, please try again.\n")
                select_item()
            index = int(command) - 1
            item_id = list(global_variables.PLAYER.inventory.keys())[index]
            item = global_variables.PLAYER.inventory[item_id]
            if global_variables.PLAYER.equip(item) is True:
                check_player_inventory(next)
            else:
                print("\nCan't equip that.")
                select_item()
    select_item()

def menu_options():
    global_commands.type_with_lines("What would you like to do?")
    print("\t Enter the Dungeon - (e) | Rest - (r) | Visit the Shop - (v) | Inventory - (i) \n")
    command = input(">> ").lower()
    match command:
            case "e": #enter the dungeon again
                global_variables.START_CMD = True
            case "r": #rest text
                rest()
            case "v": #visit the shop
                shopkeep_options()
            case "i": #check inventory
                check_player_inventory(menu_options)
            case "exit":
                global_commands.exit()
            case _:
                print(f"Invalid command: '{command}'. please try again\n")
                menu_options()

