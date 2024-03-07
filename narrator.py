import time
import random
import global_commands
import global_variables
import shopkeep
import monster_manual

SCENE_CHANGE = [
    " You press on...\n",
    " Your resolve steeled, you continue forwards...\n",
    " Your weary legs carry you on...\n",
    " You venture deeper into the dungeon...\n"
]
def next_scene_options():
    global_commands.type_text(random.choice(SCENE_CHANGE))
    ominous = f'    ...\n'
    for i in range(5):
        time.sleep(.5)
        print('\t'*i + ominous)

def level_up_options():
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
        exit_the_dungeon()
    else:
        global_commands.type_text("\n Invalid command. Please try again.\n")
        continue_run(next)

def exit_the_dungeon():
    print('')
    global_commands.type_text(" As you emerge from the Dungeon's darkness, the harsh light of day stings your eyes.\n")
    menu_options()

def buy_something():
    global_variables.SHOPKEEP.print_invevtory()
    global_commands.type_text(" What would you like to buy? Enter an item's number to purchase it.\n")
    command = input(">")

def shopkeep_options():
    print("-"*110+'\n')
    global_commands.type_text(" The Shopkeep eyes you wearily.\n")
    print("-"*110+'\n')
    print(" What would you like to do? Buy Something - (b) | Leave - (l)\n")
    command = input(">")
    if command.lower() == "b":
        command = None
        buy_something()
    elif command.lower() == "l":
        command = None
        menu_options()
    else: 
        print(" Invalid command, please try again")
        shopkeep_options()


def menu_options():
    print(" What would you like to do? Enter the Dungeon - (e) | Rest - (r) | Visit the Shop - (v)\n")
    command = input(">")
    print('')
    if command.lower() == "e":
        global_commands.type_text(" Would you like to enter the Dungeon? y/n\n", 0.03)
        command = input(">")
        if command.lower() == "y":
            global_variables.RUNNING = True
    elif command.lower() == "r":
        global_commands.type_text(" Plenty of time to sleep when you're dead.\n")
        menu_options()
    elif command.lower() == "v":
        print('')
        shopkeep_options()
    else:
        command = None
        global_commands.type_text(" Invalid command please try again\n")
        menu_options()
