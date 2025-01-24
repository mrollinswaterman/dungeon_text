import random
import game_objects
import globals
import game

class Event(game_objects.Game_Object):
    def __init__(self):
        self.id = self.__class__.__name__.lower()
        self._attempts = 2

        self.stats:dict[str, int] = {}

    @property
    def attempts(self) -> int:
        return self._attempts

    @property
    def done(self) -> bool:
        return self.attempts <= 0
    
    def success(self):
        return True
    
    def failure(self):
        self.message("end")
        return False
    
    def run(self, stat:str):
        self.id = "default"
        if self.done: raise ValueError("event is finished")

        self._attempts -= 1

        if self.try_with(stat): return self.success()
        
        if self.done: return self.failure()

        return False

    def try_with(self, stat:str):
        if stat not in self.stats:
            self.message("failure", stat)
            return False
        
        if game.PLAYER.roll_a_check(stat) >= self.stats[stat]:
            self.message("success", stat)
            return True
        
        self.message("failure", stat)
        return False
        
    def message(self, msg_type:str, stat:str=None):
        filename = f"event_text/{self.id}/{msg_type}/{stat}.txt"

        if stat is None: filename = f"event_text/{self.id}/{msg_type}.txt"

        with open(filename, "r") as file:
            content = file.read().split("\n\n")

            text = random.choice(content)

            file.close()
        
        if text[0] != "*":
            return self.failure_message(stat)
        
        globals.type_text(text[1:len(text)])
