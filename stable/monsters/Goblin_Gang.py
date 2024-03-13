#Goblin Gang mob file
import random
import mob, player, global_commands

stats = mob.Statblock("Goblin Gang")

stats.set_hp(6)
stats.set_damage(5)
stats.set_evasion(7)
stats.set_armor(0)
stats.set_gold(30)
stats.set_xp(10)
stats.set_min_max((2, 6))

def special():
    """
    Goblin gang special tbd
    
    maybe the gang scatters, rasing evasion but lowering damage??
    """
    pass

#stats.set_special(special)