import sys, random
import mob, monster_manual
import narrator, player_commands, enemy_commands
import item_compendium
import dm_guide
import event as ev
import global_commands, global_variables
import status_effects

PLAYER = global_variables.PLAYER

TEST = False

item_compendium.PLAYER = PLAYER
status_effects.PLAYER = PLAYER
enemy_commands.PLAYER = PLAYER
player_commands.TEST = TEST

ENEMY:mob.Mob = None

def next_scene():
        """
        Starts a new scene with a new enemy or event
        """
        global ENEMY
        ENEMY = None
        if global_commands.probability(1): #85% chance of an enemy spawning next
            ENEMY = monster_manual.spawn_random_mob()
            global_variables.RUNNING = False
            link_start()
        else: #remainging 15% chance of an event spawning
            next_event: ev.Event = dm_guide.spawn_random_event()
            next_event.set_tries(2)
            next_event.set_passed(False)
            next_event.start()#prints event start text
            run_event(next_event)

def begin_encounter():
    """
    Begins an encounter
    """
    if ENEMY is None:
        next_scene()
        return None
    global_commands.type_text(f"You encounter a Level {ENEMY.level} {ENEMY.id.upper()}!")

def player_turn():
    """
    Begins the Player turn
    """
    ENEMY.set_header(False)#reset enemy's formatting header
    PLAYER.update()
    player_commands.turn_options()

def enemy_turn():
    """
    Begins the enemy turn
    """
    ENEMY.update()
    enemy_commands.turn_options()

def player_death():
    #smth else
    global_commands.type_with_lines("You have died.", 2)
    global_variables.RUNNING = False
    player_commands.reset()
    sys.exit()

def end_scene():
    global ENEMY
    global_commands.type_text(f"You killed the {ENEMY.id}!\n")
    PLAYER.recieve_reward(ENEMY.loot)
    PLAYER.update()
    ENEMY = None
    if not PLAYER.can_level_up:
        narrator.continue_run(next_scene)
    else:
        level_up_player()

def run_event(event: ev.Event):
    narrator.event_options()
    command = input(">> ")
    print("")#newline after cmd prompt
    if command.lower() in ev.FAILURE_LINES:
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
        global_commands.exit()
    else:
        global_commands.type_text(f"Invalid command '{command}', please try again.")
        run_event(event)

def level_up_player():
    narrator.level_up_options()
    command = input(">> ")
    print("")#newline after cmd prompt
    PLAYER.level_up(command)
    global_commands.type_text(f"Your {global_commands.TAG_TO_STAT[command]} increased by 1. You are now Level {PLAYER.level}")
    global_variables.SHOPKEEP.set_player_level(PLAYER.level)#make sure shopkeep's threat changes
    if PLAYER.can_level_up is True:
        level_up_player()
    else:
        narrator.continue_run(next_scene)

def link_start() -> None:

    if ENEMY is None:
        next_scene()
        return None

    global_variables.RUNNING = True
    enemy_commands.ENEMY = ENEMY
    player_commands.ENEMY = ENEMY

    #starting print statements
    begin_encounter()
    player_turn()

    while global_variables.RUNNING is True:

        command = input(">> ").lower()
        print("")

        #command interpretation
        if command == "exit":
            global_variables.RUNNING = False
            global_commands.exit()
        if command == "reset":
            player_commands.reset()
            sys.exit()
        try:
            command = int(command)
            try:
                item = list(PLAYER.inventory.values())[command - 1]
            except IndexError:
                item = None
            player_commands.use_an_item(item, ENEMY)
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
                player_death()
            case "p": #pass the turn
                enemy_turn()
            case "c": #cleans an effect
                player_commands.cleanse_an_effect()
            case "f": #attempt to flee
                global_variables.RUNNING = False
                player_commands.flee()
                enemy = None

def begin():
    print("")
    global ENEMY
    global_commands.type_text("Would you like to enter the dungeon? y/n\n")
    ENEMY = monster_manual.spawn_random_mob() if TEST is False else monster_manual.spawn_mob("Land Shark")

    if ENEMY is None:
        ENEMY = monster_manual.mobs[0]()

    command = input(">> ").lower()
    if command == "y":
        print("")#formatting
        global_variables.RUNNING = True
        link_start()
    elif command == "t":
        global_variables.restock_the_shop()
        global_variables.SHOPKEEP.print_inventory()
    elif command == "n":
        narrator.exit_the_dungeon()

player_commands.load()

#Set constants for command files
enemy_commands.NEXT_SCENE = next_scene
player_commands.NEXT_SCENE = next_scene

enemy_commands.PLAYER_TURN = player_turn
player_commands.PLAYER_TURN = player_turn

enemy_commands.ENEMY_TURN = enemy_turn
player_commands.ENEMY_TURN = enemy_turn

enemy_commands.PLAYER_DEATH = player_death
player_commands.PLAYER_DEATH = player_death

enemy_commands.END_SCENE = end_scene
player_commands.END_SCENE = end_scene

PLAYER.set_level_up_function(level_up_player)

while global_variables.START_CMD is True:
    global_variables.START_CMD = False
    begin()
