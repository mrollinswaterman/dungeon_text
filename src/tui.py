import global_variables, global_commands
import monster_manual
import player_commands
import narrator
import controller

def link_start() -> None:
    controller.begin_encounter()
    global_variables.RUNNING = True
    player_commands.turn()

def etd():
    """
    Short for "Enter the Dungeon", runs when the player hits
    "y" initially
    """
    player_commands.load()
    global_variables.PLAYER.gain_gold(300)
    global_variables.RUNNING = True
    link_start()

def test():
    player_commands.load()
    global_variables.PLAYER.print_inventory()

def ltd():
    """
    Short for "Leave the Dungeon", runs when
    the player hits "n" initally.
    """
    player_commands.load()
    narrator.exit_the_dungeon()
def begin():
    from command_dict import all

    tui = all["tui"]

    global_commands.type_text("Would you like to enter the dungeon? y/n")

    if not controller.TEST:
        controller.SCENE.enemy = monster_manual.spawn_random_mob()  
    else:
        controller.SCENE.enemy = monster_manual.spawn_mob("Bandit")

    done = False
    while not done:
        cmd = global_commands.get_cmd()

        if cmd in tui:
            done = True
            tui[cmd]()
        else:
            global_commands.type_text(f"Invalid command '{cmd}'. Please try again.", 0.01)


while global_variables.START_CMD is True:
    global_variables.START_CMD = False
    print("")
    begin()
