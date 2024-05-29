#Mysterious Berries event class
import event
import global_commands
import random

success_poison = {
    "int": ["You identify the berries as a poisonous species. Best to steer clear.",
            "Upon closer inspection, you recogize the berries as poisonous. You push your hunger down.",
            "'White and yellow, kill a fellow. Purple and blue, good for you.' You turn away from the tainted meal."],

    "wis": ["You reckon those berries are no good and continue on your way.", "Something tells you that you shouldn't be eating those..."]
}

success_safe = {
    "int": ["You scrutinze the berries closely and detect no abnormalities. These should be safe.", 
            "These berries are identical to a safe species from one ouf your botany textbooks. Good thing you were paying attention."],

    "wis": ["You've seen many a berry in your time, and these look safe.",
            "Your gut is telling you these berries are good. And that you should eat some."]
}

failure = {
    "int": ["What was that rhyme again? Blue and yellow... something something, good for a fellow? You're sure it doesn't matter.", 
            "If only you paid more attention in botany. Oh well...",
            "You squint at the berries trying to glean some kind of information from them, but all you can think about is how long it's been since you've eaten.",
            "You can't recall anything specific about these types of berries."],

    "wis": ["Your gut is telling you... that you're hungry.", "Berries aren't you're strong suite."]
}

end = [
    "You shrug and grab a handful.",
    "Never one to waste a meal, you dig in.",
    "You snatch a bunch for the road as you continue forward.",
    "Food is food. You eat the berries.",
    "Your mother didn't raise you to be picky.",
    "You pop a few in your mouth and move on.",
    "You eat some to ward off hunger.",
]

class Mysterious_Berries(event.Event):

    def __init__(self, id="Mysterious_Berries"):
        super().__init__(id)

        #determines if the berries are poisonous
        self._poisonous = global_commands.probability(50)
        #checks whether the player eats the berries or not

        self.add_stat("int", 1)

        self.add_stat("wis", 20)

        self.add_text("You happen upon some mysterious berries. Your stomach growls...")

        #poison changes the success messages
        if self._poisonous:
            self.add_message(True, success_poison)
        else:
            self.add_message(True, success_safe)

        self.add_message(False, failure)

        self.add_end_message(end)

    def success(self, code:str) -> None:
        self._passed = True
        if self._loot["xp"] <= 0:
            #self.set_xp(int(self.stat_dc(code) / 1.5))
            self.set_xp(10)
        global_commands.type_text(random.choice(self._messages[True][code]) + "\n")#print a random success message
        if self._poisonous:
            global_commands.type_text("You pass on the poisonous snacks.\n")#XP msg comes after this so \n is needed
            return None
        else:
            if self._player.hp < self._player.max_hp:
                global_commands.type_text("Delicious! You can feel your strength returning.\n")#heal msg comes after so \n is needed
                self._player.heal(4)
                print("")#formatting
            else:
                global_commands.type_text("Delicious!\n")
            return None

    def failure(self):
        print("")#formatting
        super().failure()
        print("")#formatting
        if self._poisonous:
            global_commands.type_text("You probably shouldn't have eaten those...\n")#not last item so \n is needed
            if self._player.hp >= 4*2:
                self._player.lose_hp(3)
                global_commands.type_text("The posion berries did 3 damage to you.")
            else:
                global_commands.type_text("You don't feel so good, but nothing bad happened this time.")
            return None
        else:
            if self._player.hp < self._player.max_hp:
                global_commands.type_text("You got lucky. The berries turned out to be edible.\n")#not last item so \n is needed
                self._player.heal(2)
            else:
                global_commands.type_text("You got lucky. The berries turned out to be edible.")#last item so no \n
                self._player.heal(2)
            return None

object = Mysterious_Berries