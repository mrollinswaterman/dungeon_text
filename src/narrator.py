import time, random
import global_commands, global_variables

SCENE_CHANGE = [
    "You press towards your goal...\n",
    "Your resolve steeled, you continue on...\n",
    "Your weary legs carry you ever further...\n",
    "You venture deeper into the dungeon...\n",
    "May your limbs never tire, may your heart never waiver, and may you never look back...",
    "There is no way but onward, no path but forward, no place but here...",
    "Do you even remeber what you're searching for? Perhaops you never were..."
]

EXIT_DUNGEON = [
    "You climb out of the darkness.",
    "You take your first breath of fresh air in what feels like an eternity.",
    "Finally... out...",
    "The soft moonlight bathes the world in a gentle glow.",
    "The sky above you seems real enough to touch. You barely remember what it looked like...",
    "You breathe a sigh of relief, yet you can't help but wonder if you'll make it out the next time...",
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
    "The Shopkeep eyes you wearily.",
    "The Shopkeep shakes off his slumber",
    "The Shopkeep gives you a nod."
]

EXIT_THE_SHOP = [
    "You go on your way.",
    "Your business is concluded.",
    "You slink out of the Shop.",
    "You leave, wondering if you'll see this place again...",
]

STATS = "\t Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n"

PREV_MENU = None

def back():
    PREV_MENU()

def next_scene_options():
    global_commands.type_text("\n" + " " + random.choice(SCENE_CHANGE))
    ominous = f'    ...\n'
    for i in range(4):
        time.sleep(.4)
        print('\t'*i + ominous)
    print("\n")

def level_up_options():
    global_commands.type_with_lines("You have gained enough XP to level up! Which stat would you like to level up?", 0.01)
    print(STATS)

def event_options():
    global_commands.type_header("Which stat would you like to roll?")
    print(STATS)

def continue_run():
    import scene_controller

    global_commands.type_with_lines("Continue? y/n")
    done = False
    while not done:
        cmd = input(">> ").lower()
        match cmd:
            case "exit":
                done = True
                global_commands.exit()
            case "y":
                done = True
                next_scene_options()
                scene_controller.SCENE.select_next()
            case "n":
                done = True
                print("")
                exit_the_dungeon()
            case _:
                global_commands.error_message(cmd)

def exit_the_dungeon():
    global_variables.RUNNING = False
    global_commands.type_with_lines(random.choice(EXIT_DUNGEON))
    global_variables.SHOPKEEP.restock()
    menu_options()

def ask_quantity() -> int | bool:
    from command_dict import commands
    default = commands["_"]

    global_commands.type_text(f"Please enter desired quantity:")
    done = False
    while not done:
        cmd = global_commands.get_cmd()

        if cmd in default:
            done = True
            default[cmd]()
        else:
            try:
                return int(cmd)
        
            except TypeError:
                print(f"Invalid quantity '{cmd}'. Please enter a valid quantity.", 0.01)

def buy_something():
    from command_dict import commands
    options = commands["_"]
    done = False
    while not done:
        global_variables.SHOPKEEP.print_inventory()
        global_commands.type_with_lines()
        print("Enter an item's number to purchase it -OR- Go Back - (b)\n")
        cmd = global_commands.get_cmd()
        if cmd in options:
            options[cmd]()
            return None
        else:
            try:
                item_index = int(cmd) - 1
                item = global_variables.SHOPKEEP.get(item_index)
                if item is not None:
                    global_variables.SHOPKEEP.sell(item)
                    done = True
                    return buy_something()
                else:
                    global_commands.error_message(cmd)
            except IndexError:#ValueError:
                global_commands.error_message(cmd)

def leave_the_shop():
    global_commands.type_with_lines(random.choice(EXIT_THE_SHOP))
    menu_options()

def shopkeep_options():
    from command_dict import commands
    options = commands["shopkeep_options"]

    global PREV_MENU
    PREV_MENU = shopkeep_options
    global_commands.type_with_lines(random.choice(ENTER_THE_SHOP))
    global_commands.type_header_with_lines("What would you like to do?")
    print("\t Purcahse Items - (p) | Sell something - (s) | Inventory - (i) | Leave - (l)\n")
    done = False
    while not done:
        cmd = global_commands.get_cmd()
        if cmd in options:
            done = True
            options[cmd]()
        else:
            global_commands.error_message(cmd)

def rest():
    global_commands.type_with_lines("Plenty of time to rest when you're dead.")
    back()

def select_item():
    from command_dict import commands
    options = commands["_"]

    global_commands.type_header("Enter an item's number to use it -OR- Go Back - (b)")
    done = False
    while not done:
        cmd = global_commands.get_cmd()

        if cmd in options:
            done = True
            options[cmd]()
        else:
            try:
                item = global_variables.PLAYER.get_item(int(cmd) - 1)
                if global_variables.PLAYER.use(item):
                    done = True
                    show_inventory()
                else:
                    global_commands.error_message(None, "You can't use that, please try again.")
            except ValueError:
                global_commands.error_message(cmd)

def show_inventory():
    global_variables.PLAYER.print_inventory()
    select_item()

def menu_options():
    from command_dict import commands
    options = commands["overworld_menu"]

    global PREV_MENU
    PREV_MENU = menu_options
    global_commands.type_header_with_lines("What would you like to do?")
    print("\t Enter the Dungeon - (e) | Visit the Shop - (v) | Inventory - (i) | Rest - (r)\n")
    
    done = False
    while not done:
        cmd = global_commands.get_cmd()

        if cmd in options:
            done = True
            options[cmd]()

        else:
            global_commands.error_message(cmd)

