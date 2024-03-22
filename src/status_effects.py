#status effects file
import random
import global_commands

class Status_Effect():

    def __init__(self, src, target, id):
        #SRC is a player or mob object
        self._id = id
        self._src = src
        self._target = target
        self._potency = 1
        self._duration = 0
        self._message:str = ""
        self._cleanse_message:str = ""
        self._cleanse_stat = None
        self._cleanse_option = ""
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
        self._duration -= 1
        if self._duration <= 0:
            self._duration = 0
            self._active = False

    def apply(self) -> None:
        global_commands.type_text(self._message)

    def set_potency(self, num:int) -> None:
        self._potency = num

    def set_duration(self, num:int) -> None:
        self._duration = num

    def set_message(self, msg:str) -> None:
        self._message = msg

    def set_cleanse_message(self, msg:str) -> None:
        self._cleanse_message = msg
    
    def set_id(self, id:str="") -> None:
        self._id = id

    def cleanse(self) -> None:
        self._duration = 0
        self._active = False
        global_commands.type_with_lines(self._cleanse_message)

class On_Fire(Status_Effect):

    def __init__(self, src=None, target=None, id="On Fire"):
        super().__init__(src, target, id)
        self._message = f" The {self._target} is now {id}."
        self._cleanse_message = f" The {self._target} is not longer {id}."
        self._cleanse_option = f" Remove {id} - (r)"
    
    def update(self):
        self._duration -= 1

        taken = self._target.take_damage(self._potency, True)

        global_commands.type_text(f" The {self._target} took {taken} damage from from the fire.\n")

        if self._duration <= 0:
            self.cleanse()

class Stat_Buff(Status_Effect):

    def __init__(self, src=None, target=None, id="Buff"):
        super().__init__(src, target, id)
        self._stat = ""
        self._id = self._stat + id
        self._message = f" Your {self._stat} is being increased by {self._potency} by the {self._src}'s {self._id}."
        self._cleanse_message = f" Your {self._stat} has returned to normal."

    @property
    def stat(self) -> str:
        return self._stat

    def set_stat(self, stat:str) -> None:
        self._stat = stat
        self._id = stat + self._id

    def apply(self):
        super().apply()
        self._target.stats[self._stat] += self._potency

    def cleanse(self) -> None:
        super().cleanse()
        self._target.stats[self._stat] -= self._potency

class Stat_Debuff(Stat_Buff):
    def __init__(self, src=None, target=None, id="Debuff"):
        super().__init__(src, target, id)
        self._potency = -self._potency
        self._message = f" Your {self._stat} is being decreased by {self._potency} by the {self._src.id}'s {self._id}."

class Entangled(Status_Effect):

    def __init__(self, src=None, target=None, id="Entangled"):
        super().__init__(src, target, id)
        self._stat = "ap"
        self._message = f" You are now {id}."
        self._cleanse_message = f" You are no longer {id}."
        self._cleanse_option = f" Remove {id} - ({id[0].lower()})"
    
    def apply(self):
        super().apply()
        self._target.stats[self._stat] -= self._potency
        self._target.reset_ap()

    def cleanse(self):
        super().cleanse()
        self._src._applied_status_effects.remove(self)
        self._target.stats[self._stat] += self._potency
        self._target.reset_ap()
