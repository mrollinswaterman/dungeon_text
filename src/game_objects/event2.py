import random
import game_objects
import globals
import game

class Event(game_objects.Game_Object):
    def __init__(self):
        self.id = self.__class__.__name__.lower()
        self._attempts = 2

        self.stats:dict[str, int] = {}

        if self.id == "event": self.id = "default"

    @property
    def attempts(self) -> int:
        return self._attempts

    @property
    def done(self) -> bool:
        return self._attempts <= 0
    
    def start(self) -> None:
        return self.message("start")
    
    def success(self) -> bool:
        return True
    
    def failure(self) -> bool:
        self.message("end")
        return False
    
    def end(self) -> bool:
        return self.failure()
    
    def run(self, stat:str) -> bool:
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
        
    def message(self, msg_type:str, stat:str=None) -> None:
        filename = f"event_text/{self.id}/{msg_type}/{stat}.txt"

        if stat is None: filename = f"event_text/{self.id}/{msg_type}.txt"

        filename = self.check_default(filename)

        with open(filename, "r") as file:
            content = file.read().split("\n\n")

            text = random.choice(content)

            file.close()
        
        if text[0] != "*":
            return self.message(msg_type, stat)
        
        if text[-1] == '\n':
            text = text[0:-1]
        
        globals.type_text(text[1:len(text)])
    
    def check_default(self, filename:str) -> str:
        try:
            with open(filename, "r") as file:
                file.close()
            return filename
        except:
            ret = filename.split("/")
            ret[1] = "default"
            return "/".join(ret)
