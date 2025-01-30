#Mysterious Berries event class
import random
import globals
import game_objects.event as event
import game


class Berries(event.Event):

    def __init__(self, id="Berries"):
        super().__init__(id)

        #determines if the berries are poisonous
        self._poisonous = globals.probability(50)

        self.stats["int"] = 15
        self.stats["wis"] = 20

    def success(self):
        if self._poisonous: 
            self.message("end_poisonous")
            return True
        else: 
            self.message("end")
            if game.PLAYER.heal(4) > 0:
                globals.type_text("Delicious! You can feel your strength returning.")
            else:
                globals.type_text("Delicious!")
        return True

    def message(self, msg_type:str, stat:str=None):
        if msg_type == "success":
            if self._poisonous: return super().message("success_poisonous", stat)
            else: return super().message("success_safe", stat)

    def failure(self):
        print("")#formatting
        super().failure()
        print("")#formatting
        if self._poisonous:
            functions.type_text("You probably shouldn't have eaten those...")
            if self._player.hp >= 4*2:
                self._player.lose_hp(3)
                functions.type_text("The posion berries did 3 damage to you.")
            else:
                functions.type_text("You don't feel so good, but nothing bad happened this time.")
            return None
        else:
            if self._player.hp < self._player.max_hp:
                functions.type_text("You got lucky. The berries turned out to be edible.")
                self._player.heal(2)
            else:
                functions.type_text("You got lucky. The berries turned out to be edible.")
                self._player.heal(2)
            return None

object = Berries