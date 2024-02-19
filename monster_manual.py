import mob
import player
import commands
import random


GOBLIN_STATS = mob.Statblock("Goblin")

GOBLIN_STATS.set_hp(5)
GOBLIN_STATS.set_damage(4)
GOBLIN_STATS.set_evasion(10)
GOBLIN_STATS.set_armor(0)
GOBLIN_STATS.set_loot((15, 10))

def steal(source: mob.Mob, target: player.Player) -> bool:
    """
    Steals a random amount of gold from the player if they fail a dex check
    """
    commands.type_text(f"The {source.id} makes a grab at your gold pouch.\n")
    if target.roll_a_check("dex") >= source.roll_attack():
        commands.type_text(f"It missed.")
        return False
    
    else:
        prospective = random.randrange(1,20)
        actual = target.lose_gold(prospective)
        commands.type_text(f"The {source.id} stole {actual} gold from you!\n")
        return True

GOBLIN = mob.Mob(1, GOBLIN_STATS)
GOBLIN.add_special_move(steal)

HOBGOBLIN_STATS = mob.Statblock("Hobgoblin")

HOBGOBLIN_STATS.set_hp(6)
HOBGOBLIN_STATS.set_damage(5)
HOBGOBLIN_STATS.set_evasion(9)
HOBGOBLIN_STATS.set_armor(1)
HOBGOBLIN_STATS.set_loot((10, 10))
HOBGOBLIN_STATS.set_dc(14)

def taunt(source: mob.Mob, target: player.Player) -> bool:
    commands.type_text(f"The {source.id} hurls enraging insults at you.\n")

    if target.roll_a_check("cha") >= source.dc:
        commands.type_text(f"Your mind is an impenetrable fortess. The {source.id}'s words have no effect.\n")

    else:
        commands.type_text(f"The {source.id}'s insults distract you, making you an easier target.\n")
        target.debuff("evasion", 2)

HOBGOBLIN = mob.Mob(1, HOBGOBLIN_STATS)
HOBGOBLIN.add_special_move(taunt)

#BANDIT = mob.Statblock("Bandit")

"""BANDIT.set_hp(8)
BANDIT.set_damage(5)
BANDIT.set_evasion(10)
BANDIT.set_armor(2)
BANDIT.set_loot((25, 10))

GOBLIN_GANG = mob.Statblock("Goblin Gang")

GOBLIN_GANG.set_hp(6)
GOBLIN_GANG.set_damage(4)
GOBLIN_GANG.set_evasion(7)
GOBLIN_GANG.set_armor(0)
GOBLIN_GANG.set_loot((30, 10))"""