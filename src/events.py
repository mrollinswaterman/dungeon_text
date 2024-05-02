
from typing import Optional
import random
import global_commands
import global_variables

FAILURE_LINES = {
    "str": [
        "You're going to need more than brawn to solve this one.",
        "Your bulging biceps aren't up to this task.",
        "No amount of strength can solve this problem."
    ],

    "dex": [
        "You do a sick spin move. Nothing happens.",
        "You can't think of a way to come at this problem using your dexterity.",
        "This will require substancially more than the ability to twist yourself into a pretzel.",
        "No way to wriggle your way out of this."
    ],

    "con": [
        "After the 5th consecutive minute of holding your breath, you give up.",
        "Being stout of heart won't do you much good here.",
        "Your above average pain tolerance will get you nowhere with this."
    ],

    "int": [
       "You can't think your way out of this one.",
       "You deduce you should try a different approach.",
       "Maybe those kids that picked on you in school had a point..."
    ],

    "wis": [
        "You pause for a while to ponder the forms. The forms are throughly unhelpful.",
        "You sense that your Wisdom is useless here.",
        "Your intution tells you to try something else.",
        "The ability to keep a cool head is useful, but this will require a different skill set"
    ],

    "cha": [
        "You tell a mildly amusing Knock, Knock joke. Nobody laughs.",
        "Your silver tongue is of no use.",
        "Now is not the time for smooth talking",
        "Good looks can only get you so far..."
    ]
}


class Event():

    def __init__(self, id=""):

        self._id = id
        self._stats:dict[str, int] = {}
        self._tries = 0
        self._text = ""
        self._messages = {True: {}, False: {}}
        self._passed = False
        self._end_messages:list[str] = []
        self._loot = {
            "xp": 0,
            "gold": 0,
            "drops": None
        }

        self._player = global_variables.PLAYER

    #properties
    @property
    def stats(self) -> None:
        return self._stats
    @property
    def id(self) -> None:
        return self._id
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
    def end_messages(self) -> str:
        return self._end_messages
    @property
    def loot(self):
        return self._loot

    #methods

    #ADD
    def add_stat(self, stat:str, dc:int) -> None:
        """
        Adds a stat to the events stat list
        """
        self._stats[stat] = dc

    def add_text(self, text:str) -> None:
        """
        Sets the event's text to a given string
        """
        self._text = text

    def add_message(self, type:bool, message_dict:dict[str, str]) -> None:
        """
        Adds a message to the event's message list. 
        
        message: a tuple containing a bool indicating success or failure message,
        a str denoting the stat the message is associated with, and a list of strings 
        containing the messages to be displayed

        Returns nothing
        """
        for stat in message_dict:
            if stat in self._stats[type]:
                self._stats[type][stat].append(message_dict[stat])
            else:
                self._stats[type][stat] = message_dict[stat]
            

    def add_end_message(self, msg) -> None:
        """
        Adds an end message to the event
        """
        if isinstance(msg, list):
            self._end_messages = msg
            return None
        self._end_messages.append(msg)



    #SETTERS
    def set_tries(self, tries:int) -> None:
        """
        Sets the number of tries the event has to a given integer
        """
        self._tries = tries

    def set_loot(self, loot) -> None:
        """
        Adds loot to the event
        """
        for idx, entry in enumerate(self._loot):
            self._loot[entry] = loot[idx]

    def set_gold(self, num:int) -> None:
        self._loot["gold"] = num

    def set_xp(self, num:int) -> None:
        self._loot["xp"] = num

    def set_drop(self, item) -> None:
        self._loot["drops"] = [item]

    def add_drop(self, item) -> None:
        if self._loot["drops"] is None:
            self.set_drop(item)
        else:
            self._loot["drops"].append(item)

    def set_passed(self, val:bool) -> None:
        self._passed = val

    #EVENT INFO
    def has_stat(self, stat:str) -> bool:
        """
        Checks to see if the event has a stat in its stat list.

        Return True if it does, False if it does not
        """
        for key in self._stats:
            print(key, stat)
            if key == stat:
                return True
        return False
    
    def stat_dc(self, stat:str) -> int:
        """
        Returns the DC associated with a given stat
        """
        if stat not in self._stats:
            return 0
        return self._stats[stat]

    #RUN
    def start(self) -> None:
        """
        Prints the start text and associated formatting of the event
        """
        global_commands.type_with_lines(self.text)

    def success(self) -> None:
        """
        Runs if the player has succeded the check
        """
        return None
    
    def failure(self) -> None:
        """
        Runs if the player fails the event
        """
        return None
    
    def run(self, stat:str, roll:int) -> str:
        """
        Runs the event for a given stat and roll

        Returns an f-string determined by the stat rolled and whether or not
        the check succeded
        """
        if self.tries is False:
            raise ValueError("No more tries")
        self._tries -= 1
        if self.has_stat(stat) is True:
            for key in self._stats:
                dc = self.stat_dc(key)
                if key == stat and roll >= dc:
                    for msg in self._messages[True]: #SUCCESS
                        if msg[0] == stat:
                            self._passed = True
                            if self._loot["xp"] <= 0:
                                self.set_xp(int(dc / 1.5))
                            global_commands.type_text(random.choice(msg[1])+"\n")
                            return True
            for msg in self._messages[False]: #FAILURE
                if msg[0] == stat:
                    global_commands.type_text(random.choice(msg[1]))
                    return self.tries

        #print(stat, self._stats)
        global_commands.type_text(random.choice(FAILURE_LINES[stat])) #WRONG STAT
        return self.tries

    def end(self) -> None:
        """
        Prints the end text and associated formatting of the event
        """
        print("")#newline b4 end
        global_commands.type_text(random.choice(self._end_messages))
        if self._passed is True:
            self.success()
        else:
            self.failure()