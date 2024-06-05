import random
import global_variables
import mob
import monsters

LEVELCAP = 7

def spawn_mob(name:str):
    for entry in monsters.mobs:
        mob_object: mob.Mob = entry()
        if mob_object.id == name:
            return mob_object
    raise ValueError(f"No mob by id '{name}'.")

def spawn_random_mob():
    """
    Spawns a random mob.

    If the given level is not within the mob's level range, it picks a different random mob
    """
    if global_variables.PLAYER.level >= LEVELCAP:
        raise ValueError("Player level too high!")

    enemy:mob.Mob = random.choice(monsters.mobs)()

    if global_variables.PLAYER.level in range(enemy.range[0],enemy.range[1]):
        return enemy
    else:
        return spawn_random_mob()
    #might be a more efficient way to do all this, but it's fine for now