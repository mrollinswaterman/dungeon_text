import global_variables, global_commands
import player_commands, tui, narrator

all = {
    "tui": {
        "y": tui.etd,
        "n": tui.ltd,
        "test": tui.test
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
        "a": global_variables.PLAYER.attack,
        "ct": player_commands.combat_tricks,
        "e": player_commands.cleanse_an_effect,
        "i": player_commands.show_inventory,
        "w": global_variables.PLAYER.spend_ap,
        "r": player_commands.flee
    },

    "combat_tricks": {
        "p": global_variables.PLAYER.power_attack,
    },

    "overworld_menu": {
        "e": global_variables.start,
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

for entry in all:
    all[entry]["exit"] = global_commands.exit
    all[entry]["reset"] = player_commands.reset
    all[entry]["c"] = player_commands.cancel
    all[entry]["b"] = narrator.back
