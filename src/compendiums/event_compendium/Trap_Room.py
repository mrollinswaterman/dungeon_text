#Trap Room Event class
import game_objects
import mechanics
import game

class Trap_Room(game_objects.Event):

    def __init__(self):
        super().__init__()

        self.stats["dex"] = 18

        self.damage_type = mechanics.DamageType()
        self.damage_type.set(["Physical"])

        self.header = game_objects.Header(self)
        self.header._damage = "the Dwarven trap"

        self._damage_cap = 5

    def deal_damage(self):
        damage = mechanics.DamageInstance(self, self._damage_cap)
        taken = game.PLAYER.take_damage(damage)
        return taken

    def failure(self):
        self.deal_damage()
        return False
    
    def run(self):
        result = super().run("dex")
        match result:
            case True: return self.success()
        
            case _: return self.failure()

object = Trap_Room
