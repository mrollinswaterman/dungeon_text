import sys
import math
import random
import player, items, mob
import monster_manual
import narrator
import player_commands
import item_compendium
import dms_guide
import events
import global_commands
import shopkeep
import global_variables

print(math.ceil(5/4))
print(math.ceil(5/2))
global_commands.type_text("\nWould you like to enter the Dungeon? y/n\n", 0.03)

STARTING_ENEMY: mob.Mob = monster_manual.random_mob(1)
STARTING_ENEMY.set_level(1)


def link_start(enemy:mob.Mob) -> None:
    global_variables.RUNNING = True

    #functions

    def player_turn():
        """
        Begins the Player turn
        """
        global_variables.PLAYER.update()
        player_commands.player_turn_options()
    
    def player_death():
        #some text probably too
        global_variables.RUNNING
        sys.exit()

    def enemy_turn():
        """
        Begins the enemy turn
        """
        print("-" * 110+"\n")

        if random.randrange(1,100) > 50 or enemy.statblock.special is None: # 50% chance of attack
            attack = enemy.roll_attack()
            global_commands.type_text(f'The {enemy.id} attacks you, rolling a {attack}\n')
            if attack == 0:
                global_commands.type_text(f"A critical hit! Uh oh.\n")
                taken = global_variables.PLAYER.take_damage(enemy.roll_damage() * 2)
                global_commands.type_text(f'The {enemy.id} hit you for {taken} damage!\n')
                print("-" * 110+"\n")
                if global_variables.PLAYER.dead is False:
                    player_turn()
                else:
                    player_death()
            elif attack == 1:
                global_commands.type_text(f"It critically failed!\n")
                if enemy.fumble_table() is True:
                    taken = enemy.take_damage(enemy.roll_damage())
            
                    global_commands.type_text(f'The {enemy.id} hit itself for {taken} damage!\n')
                else:
                    global_commands.type_text(f"It missed.\n")
                    print("-" * 110+"\n")
                if enemy.dead is False:
                    player_turn()
                else:
                    end_scene()
            else: 
                if attack >= global_variables.PLAYER.evasion:
                    taken = global_variables.PLAYER.take_damage(enemy.roll_damage())
                    global_commands.type_text(f'The {enemy.id} hit you for {taken} damage.\n')
                    print("-" * 110+"\n")
                    if global_variables.PLAYER.dead is False:
                        player_turn()
                    if global_variables.PLAYER.dead is True:
                        player_death()
                else:
                    global_commands.type_text(f"The {enemy.id} missed.\n")
                    print("-" * 110+"\n")
                    player_turn()
        else:# ...aaaaand 50% chance of performing a special move
            enemy.special_move(enemy, global_variables.PLAYER)
            print("-" * 110+"\n")
            player_turn()

    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        narrator.next_scene_options()
        if random.randrange(0, 100) > 33: #66% chance of an enemy spawning next
            next_enemy: mob.Mob = monster_manual.random_mob(global_variables.PLAYER.level) 
            #^ picks a random mob from the list, wth a min level equal to the player's level
            next_enemy.set_level(random.randrange(next_enemy.level_range[0], global_variables.PLAYER.threat))
            #^ sets the enemy's level to a random value between its minimum level and the player's 'threat level'.
            RUNNING = False
            link_start(next_enemy)
        else: #remainging 33% chance of an event spawning
            next_event: events.Event = random.choice(dms_guide.EVENT_LIST)
            next_event.set_tries(2)
            print(next_event.text)
            print("-" * 110+'\n')
            run_event(next_event)

    def begin_encounter():
        """
        Begins an encounter
        """

        global_commands.type_text(f'\nYou encounter a Level {enemy.level} {enemy.id}!\n')

    def level_up_player():
        narrator.level_up_options()
        command = input(">")
        global_variables.PLAYER.spend_xp(command)

        global_commands.type_text(f'\nYour {command} increased by 2. You are now Level {global_variables.PLAYER.level}\n')
        narrator.continue_run(next_scene)

    def run_event(event: events.Event):
        narrator.event_options()
        command = input(">")
        if command.lower() != "w":
            print('\n'+"-" * 110)
            global_commands.type_text(event.run(command, global_variables.PLAYER.roll_a_check(command)))
            print("-" * 110)
            if event.passed is True:# if passed, reset event tries
                event.set_tries(2)
                if event.reward is not None:
                    global_variables.PLAYER.recieve_reward(event.reward)
                next_scene()
            elif event.tries is True:# if not passed yet, and still tries, run it again
                run_event(event)
            else: # in failed, tell the player
                global_commands.type_text(event.end_message)
                next_scene()

    def end_scene():
        global_variables.PLAYER.gain_gold(enemy.loot[0])
        global_variables.PLAYER.gain_xp(enemy.loot[1])
        global_variables.PLAYER.reset_ap()
        global_commands.type_text(f"You killed the {enemy.id}!\n")
        print("-"*110+'\n')
        if global_variables.PLAYER.level_up is True:
            level_up_player()
        else:
            narrator.continue_run(next_scene)

    #starting print statements
    begin_encounter()
    player_turn()

    while global_variables.RUNNING is True:
        if enemy is None:
            next_scene()

        command = input(">")

        #command interpretation
        if command.lower() == "exit":
            global_variables.RUNNING = False
            sys.exit()
        if command.lower() == "a":
            player_commands.attack(enemy, enemy_turn, end_scene)
        if command.lower() == "hp":
            player_commands.hp(player_turn)
        if command.lower() == "i":
            player_commands.inventory(player_turn)
        if command.lower() == "u":
            player_commands.use_an_item("Health Potion", enemy_turn, player_turn)
        if command.lower() == "f":
            global_variables.RUNNING = False
            player_commands.flee(enemy)
            enemy = None
   
if input(">").lower() == "y":
    link_start(STARTING_ENEMY)
