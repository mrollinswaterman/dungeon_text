#All globally required game objects (player, scene, shopkeep, etc) are intialized here

from typing import TYPE_CHECKING, Union, Any
if TYPE_CHECKING:
    import game_objects
    import controllers

COMMANDS:dict[str, Any] = {}

PLAYER:Union["game_objects.Player", None] = None

SCENE:Union["controllers.Scene", None] = None

SHOPKEEP:Union["game_objects.Shopkeep", None] = None

ARMORY:Union["game_objects.Armory", None] = None

START_CMD = True

RUNNING = False

def initialize():
    print(float('inf'))
    global PLAYER, SHOPKEEP, ARMORY, SCENE
    import items, globals, game_objects, controllers, mechanics

    PLAYER = game_objects.Player()

    SCENE = controllers.Scene()
    SCENE.player = PLAYER

    SHOPKEEP = game_objects.Shopkeep()

    ARMORY = game_objects.Armory()

    game_objects.forge_all_items()

    PLAYER.equip(ARMORY.get("Longsword"), True)
    PLAYER.equip(ARMORY.get("Padded Leather"), True)
    PLAYER.gain_gold(10000)

    #hp_pots:"items.Stackable" = item_compendium.Health_Potion(max(1, PLAYER.level // 4))
    #hp_pots.set_quantity(5)
    #PLAYER.pick_up(hp_pots, True)

    create_commands_dict()

    #PLAYER.weapon.enchant("Molten")

    return True

def start():
    import tui
    global START_CMD
    START_CMD = True
    tui.begin()

def stop():
    global START_CMD
    START_CMD = False

def create_commands_dict():
    global COMMANDS
    import controllers.player_turn as player_turn
    import tui
    import narrator
    COMMANDS = {
        "tui": {
            "y": tui.etd,
            "n": tui.ltd,
            "test": tui.test,
            "t":tui.test,
            "i":PLAYER.print_inventory,
        },

        "stats": {
            "str": None,
            "dex": None,
            "con": None,
            "int": None,
            "wis": None,
            "cha": None
        },

        "actions": {
            "a": PLAYER.attack,
            "ct": player_turn.combat_tricks,
            "e": player_turn.cleanse_a_condition,
            "i": player_turn.show_inventory,
            "w": PLAYER.spend_ap,
            "r": player_turn.flee
        },

        "combat_tricks": {
            "p": PLAYER.power_attack,
            "f":PLAYER.feint,
            "ri":PLAYER.riposte,
            "t":PLAYER.total_defense,
            "all":PLAYER.all_out,
            "s":PLAYER.study_weakness,
        },

        "overworld_menu": {
            "e": start,
            "r": narrator.rest,
            "v": narrator.shopkeep_options,
            "i": narrator.show_inventory
        },

        "shopkeep_options": {
            "p":narrator.buy_something,
            "l":narrator.leave_the_shop,
            "s": None,
            "i": narrator.show_inventory,
        },

        "cleanse_an_effect": {
        },

        "item_select": {
        },

        "_": {
        },
    }

    for entry in COMMANDS:
        COMMANDS[entry]["exit"] = exit
        COMMANDS[entry]["reset"] = player_turn.reset
        COMMANDS[entry]["c"] = player_turn.cancel
        COMMANDS[entry]["b"] = narrator.back
