import random

import globals
import game

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import game_objects
    import mechanics
    import items

def build_damage_type(input:str=None) -> "mechanics.DamageType":
    """
    Creates and returns a DamageType object based on an input string.
    Returns an empty type if input is None
    """
    import mechanics
    ret = mechanics.DamageType()
    if input is None: return ret 
    types = input.split("/")
    if types[0] != "Magic":
        final = ["Physical"] + types
        ret.set(final)
    else:
        ret.set(["Magic"] + types)

    return ret

def generate_item_rarity():
    import items
    """Generates item rarity based on player level"""

    if globals.probability(1+game.PLAYER.level):
        return items.Rarity("Legendary")
    
    if globals.probability(5+game.PLAYER.level):
        return items.Rarity("Epic")
    
    if globals.probability(10+game.PLAYER.level * 1.25):
        return items.Rarity("Rare")
    
    if globals.probability(25+game.PLAYER.level // 2):
        return items.Rarity("Uncommon")
    
    return items.Rarity("Common")

def create_status(name:str, source:"game_objects.Game_Object") -> "mechanics.Status":
    import compendiums.status_compendium as statuses

    return statuses.dict[name](source)

def create_enchantment(name:str, source:"game_objects.Game_Object | items.Item") -> "mechanics.Enchantment":
    import compendiums.enchantment_compendium as enchants

    if name in enchants.dict:
        return enchants.dict[name](source)
    return None

def create_item(source_dict={}):
    import items
    import compendiums.item_compendium as item_compendium

    cast = items.Anvil()
    cast.copy(source_dict)
    match cast.anvil_type:
        case "Weapon":
            return items.Weapon(cast)
        case "Armor":
            return items.Armor(cast)
        case _:
            pass

    if cast.anvil_type in item_compendium.dict:
        final:items.Stackable = item_compendium.dict[cast.anvil_type](cast.rarity)
    else: final = items.Stackable(cast)

    final.set_quantity(cast.quantity)
    return final

def spawn_mob(name:str) -> "game_objects.Mob":
    """
    Spawn a specific mob by name
    Returns a Mob Object
    """
    import compendiums.monster_manual as monster_manual
    try:
        return monster_manual.dict[name]()
    except KeyError:
        raise ValueError(f"No mob by id '{name}'.")

def spawn_random_mob() -> "game_objects.Mob":
    """
    Spawns a random mob, appropriate for the player's level
    """
    import compendiums.monster_manual as monster_manual
    if game.PLAYER.level >= globals.LEVELCAP:
        raise ValueError("Player level too high!")

    enemy:"game_objects.Mob" = random.choice(list(monster_manual.dict.values()))()

    lower_bound = max(game.PLAYER.level - 2, 1)
    upper_bound = min(game.PLAYER.level + 5, 20)

    base_level = enemy.stats.level_range[0]
    max_level = enemy.stats.level_range[1]

    if max_level > upper_bound or base_level < lower_bound:
        return spawn_random_mob()
    else: return enemy

def spawn_event(name:str):
    import compendiums.event_compendium as events
    print(events.dict)
    try:
        return events.dict[name]()
    except KeyError:
        raise ValueError(f"No event by id '{name}'.")

def spawn_random_event():
    import compendiums.event_compendium as events

    ev = random.choice(list(events.dict.values()))()

    if ev.id != "Trap_Room":
        return ev
    else:
        return spawn_random_event()
