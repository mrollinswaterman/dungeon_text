#Boulder Event class
import game_objects

class Boulder(game_objects.Event):
    def __init__(self):
        super().__init__()
        self.stats["str"] = 10
        self.stats["dex"] = 15

object = Boulder
