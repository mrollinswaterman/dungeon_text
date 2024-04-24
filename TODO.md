External stuff:
    [X]Player save file

Internal Logic:
    []Magic system???
    []Achievements??
    []Legendary / unique weapons
    []Shopkeep “mood” meter → different narration lines depending on how much he likes you (impacted by how much you buy+sell, and charisma) 
    []Templates → demonic, hellish, angelic, divine → templates that can be applied to mobs that give them stat bonus + special abilities?
    [X]Fix status effects
    [X]Multiple special moves,  each with different triggers
    []Player special moves (power attack, feint, etc)
    [X]Add mob specific attack narration (ie the ___ swings it’s dagger at you, the dragon breathes a gout of flame []in your direction, etc)
    []Give status effect their own file like item compendium where each individual effect is made its own subclass of status effect

Mechanics:
    []Some kind of reward for stat check events
    [X]Shopkeep/exiting the dungeon in general
    []Damage types??
    []Max level?
    []Player death / respawning
    []Minibosses / unique enemies
    []Making durability actually matter
    [X]Weight class for armors → heavier == more armor, but less evasion + dex checks
    [X]Add message when buffed / debuffed + message when status effects end
    []Mob drops that can be sold at the shop
    [X]Fail to flee scenario → %chance the enemy tries to stop you, if you get caught, you have to keep fighting, else lose some gold + small %chance you lose an item (value cap on how much gold you can lose total including item values)
    [X]Add flee action to mobs → works the same as the players?
    []Failing events gives some drawback (ie take a little bit of damage, lose some gold, etc), BUT can withdraw at any time
    []Add a view equipped items menu to menu_options()



Item Ideas:
    [X]Firebomb → does a set amount of damage, target can dex save for half, if they beat by more than 10, save for full. Chance to set on fire if they don't save by for full

Enemy designs:
    []Clockwork hound that eats your equipped gear → takes some amount of durability off it, and heals itself for that amount
    []Cave spider that shoots webbing at you, can dodge with a dex check. If you get hit, either -1 AP, or no AP for next turn(s). Either way, can roll str on your turn to end all effects
    []“Evil eye”, giant floating eye that shoots magic lasers at you, either executes at low HP or does execute damage (ie more damage based on missing HP)
    []Lesser angel → winged fighters that attack you with flaming swords → chance to be set on fire on hit → burn damage per turn, can put it out on your turn with 1 AP. 
    []Greater angel → same as above but can mitigate / heal damage
    [X]Land shark → can burrow underground to either increase its armor or its evasion (i haven't decided yet)
    []Mimic: takes the form of a random enemy (or the last enemy you fought), copies only stats not abilities (subject to change), 5% chance you fight a clone of yourself. 
    []Gorgon: have to fight with your eyes closed (ie blind), 50% miss chance on all attacks before attack is even rolled. Can choose to look into its eyes, no more miss chance, but massive dex penalty 
    []Decaying clockwork golem: Heals for half its max hp every round, but its max hp “decays” by a certain amount each round as well.
    []Armordillo: deals ⅓ (or ½ or just some flat amount) of any damage taken back to the player. Can “curl up” defensively to halve all damage he takes during the next turn (does this frequently, never chases after the player just wants to be left alone. Give him a really good drop???)


Event Ideas:
    []Gnomish miner
    []Talking wall
    []Mysterious cypher
    []Sphinx??
    []Gas cloud → constitution check finally!
    []Elaborate trap room → int/dex

Balance:
    [X] HP potions should restore double their power in health (ie 4 instead of 2)