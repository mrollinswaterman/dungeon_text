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
        self._active = True

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def src(self):
        return self._src
    @property
    def potency(self) -> int:
        return self._potency
    @property
    def duration(self) -> int:
        return self._duration
    @property
    def target(self):
        return self._target
    @property
    def message(self):
        return self._message
    @property
    def active(self):
        return self._active
    @property
    def cleanse_stat(self):
        return self._cleanse_stat
    
    #methods
    def update(self) -> None:
        self._duration -= 1
        if self._duration <= 0:
            self._duration = 0
            self._active = False

    def apply(self) -> None:
        """
        Types the effect's apply message
        """
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
        """
        Sets the effect's duration to 0, and
        sets the effect's active property to False and
        types the effect's cleans message
        """
        self._duration = 0
        self._active = False
        global_commands.type_text(self._cleanse_message)
        return None

    def attempt_cleanse(self, roll:int = 0):
        raise NotImplementedError

class On_Fire(Status_Effect):

    def __init__(self, src, target, id="On Fire"):
        super().__init__(src, target, id)
        self._message = f"The {self._target} is now {id}."
        self._cleanse_message = f"The {self._target} is not longer {id}."
    
    def update(self):
        self._duration -= 1

        taken = self._target.take_damage(self._potency, True)

        global_commands.type_text(f"The {self._target} took {taken} damage from from the fire.\n")

        if self._duration <= 0:
            self._target.remove_status_effect(self)
    
    def attempt_cleanse(self) -> bool:
        global_commands.type_text(" You put out the fire.\n")
        return self._target.remove_status_effect(self)

class Stat_Buff(Status_Effect):

    def __init__(self, src, target, id="Buff"):
        super().__init__(src, target, id)
        self._stat = ""
        self._id = self._stat + id
        self._message = f"Your {self._stat} is being increased by {self._potency} by the {self._src}'s {self._id}."
        self._cleanse_message = f"Your {self._stat} has returned to normal."

    @property
    def stat(self) -> str:
        return self._stat

    def set_stat(self, stat:str) -> None:
        self._stat = stat
        self._id = stat + self._id

    def apply(self):
        super().apply()
        self._target.stats[self._stat] += self._potency
        print(self._target.stats[self._stat])

    def cleanse(self) -> None:
        self._target.stats[self._stat] -= self._potency
        super().cleanse()

class Stat_Debuff(Stat_Buff):
    def __init__(self, src, target, id="Debuff"):
        super().__init__(src, target, id)
        self._message = f"Your {self._stat} is being decreased by {self._potency} by the {self._src.id}'s {self._id}."

    def apply(self):
        super().apply()
        self._target.stats[self._stat] -= self._potency
        print(self._target.stats[self._stat])

class Entangled(Status_Effect):

    def __init__(self, src, target, id="Entangled"):
        super().__init__(src, target, id)
        self._stat = "ap"
        self._message = f"You are now {id}."
        self._cleanse_message = f"You are no longer {id}."
        self._cleanse_stat = "str"

    def apply(self):
        super().apply()
        self._target.stats[self._stat] -= self._potency

    def cleanse(self):
        self._src._applied_status_effects.remove(self)
        self._target.stats[self._stat] += self._potency
        super().cleanse()

    def attempt_cleanse(self, roll: int = 0) -> bool:
        global_commands.type_with_lines("You try to break free of your entanglement...\n")
        if roll >= self._src.dc - 2:
            global_commands.type_text("You succeed!\n")
            return self._target.remove_status_effect(self)
        global_commands.type_text("You failed.\n")
        return False

class Vulnerable(Stat_Debuff):

    def __init__(self, src, target, id="Vulnerable"):
        super().__init__(src, target, id)

        self._message = f"You are now {self._id}."
        self._cleanse_message = f"You are no longer {self._id}."
        self._stat = "damage-taken-multiplier"
        self._potency = -1