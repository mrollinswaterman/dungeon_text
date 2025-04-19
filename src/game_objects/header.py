import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import effects

class Header():
    """
    A Header controls which text is used for a GameObject when the TUI needs to describe or reference it.

    There are currently 4 types:
        Default = the normal (eg. "you" for the player or "the monster" for a monster)
        
        Action = When the TUI needs to communicate that the object is doing something (eg. "You are")

        Ownership = When the TUI needs to communicate that something belongs to the object (eg. "Your")

        Damage = When the TUI needs to communicate that the object dealt some damage. 
        Is set to Default by default can be changed (eg. Instead of "The On_fire" for the 'On_Fire'
        status effect it would say "the fire")
    """

    def __init__(self, parent:"game_objects.Game_Object | effects.Status_Effect"):
        self.parent = parent
        self._default:str = f"the {self.parent.id}"
        self._action:str = f"the {self.parent.id} is"
        self._ownership:str = f"the {self.parent.id}'s"
        self._tries = [f"the {self.parent.id} attempts", f"the {self.parent.id} tries"]
        self._damage:str = None

        self.alt = True

        self.prev = ""

    @property
    def default(self):
        if self.alt: return "it"
        return self._default
        
    @property
    def action(self):
        if self.alt: return "it's"
        return self._action

    @property
    def ownership(self):
        if self.alt: return "its"
        return self.ownership
        
    @property
    def tries(self):
        if self.alt: return random.choice(["it tries", "it attempts"])
        return self.tries
        
    @property 
    def damage(self):
        if self._damage is None: 
            return self.default
        else:
            return self._damage
