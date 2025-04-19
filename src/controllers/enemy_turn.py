#enemy turn controller file

##Required Modules: globals, controllers, controllers
from errno import EMEDIUMTYPE
import controllers.player_turn
import globals
import controllers
import game
import narrator

def turn():
    enemy = game.SCENE.enemy

    if enemy is not None:
        enemy.update()

        if enemy.dead:
            return game.SCENE.end()

        while enemy.can_act:
            done = turn_options()
            
            if done is None:#wait for turn_options to finish running before checking states
                if game.PLAYER.dead:
                    controllers.player_turn.end_game()
                    return None
            
                if enemy.dead:
                    return game.SCENE.end()
            
                if enemy.can_act and not enemy.fleeing:
                    print("\n")

        globals.type_with_lines()
        game.SCENE.turn_order.go()
        return None
    
    else:
        raise ValueError("Enemy is None.")

def turn_options():
    """Chooses a course of action for the enemy"""
    enemy = game.SCENE.enemy

    if enemy.fleeing:
        enemy.spend_ap(0)
        return enemy_flee_attempt()

    #if trigger is active, 85% chance to try special
    if enemy.trigger() and globals.probability(85):
        return enemy.special()

    #if no trigger, don't special
    return enemy_attack()

def enemy_flee_attempt():
    """Runs when the enemy tries to escape"""
    enemy = game.SCENE.enemy

    globals.type_text(f"The {enemy.id} attempts to flee...")
    globals.type_text("Try to stop them? y/n")
    done = False
    while not done:
        command = input(">> ").lower()
        print("")
        match command:
            case "exit":
                globals.exit()
            case "y":
                if game.PLAYER.roll_to_hit() >= enemy.evasion():
                    globals.type_text(f"You cut off the {enemy.id}'s escape. It turns to fight...")
                    globals.type_with_lines()
                    game.SCENE.turn_order.go()
                else:
                    globals.type_text(f"You try catching the {enemy.id} to no avail. It got away.")
                    game.SCENE.end()
                return None
            case "n":
                globals.type_text(f"You let the {enemy.id} go.")
                game.SCENE.end()
                return None
            case _:
                globals.type_text(f"Invalid command '{command}'. Please try again.")
    return None

def enemy_attack():
    """Runs the enemy attack"""
    game.SCENE.enemy.attack()
    return None
