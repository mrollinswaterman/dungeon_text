import effects
import csv

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

class StatModifier(effects.Constant_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.id = None
        self._effects = [effects.ModifyStat(self.source)]
        self.effect.duration = 3
        self.effect.potency = -3

    @property
    def effect(self) -> "effects.ModifyStat":
        return self._effects[0]

    def start(self):
        assert self.id is not None
        super().start()

    def refresh(self):
        if self.target.roll_a_check(self.effect.stat) < self.save_DC:
            globals.type_text(f"{self.target.header.default} resisted the additional effects!")
        else:
            self.effect.duration += 1

    def acquire(self, src):
        """
        Alters this object instance to match the desired status based on src input

        src can be either a str, in which case load_from_csv is called, or a dictionary
        """
        match src:
            case str(): src = self.load_from_csv(src)
            case dict(): pass
            case _: raise ValueError("Incorrect input value for src in StatModifier.acquire.")

        self.copy_from(src)

    def copy_from(self, source_dict):
        """
        Copies the appropriate info (effected stat, id, etc) from source dictionary
        to this object
        """
        self.effect.stat = source_dict["stat"]
        self.id = source_dict["id"]

        if source_dict["potency"] is not None or source_dict["potency"] != '':
            self.effect.potency = int(source_dict["potency"])

    def load_from_csv(self, effect_id) -> dict[str, str]:
        """
        Attempts to retrieve the source dictionary of a given effect id (weakend, slowed, etc) from
        the statuses csv file. Will raise an error if nothing is found.
        """
        ret = None
        with open("statuses.csv", "r+") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] == effect_id:
                    ret = row
                    break
        file.close()

        if ret is None: raise ValueError(f"Unknown Status '{effect_id}'.")

        return ret

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
