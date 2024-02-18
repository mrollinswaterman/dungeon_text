
from typing import Optional
import random

FAILURE_LINES = {
    "str": [
        f"\nYou're going to need more than brawn to solve this one.\n"
    ],

    "dex": [
        f"\nYou do a sick spin move. Nothing happens.\n"
    ],

    "con": [
        f"\nAfter the 5th consecutive minute of holding your breath, you give up.\n"
    ],

    "int": [
       f"\nCan't think your way out of this one nerd!\n"
    ],

    "wis": [
        f"\nYou pause for a while to ponder the forms. The forms are throughly unhelpful.\n"
    ],

    "cha": [
        f"\nYou tell a mildly amusing Knock, Knock joke. Nobody laughs.\n"
    ]
}


class Event():

    def __init__(self):

        self._stats = set()
        self._tries = 0
        self._text = ""
        self._messages: dict[bool, list[tuple[str, list[str]]]] = {True: [], False: []}
        self._passed = False
        self._end_message = ""

    #properties
    @property
    def stats(self) -> None:
        return self._stats
    @property
    def tries(self) -> bool:
        return self._tries > 0
    @property
    def text(self) -> str:
        return self._text
    @property
    def passed(self) -> bool:
        return self._passed
    @property
    def end_message(self) -> str:
        return self._end_message
    #methods
    def add_stat(self, stat: tuple[str, int]) -> None:
        self._stats.add(stat)

    def add_tries(self, tries:int) -> None:
        self._tries = tries
    
    def has_stat(self, stat:str) -> bool:
        for pair in self._stats:
            if pair[0] == stat:
                return True
        return False

    def stat_dc(self, stat:str) -> None | tuple[str, int]:
        for pair in self._stats:
            if pair[0] == stat:
                return self._stats[pair]
            
    def add_text(self, text:str) -> None:
        self._text = text

    def add_message(self, message:tuple[bool, str, list[str]]) -> None:
        msg_type, stat, msg = message
        self._messages[msg_type].append((stat, msg))

    def add_end_message(self, msg:str) -> None:
        self._end_message = msg

    def run(self, stat:str, roll:int) -> str:
        if self.tries is False:
            raise ValueError("No more tries")
        self._tries -= 1
        if self.has_stat(stat) is True:
            for item in self._stats:
                code, check = item
                if code == stat and roll >= check:
                    for msg in self._messages[True]:
                        if msg[0] == stat:
                            self._passed = True
                            return random.choice(msg[1])
            for msg in self._messages[False]:
                if msg[0] == stat:
                    return random.choice(msg[1])

        return random.choice(FAILURE_LINES[stat])
