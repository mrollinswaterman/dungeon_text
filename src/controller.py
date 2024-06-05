import global_variables, global_commands
import monster_manual
import event as ev
import dm_guide
import narrator

TEST = True

class Scene():

    def __init__(self):
        self.enemy:monster_manual.mob.Mob = None
        self.event:ev.Event = None

SCENE = Scene()

def next_scene():
        """
        Starts a new scene with a new enemy or event
        """
        import tui
        if global_commands.probability(99): #85% chance of an enemy spawning next
            SCENE.enemy = monster_manual.spawn_mob("Evil Eye")
            global_variables.RUNNING = False
            tui.link_start()
        else: #remainging 15% chance of an event spawning
            next_event: ev.Event = dm_guide.spawn_random_event()
            next_event.set_tries(2)
            next_event.set_passed(False)
            SCENE.event = next_event
            global_variables.PLAYER.update()#update player before event text goes off
            next_event.start()#prints event start text
            global_commands.type_with_lines("")
            run_event(next_event)

def begin_encounter():
    """
    Sets the enemy for the scene if it's None,
    and prints the encounter header
    """
    if SCENE.enemy is None:
        next_scene()
        return None

    global_commands.type_text(f"You encounter a Level {SCENE.enemy.level} {SCENE.enemy.id}!")
    global_commands.type_with_lines("")

def end_scene():
    global_commands.type_text(f"You killed the {SCENE.enemy.id}!")
    global_variables.PLAYER.recieve_reward(SCENE.enemy.loot)
    SCENE.enemy = None
    if not global_variables.PLAYER.can_level_up:
        narrator.continue_run(next_scene)
    else:
        level_up_player()

def run_event(event: ev.Event):
    narrator.event_options()
    command = input(">> ")
    print("")#newline after cmd prompt
    if command.lower() in ev.FAILURE_LINES:
        event.run(command, global_variables.PLAYER.roll_a_check(command))
        if event.passed is True:# if passed, reset event tries and next_scene()
            event.set_tries(2)
            event.set_passed(False)
            global_variables.PLAYER.recieve_reward(event.loot)
            if not global_variables.PLAYER.can_level_up:
                narrator.continue_run(next_scene)
            else:
                level_up_player()
        elif event.tries is True:# if not passed yet, and still tries left, run it again
            global_commands.type_with_lines("")
            run_event(event)
        else: # if failed, tell the player and move on
            event.failure()
            SCENE.event = None
            narrator.continue_run()
    elif command.lower() == "exit":
        global_commands.exit()
    else:
        global_commands.type_text(f"Invalid command '{command}', please try again.")
        run_event(event)

def level_up_player():
    narrator.level_up_options()
    command = input(">> ")
    print("")#newline after cmd prompt
    global_variables.PLAYER.level_up(command)
    global_commands.type_text(f"Your {global_commands.TAG_TO_STAT[command]} increased by 1. You are now Level {global_variables.PLAYER.level}")
    if global_variables.PLAYER.can_level_up is True:
        level_up_player()
    else:
        narrator.continue_run()