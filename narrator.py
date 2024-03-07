import time
import random
import global_commands
import global_variables
import shopkeep
import monster_manual




def next_scene_options():
    global_commands.type_text("\nYou venture deeper into the dungeon...\n")
    ominous = f'    ...\n'
    for i in range(5):
        time.sleep(.5)
        print('\t'*i + ominous)

def level_up_options():
    global_commands.type_text('You have gained enough XP to level up! Which stat would you like to level up?\n')
    print('Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n')

def event_options():
    global_commands.type_text(f"\nWhich stat would you like to roll?\n")
    print("Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n")

def continue_run(next):
    global_commands.type_text("Continue? y/n\n")
    command = input(">")
    if command.lower() == "y":
        next()
    elif command.lower() == "n":
        pass
    else:
        global_commands.type_text("\nInvalid command. Please try again.\n")
        continue_run(next)

def exit_the_dungeon():
    global_commands.type_text("As you emerge from the Dungeon's darkness, the harsh light of day stings your eyes.")
    menu_options()

def buy_something():
    global_variables.SHOPKEEP.print_invevtory()
    global_commands.type_text(f"What would you like to buy? Enter an item's number to purchase it.\n")
    command = input(">")

def shopkeep_options():
    print("\n"+"-"*110+'\n')
    global_commands.type_text("The Shopkeep eyes you wearily.\n")
    print("What would you like to do? Buy Something - (b) | Leave - (l)\n")
    command = input(">")
    if command.lower() == "b":
        command = None
        buy_something()
    elif command.lower() == "l":
        command = None
        menu_options()
    else: 
        print("Invalid command, please try again")
        shopkeep_options()


def menu_options():
    print("\nWhat would you like to do? Enter the Dungeon - (e) | Rest - (r) | Visit the Shop - (v)\n")
    command = input(">")
    if command.lower() == "e":
        global_commands.type_text("\nWould you like to enter the Dungeon? y/n\n", 0.03)
        command = input(">")
        if command.lower() == "y":
            command = None
            global_variables.RUNNING = True
    elif command.lower() == "r":
        command = None
        global_commands.type_text("\nPlenty of time to sleep when you're dead.\n")
        menu_options()
    elif command.lower() == "v":
        command = None
        shopkeep_options()
    else:
        command = None
        global_commands.type_text("\nInvalid command please try again\n")
        menu_options()
