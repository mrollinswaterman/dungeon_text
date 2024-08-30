#status effects file
import global_commands

class Status_Effect():
    def __init__(self, src, target, id):
        import global_variables, player, mob
        #SRC is a global_variables.PLAYER or mob object
        self._id = id
        self._src = src
        self._target:player.Player | mob.Mob = target
        self.player = False
        if self._target == global_variables.PLAYER:
            self.player = True
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
    @property
    def damage_header(self):
        return self._id
    
    #methods
    def update_message(self):
        pass

    def update(self) -> None:
        if self._active:
            self._duration -= 1
            if self._duration <= 0:
                self._duration = 0
                self._active = False

    def apply(self) -> None:
        self.update_message()
        global_commands.type_text(self._message)

    def set_potency(self, num:int) -> None:
        self._potency = num
        self.update_message()

    def set_stacks(self) -> None:
        raise NotImplementedError

    def set_duration(self, num:int) -> None:
        self._duration = num
        self.update_message()

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

