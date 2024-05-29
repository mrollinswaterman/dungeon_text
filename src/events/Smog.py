#Smog Cloud Event class
import event

success = {
    "con": ["You grit your teeth and continue forwards.", 
            "You pinch your nose and march in.",
            "You take a deep breath then dive into the cloud."],

    "int": ["With scraps from your gear, you fashion a make-shift face mask and brave the smog.",
            "You study the smog and recoginze it as harmless. Rank, but harmless. You press on without fear."]
}

failure = {
    "con": ["You try holding your breath, but can't make it far enough. You scramble back before you pass out, ready to try again.", 
            "You aren't sure you can just tough this out."],

    "int": ["You can't quite think of a way to navigate this obstacle.",
            "The smog isn't recogizable to you.",
            "You scratch your head and stare at the cloud, trying to figure out if it's dangerous or not. Nothing comes to you."]
}

end = ["You push through the cloud, but not unscathed.",
       "You come out the other side coughing and heaving.",
       "You've made it, but you feel sickly and nauseous."]

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

object = Smog
