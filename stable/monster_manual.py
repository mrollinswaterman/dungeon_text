import random
import global_variables
import mob
import monsters

LEVELCAP = 7

def spawn_mob(name:str):
    try:
        return monsters.dict[name]()
    except KeyError:
        raise ValueError(f"No mob by id '{name}'.")

def spawn_random_mob():
    """
    Spawns a random mob, appropriate for the player's level
    """
    if global_variables.PLAYER.level >= LEVELCAP:
        raise ValueError("Player level too high!")

    enemy:mob.Mob = random.choice(list(monsters.dict.values()))()

    lower_bound = max(global_variables.PLAYER.level - 2, 1)
    upper_bound = min(global_variables.PLAYER.level + 5, 20)

    base_level = enemy.stats.level_range[0]
    max_level = enemy.stats.level_range[1]

    if max_level > upper_bound or base_level < lower_bound:
        return spawn_random_mob()
    else: return enemy

