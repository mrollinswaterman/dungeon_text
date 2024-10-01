import random
from trick import Combat_Trick

class Study_Weakness(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent, parent)
        texts = [
            f"You study the {self.parent.target.id} for weak points.",
            f"You search for ways to make your attacks more deadly.",
            f"You assess your opponent for vulnerabilities."
        ]
        self.start_message = random.choice(texts)

    def start(self):
        self.parent.spend_ap()
        super().start()
        self.parent._bonus_crit_range += 2
        self.end()

object = Study_Weakness
