#Glyphs event class
import game_objects
import globals

class Glyphs(game_objects.Event):
    def __init__(self):
        super().__init__()
        self.stats["int"] = 15

    def failure(self):
        from compendiums import event_compendium as events
        super().failure()
        print("="*110+'\n')
        trap = globals.spawn_event("Trap_Room")
        trap.start()
        trap.run()
        return False

object = Glyphs
