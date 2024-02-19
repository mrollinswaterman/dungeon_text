import sys
import random
import player, items, mob
import monster_manual
import narrator
import commands
import item_compendium
import dms_guide
import events
import time

MOBS = {
    "Goblin": monster_manual.GOBLIN,

    "Hobgoblin": monster_manual.HOBGOBLIN,
}

#    "Bandit": monster_manual.BANDIT,

  #  "Goblin Gang": monster_manual.GOBLIN_GANG

PLAYER = player.Player()

iron_sword = items.Weapon("Iron Sword", 1)
iron_sword.set_damage_dice(1,8)
iron_sword.set_crit_multiplier(2)

leather_armor = items.Armor("Leather Armor", 1)
leather_armor.set_armor_value(2)

PLAYER.equip_armor(leather_armor)
PLAYER.equip_weapon(iron_sword)

PLAYER.pick_up(item_compendium.Health_Potion("Health Potion", 1), 5)

commands.type_text("\nWould you like to enter the Dungeon? y/n\n", 0.03)

STARTING_ENEMY: mob.Mob = monster_manual.GOBLIN#random.choice(list(MOBS.values()))
STARTING_ENEMY.set_level(1)

def link_start(enemy:mob.Mob) -> None:
    RUNNING = True

    #functions
    def player_turn():
        """
        Begins the Player turn
        """
        narrator.player_turn_options()
    
    def player_death():
        #some text probably too
        RUNNING = False
        sys.exit()

    def enemy_turn():
        """
        Begins the enemy turn
        """
        print("-" * 110+"\n")

        enemy.special_move(enemy, PLAYER)
       

    def next_scene():
        """
        Starts a new scene with a new enemy
        """
        narrator.next_scene_options()
        if random.randrange(1, 5) > 1:
            next_enemy: mob.Mob = random.choice(list(MOBS.values()))
            next_enemy.set_level(random.randrange(PLAYER.threat[0], PLAYER.threat[1]))
            RUNNING = False
            link_start(next_enemy)
        else:
            next_event: events.Event = random.choice(dms_guide.EVENT_LIST)
            next_event.add_tries(2)
            print(next_event.text)
            run_event(next_event)

    def begin_encounter():
        """
        Begins an encounter
        """

        commands.type_text(f'\nYou encounter a Level {enemy.level} {enemy.id}!\n')

    def level_up_player():
        narrator.level_up_options()
        command = input(">")
        PLAYER.spend_xp(command)

        commands.type_text(f'\nYour {command} increased by 2. You are now Level {PLAYER.level}\n')
        narrator.continue_run(next_scene)

    def run_event(event: events.Event):
        narrator.event_options()
        command = input(">")
        if command.lower() != "w":
            print('\n'+"-" * 110)
    
            commands.type_text(event.run(command, PLAYER.roll_a_check(command)))
            print("-" * 110+'\n')
            if event.passed is True:
                event.add_tries(2)
                next_scene()
            elif event.tries is True:
                run_event(event)
            else: 
                commands.type_text(event.end_message)
                next_scene()

    def end_scene():
        PLAYER.gain_gold(enemy.loot[0])
        PLAYER.gain_xp(enemy.loot[1])

        commands.type_text(f"You killed the {enemy.id}!\n")
        print("-"*110+'\n')
        if PLAYER.level_up is True:
            level_up_player()
        else:
            narrator.continue_run(next_scene)

    #starting print statements
    begin_encounter()
    player_turn()

    while RUNNING:

        command = input(">")

        #command interpretation
        if command.lower() == "exit":
            RUNNING = False
            sys.exit()
        if command.lower() == "a":
            commands.attack(PLAYER, enemy, enemy_turn, end_scene)
        if command.lower() == "hp":
            commands.hp(PLAYER, player_turn)
        if command.lower() == "i":
            commands.inventory(PLAYER, player_turn)
        if command.lower() == "u":
            commands.use_an_item(PLAYER, "Health Potion", PLAYER, enemy_turn, player_turn)
            
        
if input(">").lower() == "y":
    link_start(STARTING_ENEMY)