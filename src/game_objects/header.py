from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

class Header():
    """Header class, controls which text is used to describe a GameObject
        3 types: default, action, ownership"""

    def __init__(self, parent:"game_objects.Game_Object"):
        self.parent = parent
        self._default:str = f"The {self.parent.id}"
        self._action:str = f"The {self.parent.id} is"
        self._ownership:str = f"The {self.parent.id}'s"
        self.damage:str = self._default

        self.prev = ""

    @property
    def default(self):
        if self.prev != self._default:
            self.prev = self._default
            return self._default
        else:
            self.prev = "It"
            return self.prev
        
    @property
    def action(self):
        if self.prev != self._action:
            self.prev = self._action
            return self._action
        else:
            self.prev = "It's"
            return self.prev

    @property
    def default(self):
        if self.prev != self._ownership:
            self.prev = self._ownership
            return self._ownership
        else:
            self.prev = "Its"
            return self.prev
