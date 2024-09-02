#Smog Cloud Event class
import event
import status_effect

success = {
    "con": ["You grit your teeth and continue forwards, making it out without a scratch.", 
            "A little noxious gas is nothing to you. You pinch your nose and march across.",
            "You take a deep breath and dive through the cloud.",
            "As you make your way through, you begin to feel nauseous. You shake it off and press on."],

    "int": ["With scraps from your gear, you fashion a make-shift face mask and brave the smog.",
            "You study the smog and recoginze it as harmless. Rank, but harmless. You continue without fear."]
}

failure = {
    "con": ["You don't reckon you can hold your breath long enough to get out the other side.", 
            "You might not be tough enough for this yet.",
            "Approaching the cloud, you shrink away in disgust. You've never been a fan of repugnant stenches."],

    "int": ["You can't yet think of a way to navigate this obstacle.",
            "The smog isn't recogizable to you.",
            "You scratch your head and stare at the cloud, trying to figure out if it's dangerous or not. Nothing comes to you."]
}

end = ["No way to go but straight. You make it out the other side, but not unscathed.",
       "You push through the cloud head on, coughing and heaving all the way. You don't feel so good...",
       "You decide to tackle this obstacle head on. Not the best idea, but you're through it now."]

class Smog(event.Event):
    def __init__(self, id="Smog"):
        super().__init__(id)

        self.add_stat("con", 15)

        self.add_stat("int", 21)

        #event text
        self.add_text("The path before you is filled with a foul smelling smog.")

        #success lines
        self.add_message(True, success)

        #failure lines
        self.add_message(False, failure)

        #out of tries
        self.add_end_message(end)

    def failure(self):
        super().failure()
        #poison:status_effect.Status_Effect = Poisoned.Condition(self)
        #poison.set_stacks(3)
        #poison.set_potency(1)
        #self._player.add_status_effect(poison)

object = Smog
