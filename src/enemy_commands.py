#enemy commands file
import global_commands
import global_variables
import narrator
import player_commands
import mob

ENEMY:mob.Mob = None
ENEMY_TURN = None
END_SCENE = None

PLAYER = global_variables.PLAYER
PLAYER_TURN = None
PLAYER_DEATH = None

NEXT_SCENE = None


def start_turn():

    if ENEMY is not None:
        ENEMY.update()

        if ENEMY.dead:
            END_SCENE()
            return None

        while ENEMY.can_act:
            done = turn_options()
            
            if done is None:#wait for turn_options to finish running before checking states
                if PLAYER.dead:
                    PLAYER_DEATH()
                    return None
            
                if ENEMY.dead:
                    END_SCENE()
                    return None
            
                if ENEMY.can_act and not ENEMY.fleeing:
                    global_commands.type_with_lines("")

        if global_variables.RUNNING:
            global_commands.type_with_lines("")
            player_commands.start_turn()
     
    else:
        raise ValueError("Enemy is None.")

def turn_options():
    """
    Chooses a course of action for the enemy
    """
    if ENEMY.fleeing:
        ENEMY.spend_ap(0)
        return enemy_flee_attempt()

    if ENEMY.trigger() and global_commands.probability(99):#if trigger is active, 75% chance of special
            return ENEMY.special()
    elif global_commands.probability(99):#if no trigger, only 10% chance of special
            return ENEMY.special()
    else:
       return enemy_attack()

def enemy_flee_attempt():
    """
    Runs when the enemy tries to escape. Lets the player
    choose whether to let them go or pursue them.
    """
    global_commands.type_text(f"The {ENEMY.id} attempts to flee...")
    global_commands.type_text("Try to stop them? y/n")
    done = False
    while not done:
        command = input(">> ").lower()
        print("")
        match command:
            case "exit":
                global_commands.exit()
            case "y":
                if PLAYER.roll_attack() >= ENEMY.evasion:
                    global_commands.type_text(f"You cut off the {ENEMY.id}'s escape. It turns to fight...")
                    global_commands.type_with_lines("")
                    player_commands.start_turn()
                else:
                    global_commands.type_text(f"You try catching the {ENEMY.id} to no avail. It got away.")
                    narrator.continue_run(NEXT_SCENE)
                return None
            case "n":
                global_commands.type_text(f"You let the {ENEMY.id} go.")
                narrator.continue_run(NEXT_SCENE)
                return None
            case _:
                global_commands.type_text(f"Invalid command '{command}'. Please try again.")
    return None

def enemy_attack():
    """
    Runs the enemy attack
    """
    ENEMY.spend_ap()
    attack = ENEMY.roll_attack()

    if attack == 0:
        global_commands.type_text(f"The {ENEMY.id} attacks you, rolling a natural 20.")
    else:
        global_commands.type_text(f"The {ENEMY.id} attacks you, rolling a {attack}.")

    match attack:
        case 0:
            global_commands.type_text(f"A critical hit! Uh oh.")
            taken = global_variables.PLAYER.take_damage(ENEMY.roll_damage() * 2, ENEMY)
            return None
        case 1:
            global_commands.type_text(f"It critically failed!")
            if ENEMY.fumble_table():
                taken = ENEMY.take_damage(ENEMY.roll_damage(), ENEMY)
            else:
                global_commands.type_text(f"It missed.")
            return None
        case _:
            pass

    if attack >= global_variables.PLAYER.evasion: 
        taken = global_variables.PLAYER.take_damage(ENEMY.roll_damage(), ENEMY)
        return None

    global_commands.type_text(f"The {ENEMY.id} missed.")
    return None
