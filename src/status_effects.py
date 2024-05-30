#status effects file
import random
import global_commands

PLAYER = None

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

    def set_target(self, tar):
        self._target = tar

    def additional_effect(self, effect:"Status_Effect"):
        return None

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
    def __init__(self, src, target=PLAYER, id="On Fire"):
        super().__init__(src, target, id)
        if target is None:
            self._target = PLAYER
        self._target_header = "You are"
        if self._target != PLAYER:
            self._target_header = f"The {self._target.id} is"
        self._message = f"{self._target_header} now {id}."
        self._cleanse_message = f"{self._target_header} not longer {id}.\n"
    
    def update(self):
        self._duration -= 1
        taken = self._target.take_damage(self._potency, True)
        if self._target != PLAYER:
            global_commands.switch(self._target.header, f"The {self._target.id} took {taken} damage from from the fire.\n")
            self._target.set_header(True)
        else:
            global_commands.type_text(f"You took {taken} damage from the fire.\n")

        if self._duration <= 0:
            self._active = False
    
    def additional_effect(self, effect: Status_Effect):
        global_commands.type_text("More fire has no effect.\n")

class Poisoned(Status_Effect):
    def __init__(self, src, target=PLAYER, id="Poisoned"):
        super().__init__(src, target, id)
        if target is None:
            self._target = PLAYER
        self._stacks = 0
        self._target_header = "You are"
        if self._target != PLAYER:
            self._target_header = f"The {self._target.id} is"

        self._message = f"{self._target_header} now {id}."
        self._cleanse_message = f"{self._target_header} no longer {self._id}."

    @property
    def stacks(self):
        return self._stacks

    def set_stacks(self, num:int):
        self._stacks = num
        self._duration = self._stacks
    
    def additional_effect(self, effect):
        self._potency += effect.duration
        global_commands.type_text("The poison's effect becomes more severe...\n")
        return None

    def update(self):
        self._duration -= 1
        damage = self._potency * self._stacks
        self._stacks -= 1
        if self._target.roll_a_check("con") >= damage * self._potency:
            damage //= 2
        self._target.take_damage(damage, True)
        if self._target != PLAYER:
            global_commands.switch(self._target.header, f"The {self._target.id} took {damage} damage from from the poison.\n")
            self._target.set_header(True)
        else:
            global_commands.type_text(f"You took {damage} damge from the poison.\n")
        if self._duration <= 0:
            self._stacks = 0
            self._active = False
    
    def attempt_cleanse(self, roll: int = 0):
        if roll >= self._potency * 2 * self._stacks:
            self.cleanse()
        else:
            if self._target != PLAYER:
                global_commands.switch(self._target.header, f"The {self._target.id} failed to cleanse the poison.\n")
                self._target.set_header(True)
            else:
                global_commands.type_text(f"You failed to cleanse the poison.\n")

    def cleanse(self) -> None:
        self._active = False
        self._duration = 0
        self._stacks = 0
        if self._target != PLAYER:
            global_commands.switch(self._target.header, self._cleanse_message)
            self._target.set_header(True)
        else:
            global_commands.type_text(self._cleanse_message)
        return None
    
    def apply(self) -> None:
        global_commands.type_text(self._message)

class Stat_Buff(Status_Effect):
    def __init__(self, src, target=PLAYER, id="Buff"):
        super().__init__(src, target, id)
        if target is None:
            self._target = PLAYER
        self._stat = ""
        self._id = self._stat +" " + id
        self._target_header = f"Your"
        if self._target != PLAYER:
            self._target_header = f"The {self._target.id}'s"

    @property
    def stat(self) -> str:
        return self._stat

    def set_stat(self, stat:str) -> None:
        self._stat = stat
        self._id = f"{stat} {self._id}"
        self._message = f"{self._target_header} {global_commands.TAG_TO_STAT[self._stat]} increased by {self._potency}."
        self._cleanse_message = f"{self._target_header} {global_commands.TAG_TO_STAT[self._stat]} has returned to normal."

    def apply(self):
        super().apply()
        self._target.stats[self._stat] += self._potency

    def cleanse(self) -> None:
        self._target.stats[self._stat] -= self._potency
        super().cleanse()
    
    def additional_effect(self, effect: Status_Effect):
        self.apply()
        return None

class Stat_Debuff(Stat_Buff):
    def __init__(self, src, target=PLAYER, id="Debuff"):
        super().__init__(src, target, id)

    def apply(self):
        super().apply()
        self._target.stats[self._stat] -= self._potency

    def set_stat(self, stat: str) -> None:
        super().set_stat(stat)
        self._message = f"{self._target_header} {global_commands.TAG_TO_STAT[self._stat]} is being decreased by {self._potency}."

class Entangled(Status_Effect):

    def __init__(self, src, target=PLAYER, id="Entangled"):
        """
        Init function for Entangled status effect

        target_header and cleanse_header change based on the target of the effect,
        either the Player or a mob, and head the self._message and cleanse function text ouput.
        """
        super().__init__(src, target, id)
        if target is None:
            self._target = PLAYER
        self._stat = "ap"
        self._target_header = "You are"
        self._cleanse_header = "You try"
        if self._target != PLAYER:
            self._target_header = f"The {self._target.id} is"
            self._cleanse_header = f"The {self._target.id} tries"

        self._message = f"{self._target_header} now {id}."
        self._cleanse_message = f"{self._target_header} no longer {id}."
        self._cleanse_stat = "str"

    def apply(self):
        super().apply()
        self._target.stats[self._stat] -= self._potency

    def cleanse(self):
        self._src._applied_status_effects.remove(self)
        self._target.stats[self._stat] += self._potency
        super().cleanse()

    def attempt_cleanse(self, roll: int = 0) -> bool:
        global_commands.type_with_lines(f"{self._cleanse_header} to break free of the entanglement...\n")
        if roll >= self._src.dc - 2:
            global_commands.type_text("Success!\n")
            return self._target.remove_status_effect(self)
        global_commands.type_text("No luck.\n")
        return False
    
    def additional_effect(self, effect: Status_Effect):
        global_commands.type_text("The entanglment's duration grows...\n")
        self._duration += 1
        return None

class Vulnerable(Stat_Buff):
    """
    Makes the target vulnerable,
    meaning they take x2 damage for the duration
    """
    def __init__(self, src, target=PLAYER, id="Vulnerable"):
        super().__init__(src, target, id)
        if target is None:
            self._target = PLAYER
        self._target_header = "You are"
        if self._target != PLAYER:
            self._target_header = f"The {self._target.id} is "

        self._message = f"{self._target_header} now {self._id}."

        if target == src and self._target != PLAYER:
            self._message = f"The {self._target.id} made itself {self._id}"
        elif target == src:
            self._message = f"You made yourself {self._id}"

        self._cleanse_message = f"{self._target_header} no longer {self._id}."
        self._stat = "damage-taken-multiplier"
        self._potency = 1# this is because the apply function adds to the stat,
        #so a potency of 2 would result in a damage-taken of 3, not 2 like we want

    def additional_effect(self, effect: Status_Effect):
        self._potency += 1#might need re-balancing
    
