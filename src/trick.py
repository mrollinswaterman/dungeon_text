import global_commands
from game_object import Game_Object

class Combat_Trick():

    def __init__(self, parent:Game_Object, target:Game_Object=None):
        from effects import MethodReplacement
        self.id = self.__class__.__name__
        self.parent = parent
        self.target = target

        self.start_message:str = ""
        self.end_message:str = ""

        self.replace_effect = MethodReplacement(self, target)

    def update(self) -> None:
        self.replace_effect.update()
        if not self.replace_effect.active:
            self.end()

    def start(self) -> None:
        global_commands.type_text(self.start_message)
        self.replace_effect.start()

    def end(self) -> None:
        global_commands.type_text(self.end_message)
        self.replace_effect.end()
        self.parent.combat_trick = None
