import game
import controllers.player_turn as player_turn
import narrator

def etd():
    """Short for "Enter the Dungeon", runs when the player hits "y" initially"""
    player_turn.load()
    game.RUNNING = True
    game.SCENE.begin_encounter()

def test():
    game.SHOPKEEP.restock()
    game.SHOPKEEP.print_inventory()

def ltd():
    """Short for "Leave the Dungeon", runs when the player hits "n" initially."""
    player_turn.load()
    narrator.exit_the_dungeon()

def begin():
    import globals
    if game.initialize():
        tui = game.COMMANDS["tui"]

        globals.type_text("would you like to enter the dungeon? y/n")

        done = False
        while not done:
            cmd = globals.get_cmd()

            if cmd in tui:
                done = True
                tui[cmd]()
            else:
                globals.error_message(cmd)

print("")
while game.START_CMD is True:
    game.START_CMD = False
    begin()
