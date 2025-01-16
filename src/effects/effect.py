import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

class Effect(mechanics.Mechanic):
    """
    An effect is a mechanical function that changes a game objects' properties in some way
    """
    def __init__(self, source:"game_objects.Game_Object" | mechanics.Mechanic):
        super().__init__(source)
        self.id = "Effect"
        self.potency = 2

    @property
    def active(self):
        return True
    
    def start(self):
        return True

    def deal_damage(self, amount:int):
        dealt = mechanics.DamageInstance(self.source, amount)
        return self.target.take_damage(dealt)

    def end(self):
        raise NotImplementedError

class Instant_Effect(Effect):
    """
    Instants are (1) time effects. They do one thing then terminate

    Ex. Single instance of damage, gaining temp hp, a draining attack
    """
    def __init__(self, source):
        super().__init__(source)
        self.id = "Instant"

    @property
    def active(self):
        return False
    
    def end(self):
        return None

class Constant_Effect(Effect):
    """
    Constants are similar to instants except they're effect linger until specifically dispelled

    Ex. buffing/debuffing a stat, changing a game object's method, 
    """
    def __init__(self, source):
        super().__init__(source)
        self.id = "Constant"
        self.duration = float('inf')

    @property
    def active(self):
        return self.duration > 0
    
    def update(self):
        self.duration -= 1
        if not self.active:
            self.end()

    def end(self):
        self.duration = 0


class Repeated_Effect(Effect):
    """
    Statuses are effects that do something each turn cycle, usually damage. They are similar
    to constant effects, except that their update involves more than just ticking duration down
    """
    def __init__(self, source):
        super().__init__(source)
        self.id = "Repeated"
        self.duration = 2

    @property
    def active(self):
        return self.duration > 0
    
    def update(self):
        self.duration -= 1
        if not self.active:
            self.end()

    def end(self):
        self.duration = 0