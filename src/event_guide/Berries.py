#Mysterious Berries event class
import events
import global_commands

success_poison = {
    "int": ["You identify the berries as a poisonous species. Best to steer clear.",
            "Upon closer inspection, you recogize the berries as poisonous. You push your hunger down.",
            "White and yellow, kill a fellow. Purple and blue, good for you. You turn away from the tainted meal."],

    "wis": ["You reckon those berries are no good and continue on your way.", "Something tells you that you shouldn't be eating those..."]
}

success_safe = {
    "int": ["You scrutinze the berries closely. After detecting no abnormalities, you pop a few in your mouth and continue on.", 
            "These berries are identical to a safe species from one ouf your botany textbooks. Good thing you were paying attention. You eat a few to ward off hunger."],

    "wis": ["You've seen many a barry in your time, and these look safe. You take a few tentative bites. After nothing happens, you breathe a sigh of relief.",
            "Your gut is telling you these berries are good. And that you should eat some. You oblige."]
}

failure = {
    "int": ["What was that rhyme again? Blue and yellow... something something, good for a fellow? You're sure it doesn't matter.", 
            "If only you paid more attention in botany. Oh well, better get 'em while they're fresh.",
            "You squint at the berries trying to recall any information about them, but all you can think about is how long it's been since you've eaten."],

    "wis": ["Your gut is telling you... that you're hungry.", "Berries aren't you're strong suite."]
}

end = [
    "You shrug and grab a handful.",
    "Never one to waste a meal, you dig in.",
    "You snatch a few for the road as you continue on.",
    "Food is food. You eat the berries.",
    "Mama didn't raise no picky eater."
]

class Mysterious_Berries(events.Event):

    def __init__(self):
        super().__init__()

        self._poisonous = global_commands.probability(50)

        self.add_stat(("int", 15))
        self.add_stat(("wis", 20))

        self.add_text(" You happen upon some mysterious berries. They look delicious...")

        if self._poisonous:
            self.add_message(True, success_poison)
        else:
            self.add_message(True, success_safe)

        self.add_message(False, failure)

        self.add_end_message(end)
    
