import sys
import random
import secrets
import player, items, mob

#statblock --> id, hp, damage, evasion, armor, loot

MOBS = {
    "Goblin": dungeon_text.Statblock("Goblin", 5, 6, 10, 0, (10, 10)),

    "Hobgoblin": dungeon_text.Statblock("Hobgoblin", 8, 8, 12, 3, (15,15)),

    "Bandit": dungeon_text.Statblock("Bandit", 12, 6, 10, 2, (15, 15))
}

MOBS_LIST = ["Goblin", "Hobgoblin", "Bandit"]

PLAYER = dungeon_text.Player()

starting_weapon = dungeon_text.Weapon("starting-sword", 1, 8, 2)

starting_armor = dungeon_text.Armor("starting-armor", 1, 2)

PLAYER.equip_armor(starting_armor)
PLAYER.equip_weapon(starting_weapon)

print("Would you like to enter the Dungeon? y/n \n")

STARTING_ENEMY_STATS = MOBS[MOBS_LIST[random.randrange(0,2)]]
STARTING_ENEMY = dungeon_text.Mob(1, STARTING_ENEMY_STATS)


def link_start(enemy:dungeon_text.Mob) -> None:
    RUNNING = True

    def player_turn():
        """
        Begins the Player turn
        """
        print('What would you like to do?  Attack - (a), Check HP - (hp), Flee - (f)\n')

    def enemy_turn():
        """
        Begins the enemy turn
        """
        print(f'The {enemy.id} attacks you.')
        attack = enemy.roll_attack()
        print(f'It rolled a {attack}! \n')

        if attack == 20:
            print("He rolled a crit. Uh oh. \n")
        if attack == 1:
            print("He critically failed! \n")

        if attack >= PLAYER.evasion:
            taken = PLAYER.take_damage(enemy.roll_damage())
            print(f'The {enemy.id} hit you for {taken} damage. \n')
            if PLAYER.dead is False:
                player_turn()

        elif attack < PLAYER.evasion:
            print(f"The {enemy.id} missed. \n")
            player_turn()
    
    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        print("You venture deeper into the dungeon... \n")
        next_enemy = dungeon_text.Mob(random.randrange(1,3), MOBS[MOBS_LIST[random.randrange(0,2)]])
        RUNNING = False
        link_start(next_enemy)

    def begin_encounter():
        """
        Begins an encounter
        """
        print(f'You encounter a Level {enemy.level} {enemy.id}! \n')

    #starting print statements
    begin_encounter()
    player_turn()

    while RUNNING:

        command = input(">")

        #command interpretation
        if command.lower() == 'exit':
            RUNNING = False
            sys.exit()

        if command.lower() == 'a':
            #PLAYER.roll_attack()
            print(f'You attack the {enemy.id}.')
            attack = 100
            print(f'You rolled a {attack}. \n')

            if attack == 20:
                print("Critical Hit! \n")

            if attack == 1:
                print("Crtical Fail! \n")

            if attack >= enemy.evasion:
                #PLAYER.roll_damage()

                taken = enemy.take_damage(1000)
                print(f'You hit the {enemy.id}, dealing {taken} damage! \n')
                if enemy.dead is False:
                    enemy_turn()
                elif enemy.dead is True:
                    print(f"You killed the {enemy.id}! Continue? y/n\n")
                    command = input(">")
                    if command.lower() == "y":
                        next_scene()
            elif attack < enemy.evasion:
                print("You missed! \n")
                enemy_turn()
        
if input(">").lower() == "y":
    link_start(STARTING_ENEMY)
    