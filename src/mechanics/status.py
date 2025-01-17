import csv
import effects.constant_effects
import globals
import mechanics
import effects
#import game_objects
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import items

class StatModifier(Status):

    def __init__(self, source):
        super().__init__(source)
        self.id = None
        self._effects = [effects.ModifyStat(self.source)]
        self.effect.duration = 3
        self.effect.potency = -3

    @property
    def effect(self) -> effects.ModifyStat:
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
