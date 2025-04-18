#Filepaths
MOBS_FILEPATH = "csv_files/monster_stats.csv"
PLAYER_FILEPATH = "csv_files/player.csv"
INVENTORY_FILEPATH = "csv_files/inventory.csv"
EQUIPMENT_FILEPATH = "csv_files/equipment_stats.csv"
ITEMS_FILEPATH = "csv_files/item_stats.csv"

LEVELCAP = 7

BONUS = {
    5: -4,
    6: -3,
    7: -2,
    8: -1, 
    9: -1,
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5,
    21: 5,
    22: 6,
    23: 6,
    24: 7
}

DICE_PROGRESSION = [
    1,
    "1d2",
    "1d3",
    "1d4",
    "1d6",
    "1d8",
    "1d10",
    "2d6",
    "2d8",
    "3d6",
    "3d8",
    "4d6",
    "4d8",
    "6d6",
    "6d8",
    "8d6",
    "8d8",
    "12d6",
    "12d8",
    "16d6"
]

ABILITY_SCORES = {
    "str": "Strength",
    "dex": "Dexterity",
    "con": "Constitution",
    "int": "Intelligence",
    "wis": "Wisdom",
    "cha": "Charisma",
}

STATS = {
    "base_evasion": "Evasion",
    "damage_taken_multiplier": "Vulnerability",
    "damage_multiplier": "Damage",
    "armor": "Armor",
    "max_hp": "Maximum Health"
}

for score in ABILITY_SCORES:
    STATS[score] = ABILITY_SCORES[score]