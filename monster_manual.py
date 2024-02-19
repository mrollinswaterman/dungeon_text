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
    commands.type_text(f"The {source.id} makes a grab at your gold pouch.")
    if target.roll_a_check("dex") >= source.roll_attack():
        commands.type_text(f"It missed.")
        return False
    
    else:
        robbed = random.randrange(1,20)
        source.add_gold(robbed)
        commands.type_text(f"The {source.id} stole {robbed} gold from you!")
        target.lose_gold(robbed)
        return True

GOBLIN = mob.Mob(1, GOBLIN_STATS)
GOBLIN.add_special_move(steal)


HOBGOBLIN = mob.Statblock("Hobgoblin")

HOBGOBLIN.set_hp(6)
HOBGOBLIN.set_damage(5)
HOBGOBLIN.set_evasion(9)
HOBGOBLIN.set_armor(1)
HOBGOBLIN.set_loot((10, 10))

BANDIT = mob.Statblock("Bandit")

BANDIT.set_hp(8)
BANDIT.set_damage(5)
BANDIT.set_evasion(10)
BANDIT.set_armor(2)
BANDIT.set_loot((25, 10))

GOBLIN_GANG = mob.Statblock("Goblin Gang")

GOBLIN_GANG.set_hp(6)
GOBLIN_GANG.set_damage(4)
GOBLIN_GANG.set_evasion(7)
GOBLIN_GANG.set_armor(0)
GOBLIN_GANG.set_loot((30, 10))