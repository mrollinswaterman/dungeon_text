# Text-Dungeon To-Do List

This file contains a list of tasks and ideas

## External

- [ ] Add a start menu where the user can choose a name for their character and maybe choose starting stats as well?? (give them 8 points, all stats start at 10, some sort of diminishing returns on pumping stats?)
- [ ] Use ~~Tkinter~~ HTML/JS/CSS or some GUI framework to take the game off the Command Line
- [ ] Implement a unit testing suite


## GUI

- [ ] Have the backdrop start off grayish instead of black, and each time the player choose to
continue deeper into the dungeon, the backdrop gets a little darker (1%???)
- [ ] Have a sky/midnight blue backdrop for when the player enters the overworld, chooses randomly
between day and night?
- [ ] Have ">>" between levels during level up screen blink
- [ ] Fix the bug that breaks the control flow of the GUI if you try to type something that's
identical to something that's still on the screen (hint: line 2 of the type function!!)


## Internal Logic

- [ ] Magic system
- [ ] Achievements
- [ ] Legendary / unique weapons
- [ ] Shopkeep “mood” meter → different narration lines depending on how much he likes you (impacted by how much you buy+sell, and charisma) 
- [ ] Templates → demonic, hellish, angelic, divine → templates that can be applied to mobs that give them stat bonus + special abilities?
- [ ] ~~Player special moves (power attack, feint, etc)~~ now WIP
- [ ] Add a companion, Gears the friendly Clockwork Hound. If you have a Clockwork Heart and some scrap, you have a chance to encounter him, can repair him with an int check, he joins you. Increases loot chances???
- [ ] Maybe make a stance class (riposte, total defense, defensive, offensive, all-out, etc) each with different effects.
- [ ] Figure out how to implment advantage and disadvantage
- [ ] Make Inventory its own class

## Mechanics

- [ ] Max level?
- [ ] Player death / respawning
- [ ] Minibosses / unique enemies
- [ ] Making durability actually matter
- [ ] Mob drops that can be sold at the shop
- [ ] Fail to flee scenario → %chance the enemy tries to stop you, if you get caught, you have to keep fighting, else lose some gold + small %chance you lose an item (value cap on how much gold you can lose total including item values)
- [ ] Failing events gives some drawback (ie take a little bit of damage, lose some gold, etc), BUT can withdraw at any time
- [ ] Add a "talk" mechanic with the Shopkeep to give player hints about how to unlock legendary weapons
(ie, "The Shopkeep says the Blacksmith might be able to craft something special with enough Land Shark teeth)
- [ ] Add a menu if the player hits "n" initally that lets them enter the overworld, save, or quit the game.
- [ ] Add a 1/round "Reaction" ability to all objects, can act on the opponents turn to do something (i.e add +5 to Evasion at the cost of -5 on all attack checks on your next turn, interurrpt a spell cast, chase a fleeing enemy, etc) 
- [ ] Add the ability to "loot" an enemy, taking the items in their inventory.
- [X] Offer player half the counter's loot for letting an enemy go, else there's no reason to do so
- [ ] Add specific narration options for Player's weapon type (i.e. "You slash forwards with your ______" for a Slashing weapon)

## Items

- [ ] Firebomb → does a set amount of damage, target can dex save for half, if they beat by more than 10, save for full. Chance to set on fire if they don't save for full
- [ ] Distilled Rage -> self-buff, induces enraged condition for 3(?) rounds when used
- [ ] Add "Scroll" type items that can be used to cast spells. Every 3-5 uses (maybe Int dependent) can roll an int check to "learn" the spell, permanently adding it to your spellbook. Scrolls have a use cap (6-10, Int dependent as well??) and can't be repaired. 

## Unique Items

- [ ] Clockwork Maul --> A great hammer crafted from clockwork scrap. Always loses durability on-hit.
Special move, uses half max durability for a double damage on the attack (can miss, takes 1/4 durability instead of 1/2). passively regens some durability per turn 
- [ ] Sharkbone Greatsword --> greatsword made from Land Shark teeth and bone. Serrated edge, causes bleed, DoT on hit. some form of blood related buff, either a +1 to damage per kill until you leave the dungeon (capped at your level) or does bonus damage to enemies below HP thresholds (ie +2 to below 50%, +3 to below 30%, etc)
- [ ] Helm of the Radiant Lord --> legendary medium armor item, any attacks against you have a chance to smite the attacker in retaliation dealing 1d6+cha damage to them (maybe this chance builds up each time you are hit and it doesn't proc??)
- [ ] Volcanic Breastplate --> legendary heavy breastplate forged in an erupting volcano, every enemy in combat with you takes 2+con damage on each of your(their??) turns, with a chance to be set on fire.
- [ ] Spectre's Cowl --> legendary light armor, every non-magical attack against you has a chance to miss, any attack that would kill you misses automatically, but this item loses 1/2(or 1/3) durability, any attack that would break this item misses, but the item still breaks
- [ ] Ghostcrawler's Cape --> legendary light armor, once per encounter can try and force an enemy to flee, if successful gain 1/2 gold and XP from encounter. enemies can't stop your flee attempts, unless this item is below 1/3 durability or you are below 25% HP. 
- [ ] Cloak of the Stormcaller --> legendary light armor, every time an enemy attacks you, they are reactively struck by 2d6 lightning damage 

## Mobs

- [ ] Cave spider that shoots webbing at you, can dodge with a dex check. If you get hit, either -1 AP, or no AP for next turn(s). Either way, can roll str on your turn to end all effects
- [ ] “Evil eye”, giant floating eye that shoots magic lasers at you, either executes at low HP or does execute damage (ie more damage based on missing HP)
- [ ] Lesser angel → winged fighters that attack you with flaming swords → chance to be set on fire on hit → burn damage per turn, can put it out on your turn with 1 AP. 
- [ ] Greater angel → same as above but can mitigate / heal damage
- [ ] Mimic: takes the form of a random enemy, copies stats and abilities(subject to change), 5% chance you fight a clone of yourself. changes form when below 50% HP to something stronger, and again at 25% HP.
- [ ] Gorgon: have to fight with your eyes closed (ie blind), 50% miss chance on all attacks before attack is even rolled. Can choose to look into its eyes, no more miss chance, but massive dex penalty 
- [ ] Decaying clockwork golem: Heals for half its max hp every round, but its max hp “decays” by a certain amount each round as well.
- [ ] Armordillo: deals ⅓ (or ½ or just some flat amount) of any damage taken back to the player. Can “curl up” defensively to halve all damage he takes during the next turn (does this frequently, never chases after the player just wants to be left alone. Give him a really good drop???)
- [ ] Flaming Skull --> chance to catch fire on attack, regens to full when killed, but max_hp decays each resurrection, to a minimum of 5-10. Dies for good if you one-shot it (from full??), ie do its max hp in one attack.
- [ ] Wraith / Ice Wraith --> Ghost that drains with each basic attack, ganing overheal as temp HP. if no Ghost Touch on weapon / armor 50-75% miss chance before attack roll.
- [ ] Hellhound --> Fiery doggo that breathes flames at you for 6d6 damage, dex save for half (recharge mechanic here???)

## Enchantments

- [ ] Flaming: chance to set target on fire on hit
- [ ] Molten/Searing/Super fucking hot: target takes a small amount of damage regardless of if the attack hits, plus a small chance to be set on fire. If the attack hits, target is set on fire, still take small unavoidable damage
- [ ] AP: ignores armor
- [ ] Freezing: reduces Action Points by 1 for 2 turns on hit
- [ ] Poisoned: applies poison on-hit
- [ ] Draining: heals attacker for some % of pre-mitigation damage done on-hit
- [ ] Serrated: applies Bleed on-hit

## Spells:

- [ ] Diamond Body: reduce all incoming (physical only?) damage by 1/3 for X rounds.
- [ ] Immunity: make yourself unable to take on any new status effects, good or bad, for X rounds
- [ ] Poison Arrow: apply poison to a single target
- [ ] Noxious Cloud: creates a cloud lasting for X rounds that applies poison to all combatants (stacks with each round you stay in it)
- [ ] Burning Vengeance: deals damage to an enemy equal to 1/2 damage recently taken, up to X rounds max
- [ ] Reversal: switch all status effects with an enemy
- [ ] Repair: repair an item
- [ ] Vampiric Touch: next attack against an enemy drains them for 33% of attack's damage.
- [ ] Bitter end: if target is below 25% HP and fails a con check, freeze them from the inside out, executing them
- [ ] Acid Rain: reduces targets armor by X for Y rounds. targets with 0 armor become Vulnerable instead

## Events

- [ ] Gnomish miner
- [ ] Talking wall
- [ ] Sphinx??

## Balance

- [ ] Can only use 1 combat trick per round???

## Combat Tricks

- [ ] Power Attack(1AP): no dex bonus to attack roll, but roll damage twice (take highest) and add x1.5 str to attack
- [ ] Feint(1AP): If you beat the enemy in a Cha check, they don't get their dex bonus to AC until your next turn
- [ ] Riposte(2AP): Gain +2 to base-evasion, if enemy misses next att by (your dex bonus - 5) or more, deal 1/2 of the attack's potential damage back to them instead. ends at the end of the enemy's turn regardless of outcome.
- [ ] Total Defense(All AP): add 5+(level//5) to base-evasion for enemy's next turn, but on your next turn, no dex bonus to attacks (potenitally more penalties like roll twice and take lowest on attacks)
- [ ] All-out(All AP): no dex bonus to evasion (and enemies get to roll twice take highest vs you??) for next turn, but attack rolls now add str+dex or dex+dex, whichever is highest
- [ ] Study Weakness(1AP): Spend some time studying the enemy for potential weakspots. Next attack has +2 crit range (ie 20-->18, 18-->16, etc)(does stack)
- [ ] Flurry(All AP): Make (level//4) extra attacks at a -1 to-hit per attack (ie first attack is -1, second attack is -2. etc)

## Bugs / QoL

- [ ] Add specific text for when a mob damages itself on a crit fail
- [ ] Add a parameter that tells conditions and effects to not print their "end()" text when the game is saving.
Alternatively, just prevent the game from printing anything at all while it's saving (maybe make type_text() function always return None??)
- [ ] There is an extra "|" character after all menu options that shouldn't be there
- [ ] Find a prettier way to handle not passing a roll check to the mob's narration function (line 320 in game_object)
- [ ] Make Shopkeep successful sale message print before player spend_gold() message print (maybe add a silent gold check, then print successful sale, then print spent gold?)



