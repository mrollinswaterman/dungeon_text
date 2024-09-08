import global_variables, global_commands
import monster_manual
import player_commands
import narrator
import controller

def etd():
    """
    Short for "Enter the Dungeon", runs when the player hits
    "y" initially
    """
    player_commands.load()
    global_variables.RUNNING = True
    controller.SCENE.begin_encounter()

def test():
    global_variables.SHOPKEEP.restock()
    global_variables.SHOPKEEP.print_inventory()

def ltd():
    """
    Short for "Leave the Dungeon", runs when
    the player hits "n" initally.
    """
    player_commands.load()
    narrator.exit_the_dungeon()

def begin():
    from command_dict import commands

    tui = commands["tui"]

    global_commands.type_text("would you like to enter the dungeon? y/n")

    done = False
    while not done:
        cmd = global_commands.get_cmd()

        if cmd in tui:
            done = True
            tui[cmd]()
        else:
            global_commands.error_message(cmd)

print("")
while global_variables.START_CMD is True:
    global_variables.START_CMD = False
    begin()
