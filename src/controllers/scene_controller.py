##Required Modules: globals, controllers, narrator, commands

from typing import Any, Union
import globals
import game
import controllers.enemy_turn
import controllers.player_turn
import narrator
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

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
        #Player
        self.player:Union[game_objects.Player, None] = None
        #Enemy
        self.enemy:Union[game_objects.Mob, None] = None
        #Event
        self.event:Union[game_objects.Event, None] = None
        #Turn Order
        self.turn_order = Turn_Order()

        #self.turn_order.add(self.player, controllers.player_turn.turn)
        #self.turn_order.add(self.enemy, controllers.enemy_turn.turn)

    def start_combat_round(self):
    
        self.turn_order.add(self.player, controllers.player_turn.turn)
        self.turn_order.add(self.enemy, controllers.enemy_turn.turn)

        self.turn_order.go()

    def select_next(self):
        """Starts a new scene with a new enemy or event"""
        if globals.probability(85): #85% chance of an enemy spawning next
            self.enemy = controllers.spawn_random_mob()
            self.begin_encounter()
        else: #remainging 15% chance of an event spawning
            self.event: game_objects.Event = globals.spawn_random_event()
            self.event.set_tries(2)
            self.event.set_passed(False)
            game.PLAYER.update()#update player before event text goes off
            self.event.start()#prints event start text
            globals.type_with_lines()
            #run_event(self.event)

    def begin_encounter(self):
        """Sets the enemy for the scene if it's None, and prints the encounter header"""
        if self.enemy is None:
            #return self.select_next()
            self.enemy = globals.spawn_random_mob()

        globals.type_text(f"You encounter a Level {self.enemy.level} {self.enemy.id}!")
        globals.type_with_lines()
        self.start_combat_round()

    def end(self):
        globals.type_text(f"You killed the {self.enemy.id}!")
        game.PLAYER.receive_loot()
        self.enemy = None
        self.turn_order.clear()

        if not game.PLAYER.can_level_up:
            narrator.continue_run()
        else:
            pass
            #level_up_player()

"""

def run_event(event: "game_objects.Event"):
    stats = commands.commands["stats"]

    done = False
    while not done:
        narrator.event_options()
        cmd = globals.get_cmd()

        if cmd in stats:
            if stats[cmd] is None:
                event.run(cmd, globals.PLAYER.roll_a_check(cmd))
                if event.passed is True:# if passed, reset event tries and SCENE.next()
                    done = True
                    event.set_tries(2)
                    event.set_passed(False)
                    globals.PLAYER.recieve_reward(event.loot)
                    if not globals.PLAYER.can_level_up:
                        narrator.continue_run()
                    else:
                        level_up_player()
                elif event.tries is True:# if not passed yet, and still tries left, run it again
                    globals.type_with_lines()
                else: # if failed, tell the player and move on
                    done = True
                    event.failure()
                    SCENE.event = None
                    narrator.continue_run()
            else:
                stats[cmd]()

        else:
            globals.type_text(f"Invalid stat '{cmd}'. Please try again.")

def level_up_player():
    stats = commands.commands["stats"]

    narrator.level_up_options()
    done = False
    while not done:
        cmd = globals.get_cmd()
        if cmd in stats:
            done = True
            if stats[cmd] is None:
                globals.PLAYER.level_up(cmd)
            else:
                stats[cmd]()

    globals.type_text(f"Your {globals.STATS[cmd]} increased by 1. You are now Level {globals.PLAYER.level}")
    if globals.PLAYER.can_level_up is True:
        level_up_player()
    else:
        narrator.continue_run()

        
"""