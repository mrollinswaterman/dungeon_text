import effects
from typing import TYPE_CHECKING

from effects import effect
if TYPE_CHECKING:
    import game_objects

class ModifyStat(effects.Constant_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.stat:str = ""
        self.duration = float('inf')

    def start(self):
        self.potency = globals.XdY(self.potency)
        try:
            self.target.stats.modify(self.stat, self.potency)
        except KeyError:
            raise ValueError(f"Can't modify non-existent stat '{self.stat}'.")

        polarity = "increased" if self.potency > 0 else "decreased"
        text = f"{self.target.header.ownership} {globals.STATS[self.stat]} {polarity} by {abs(self.potency)}."

        globals.type_header(text)

    def end(self):
        self.target.stats.modify(self.stat, -(self.potency))
        globals.type_header(f"{self.target.header.ownership} {globals.STATS[self.stat]} returned to normal.")
        super().end()

class MethodReplacement(effects.Constant_Effect):
    
    def __init__(self, source, target:"game_objects.Game_Object"):
        super().__init__(source)
        self._target = target
        self.duration = float('inf')
        self.default:function = None
        self.replacement_target = ""

    @property
    def target(self):
        return self._target

    def start(self):
        self.target.__setattr__(self.replacement_target, self.source.__getattribute__("replacement_method"))

    def replacement_method(self):
        raise NotImplementedError

    def end(self):
        self.target.__setattr__(self.replacement_target, self.source.__getattribute__("default"))
        super().end()
