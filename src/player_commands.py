import random
import global_commands
import global_variables
import mob
import items
import narrator

GOD_MODE = False

def player_turn_options():
    global_commands.type_with_lines(f" What would you like to do? Action Points: {global_variables.PLAYER.ap}/{global_variables.PLAYER.max_ap}\n")
    print (f"\t Attack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i) | Use a Health Potion - (u)\n")


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

    global_commands.type_with_lines(f" You attack the {enemy.id}, rolling a {attack_roll}.\n")

    if attack_roll == 0:
        global_commands.type_text(f" Critical Hit!\n")
        taken = enemy.take_damage(global_variables.PLAYER.roll_damage() * global_variables.PLAYER.weapon.crit)

    if attack_roll == 1:
        global_commands.type_text(f" Crtical Fail!\n")

    if attack_roll >= enemy.evasion:
        if GOD_MODE is True:
            taken = enemy.take_damage(1000)
        else:
            taken = enemy.take_damage(global_variables.PLAYER.roll_damage())
        
        
        if enemy.dead is False and global_variables.PLAYER.can_act is False:
            global_variables.PLAYER.reset_ap()
            global_commands.type_text(f" You hit the {enemy.id} for {taken} damage.") #last thing printed = no \n
            enemy_turn()
        elif enemy.dead is True:
            global_commands.type_text(f" You hit the {enemy.id} for {taken} damage.\n")
            end_scene()
        else:
            player_turn_options()

    elif attack_roll < enemy.evasion:
        global_commands.type_text(f" You missed.") #last thing printed = no \n
        if global_variables.PLAYER.can_act is False:
            global_variables.PLAYER.reset_ap()
            enemy_turn()
        else: 
            player_turn_options()

def hp(player_turn) -> None:
    """
    Prints the player's HP then runs the given function
    """
    global_commands.print_with_lines(f' HP: {global_variables.PLAYER.hp}/{global_variables.PLAYER.max_hp}')
    print(" ["+"/"*global_variables.PLAYER.hp+" "*(global_variables.PLAYER.max_hp-global_variables.PLAYER.hp)+"]")
    player_turn()

def inventory(player_turn) -> None:
    """
    Prints the player's inventory then runs the given function
    """
    global_commands.print_with_lines(f" Gold: {global_variables.PLAYER.gold}\n")
    global_variables.PLAYER.print_inventory()
    player_turn()

def use_an_item(item: items.Consumable, enemy_turn, player_turn, target=global_variables.PLAYER) -> None:
    """
    Uses an item on the Player, if the player has the item in their inventory
    """
    if global_variables.PLAYER.has_item(item) is True:#check the player has the item
        index = global_variables.PLAYER.find_consumable_by_id(item)
        held_item:items.Consumable = global_variables.PLAYER.inventory[index]

        if held_item.quantity == 0: #if the items quantity is 0, remove it
            global_variables.PLAYER.inventory.remove(held_item)
            global_commands.type_with_lines(f' No {item.id}s avaliable!\n')
            player_turn()
        held_item.use(target)
        global_variables.PLAYER.spend_ap(1)
        if global_variables.PLAYER.can_act is False:
            global_variables.PLAYER.reset_ap()
            enemy_turn()
        else:
            player_turn()
    else:
        global_commands.type_with_lines(f' No {item.name}s avaliable!\n')
        player_turn()

def stop_flee_attempt(enemy: mob.Mob, ) -> None:
    """
    Checks to see if an enemy is able to successfuly interrupt
    a player's attempt to flee
    """
    global_commands.type_text(f" The {enemy.id} attempts to stop you!")
    if enemy.attack_of_oppurtunity(global_variables.PLAYER) is True:
        global_commands.type_text(f" It caught up with you! You escape but not unscathed.")
        #player.lose_some_items
        narrator.exit_the_dungeon()
    else:
        global_commands.type_text(f" It failed. You've escaped.")

def flee(enemy: mob.Mob) -> None:
    """
    Attempts to run away from the current encounter
    """
    global_commands.type_with_lines(f" You attempt to flee...\n")
    chase_chance = random.randrange(0, 100)
    if global_variables.PLAYER.hp > global_variables.PLAYER.max_hp * 0.75 and chase_chance <= 10: 
        # above 75% hp, 10% chance enemy chases you
        stop_flee_attempt(enemy)
    elif global_variables.PLAYER.hp > global_variables.PLAYER.max_hp * 0.5 and chase_chance < 33: 
        #above 50% hp 33% chance enemy chases you
        stop_flee_attempt(enemy)
    elif global_variables.PLAYER.hp <= global_variables.PLAYER.max_hp * 0.3 and chase_chance < 50: 
        # below 30% hp, 50% chance enemy chases you
        stop_flee_attempt(enemy)
    else:
        global_commands.type_text(f" The {enemy.id} lets you go.")
        narrator.exit_the_dungeon()