#Bandit mob file
import random
import mob, player, global_commands

stats = mob.Statblock("Bandit")

stats.set_hp(8)
stats.set_damage(6)
stats.set_evasion(10)
stats.set_armor(2)
stats.set_gold(25)
stats.set_xp(10)
stats.set_min_max((1, 7))

def special():
    """
    bandit special tbd
    """
    pass

#stats.set_special(special)