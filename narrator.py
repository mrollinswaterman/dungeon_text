import time
import sys
import random
import global_commands
import global_variables



SCENE_CHANGE = [
    " You press towards your goal...\n",
    " Your resolve steeled, you continue forwards...\n",
    " Your weary legs carry you on...\n",
    " You venture deeper into the dungeon...\n"
]

EXIT_DUNGEON = [
    " You climb out of the darkness.\n",
    " You take your first breath of fresh in what feels like an eternity.\n",
    " Finally, out...\n",
    " The soft moonlight bathes the world in a gentle glow.\n",
    " The sky above you seems too real to touch. You barely remember what it looked like...\n",
    " As you breathe a sigh of relief, you can't help but wonder if you ever even made it out...\n",
    " The openess of the Overworld is a stark contrast to the confines of the Dungeon.\n",
    " As you emerge from the Dungeon's darkness, the harsh light of day stings your eyes.\n"
]

ENTER_THE_SHOP = [
    " The Shopkeep eyes you sleepily.\n",
    " The Shopkeep glances at you warmly.\n",
    " The Shopkeep glares at you.\n",
    " The Shopkeep shoots you a friendly look.\n",
    " The Shopkeep barely notices you.\n",
    " The Shopkeep seems to look right through you.\n",
    " The Shopkeep eyes you eagerly.\n",
    " The Shopkeep grunts at your approach.\n",
    " The Shopkeep eyes you wearily.\n"
]
def next_scene_options():
    global_commands.type_text(random.choice(SCENE_CHANGE))
    ominous = f'    ...\n'
    for i in range(5):
        time.sleep(.5)
        print('\t'*i + ominous)

def level_up_options():
    print("-"*110 + '\n')
    global_commands.type_text(' You have gained enough XP to level up! Which stat would you like to level up?\n')
    print(' Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n')

def event_options():
    print('-'*110+'\n')
    print(" Which stat would you like to roll?\n")
    print(" Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n")

def continue_run(next):
    print("-"*110+"\n")
    global_commands.type_text(" Continue? y/n\n")
    command = input(">")
    if command.lower() == "y":
        print("")
        next()
    elif command.lower() == "n":
        print("")
        exit_the_dungeon()
    else:
        global_commands.type_text("\n Invalid command. Please try again.\n")
        continue_run(next)

def exit_the_dungeon():
    print("-" * 110+'\n')
    global_commands.type_text(random.choice(EXIT_DUNGEON))
    print("-"*110+'\n')
    menu_options()

def buy_something():
    global_commands.type_text(" Enter an item's number to purchase it OR (c) - Cancel Order\n")
    command = input(">")
    #print("")

    if command.lower() == "exit":
        sys.exit()
    elif command.lower() == "c":
        shopkeep_options()
    else:
        try:
            stock_num = int(command)
        except ValueError:
            print(" Invalid option, please try again.\n")
            buy_something()
        if stock_num <= global_variables.SHOPKEEP.stock_size+1:
            if global_variables.SHOPKEEP.inventory[stock_num-1].is_consumable is False:
                global_variables.SHOPKEEP.sell(global_variables.SHOPKEEP.inventory[stock_num-1],
                                        global_variables.PLAYER)
            else:
                global_commands.type_text(f" Please enter desired quantity:\n")
                command_2 = input(">")
                #print("")
                global_variables.SHOPKEEP.sell(global_variables.SHOPKEEP.inventory[stock_num-1],
                                        global_variables.PLAYER, int(command_2))
            shopkeep_options()
        else:
            print(f" Invalid item number '{int(command)}'. Please try again.\n")
            buy_something()

def leave_the_shop():
    print("-" * 110+'\n')
    global_commands.type_text(" You go on your way.\n")
    print("-"*110+'\n')
    menu_options()

def shopkeep_options():
    print("-"*110+'\n')
    global_commands.type_text(random.choice(ENTER_THE_SHOP))
    print("-"*110+'\n')
    global_commands.type_text(" What would you like to do?\n")
    print(" Buy Something - (b) | Leave - (l) | Sell something - (s) | Inventory - (i)\n")
    command = input(">")
    if command.lower() == "b":
        global_variables.SHOPKEEP.print_invevtory()
        buy_something()
    elif command.lower() == "l":
        leave_the_shop()
    elif command.lower() == "i":
        check_player_inventory(shopkeep_options)
    elif command.lower() == "exit":
        sys.exit()
    else: 
        print(" Invalid command, please try again")
        shopkeep_options()

def rest():
    print("-" * 110+'\n')
    global_commands.type_text(" Plenty of time to rest when you're dead.\n")
    print("-"*110+'\n')
    menu_options()

def check_player_inventory(next):
    print('')
    global_variables.PLAYER.print_inventory()
    global_commands.type_list(" Enter an item's number to equip it OR (b) - Go Back\n")
    command = input(">")
    print('')
    if command.lower() == "b":
        next()
    elif command.lower() == "exit":
        sys.exit()
    else:
        try:
            x = int(command)
        except ValueError:
            print(" Invalid command, please try again.\n")
            next()
        item = global_variables.PLAYER.inventory[int(command)-1]
        if global_variables.PLAYER.equip(item) is True:
            global_variables.PLAYER.equip(item)
        next()

def menu_options():
    global_commands.type_text(" What would you like to do?\n")
    print(" Enter the Dungeon - (e) | Rest - (r) | Visit the Shop - (v) | Inventory - (i) \n")
    command = input(">")
    print('')
    if command.lower() == "e":
        global_variables.START_CMD = True
    elif command.lower() == "r":
        rest()
    elif command.lower() == "v":
        shopkeep_options()
    elif command.lower() == "i":
        check_player_inventory(menu_options)
    elif command.lower() == "exit":
        sys.exit()
    else:
        command = None
        global_commands.type_text(" Invalid command please try again\n")
        menu_options()
