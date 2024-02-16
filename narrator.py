import player

def player_turn_options():
    print('What would you like to do? | Attack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i) | Use a Health Potion - (u)\n')


def next_scene_options():
    print("You venture deeper into the dungeon...\n")
    ominous = f'    ...\n'
    for i in range(5):
        print('\t'*i + ominous)

def level_up_options():
    print(f'You gave gained enough XP to level up! Which stat would you like to level up?\n')
    print(f'Strength - (str) | Dexterity - (dex) | Constitution - (con) | Intelligence - (int) | Wisdom - (wis) | Charisma - (cha)\n')

