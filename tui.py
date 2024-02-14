import sys
import random
import dungeon_text

#statblock --> id, hp, damage, evasion, armor, loot

MOBS = {
    "Goblin": dungeon_text.Statblock("Goblin", 8, 6, 10, 0, (10, 10)),

    "Hobgoblin": dungeon_text.Statblock("Hobgoblin", 10, 8, 12, 3, (15,15)),

    "Bandit": dungeon_text.Statblock("Bandit", 16, 6, 10, 2, (15, 15))
}

MOBS_LIST = ["Goblin", "Hobgoblin", "Bandit"]

RUNNING = True

PLAYER = dungeon_text.Player()

starting_weapon = dungeon_text.Weapon("starting-sword", 1, 8, 2)

starting_armor = dungeon_text.Armor("starting-armor", 1, 1)

PLAYER.equip_armor(starting_armor)
PLAYER.equip_weapon(starting_weapon)

current_enemy_stats = MOBS[MOBS_LIST[random.randrange(2)]]

current_enemy = dungeon_text.Mob(1, current_enemy_stats)

while RUNNING:
    command = input(">")

    def player_turn():
        print('What would you like to do?')

    def enemy_turn():
        print(f'The {current_enemy.id} attacks you.')
        attack = current_enemy.roll_attack()

        if attack == 20:
            print("He rolled a crit. Uh oh")
        if attack == 1:
            print("He critically failed!")

        if attack >= PLAYER.evasion:
            damage = current_enemy.roll_damage()
            print(f'It hit you for {damage} damage')
            PLAYER.take_damage(damage)

    if command.lower() == 'exit':
        RUNNING = False
        sys.exit()

    if command.lower() == 'atk':
        attack = PLAYER.roll_attack()

        if attack == 20:
            print("Critical Hit!")

        if attack == 1:
            print("Crtical Fail!")

        if attack >= current_enemy.evasion:
            print("A hit")
            damage = PLAYER.roll_damage()
            taken = current_enemy.take_damage(damage)
            print(f'You dealt {taken} damage to the {current_enemy.id}!')
        elif attack < current_enemy.evasion:
            print("You missed!")



    elif command.lower() == "y":
        print(f'You encounter a Level {current_enemy.level} {current_enemy.id}!')
        player_turn()

    