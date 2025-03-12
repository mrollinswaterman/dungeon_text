import sys
import globals

def run():
    import game_objects, controllers, compendiums, game

    
    enemy = globals.spawn_random_mob()

    game.SCENE.enemy = enemy

    game.PLAYER.attack()

    game.PLAYER.reset_ap()

    game.PLAYER.attack()

    sys.exit()