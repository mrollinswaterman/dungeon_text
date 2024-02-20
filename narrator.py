import time
import global_commands

def player_turn_options():
    
    print('What would you like to do?  Attack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i) | Use a Health Potion - (u)\n')


def next_scene_options():
    
    global_commands.type_text(f"\nYou venture deeper into the dungeon...\n")
    ominous = f'    ...\n'
    for i in range(5):
        time.sleep(.5)
        print('\t'*i + ominous)

def level_up_options():
    
    global_commands.type_text(f'You have gained enough XP to level up! Which stat would you like to level up?\n')
    print(f'Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n')

def event_options():
    
    global_commands.type_text(f"Which stat would you like to roll?\n")
    print(f"Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n")

def continue_run(next):
    global_commands.type_text(f"Continue? y/n\n")
    command = input(">")
    if command.lower() == "y":
        next()
    elif command.lower() == "n":
        pass
    else:
        global_commands.type_text(f"\nInvalid command. Please try again.\n")
        continue_run(next)