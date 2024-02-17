import sys
import random
import player, items, mob
import monster_manual
import narrator
import commands
import item_compendium

print(round(2/3))

MOBS = {
    "Goblin": monster_manual.GOBLIN,

    "Hobgoblin": monster_manual.HOBGOBLIN,

    "Bandit": monster_manual.BANDIT,

    "Gang of Goblins": monster_manual.GANG_OF_GOBLINS
}

PLAYER = player.Player()

iron_sword = items.Weapon("Iron Sword", 1)
iron_sword.set_damage_dice(1,8)
iron_sword.Set_crit_multiplier(2)

leather_armor = items.Armor("Leather Armor", 1)
leather_armor.set_armor_value(2)

PLAYER.equip_armor(leather_armor)
PLAYER.equip_weapon(iron_sword)

PLAYER.pick_up(item_compendium.Health_Potion("Health Potion", 1), 5)

print("\nWould you like to enter the Dungeon? y/n\n")

STARTING_ENEMY_STATS = MOBS[random.choice(list(MOBS.keys()))]
STARTING_ENEMY = mob.Mob(PLAYER.threat[0], STARTING_ENEMY_STATS)

def link_start(enemy:mob.Mob) -> None:
    RUNNING = True

    #functions
    def player_turn():
        """
        Begins the Player turn
        """
        narrator.player_turn_options()
    
    def player_death():
        #some text probably too
        RUNNING = False
        sys.exit()

    def enemy_turn():
        """
        Begins the enemy turn
        """
        print("-" * 110+"\n")
        print(f'The {enemy.id} attacks you.\n')
        attack = enemy.roll_attack()
        print(f'It rolled a {attack}.\n')

        if attack == 20:
            print("A critical hit! Uh oh.\n")
            taken = PLAYER.take_damage(enemy.roll_damage() * 2)
            print(f'The {enemy.id} hit you for {taken} damage!\n')
            print("-" * 110+"\n")
            if PLAYER.dead is False:
                player_turn()
            else:
                player_death()
        elif attack == 1:
            print("It critically failed!\n")
            if enemy.fumble_table() is True:
                taken = enemy.take_damage(enemy.roll_damage())
                print(f'The {enemy.id} hit itself for {taken} damage!\n')
            else:
                print("It missed.\n")
                print("-" * 110+"\n")
            if enemy.dead is False:
                player_turn()
            else:
                end_scene()
        else:
            if attack >= PLAYER.evasion:
                taken = PLAYER.take_damage(enemy.roll_damage())
                print(f'The {enemy.id} hit you for {taken} damage.\n')
                print("-" * 110+"\n")
                if PLAYER.dead is False:
                    player_turn()
                if PLAYER.dead is True:
                    player_death()

            else:
                print(f"The {enemy.id} missed.\n")
                print("-" * 110+"\n")
                player_turn()

    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        print('\n')
        narrator.next_scene_options()
        next_enemy = mob.Mob(random.randrange(PLAYER.threat[0], PLAYER.threat[1]), MOBS[random.choice(list(MOBS.keys()))])
        RUNNING = False
        link_start(next_enemy)

    def begin_encounter():
        """
        Begins an encounter
        """
        print(f'\nYou encounter a Level {enemy.level} {enemy.id}!\n')

    def level_up_player():
        narrator.level_up_options()
        command = input(">")
        PLAYER.spend_xp(command)
        print(f'\nYour {command} increased by 2.\n')
        print("Continue? y/n\n")
        command = input(">")
        if command.lower() == "y":
            next_scene()

    def end_scene():
        PLAYER.gain_gold(enemy.loot[0])
        PLAYER.gain_xp(enemy.loot[1])
        print(f"You killed the {enemy.id}!\n")
        print("-"*110+'\n')
        if PLAYER.level_up is True:
            level_up_player()
        else:
            print("Continue? y/n\n")
            command = input(">")
            if command.lower() == "y":
                next_scene()

    #commands dict

    #starting print statements
    begin_encounter()
    player_turn()

    while RUNNING:

        command = input(">")

        #command interpretation
        if command.lower() == "exit":
            RUNNING = False
            sys.exit()
        if command.lower() == "a":
            commands.attack(PLAYER, enemy, enemy_turn, end_scene)
        if command.lower() == "hp":
            commands.hp(PLAYER, player_turn)
        if command.lower() == "i":
            commands.inventory(PLAYER, player_turn)
        if command.lower() == "u":
            commands.use_an_item(PLAYER, "Health Potion", PLAYER, enemy_turn, player_turn)
            
        
if input(">").lower() == "y":
    link_start(STARTING_ENEMY)