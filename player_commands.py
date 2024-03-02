import random
import global_commands
import global_variables
import mob
import items
import narrator

GOD_MODE = False

def player_turn_options():
    print(f'What would you like to do? Action Points: {global_variables.PLAYER.ap}/{global_variables.PLAYER.max_ap}\n\nAttack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i) | Use a Health Potion - (u)\n')


def attack(enemy: mob.Mob, enemy_turn, end_scene) -> None:
    """
    Attacks an enemy. 

    player: a Player object, the attacker
    enemy: a Mob object, the target

    enemy_turn: a function to run if the enemy is not dead after the
    player's attack

    end_scene: function to run if the player kills the enemy

    Returns nothing
    """
    if GOD_MODE is True:
        attack_roll = 1000000
    else:
        attack_roll = global_variables.PLAYER.roll_attack()
        global_variables.PLAYER.spend_ap(1)
    
    print('\n'+"-" * 110)
    global_commands.type_text(f'\nYou attack the {enemy.id}, rolling a {attack_roll}.\n')

    if attack_roll == 0:
        global_commands.type_text(f"Critical Hit!\n")
        taken = enemy.take_damage(global_variables.PLAYER.roll_damage() * global_variables.PLAYER.weapon.crit)

    if attack_roll == 1:
        global_commands.type_text(f"Crtical Fail!\n")

    if attack_roll >= enemy.evasion:
        if GOD_MODE is True:
            taken = enemy.take_damage(1000)
        else:
            taken = enemy.take_damage(global_variables.PLAYER.roll_damage())
        
        global_commands.type_text(f'You hit the {enemy.id} for {taken} damage.\n')
        if enemy.dead is False and global_variables.PLAYER.can_act is False:
            global_variables.PLAYER.reset_ap()
            enemy_turn()
        elif enemy.dead is True:
            end_scene()
        else:
            player_turn_options()

    elif attack_roll < enemy.evasion:
        global_commands.type_text(f"You missed.\n")
        if global_variables.PLAYER.can_act is False:
            global_variables.PLAYER.reset_ap()
            enemy_turn()
        else: 
            player_turn_options()

def hp(player_turn) -> None:
    """
    Prints the player's HP then runs the given function
    """
    print('\n'+"-" * 110)
    print(f'\nHP: {global_variables.PLAYER.hp}/{global_variables.PLAYER.max_hp}')
    print("["+"/"*global_variables.PLAYER.hp+" "*(global_variables.PLAYER.max_hp-global_variables.PLAYER.hp)+"]")
    print('\n'+"-" * 110+'\n')
    player_turn()

def inventory(player_turn) -> None:
    """
    Prints the player's inventory then runs the given function
    """
    print('\n'+"-" * 110)
    print(f'\nGold: {global_variables.PLAYER.gold}\n')
    global_variables.PLAYER.print_inventory()
    print("\n"+"-" * 110+'\n')
    player_turn()

def use_an_item(item: items.Consumable, enemy_turn, player_turn) -> None:
    """
    Uses an item on the Player, if the player has the item in their inventory
    """
    print('\n'+"-" * 110)
    if global_variables.PLAYER.has_item(item) is not False and global_variables.PLAYER.has_item(item).quantity > 0:
        if global_variables.PLAYER.has_item(item).use(global_variables.PLAYER) is True:
            global_commands.type_text(f'\n{global_variables.PLAYER.has_item(item).quantity} {item}(s) remaining.\n')
            global_variables.PLAYER.spend_ap(1)
            if global_variables.PLAYER.can_act is False:
                global_variables.PLAYER.reset_ap()
                enemy_turn()
            else:
                player_turn()
        else:
            global_commands.type_text(f'\nAlready full HP.\n')
            player_turn()
    else:
        global_commands.type_text(f'\nNo {item}(s) avaliable!\n')
        player_turn()

def stop_flee_attempt(source: mob.Mob, ) -> None:
    """
    Checks to see if an enemy is able to successfuly interrupt
    a player's attempt to flee
    """
    enemy_attack = source.roll_attack()
    if enemy_attack - 2 >= global_variables.PLAYER.evasion:
        if global_variables.PLAYER.dead is False:
            global_commands.type_text(f"The {source.id} attacks you while you attempt to flee. You escape, but not unscathed.\n")
            #global_variables.PLAYER.fail_to_flee() #to be added
            print("-" * 110+'\n')
            narrator.exit_the_dungeon()
            #insert a LEAVE DUNGEON command here
        else:
            #idk kill the player
            global_variables.PLAYER.die()
    else:
        global_commands.type_text(f"The {source.id} tries to stop you from retreating, but fails. You've fled successfully.\n")

def flee(enemy: mob.Mob) -> None:
    """
    Attempts to run away from the current encounter
    """
    print('\n'+"-" * 110)
    global_commands.type_text(f"You attempt to flee.\n")
    chase_chance = random.randrange(0, 100)
    if global_variables.PLAYER.hp > global_variables.PLAYER.max_hp * 0.75 and chase_chance <= 10: # above 75% hp, 10% chance enemy chases you
        print('option 1')
        enemy_attack = enemy.roll_attack()
        stop_flee_attempt(enemy)
        
    elif global_variables.PLAYER.hp > global_variables.PLAYER.max_hp * 0.5 and chase_chance < 33: #above 50% hp 33% chance enemy chases you
        print('option 2')
        enemy_attack = enemy.roll_attack()
        stop_flee_attempt(enemy)


    elif global_variables.PLAYER.hp <= global_variables.PLAYER.max_hp * 0.3 and chase_chance < 50: # below 30% hp, 50% chance enemy chases you
        print('option 3')
        enemy_attack = enemy.roll_attack()
        stop_flee_attempt(enemy)

    else:
        print('else')
        global_commands.type_text(f"The {enemy.id} lets you go.\n")
        print("-" * 110+'\n')
        narrator.exit_the_dungeon()