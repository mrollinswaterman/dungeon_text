from typing import Any
import global_variables, global_commands
import monster_manual
import event as ev
import dm_guide
import narrator

class Turn_Order():

    def __init__(self):
        self.combatants = {}
        self.queue:list[Any] = []
        self.passed = []
        self.round = 0

    @property
    def empty(self) -> bool:
        return len(self.queue) <= 0
    @property
    def current(self):
        return self.queue[0]

    @property
    def next(self):
        try:
            return self.queue[1]
        except IndexError:
            return None

    def go(self):
        if not self.empty:
            actor = self.queue[0]
            self.queue.remove(actor)
            self.passed.append(actor)
            self.combatants[actor]()
            return None

        self.round += 1
        for entry in self.passed:
            self.queue.append(entry)

        self.passed = []
        return self.go()

    def add(self, combatant, turn_function):

        if combatant not in self.combatants:
            self.combatants[combatant] = turn_function

        if combatant not in self.queue:
            self.queue.append(combatant)

    def clear(self):
        self.queue = []
        self.passed = []

class Scene():

    def __init__(self):
        import player_commands
        import enemy_commands
        #Player
        self.player = global_variables.PLAYER
        #Enemy
        self.enemy:monster_manual.mob.Mob = monster_manual.spawn_random_mob()
        #Event
        self.event:ev.Event = None
        #Turn Order
        self.turn_order = Turn_Order()

        self.turn_order.add(self.player, player_commands.turn)
        self.turn_order.add(self.enemy, enemy_commands.turn)

    def start_combat(self):
        import player_commands
        import enemy_commands
    
        self.turn_order.add(self.player, player_commands.turn)
        self.turn_order.add(self.enemy, enemy_commands.turn)

        self.turn_order.go()

    def select_next(self):
        """Starts a new scene with a new enemy or event"""
        if global_commands.probability(85): #85% chance of an enemy spawning next
            self.enemy = monster_manual.spawn_random_mob()
            self.begin_encounter()
        else: #remainging 15% chance of an event spawning
            self.event: ev.Event = dm_guide.spawn_random_event()
            self.event.set_tries(2)
            self.event.set_passed(False)
            global_variables.PLAYER.update()#update player before event text goes off
            self.event.start()#prints event start text
            global_commands.type_with_lines()
            run_event(self.event)

    def begin_encounter(self):
        """Sets the enemy for the scene if it's None, and prints the encounter header"""
        if self.enemy is None:
            return self.select_next()

        global_commands.type_text(f"You encounter a Level {self.enemy.level} {self.enemy.id}!")
        global_commands.type_with_lines()
        self.start_combat()

    def end(self):
        global_commands.type_text(f"You killed the {self.enemy.id}!")
        global_variables.PLAYER.recieve_reward(self.enemy)
        self.enemy = None
        self.turn_order.clear()

        if not global_variables.PLAYER.can_level_up:
            narrator.continue_run()
        else:
            level_up_player()

SCENE = Scene()

def run_event(event: ev.Event):
    from command_dict import commands
    stats = commands["stats"]

    done = False
    while not done:
        narrator.event_options()
        cmd = global_commands.get_cmd()

        if cmd in stats:
            if stats[cmd] is None:
                event.run(cmd, global_variables.PLAYER.roll_a_check(cmd))
                if event.passed is True:# if passed, reset event tries and SCENE.next()
                    done = True
                    event.set_tries(2)
                    event.set_passed(False)
                    global_variables.PLAYER.recieve_reward(event.loot)
                    if not global_variables.PLAYER.can_level_up:
                        narrator.continue_run()
                    else:
                        level_up_player()
                elif event.tries is True:# if not passed yet, and still tries left, run it again
                    global_commands.type_with_lines()
                else: # if failed, tell the player and move on
                    done = True
                    event.failure()
                    SCENE.event = None
                    narrator.continue_run()
            else:
                stats[cmd]()

        else:
            global_commands.type_text(f"Invalid stat '{cmd}'. Please try again.")

def level_up_player():
    from command_dict import commands
    from global_variables import STATS
    stats = commands["stats"]

    narrator.level_up_options()
    done = False
    while not done:
        cmd = global_commands.get_cmd()
        if cmd in stats:
            done = True
            if stats[cmd] is None:
                global_variables.PLAYER.level_up(cmd)
            else:
                stats[cmd]()

    global_commands.type_text(f"Your {STATS[cmd]} increased by 1. You are now Level {global_variables.PLAYER.level}")
    if global_variables.PLAYER.can_level_up is True:
        level_up_player()
    else:
        narrator.continue_run()
