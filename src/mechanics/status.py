import csv
import globals
import mechanics
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

        self._effect:mechanics.Effect | None = None

        self.switch_word = ""

        self.save_target = 12

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
    def effect(self) -> "mechanics.Effect":
        return self._effect
    
    def start(self):
        self.effect.start()
        globals.type_text(self.start_msg)
        if not self.effect.active:
            self.end()

    def update(self):
        self.effect.update()
        if not self.effect.active:
            self.end()

    def refresh(self):
        globals.type_text(self.refresh_msg)

    def end(self):
        self.effect.duration = 0
        self.effect.end()
        globals.type_text(self.end_msg)

    def save_attempt(self) -> bool:
        return None


class StatModifier(Status):

    def __init__(self, source):
        super().__init__(source)

        self.id = None

        self._effect = mechanics.ModifyStat(self.source)
        self.effect.duration = 3
        self.effect.potency = -3

    def start(self):
        assert self.id is not None
        super().start()

    def refresh(self):
        if self.target.roll_a_check(self.effect.stat) < self.save_target:
            globals.type_text(f"{self.target.header.default} resisted the additional effects!")
        else:
            self.effect.duration += 1

    def acquire(self, src):
        match src:
            case str(): src = self.load_from_csv(src)
            case dict(): pass
            case _: raise ValueError("Incorrect input value for src in StatModifier.acquire.")

        self.copy_from(src)

    def copy_from(self, source_dict):
        self.effect.stat = source_dict["stat"]
        self.id = source_dict["id"]

        if source_dict["potency"] is not None or source_dict["potency"] != '':
            self.effect.potency = int(source_dict["potency"])

    def load_from_csv(self, effect_id) -> dict[str, str]:
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
