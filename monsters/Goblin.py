#Goblin mob file
import mob
import player
import global_commands
import random

stats = mob.Statblock("Goblin")

stats.set_hp(5)
stats.set_damage(4)
stats.set_evasion(10)
stats.set_armor(0)
stats.set_gold(15)
stats.set_xp(10)
stats.set_min_max((1, 3))

def special(source: mob.Mob, target: player.Player) -> bool:
    """
    Rob: Steals a random amount of gold from the player if they fail a dex check
    """
    global_commands.type_text(f"The {source.id} makes a grab at your gold pouch.\n")
    if target.roll_a_check("dex") >= source.roll_attack():
        global_commands.type_text(f"It missed.\n")
        return False
    
    else:
        prospective = random.randrange(1,20)
        actual = target.lose_gold(prospective)
        global_commands.type_text(f"The {source.id} stole {actual} gold from you!\n")
        return True

stats.set_special(special)