#enemy commands file
import global_commands
import player_commands
import scene_controller

def turn():
    import global_variables
    import scene_controller
    enemy = scene_controller.SCENE.enemy

    if enemy is not None:
        enemy.update()

        if enemy.dead:
            scene_controller.SCENE.end()
            return None

        while enemy.can_act:
            done = turn_options()
            
            if done is None:#wait for turn_options to finish running before checking states
                if global_variables.PLAYER.dead:
                    player_commands.end_game()
                    return None
            
                if enemy.dead:
                    scene_controller.SCENE.end()
                    return None
            
                if enemy.can_act and not enemy.fleeing:
                    print("\n")

        if global_variables.RUNNING:
            global_commands.type_with_lines()
            scene_controller.SCENE.turn_order.go()
        return None
    
    else:
        raise ValueError("Enemy is None.")

def turn_options():
    """Chooses a course of action for the enemy"""
    enemy = scene_controller.SCENE.enemy

    if enemy.fleeing:
        enemy.spend_ap(0)
        return enemy_flee_attempt()

    #if trigger is active, 85% chance to try special
    if enemy.trigger() and global_commands.probability(85):
        return enemy.special()

    #if no trigger, don't special
    return enemy_attack()

def enemy_flee_attempt():
    """Runs when the enemy tries to escape."""
    import global_variables
    import narrator
    enemy = scene_controller.SCENE.enemy

    global_commands.type_text(f"The {enemy.id} attempts to flee...")
    global_commands.type_text("Try to stop them? y/n")
    done = False
    while not done:
        command = input(">> ").lower()
        print("")
        match command:
            case "exit":
                global_commands.exit()
            case "y":
                if global_variables.PLAYER.roll_to_hit() >= enemy.evasion():
                    global_commands.type_text(f"You cut off the {enemy.id}'s escape. It turns to fight...")
                    global_commands.type_with_lines()
                    scene_controller.SCENE.turn_order.go()
                else:
                    global_commands.type_text(f"You try catching the {enemy.id} to no avail. It got away.")
                    narrator.continue_run()
                return None
            case "n":
                global_commands.type_text(f"You let the {enemy.id} go.")
                narrator.continue_run()
                return None
            case _:
                global_commands.type_text(f"Invalid command '{command}'. Please try again.")
    return None

def enemy_attack():
    """Runs the enemy attack"""
    import scene_controller

    scene_controller.SCENE.enemy.attack()
    return None
