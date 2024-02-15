import sys
import random
import player, items, mob
import monster_manual

MOBS = {
    "Goblin": monster_manual.GOBLIN,

    "Hobgoblin": monster_manual.HOBGOBLIN,

    "Bandit": monster_manual.BANDIT,

    "Gang of Goblins": monster_manual.GANG_OF_GOBLINS
}

PLAYER = player.Player()

starting_weapon = items.Weapon("starting-sword", 1, 8, 2)

starting_armor = items.Armor("starting-armor", 1, 2)

PLAYER.equip_armor(starting_armor)
PLAYER.equip_weapon(starting_weapon)

print("Would you like to enter the Dungeon? y/n \n")

STARTING_ENEMY_STATS = MOBS[random.choice(MOBS.keys())]
STARTING_ENEMY = mob.Mob(1, STARTING_ENEMY_STATS)


def link_start(enemy:mob.Mob) -> None:
    RUNNING = True

    def player_turn():
        """
        Begins the Player turn
        """
        print('What would you like to do?  Attack - (a), Check HP - (hp), Flee - (f), Inventory - (i)\n')

    def enemy_turn():
        """
        Begins the enemy turn
        """
        print(f'The {enemy.id} attacks you.')
        attack = enemy.roll_attack()
        print(f'It rolled a {attack}! \n')

        if attack == 20:
            print("It rolled a crit. Uh oh. \n")
            taken = PLAYER.take_damage(enemy.roll_damage() * 2)
            print(f'The {enemy.id} hit you for {taken} damage! \n')
            if PLAYER.dead is False:
                player_turn()
        elif attack == 1:
            print("It critically failed! \n")
            if enemy.fumble_table() is True:
                taken = enemy.take_damage(enemy.roll_damage)
                print(f'The {enemy.id} hit itself for {taken} damage!')
            else:
                print("It missed.")
                if enemy.dead is False:
                    player_turn()
                else:
                    end_scene()
        else:
            if attack >= PLAYER.evasion:
                taken = PLAYER.take_damage(enemy.roll_damage())
                print(f'The {enemy.id} hit you for {taken} damage. \n')
                if PLAYER.dead is False:
                    player_turn()

            else:
                print(f"The {enemy.id} missed. \n")
                player_turn()

    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        print("You venture deeper into the dungeon... \n")
        next_enemy = mob.Mob(random.randrange(1,3), MOBS[random.choice(MOBS.keys())])
        RUNNING = False
        link_start(next_enemy)

    def begin_encounter():
        """
        Begins an encounter
        """
        print(f'You encounter a Level {enemy.level} {enemy.id}! \n')

    def end_scene():
        PLAYER.gain_gold(enemy.loot[0])
        PLAYER.gain_xp(enemy.loot[1])
        print(f"You killed the {enemy.id}! Continue? y/n\n")
        command = input(">")
        if command.lower() == "y":
            next_scene()

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
                print(f'You hit the {enemy.id}, dealing {taken} damage. \n')
                if enemy.dead is False:
                    enemy_turn()
                elif enemy.dead is True:
                    end_scene()
            elif attack < enemy.evasion:
                print("You missed. \n")
                enemy_turn()
        
if input(">").lower() == "y":
    link_start(STARTING_ENEMY)
    