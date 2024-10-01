import global_variables, global_commands
import player_commands, tui, narrator

commands = {
    "tui": {
        "y": tui.etd,
        "n": tui.ltd,
        "test": tui.test,
        "t":tui.test,
        "i":global_variables.PLAYER.print_inventory,
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
        "e": player_commands.cleanse_a_condition,
        "i": player_commands.show_inventory,
        "w": global_variables.PLAYER.spend_ap,
        "r": player_commands.flee
    },

    "combat_tricks": {
        "p": global_variables.PLAYER.power_attack,
        "f":global_variables.PLAYER.feint,
        "ri":global_variables.PLAYER.riposte,
        "t":global_variables.PLAYER.total_defense,
        "all":global_variables.PLAYER.all_out,
        "s":global_variables.PLAYER.study_weakness,
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

for entry in commands:
    commands[entry]["exit"] = global_commands.exit
    commands[entry]["reset"] = player_commands.reset
    commands[entry]["c"] = player_commands.cancel
    commands[entry]["b"] = narrator.back
