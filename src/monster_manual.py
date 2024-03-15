import random
import mob
from monsters import Goblin, Hobgoblin, Bandit, Goblin_Gang

LEVELCAP = 7

mobs = [
    Goblin.stats, Hobgoblin.stats, Bandit.stats,
    Goblin_Gang.stats,
]

def spawn_mob(name:str):
    for entry in mobs:
        if entry.id == name:
            return mob.Mob(entry)

def spawn_random_mob(level):
    """
    Spawns a random mob.

    If the given level is not within the mob's level range, it picks a different random mob
    """
    if level >= LEVELCAP:
        raise ValueError("Player level too high!")

    mob_choice = mob.Mob(random.choice(mobs))

    if level not in range(mob_choice.level_range[0], mob_choice.level_range[1]):
        return spawn_random_mob(level)  
    
    return mob_choice
    #might be a more efficient way to do all this, but it's fine for now