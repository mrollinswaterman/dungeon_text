import mob


GOBLIN = mob.Statblock("Goblin")

GOBLIN.set_hp(5)
GOBLIN.set_damage(3)
GOBLIN.set_evasion(10)
GOBLIN.set_armor(0)
GOBLIN.set_loot((15, 5))

HOBGOBLIN = mob.Statblock("Hobgoblin")

HOBGOBLIN.set_hp(8)
HOBGOBLIN.set_damage(4)
HOBGOBLIN.set_evasion(9)
HOBGOBLIN.set_armor(1)
HOBGOBLIN.set_loot((10, 5))

BANDIT = mob.Statblock("Bandit")

BANDIT.set_hp(10)
BANDIT.set_damage(6)
BANDIT.set_evasion(10)
BANDIT.set_armor(2)
BANDIT.set_loot((25, 5))

GANG_OF_GOBLINS = mob.Statblock("Gang of Goblins")

GANG_OF_GOBLINS.set_hp(13)
GANG_OF_GOBLINS.set_damage(4)
GANG_OF_GOBLINS.set_evasion(7)
GANG_OF_GOBLINS.set_armor(0)
GANG_OF_GOBLINS.set_loot((30, 5))