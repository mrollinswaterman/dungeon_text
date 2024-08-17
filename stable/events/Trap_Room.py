#Trap Room Event class
import random
import global_commands
import event

start = [
    "As you're walking away, you hear a slight click, then a whistling sound.",
    "The ground shifts slightly benath you, and suddenly a gout of flames bursts forth from the wall beside you.",
    "The floor you're on begins open, revealing a pit of deadly spikes."
]

success = {
    "dex": ["You deftly avoid the nasty surprise.",
            "Your instincts take you out of harms' way.",
            "Good thing you're always on edge, or things might have gone badly.",
            "Your training kicks in and manage to slip away without a scratch"]
}

failure = {
    "dex": ["You duck and dodge, but not quite fast enough. Luckily, you're only hurt.",
            "Your skills weren't enough this time. The trap left its mark on you.",
            "You move, but a littel too late. You're alive, but just barely.",
            "As you nurse your injury, you vow never to fall asleep at the wheel like that again."]
}

class Trap_Room(event.Event):

    def __init__(self, id="Trap Room"):
        super().__init__(id)

        self.add_stat("dex", 15)

        self.add_text(random.choice(start))

        self.add_message(True, success)

        self.add_message(False, failure)

        self._damage_cap = 7 + self._player.level // 3

        self._damage_header = "Dwarven trap"

    @property
    def damage_type(self) -> str:
        return "Physical"

    def success(self, code:str="dex") -> None:
        self._passed = True
        if self._loot["xp"] <= 0:
            self.set_xp(int(self.stat_dc(code) / 1.5))
        global_commands.type_text(random.choice(self._messages[True][code]))#print a random success message

    def failure(self):
        self._tries = -1
        global_commands.type_text(random.choice(self._end_messages))
        
    def run(self, code:str="dex"):
        dmg = 0
        roll = self._player.roll_a_check(code)
        if roll >= self.stat_dc(code):
            self.success(code)
            return None
        self.try_again(code)
        diff = ((self.stat_dc(code) - roll) + 1) // 2
        for _ in range(diff):
            dmg += 1
        
        if roll == 0:
            dmg = self._damage_cap

        taken = self._player.take_damage(min(dmg, self._damage_cap), self)
        return None

object = Trap_Room
