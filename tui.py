import sys
import random
import mob
import monster_manual
import narrator
import player_commands
import item_compendium
import dms_guide
import events
import global_commands
import global_variables

#notes on formatting

def link_start(enemy:mob.Mob) -> None:
    global_variables.RUNNING = True

    if enemy is None:
        next_scene()
    #functions

    def player_turn():
        """
        Begins the Player turn
        """
        global_variables.PLAYER.update()
        player_commands.player_turn_options()

    def player_death():
        #some text probably too
        global_variables.RUNNING = False
        sys.exit()
 
    def begin_encounter():
        """
        Begins an encounter
        """
        global_commands.type_text(f" You encounter a Level {enemy.level} {enemy.id.upper()}!")

    def end_scene():
        global_commands.type_text(f" You killed the {enemy.id}!\n")
        global_variables.PLAYER.recieve_reward(enemy.loot)
        global_variables.PLAYER.reset_ap()
        narrator.continue_run(next_scene)

    def enemy_turn():
        """
        Begins the enemy turn
        """
        if random.randrange(1,100) > 50 or enemy.statblock.special is None: # 50% chance of attack
            attack = enemy.roll_attack()
            global_commands.type_with_lines(f" The {enemy.id} attacks you, rolling a {attack}\n")
            if attack == 0:
                global_commands.type_text(f" A critical hit! Uh oh.\n")
                taken = global_variables.PLAYER.take_damage(enemy.roll_damage() * 2)
                global_commands.type_text(f" The {enemy.id} hit you for {taken} damage!\n")
                if global_variables.PLAYER.dead is False:
                    player_turn()
                else:
                    player_death()
            elif attack == 1:
                global_commands.type_text(f" It critically failed!\n")
                if enemy.fumble_table() is True:
                    taken = enemy.take_damage(enemy.roll_damage())
                    global_commands.type_text(f" The {enemy.id} hit itself for {taken} damage!\n")
                else:
                    global_commands.type_text(f" It missed.\n")

                if enemy.dead is False:
                    player_turn()
                else:
                    end_scene()
            else: 
                if attack >= global_variables.PLAYER.evasion:
                    taken = global_variables.PLAYER.take_damage(enemy.roll_damage())
                    global_commands.type_text(f" The {enemy.id} hit you for {taken} damage.\n")
                    if global_variables.PLAYER.dead is False:
                        player_turn()
                    if global_variables.PLAYER.dead is True:
                        player_death()
                else:
                    global_commands.type_text(f" The {enemy.id} missed.\n")
                    player_turn()
        else:# ...aaaaand 50% chance of performing a special move
            enemy.special_move(enemy, global_variables.PLAYER)
            player_turn()

    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        narrator.next_scene_options()
        roll = random.randrange(0, 100)
        if roll <= 80: #80% chance of an enemy spawning next
            next_enemy: mob.Mob = monster_manual.spawn_mob(global_variables.PLAYER.level)
            global_variables.RUNNING = False
            link_start(next_enemy)
        else: #remainging 20% chance of an event spawning
            next_event: events.Event = random.choice(dms_guide.EVENT_LIST)
            next_event.set_tries(2)
            next_event.set_passed(False)
            #print(f"TRIES: {next_event._tries}")
            next_event.start()#prints event start text
            run_event(next_event)

    def run_event(event: events.Event):
        narrator.event_options()
        command = input(">")
        print("")#newline after cmd prompt
        if command.lower() in events.FAILURE_LINES:
            event.run(command, global_variables.PLAYER.roll_a_check(command))
            if event.passed is True:# if passed, reset event tries and next_scene()
                event.set_tries(2)
                event.set_passed(False)
                global_variables.PLAYER.recieve_reward(event.loot)
                narrator.continue_run(next_scene)
            elif event.tries is True:# if not passed yet, and still tries left, run it again
                run_event(event)
            else: # if failed, tell the player and move on
                event.end()
                narrator.continue_run(next_scene)
        elif command.lower() == "exit":
            global_variables.RUNNING = False
            sys.exit()
        else:
            global_commands.type_text(f" Invalid command '{command}', please try again.")
            run_event(event)

    def level_up_player():
        narrator.level_up_options()
        command = input(">")
        print("")#newline after cmd prompt
        global_variables.PLAYER.spend_xp(command)
        global_commands.type_text(f" Your {command} increased by 1. You are now Level {global_variables.PLAYER.level}")
        global_variables.SHOPKEEP.set_threat(global_variables.PLAYER.threat)#make sure shopkeep's threat changes
        if global_variables.PLAYER.level_up is True:
            level_up_player()
        else:
            narrator.continue_run(next_scene)

    global_variables.PLAYER.set_level_up_function(level_up_player)

    #starting print statements
    begin_encounter()
    player_turn()

    while global_variables.RUNNING is True:

        command = input(">").lower()

        #command interpretation
        if command == "exit":
            global_variables.RUNNING = False
            sys.exit()
        if command == "a":
            player_commands.attack(enemy, enemy_turn, end_scene)
        if command == "hp":
            player_commands.hp(player_turn)
        if command == "i":
            player_commands.inventory(player_turn)
        if command == "u":
            player_commands.use_an_item(item_compendium.generate_hp_potions(), enemy_turn, player_turn)
        if command == "f":
            global_variables.RUNNING = False
            player_commands.flee(enemy)
            enemy = None

def begin():
    global_commands.type_text(" Would you like to enter the Dungeon? y/n\n")

    STARTING_ENEMY: mob.Mob = monster_manual.spawn_mob(global_variables.PLAYER.level)

    if STARTING_ENEMY is None:
        print(f"Error: Enemy was {STARTING_ENEMY}, generating default starting enemy...")
        STARTING_ENEMY = mob.Mob(monster_manual.mobs[0])

    STARTING_ENEMY.set_level(global_variables.PLAYER.level)

    command = input(">").lower()
    print("")#newline after command prompt
    if command == "y":
        global_variables.RUNNING = True
        link_start(STARTING_ENEMY)
    elif command == "t":
        narrator.exit_the_dungeon()
    elif command == "n":
        sys.exit()

while global_variables.START_CMD is True:
    global_variables.START_CMD = False
    print("")
    begin()