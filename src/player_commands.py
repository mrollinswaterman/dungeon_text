import random
import global_commands
import global_variables
import mob
import items
import narrator

GOD_MODE = False

ENEMY:mob.Mob = None
ENEMY_TURN = None

PLAYER = global_variables.PLAYER
PLAYER_TURN = None
PLAYER_DEATH = None

END_SCENE = None

def player_turn_options():
    global_commands.type_with_lines(f" What would you like to do? Action Points: {PLAYER.ap}/{PLAYER.max_ap}\n")
    print (f"\t Attack - (a) | Check HP - (hp) | Flee - (f) | Inventory - (i) | Use a Health Potion - (u)\n")


def attack() -> None:
    """
    Attacks an enemy. 

    enemy: a Mob object, the target

    end_scene: function to run if the player kills the enemy

    Returns nothing
    """
    if GOD_MODE is True:
        attack_roll = 1000000
    else:
        attack_roll = PLAYER.roll_attack()
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
            ENEMY_TURN()
        elif ENEMY.dead is True:
            global_commands.type_text(f" You hit the {ENEMY.id} for {taken} damage.\n")
            END_SCENE()
        else:
            player_turn_options()

    elif attack_roll < ENEMY.evasion:
        global_commands.type_text(f" You missed.") #last thing printed = no \n
        if PLAYER.can_act is False:
            PLAYER.reset_ap()
            ENEMY_TURN()
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
    if PLAYER.has_item(item) is True:#check the player has the item
        index = PLAYER.find_consumable_by_id(item)
        held_item:items.Consumable = PLAYER.inventory[index]

        if held_item.quantity == 0: #if the items quantity is 0, remove it
            PLAYER.inventory.remove(held_item)
            global_commands.type_with_lines(f' No {item.id}s avaliable!\n')
            PLAYER_TURN()
        held_item.use(target)
        PLAYER.spend_ap(1)
        if PLAYER.can_act is False:
            PLAYER.reset_ap()
            ENEMY_TURN()
        else:
            PLAYER_TURN()
    else:
        global_commands.type_with_lines(f' No {item.name}s avaliable!\n')
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
    chase_chance = random.randrange(0, 100)
    if PLAYER.hp > PLAYER.max_hp * 0.75 and chase_chance <= 10: 
        # above 75% hp, 10% chance enemy chases you
        stop_flee_attempt()
    elif PLAYER.hp > PLAYER.max_hp * 0.5 and chase_chance < 33: 
        #above 50% hp 33% chance  chases you
        stop_flee_attempt()
    elif PLAYER.hp <= PLAYER.max_hp * 0.3 and chase_chance < 50: 
        # below 30% hp, 50% chance  chases you
        stop_flee_attempt()
    else:
        global_commands.type_text(f" The {ENEMY.id} lets you go.")
        narrator.exit_the_dungeon()