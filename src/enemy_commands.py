#enemy commands file
import global_commands
import player_commands
import controller

def turn():
    import global_variables
    import controller

    if controller.SCENE.enemy is not None:
        controller.SCENE.enemy.update()

        if controller.SCENE.enemy.dead:
            controller.end_scene()
            return None

        while controller.SCENE.enemy.can_act:
            done = turn_options()
            
            if done is None:#wait for turn_options to finish running before checking states
                if global_variables.PLAYER.dead:
                    player_commands.end_game()
                    return None
            
                if controller.SCENE.enemy.dead:
                    controller.end_scene()
                    return None
            
                if controller.SCENE.enemy.can_act and not controller.SCENE.enemy.fleeing:
                    global_commands.type_with_lines("")

        if global_variables.RUNNING:
            global_commands.type_with_lines("")
            player_commands.turn()
    
    else:
        raise ValueError("Enemy is None.")

def turn_options():
    """
    Chooses a course of action for the enemy
    """
    if controller.SCENE.enemy.fleeing:
        controller.SCENE.enemy.spend_ap(0)
        return enemy_flee_attempt()

    if controller.SCENE.enemy.trigger() and global_commands.probability(99):#if trigger is active, 75% chance of special
            return True if controller.SCENE.enemy.special() else enemy_attack()
    elif global_commands.probability(99):#if no trigger, only 10% chance of special
            return True if controller.SCENE.enemy.special() else enemy_attack()
    else:
        return enemy_attack()

def enemy_flee_attempt():
    """
    Runs when the enemy tries to escape. Lets the player
    choose whether to let them go or pursue them.
    """
    import global_variables
    import player_commands
    import narrator

    global_commands.type_text(f"The {controller.SCENE.enemy.id} attempts to flee...")
    global_commands.type_text("Try to stop them? y/n")
    done = False
    while not done:
        command = input(">> ").lower()
        print("")
        match command:
            case "exit":
                global_commands.exit()
            case "y":
                if global_variables.PLAYER.roll_attack() >= controller.SCENE.enemy.evasion:
                    global_commands.type_text(f"You cut off the {controller.SCENE.enemy.id}'s escape. It turns to fight...")
                    global_commands.type_with_lines("")
                    player_commands.turn()
                else:
                    global_commands.type_text(f"You try catching the {controller.SCENE.enemy.id} to no avail. It got away.")
                    narrator.continue_run()
                return None
            case "n":
                global_commands.type_text(f"You let the {controller.SCENE.enemy.id} go.")
                narrator.continue_run()
                return None
            case _:
                global_commands.type_text(f"Invalid command '{command}'. Please try again.")
    return None

def enemy_attack():
    """
    Runs the enemy attack
    """
    import controller

    controller.SCENE.enemy.attack()
    return None

