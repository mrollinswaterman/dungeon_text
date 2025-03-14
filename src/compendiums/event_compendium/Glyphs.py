#Glyphs event class
import game_objects

class Glyphs(game_objects.Event):
    def __init__(self):
        super().__init__()
        self.stats["int"] = 15

    def failure(self):
        import controllers
        from compendiums import event_compendium as events
        super().failure()
        print("starting trap room!")
        #trap = events.Trap_Room()
        #trap.start()
        #trap.run()
        return None

object = Glyphs
