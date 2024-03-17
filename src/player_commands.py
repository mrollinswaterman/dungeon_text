import random
import global_commands
import global_variables
import mob
import items
import narrator

GOD_MODE = False

ENEMY:mob.Mob = None
ENEMY_TURN = None
END_SCENE = None

PLAYER = global_variables.PLAYER
PLAYER_TURN = None
PLAYER_DEATH = None

NEXT_SCENE = None

def player_turn_options():
    global_commands.type_with_lines(f" What would you like to do? Action Points: {PLAYER.ap}/{PLAYER.max_ap}\n")
    print (f"\t Attack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i) | Use a Health Potion - (u) | Throw a Firebomb - (t)\n")


def attack(run_on_hit=None, run_on_miss=None) -> None:
    """
    Attacks an enemy. 

    enemy: a Mob object, the target

    end_scene: function to run if the player kills the enemy

    Returns nothing
    """
    if run_on_miss is None:
        run_on_miss = ENEMY_TURN
    if run_on_hit is None:
        run_on_hit = ENEMY_TURN

    if GOD_MODE is True:
        attack_roll = 1000000
    else:
        attack_roll = 1#PLAYER.roll_attack()
        PLAYER.spend_ap(1)

    global_commands.type_with_lines(f" You attack the {ENEMY.id}, rolling a {attack_roll}.\n")

    if attack_roll == 0:
        global_commands.type_text(f" Critical Hit!\n")
        taken = ENEMY.take_damage(PLAYER.roll_damage() * PLAYER.weapon.crit)

    if attack_roll == 1:
        global_commands.type_text(f" Crtical Fail!\n")

    if attack_roll >= ENEMY.evasion:
        if GOD_MODE is True:
            taken = ENEMY.take_damage(1000)
        else:
            taken = ENEMY.take_damage(PLAYER.roll_damage())

        if ENEMY.dead is False and PLAYER.can_act is False:
            PLAYER.reset_ap()
            global_commands.type_text(f" You hit the {ENEMY.id} for {taken} damage.") #last thing printed = no \n
            run_on_hit()
        elif ENEMY.dead is True:
            global_commands.type_text(f" You hit the {ENEMY.id} for {taken} damage.\n")
            END_SCENE()
        else:
            player_turn_options()

    elif attack_roll < ENEMY.evasion:
        global_commands.type_text(f" You missed.") #last thing printed = no \n
        if PLAYER.can_act is False:
            PLAYER.reset_ap()
            run_on_miss()
        else: 
            player_turn_options()

def hp() -> None:
    """
    Prints the player's HP then runs the given function
    """
    global_commands.print_with_lines(f' HP: {PLAYER.hp}/{PLAYER.max_hp}')
    print(" ["+"/"*PLAYER.hp+" "*(PLAYER.max_hp-PLAYER.hp)+"]")
    PLAYER_TURN()

def inventory() -> None:
    """
    Prints the player's inventory then runs the given function
    """
    global_commands.print_with_lines(f" Gold: {PLAYER.gold}\n")
    PLAYER.print_inventory()
    PLAYER_TURN()

def use_an_item(item: items.Consumable, target=PLAYER) -> None:
    """
    Uses an item on the Player, if the player has the item in their inventory
    """
    if item is None:
        raise ValueError("")
    if PLAYER.has_item(item) is True:#check the player has the item
        item = PLAYER.find_item_by_name(item.name)
        held_item:items.Consumable = item
        if held_item.quantity == 0: #if the items quantity is 0, remove it
            PLAYER.inventory.remove(held_item)
            held_item.set_owner(None)
            global_commands.type_with_lines(f" No {item.name} avaliable!")
            PLAYER_TURN()
            return None
        held_item.use(target)
        if PLAYER.can_act is False:
            PLAYER.reset_ap()
            ENEMY_TURN()
        else:
            PLAYER_TURN()
    else:
        global_commands.type_with_lines(f" No {item.name} avaliable!")
        PLAYER_TURN()

def stop_flee_attempt() -> None:
    """
    Checks to see if an enemy is able to successfuly interrupt
    a player's attempt to flee
    """
    global_commands.type_text(f" The {ENEMY.id} attempts to stop you!")
    if ENEMY.attack_of_oppurtunity(PLAYER) is True:
        global_commands.type_text(f" It caught up with you! You escape but not unscathed.")
        #player.lose_some_items
        narrator.exit_the_dungeon()
    else:
        global_commands.type_text(f" It failed. You've escaped.")

def flee() -> None:
    """
    Attempts to run away from the current encounter
    """
    global_commands.type_with_lines(f" You attempt to flee...\n")
    
    if global_commands.probability(90 - int((PLAYER.hp / PLAYER.max_hp) * 100)):
        #higher HP == lower chase chance
        stop_flee_attempt()
    else:
        global_commands.type_text(f" The {ENEMY.id} lets you go.")
        narrator.exit_the_dungeon()