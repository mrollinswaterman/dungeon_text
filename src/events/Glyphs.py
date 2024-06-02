#Glyphs event class
import event
import global_commands
from events import Trap_Room
import random

success = {
    "int": ["You recognize the signs as Elvish. They warn of a trap room a litte further ahead. You boldly go the other direction.",
            "The glyphs are a message from a Fae adventurer who once walked your path. Armed with this knowledge, you can now avoid the dangers ahead.",
            "You decipher the glyphs to find they are a Dwarven instruction manual, detailing how to avoid the upcoming traps.",
            "Your Eastern Gnomish is a bit rusty, so you can't decipher all of it, but you make out enough to dodge some trouble ahead."]
}

failure = {
    "int": ["These symbols are unrecognizable to you.",
            "You can barley make out what the glyphs are depicting, let alone what they mean.",
            "You think they migh be Fae... or maybe some dialect of Archaic Dwarvish? You really should have been paying more attention in Ancient Linguistics.",
            "You try focusing on the glyphs, but are soon bored.",
            "All you can make out is something about... breadloaves?"]
}

end = [
    "You've stared at these pictures long enough. Time to move on.",
    "You gave it your best shot, better keep moving.",
    "You don't like standing still for too long. You give the glyphs one last look, then leave.",
    "If you can't understand them, they probably weren't worth translating in the first place. Right?",
    "You're fairly confident the glyphs are just meaningless scribbles anyway. You push them out of your mind and you continue your journey.",
]

class Glyphs(event.Event):

    def __init__(self, id="Glyphs"):
        super().__init__(id)

        self.add_stat("int", 15)

        self.add_text("The wall before you is covered in near-illegible glyphs.")

        self.add_message(True, success)

        self.add_message(False, failure)

        self.add_end_message(end)

    def success(self, code:str) -> None:
        self._passed = True
        if self._loot["xp"] <= 0:
            self.set_xp(int(self.stat_dc(code) / 1.5))
        global_commands.type_text(random.choice(self._messages[True][code]))#print a random success message

    def failure(self):
        self._tries = -1
        global_commands.type_text(random.choice(self._end_messages))
        global_commands.type_with_lines("")
        trap:event.Event = Trap_Room.Trap_Room()
        trap.start()
        trap.run()
        return None

object = Glyphs
