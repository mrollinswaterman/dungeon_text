import mob


GOBLIN = mob.Statblock("Goblin")

GOBLIN.set_hp(5)
GOBLIN.set_damage(6)
GOBLIN.set_evasion(10)
GOBLIN.set_armor(0)
GOBLIN.set_loot((15, 5))

HOBGOBLIN = mob.Statblock("Hobgoblin")

HOBGOBLIN.set_hp(8)
HOBGOBLIN.set_damage(6)
HOBGOBLIN.set_evasion(9)
HOBGOBLIN.set_armor(1)
HOBGOBLIN.set_loot((10, 10))

BANDIT = mob.Statblock("Bandit")

BANDIT.set_hp(10)
BANDIT.set_damage(8)
BANDIT.set_evasion(10)
BANDIT.set_armor(2)
BANDIT.set_loot((25, 15))