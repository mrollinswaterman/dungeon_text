import sys, random
import mob, monster_manual
import narrator, player_commands, enemy_commands
import item_compendium
import dms_guide, events
import global_commands, global_variables
import status_effects

PLAYER = global_variables.PLAYER

TEST = False

item_compendium.PLAYER = PLAYER
status_effects.PLAYER = PLAYER
player_commands.TEST = TEST

#notes on formatting

def link_start(enemy:mob.Mob) -> None:
    global_variables.RUNNING = True

    enemy_commands.ENEMY = enemy
    player_commands.ENEMY = enemy

    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        narrator.next_scene_options()
        if global_commands.probability(1): #80% chance of an enemy spawning next
            next_enemy: mob.Mob = monster_manual.spawn_random_mob()
            global_variables.RUNNING = False
            link_start(next_enemy)
        else: #remainging 20% chance of an event spawning
            next_event: events.Event = dms_guide.EVENTS["Mysterious_Berries"]#random.choice(list(dms_guide.EVENTS.values()))
            next_event.set_tries(2)
            next_event.set_passed(False)
            next_event.start()#prints event start text
            run_event(next_event)

    if enemy is None:
        next_scene()

    #functions
    def begin_encounter():
        """
        Begins an encounter
        """
        global_commands.type_text(f"You encounter a Level {enemy.level} {enemy.id.upper()}!")

    def player_turn():
        """
        Begins the Player turn
        """
        enemy.set_header(False)#reset enemy's formatting header
        PLAYER.update()
        player_commands.turn_options()

    def enemy_turn():
        """
        Begins the enemy turn
        """
        enemy.update()
        enemy_commands.turn_options()

    def player_death():
        #some text probably too
        global_variables.RUNNING = False
        sys.exit()

    def end_scene():
        global_commands.type_text(f"You killed the {enemy.id}!\n")
        PLAYER.recieve_reward(enemy.loot)
        PLAYER.update()
        narrator.continue_run(next_scene)

    def run_event(event: events.Event):
        narrator.event_options()
        command = input(">> ")
        print("")#newline after cmd prompt
        if command.lower() in events.FAILURE_LINES:
            event.run(command, PLAYER.roll_a_check(command))
            if event.passed is True:# if passed, reset event tries and next_scene()
                event.set_tries(2)
                event.set_passed(False)
                PLAYER.recieve_reward(event.loot)
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
            global_commands.type_text(f"Invalid command '{command}', please try again.")
            run_event(event)

    def level_up_player():
        narrator.level_up_options()
        command = input(">> ")
        print("")#newline after cmd prompt
        PLAYER.spend_xp(command)
        global_commands.type_text(f"Your {command} increased by 1. You are now Level {PLAYER.level}")
        global_variables.SHOPKEEP.set_player_level(PLAYER.level)#make sure shopkeep's threat changes
        if PLAYER.level_up is True:
            level_up_player()
        else:
            narrator.continue_run(next_scene)
    PLAYER.set_level_up_function(level_up_player)


    #Set constants for command files
    enemy_commands.PLAYER_TURN = player_turn
    player_commands.PLAYER_TURN = player_turn

    enemy_commands.PLAYER_DEATH = player_death
    player_commands.PLAYER_DEATH = player_death

    enemy_commands.END_SCENE = end_scene
    player_commands.END_SCENE = end_scene

    enemy_commands.ENEMY_TURN = enemy_turn
    player_commands.ENEMY_TURN = enemy_turn

    enemy_commands.NEXT_SCENE = next_scene
    player_commands.NEXT_SCENE = next_scene

    #starting print statements
    begin_encounter()
    player_turn()

    while global_variables.RUNNING is True:

        command = input(">> ").lower()
        print("")

        #command interpretation
        if command == "exit":
            global_variables.RUNNING = False
            player_commands.save()
            sys.exit()
        try:
            command = int(command)
            try:
                item = PLAYER.inventory[command - 1]
            except IndexError:
                item = None
            player_commands.use_an_item(item, enemy)
        except ValueError:
            pass
        match command:
            case "a": #attack
                player_commands.attack()
            case "hp": #check hp
                player_commands.show_hp()
            case "i": #show inventory
                player_commands.show_inventory()
            case "test": #test suite
                print(enemy.hp)
            case "p": #pass the turn
                enemy_turn()
            case "c": #cleans an effect
                player_commands.cleanse_an_effect()
            case "f": #attempt to flee
                global_variables.RUNNING = False
                player_commands.flee()
                enemy = None

def begin():
    global_commands.type_text(" Would you like to enter the Dungeon? y/n\n")

    STARTING_ENEMY: mob.Mob = monster_manual.spawn_random_mob() if TEST is False else monster_manual.spawn_mob("Land Shark")

    if STARTING_ENEMY is None:
        print(f"Error: Enemy was {STARTING_ENEMY}, generating default starting enemy...")
        STARTING_ENEMY = monster_manual.mobs[0]

    STARTING_ENEMY.set_level(PLAYER.level)

    command = input(">> ").lower()
    print("")#newline after command prompt
    if command == "y":
        player_commands.load()
        global_variables.RUNNING = True#
        link_start(STARTING_ENEMY)
    elif command == "t":
        narrator.exit_the_dungeon()
    elif command == "n":
        player_commands.save()
        sys.exit()

begin()