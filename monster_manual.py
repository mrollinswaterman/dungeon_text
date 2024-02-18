import mob


GOBLIN = mob.Statblock("Goblin")

GOBLIN.set_hp(5)
GOBLIN.set_damage(4)
GOBLIN.set_evasion(10)
GOBLIN.set_armor(0)
GOBLIN.set_loot((15, 10))

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