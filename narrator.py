import player

def player_turn_options():
    print('\nWhat would you like to do? | Attack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i)\n')


def next_scene_options():
    print("\nYou venture deeper into the dungeon...")
    print(" ...")
    print("     ...")

def level_up_options():
    print(f'You gave gained enough XP to level up! Which stat would you like to level up?\n')
    print(f'Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n')

def display_hp(player:player.Player):
    print(f'\nHP: {player.hp}/{player.max_hp}')
    print("["+"/"*player.hp+" "*(player.max_hp-player.hp)+"]")