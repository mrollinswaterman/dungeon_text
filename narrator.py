import time
import global_commands

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
    
    global_commands.type_text(f"Which stat would you like to roll?\n")
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
    global_commands.type_text("As you emerge from the Dungeon's darkness, the harsh light of day stings your eyes.\n")
    

def menu_options():
    global_commands.type_text("What would you like to do? Enter the Dungeon - (e) | Rest - (r) | Visit the Shop - (v)\n")
    command = input(">")
    if command.lower() == "e":
        pass
    elif command.lower() == "r":
        global_commands.type_text("Plenty of time to sleep when you're dead.\n")
    elif command.lower() == "v":
        pass
    else: 
        global_commands.type_text("Invalid command please try again\n")
        menu_options()
