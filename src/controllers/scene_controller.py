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

    def reset(self):
        self.queue = []
        self.passed = []
        self.combatants = {}
        self.round = 0

class Scene():

    def __init__(self):
        #Enemy
        self.enemy:Union[game_objects.Mob, None] = None
        #Event
        self.event:Union[game_objects.Event, None] = None
        #Turn Order
        self.turn_order = Turn_Order()

    def start_combat_round(self):
        self.turn_order.add(game.PLAYER, controllers.player_turn.turn)
        self.turn_order.add(self.enemy, controllers.enemy_turn.turn)
        self.turn_order.go()

    def select_next(self):
        self.turn_order.reset()
        """Starts a new scene with a new enemy or event"""
        if globals.probability(85): #85% chance of an enemy spawning next
            self.enemy = globals.spawn_random_mob()
            self.begin_encounter()
        else: #remainging 15% chance of an event spawning
            self.event: game_objects.Event = globals.spawn_random_event()
            game.PLAYER.update()#update player before event text goes off
            self.event.start()#prints event start text
            self.run_event()

    def begin_encounter(self):
        """Sets the enemy for the scene if it's None, and prints the encounter header"""
        if self.enemy is None:
            #return self.select_next()
            self.enemy = globals.spawn_random_mob()

        globals.type_text(f"You encounter a Level {self.enemy.level} {self.enemy.id}!")
        globals.type_with_lines()
        self.start_combat_round()

    def run_event(self):
        options = game.COMMANDS["stats"]

        done = False
        while not done:
            narrator.event_options()
            cmd = globals.get_cmd()

            if cmd in options:
                if options[cmd] is None: # not the exit command basically
                    match self.event.run(cmd):
                        case True: 
                            done = True
                            if not game.PLAYER.can_level_up:
                                narrator.continue_run()
                            else:
                                self.level_up_player()
                        case None:
                            continue
                        case False:
                            done = True
                            self.event = None
                            narrator.continue_run()

                else:
                    options[cmd]()

            else:
                globals.type_text(f"Invalid stat '{cmd}'. Please try again.")\
                
    def level_up_player(self):
        options = game.COMMANDS["stats"]

        narrator.level_up_options()
        done = False
        while not done:
            cmd = globals.get_cmd()
            if cmd in options:
                done = True
                if options[cmd] is None:
                    game.PLAYER.level_up(cmd)
                else:
                    options[cmd]()

        globals.type_text(f"Your {globals.STATS[cmd]} increased by 1. You are now Level {game.PLAYER.level}")
        if game.PLAYER.can_level_up is True:
            self.level_up_player()
        else:
            narrator.continue_run()

    def loot(self):
        game.PLAYER.gain_xp(self.enemy.xp)
        game.PLAYER.gain_gold(self.enemy.gold)

        #TODO: give the player the option to take the monster's inventory loot

    def end(self):
        globals.type_text(f"You killed the {self.enemy.id}!")
        self.loot()
        self.enemy = None
        self.turn_order.reset()

        if not game.PLAYER.can_level_up:
            narrator.continue_run()
        else:
            self.level_up_player()
