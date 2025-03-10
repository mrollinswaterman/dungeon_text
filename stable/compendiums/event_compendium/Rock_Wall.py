#Rock Wall Event class
import game_objects

class Rock_Wall(game_objects.Event):
    def __init__(self):
        super().__init__()
        self.stats["str"] = 20
        self.stats["dex"] = 10

object = Rock_Wall
