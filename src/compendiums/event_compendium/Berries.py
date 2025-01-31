#Mysterious Berries event class
import globals
import game
import game_objects


class Berries(game_objects.Event):

    def __init__(self):
        super().__init__()

        #determines if the berries are poisonous
        self._poisonous = globals.probability(1)

        self.stats["int"] = 15
        self.stats["wis"] = 20

    def end(self):
        if self._poisonous: 
            return self.message("end_poisonous")
        else:
            return self.message("end")

    def success(self) -> bool:
        self.end()
        if self._poisonous: 
            return True
        else: 
            if game.PLAYER.heal(4) > 0:
                globals.type_text("Delicious! You can feel your strength returning.")
            else:
                globals.type_text("Delicious!")
        return True

    def message(self, msg_type:str, stat:str=None) -> None:
        if msg_type == "success":
            if self._poisonous: 
                return super().message("success_poisonous", stat)
            else: 
                return super().message("success_safe", stat)
            
        else:
            return super().message(msg_type, stat)

    def failure(self) -> bool:
        super().failure()
        if self._poisonous:
            globals.type_text("You probably shouldn't have eaten those...")

            if game.PLAYER.hp > 8:
                game.PLAYER.lose_hp(3)
                globals.type_text("The posion berries did 3 damage to you.")
            else:
                globals.type_text("You don't feel well, but nothing bad happened... this time.")
        
        else:
            globals.type_text("You got lucky. The berries turned out to to be edible.")
            game.PLAYER.heal(2)

        return False

object = Berries