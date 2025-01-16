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

class Status(mechanics.Mechanic):
    
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__
        self._source:"game_objects.Game_Object | items.Item" = self.source
        self.source = ""

        self._effects:list[effects.Effect] = []
        self.switch_word = ""
        self.save_DC = 12

    @property
    def base_msg(self) -> str:
        return f"{self.target.header.action} {self.switch_word} {self.id}."

    @property
    def start_msg(self) -> str:
        self.switch_word = "now"
        return self.base_msg

    @property
    def refresh_msg(self) -> str:
        self.switch_word = "already"
        return self.base_msg
    
    @property
    def end_msg(self) -> str:
        self.switch_word = "no longer"
        return self.base_msg

    @property
    def target(self) -> "game_objects.Game_Object":
        src_type = globals.get_base_type(self._source)
        match src_type:
            case "Game_Object": return self._source.target
            case "Item": return self._source.owner.target
            
    @property
    def effects(self) -> list[effects.Effect]:
        return self._effects
    
    def start(self):
        globals.type_text(self.start_msg)
        for effect in self.effects:
            effect.start()
            if not effect.active:
                self._effects.remove(effect)
        if len(self._effects) <= 0:
            self.end()

    def update(self):
        for effect in self.effects:
            if effect.active:
                effect.update()
            elif not effect.active:
                self._effects.remove(effect)

    def refresh(self):
        globals.type_text(self.refresh_msg)

    def end(self):
        globals.type_text(self.end_msg)
        self._effects = []

    def save_attempt(self) -> bool:
        return None

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
