import global_variables, global_commands
import monster_manual
import player_commands
import narrator
import scene_controller

def etd():
    """Short for "Enter the Dungeon", runs when the player hits "y" initially"""
    player_commands.load()
    global_variables.RUNNING = True
    scene_controller.SCENE.begin_encounter()

def test():
    global_variables.SHOPKEEP.restock()
    global_variables.SHOPKEEP.print_inventory()

def ltd():
    """Short for "Leave the Dungeon", runs when the player hits "n" initally."""
    player_commands.load()
    narrator.exit_the_dungeon()

print("")
while global_variables.START_CMD is True:
    global_variables.START_CMD = False
