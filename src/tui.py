import global_variables, global_commands
import monster_manual
import player_commands
import narrator
import controller

def link_start() -> None:
    controller.begin_encounter()
    global_variables.RUNNING = True
    player_commands.start_turn()

def begin():

    global_commands.type_text("Would you like to enter the dungeon? y/n")

    if not controller.TEST:
        controller.SCENE.enemy = monster_manual.spawn_random_mob()  
    else:
        controller.SCENE.enemy = monster_manual.spawn_mob("Evil Eye")

    command = input(">> ").lower()
    print("")
    match command:
        case "exit":
            player_commands.load()
            global_commands.exit()
        case "y":
            player_commands.load()
            global_variables.PLAYER.gain_gold(300)
            global_variables.RUNNING = True
            link_start()
        case "test":
            player_commands.load()
            global_variables.PLAYER.print_inventory()
        case "n":
            player_commands.load()
            narrator.exit_the_dungeon()
        case _:#run the game by default
            player_commands.load()
            global_variables.RUNNING = True
            link_start()

while global_variables.START_CMD is True:
    global_variables.START_CMD = False
    print("")
    begin()
