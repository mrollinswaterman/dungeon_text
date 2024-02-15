
from typing import Optional
import random

FAILURE_LINES = {
    "str": [
        f"You're going to need more than brawn to solve this one."
    ],

    "dex": [
        f"You do a sick spin move. Nothing happens."
    ],

    "con": [
        f"After the 5th consecutive minute of holding your breath, you give up."
    ],

    "int": [
       f"Can't think your way out of this one nerd!"
    ],

    "wis": [
        f"You pause for a while to ponder the forms. The forms are throughly unhelpful."
    ],

    "cha": [
        f"You tell a mildly amusing Knock, Knock joke. Nobody laughs."
    ]
}

SUCCESS_LINES = {
    "str": [
        f"Another win for the big guys!"
    ],

    "dex": [
        f"Seems those ballet classes paid off after all"
    ],

    "con": [
        f"No one is sure exactly what you did, but you sure did it!"
    ],

    "int": [
        f"Brains wins the day!"
    ],

    "wis": [
        f"You've been in situations like this before and this was no more difficult."
    ],

    "cha": [
        f"You don't need money when you look like that, do ya?"
    ]
}

END_LIST = [
    f"You can't try this anymore."
]


class StatCheck_Event():

    def __init__(self, difficulties_classes:dict[str, int], tries, failure_text:Optional[dict[str,str]] = False, 
                 success_text:Optional[dict[str,str]] = False, 
                 dialogue:str = "", failure_dictionary:dict[str, list[str]] = FAILURE_LINES,
                 success_dictionary: dict[str, list[str]] = SUCCESS_LINES, end_list:list[str] = END_LIST):

        self._stats:str = list(difficulties_classes.keys())
        self._stat_codes = []
        for stat in list(difficulties_classes.keys()):
            self._stat_codes.append(stat.lower()[0:2])
        self._difficulty_classes = difficulties_classes
        self._text:str = dialogue
        self._tries = tries
        self._reward = None
        self._failure_dictionary = failure_dictionary
        self._success_dictionary = success_dictionary

        self._failure_text = failure_text
        self._success_text = success_text

        self._end_list = end_list

    #properties
    @property
    def stats(self) -> str:
        return self._stats
    @property
    def stat_codes(self) -> str:
        return self._stat_codes
    @property
    def reward(self) -> int | tuple[int,int]:
        return self._reward
    @property
    def tries(self) -> int:
        return self._tries
    @property
    def done(self) -> bool:
        return self._tries <= 0
    
    #methods
    def passed(self, stat:str, check:int) -> bool:
        if self.done:
            return random.choice(self._end_list)
        if stat not in self._stats:
            self._tries -= 1
            if self._failure_text is not False:
                return self._failure_text[stat]
            return random.choice(self._failure_dictionary[stat])

        if check >= self._difficulty_classes[stat]:
            if self._success_text is not False:
                return self._success_text[stat]
            return random.choice(self._success_dictionary[stat])
        
        elif self._failure_text is not False:
            self._tries -= 1
            return self._failure_text[stat]

        self._tries -= 1
        return random.choice(self._failure_dictionary[stat])
    
    def set_text(self, text:str) -> None:
        self._text = text
        
    def set_reward(self, reward:int | tuple[int,int]) -> None:
        self._reward = reward
