import sys
import mob
import player
import narrator
import items

GOD_MODE = False

def attack(player:player.Player, enemy: mob.Mob, enemy_turn, end_scene) -> None:

    print('\n'+"-" * 110)
    print(f'\nYou attack the {enemy.id}.\n')
    if GOD_MODE is True:
        attack_roll = 1000000
    else:
        attack_roll = player.roll_attack()
    print(f'You rolled a {attack_roll}.\n')

    if attack_roll == 20:
        print("Critical Hit!\n")

    if attack_roll == 1:
        print("Crtical Fail!\n")

    if attack_roll >= enemy.evasion:
        if GOD_MODE is True:
            taken = enemy.take_damage(1000)
        else:
            taken = enemy.take_damage(player.roll_damage())
        
        print(f'You hit the {enemy.id}, dealing {taken} damage.\n')
        if enemy.dead is False:
            enemy_turn()
        elif enemy.dead is True:
            end_scene()
    elif attack_roll < enemy.evasion:
        print("You missed.\n")
        enemy_turn()

def hp(player: player.Player, player_turn):
    print('\n'+"-" * 110)
    print(f'\nHP: {player.hp}/{player.max_hp}')
    print("["+"/"*player.hp+" "*(player.max_hp-player.hp)+"]")
    print('\n'+"-" * 110+'\n')
    player_turn()

def inventory(player: player.Player, player_turn):
    print('\n'+"-" * 110)
    print(f'\nGold: {player.gold}\n')
    player.print_inventory()
    print("-" * 110+'\n')
    player_turn()

def use_an_item(player:player.Player, item, target:mob.Mob | player.Player, enemy_turn, player_turn, ):
    print('\n'+"-" * 110)
    if player.has_item(item) is not False and player.has_item(item).quantity > 0:
        if player.has_item(item).use(target) is True:
            print(f'\n{item} used. {player.has_item(item).quantity} {item}(s) remaining.\n')
            enemy_turn()
        else:
            print(f'\nAlready full HP.\n')
            player_turn()
    else:
        print(f'\nNo {item}(s) avaliable!\n')
        player_turn()

