import global_variables, global_commands
import player_commands, tui

all = {
    "tui": {
        "y": tui.etd,
        "n": tui.ltd,
        "test": tui.test
    },

    "actions": {
        "a": global_variables.PLAYER.attack,
        "c": player_commands.combat_tricks,
        "e": player_commands.cleanse_an_effect,
        "i": player_commands.show_inventory,
        "w": global_variables.PLAYER.spend_ap,
        "r": player_commands.flee
    },

    "combat_tricks": {
        "p": global_variables.PLAYER.power_attack,
    },

    "cleanse_an_effect": {
    },

    "item_select": {
    }
}

for entry in all:
    all[entry]["exit"] = global_commands.exit
    all[entry]["reset"] = player_commands.reset
    all[entry]["b"] = player_commands.back
