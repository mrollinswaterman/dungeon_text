#Smog Cloud Event class
import game
import game_objects
import globals
import mechanics

class Smog(game_objects.Event):
    def __init__(self):
        super().__init__()
        self.stats["con"] = 15
        self.stats["int"] = 21

        self.damage_type = mechanics.DamageType()
        self.damage_type.set(["Physical"])

        self.header = game_objects.Header(self)
        self.header._damage = "the poisonous smog"
        self.header._default = "the poisonous smog"

    def failure(self):
        super().failure()
        poison = globals.create_status("poisoned", self)
        game.PLAYER.apply(poison)

object = Smog
