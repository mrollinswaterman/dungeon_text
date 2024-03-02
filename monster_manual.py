import mob
import player
import global_commands
import random


#GOBLIN stuff
GOBLIN_STATS = mob.Statblock("Goblin")

GOBLIN_STATS.set_hp(5)
GOBLIN_STATS.set_damage(4)
GOBLIN_STATS.set_evasion(10)
GOBLIN_STATS.set_armor(0)
GOBLIN_STATS.set_loot((15, 10))
GOBLIN_STATS.set_min_max((1, 3))

def goblin_special(source: mob.Mob, target: player.Player) -> bool:
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

GOBLIN_STATS.set_special(goblin_special)


#HOBGOBLIN stuff
HOBGOBLIN_STATS = mob.Statblock("Hobgoblin")

HOBGOBLIN_STATS.set_hp(6)
HOBGOBLIN_STATS.set_damage(5)
HOBGOBLIN_STATS.set_evasion(9)
HOBGOBLIN_STATS.set_armor(1)
HOBGOBLIN_STATS.set_loot((10, 10))
HOBGOBLIN_STATS.set_dc(14)
HOBGOBLIN_STATS.set_min_max((1, 5))

def hobgoblin_special(source: mob.Mob, target: player.Player) -> bool:
    """
    Taunt: Reduces the player's evasion by 2 points for 2 turns if they fail a charisma check
    """
    global_commands.type_text(f"The {source.id} hurls enraging insults at you.\n")

    if target.roll_a_check("cha") >= source.dc:
        global_commands.type_text(f"Your mind is an impenetrable fortess. The {source.id}'s words have no effect.\n")

    else:
        global_commands.type_text(f"The {source.id}'s insults distract you, making you an easier target.\n")
        taunt = player.Status_Effect("Taunt", source, "evasion", target)
        taunt.set_duration(2)
        taunt.set_power(-2)
        target.add_status_effect(taunt)

HOBGOBLIN_STATS.set_special(hobgoblin_special)



#BANDIT stuff
BANDIT_STATS = mob.Statblock("Bandit")

BANDIT_STATS.set_hp(8)
BANDIT_STATS.set_damage(6)
BANDIT_STATS.set_evasion(10)
BANDIT_STATS.set_armor(2)
BANDIT_STATS.set_loot((25, 10))
BANDIT_STATS.set_min_max((1, 7))

def bandit_special():
    """
    bandit special tbd
    """
    pass

#BANDIT_STATS.set_special(bandit_special)

GOBLIN_GANG_STATS = mob.Statblock("Goblin Gang")

GOBLIN_GANG_STATS.set_hp(6)
GOBLIN_GANG_STATS.set_damage(5)
GOBLIN_GANG_STATS.set_evasion(7)
GOBLIN_GANG_STATS.set_armor(0)
GOBLIN_GANG_STATS.set_loot((30, 10))
GOBLIN_GANG_STATS.set_min_max((2, 6))

def goblin_gang_special():
    """
    Goblin gang special tbd
    
    maybe the gang scatters, rasing evasion but lowering damage??
    """
    pass

#GOBLIN_GANG_STATS.set_special(goblin_gang_special)


MOBS = {
    1: [GOBLIN_STATS, HOBGOBLIN_STATS, BANDIT_STATS],

    2: [GOBLIN_GANG_STATS]
}

def random_mob(level):
    return mob.Mob(1, random.choice(MOBS[level]))