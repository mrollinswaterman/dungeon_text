import time

GOD_MODE = False

def type_text(text: str, speed: int = .03) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    time.sleep(.2)
    for char in text:
        time.sleep(speed)
        print(char, end='', flush=True)
    print("")

def attack(player, enemy, enemy_turn, end_scene) -> None:
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
        attack_roll = player.roll_attack()
    
    print('\n'+"-" * 110)
    type_text(f'\nYou attack the {enemy.id}, rolling a {attack_roll}.\n')

    if attack_roll == 0:
        type_text(f"Critical Hit!\n")
        taken = enemy.take_damage(player.roll_damage() * player.weapon.crit)

    if attack_roll == 1:

        type_text(f"Crtical Fail!\n")

    if attack_roll >= enemy.evasion:
        if GOD_MODE is True:
            taken = enemy.take_damage(1000)
        else:
            taken = enemy.take_damage(player.roll_damage())
        
        type_text(f'You hit the {enemy.id} for {taken} damage.\n')
        #print("-" * 110+"\n")
        if enemy.dead is False:
            enemy_turn()
        elif enemy.dead is True:
            end_scene()

    elif attack_roll < enemy.evasion:
        type_text(f"You missed.\n")
        print("-" * 110+"\n")
        enemy_turn()

def hp(player, player_turn) -> None:
    """
    Prints the player's HP then runs the given function
    """
    print('\n'+"-" * 110)
    print(f'\nHP: {player.hp}/{player.max_hp}')
    print("["+"/"*player.hp+" "*(player.max_hp-player.hp)+"]")
    print('\n'+"-" * 110+'\n')
    player_turn()

def inventory(player, player_turn) -> None:
    """
    Prints the player's inventory then runs the given function
    """
    print('\n'+"-" * 110)
    print(f'\nGold: {player.gold}\n')
    player.print_inventory()
    print("\n"+"-" * 110+'\n')
    player_turn()

def use_an_item(player, item, target, enemy_turn, player_turn) -> None:
    """
    Uses an item on the Player, if the player has the item in their inventory
    """
    print('\n'+"-" * 110)
    if player.has_item(item) is not False and player.has_item(item).quantity > 0:
        if player.has_item(item).use(target) is True:
            type_text(f'\n{item} used. {player.has_item(item).quantity} {item}(s) remaining.\n')
            enemy_turn()
        else:
            type_text(f'\nAlready full HP.\n')
            player_turn()
    else:
        type_text(f'\nNo {item}(s) avaliable!\n')
        player_turn()

