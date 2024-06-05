import time, random
import global_commands, global_variables

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

PREV_MENU = None

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

def continue_run():
    import controller

    global_commands.type_with_lines("Continue? y/n")
    command = input(">> ").lower()
    if command == "y":   
        next_scene_options()
        controller.next_scene()
    elif command == "n":
        exit_the_dungeon()
    elif command == "exit":
        global_commands.exit()
    else:
        global_commands.type_text("Invalid command. Please try again.")
        continue_run()

def exit_the_dungeon():
    global_variables.RUNNING = False
    global_commands.type_with_lines(random.choice(EXIT_DUNGEON))
    global_variables.restock_the_shop()
    menu_options()

def ask_quantity(item):
    global_commands.type_text(f"Please enter desired quantity:")
    done = False
    while not done:
        cmd = input(">> ").lower()
        print("")#newline after... you get the idea
        match cmd:
            case "exit":
                done = True
                global_commands.exit()
            case _:
                try:
                    if global_variables.SHOPKEEP.sell(item, global_variables.PLAYER, int(cmd)):
                        global_variables.SHOPKEEP.print_inventory()
                    buy_something() 
                    done = True       
                except TypeError:
                    print(f" Invalid quantity '{cmd}'. Please enter a valid quantity.")

def buy_something():
    global_commands.type_with_lines("")
    print("Enter an item's number to purchase it OR (c) - Cancel Order\n")
    done = False
    while not done:
        cmd = input(">> ").lower()
        print("")
        match cmd:
            case "exit":
                done = True
                global_commands.exit()
            case "c":
                done = True
                shopkeep_options()
            case _:
                try:
                    stock_num = int(cmd)
                    item = global_variables.SHOPKEEP.inventory[stock_num-1]
                    if stock_num <= global_variables.SHOPKEEP.stock_size+1:
                        done = True
                        if item.is_consumable:
                            ask_quantity(item)
                            return None
                        elif global_variables.SHOPKEEP.sell(item, global_variables.PLAYER):
                            global_variables.SHOPKEEP.print_inventory()
                        buy_something()
                    else:
                        global_commands.type_text(f" Invalid item number '{int(cmd)}'. Please try again.")
                except ValueError:
                    print("Invalid option, please try again.\n")

def leave_the_shop():
    global_commands.type_with_lines(random.choice(EXIT_THE_SHOP))
    menu_options()

def shopkeep_options():
    global PREV_MENU
    PREV_MENU = shopkeep_options
    global_commands.type_with_lines(random.choice(ENTER_THE_SHOP))
    global_commands.type_with_lines("What would you like to do?")
    print("\t Buy Something - (b) | Leave - (l) | Sell something - (s) | Inventory - (i)\n")
    done = False
    while not done:
        cmd = input(">> ").lower()
        print("")
        match cmd:
            case "exit":
                done = True
                global_commands.exit()
            case "b":
                done = True
                global_variables.SHOPKEEP.print_inventory()
                buy_something()
            case "l":
                done = True
                leave_the_shop()
            case "i":
                done = True
                show_inventory()
            case _:
                global_commands.type_text(f"Invalid command '{cmd}'. Please try again.")

def rest():
    global_commands.type_with_lines("Plenty of time to rest when you're dead.")
    PREV_MENU()

def select_item():
    global_commands.type_text("Enter an item's number to equip it OR (b) - Go Back")
    cmd = input(">> ").lower()
    print("")
    match cmd:
        case "exit":
            global_commands.exit()
        case "b":
            PREV_MENU()
        case _:
            try:
                item = global_variables.PLAYER.get_item_by_index(int(cmd) - 1)
                if global_variables.PLAYER.equip(item) is True:
                    show_inventory()
                else:
                    global_commands.type_text("Can't equip that.")
                    select_item()
            except ValueError:
                global_commands.type_text("Invalid command, please try again.")
                select_item()

def show_inventory():
    global_variables.PLAYER.print_inventory()
    select_item()

def menu_options():
    global PREV_MENU
    PREV_MENU = menu_options
    global_commands.type_with_lines("What would you like to do?")
    print("\t Enter the Dungeon - (e) | Rest - (r) | Visit the Shop - (v) | Inventory - (i) \n")
    command = input(">> ").lower()
    print("")
    match command:
            case "e": #enter the dungeon again
                global_variables.START_CMD = True
            case "r": #rest text
                rest()
            case "v": #visit the shop
                shopkeep_options()
            case "i": #check inventory
                show_inventory()
            case "exit":
                global_commands.exit()
            case _:
                global_commands.type_text(f"Invalid command: '{command}'. please try again.")
                menu_options()

