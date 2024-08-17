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
    Spawns a random mob.

    If the given level is not within the mob's level range, it picks a different random mob
    """
    if global_variables.PLAYER.level >= LEVELCAP:
        raise ValueError("Player level too high!")

    enemy:mob.Mob = random.choice(list(monsters.dict.values()))()

    if global_variables.PLAYER.level in range(enemy.range[0],enemy.range[1]):
        return enemy
    else:
        return spawn_random_mob()
    #might be a more efficient way to do all this, but it's fine for now