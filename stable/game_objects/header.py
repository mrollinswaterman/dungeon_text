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

    def __init__(self, parent:"game_objects.Game_Object | effects.StatusEffect"):
        self.parent = parent
        self._default:str = f"the {self.parent.id}"
        self._action:str = f"the {self.parent.id} is"
        self._ownership:str = f"the {self.parent.id}'s"
        self._damage:str = None

        self.prev = ""

    @property
    def default(self):
        if self.prev != self._default:
            self.prev = self._default
            return self._default
        else:
            self.prev = "it"
            return self.prev
        
    @property
    def action(self):
        if self.prev != self._action:
            self.prev = self._action
            return self._action
        else:
            self.prev = "it's"
            return self.prev

    @property
    def ownership(self):
        if self.prev != self._ownership:
            self.prev = self._ownership
            return self._ownership
        else:
            self.prev = "its"
            return self.prev
        
    @property 
    def damage(self):
        if self._damage is None: 
            return self.default
        else:
            return self._damage
