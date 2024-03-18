#status effects file
import random
import global_commands

class Status_Effect():

    def __init__(self, id, src, target):
        #SRC is a player or mob object
        self._id = id
        self._src = src
        self._potency = 0
        self._duration = 0
        self._stat = None
        self._target = target
        self._message:str = ""
        self._active = True

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def src(self):
        return self._src
    @property
    def power(self) -> int:
        return self._power
    @property
    def duration(self) -> int:
        return self._duration
    @property
    def stat(self) -> str:
        return self._stat
    @property
    def target(self):
        return self._target
    @property
    def message(self):
        return self._message
    @property
    def active(self):
        return self._active
    
    #methods
    def update(self) -> None:
        raise NotImplementedError

    def apply(self) -> None:
        raise NotImplementedError

    def set_power(self, num:int) -> None:
        self._power = num

    def set_duration(self, num:int) -> None:
        self._duration = num

    def set_message(self, msg:str) -> None:
        self._message = msg

    def cleanse(self) -> None:
        self._duration = 0
        self._active = False


class On_Fire(Status_Effect):

    def __init__(self, src=None, target=None, id="On Fire"):
        super().__init__(id, src, target)

    
    def update(self):
        self._duration -= 1

        taken = self._target.take_damage(self._power, True)

        global_commands.type_text(f" The {self._target} took {taken} damage from from the fire.\n")

        if self._duration <= 0:
            self.cleanse()

class Stat_Buff(Status_Effect):

    def __init__(self, src=None, target=None, stat="", id="Buff"):
        super().__init__(id, src, target)

        self._stat = stat
        self._id = self._stat + id

        self._message = f" Your {self._stat} is being increased by {self._power} by the {self._src}'s {self._id}"

    @property
    def stat(self) -> str:
        return self._stat
    
    def update(self):
        self._duration -= 1
        self._target.stats[self._stat] += self._power

        if self._duration <= 0:
            self._active = False

    def cleanse(self) -> None:
        self._duration = 0
        self._active = False
        self._target.stats[self._stat] -= self._power

class Stat_Debuff(Stat_Buff):
    def __init__(self, src=None, target=None, stat="", id="Debuff"):
        super().__init__()

        self._power = -self._power

        self._message = f" Your {self._stat} is being decreased by {self._power} by the {self._src}'s {self._id}"