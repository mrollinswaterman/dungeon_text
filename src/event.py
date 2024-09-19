import random
import global_variables, global_commands

FAILURE_LINES = {
    "str": [
        "You're going to need more than brawn to solve this one.",
        "Your bulging biceps aren't up to this task.",
        "No amount of strength can solve this problem."
    ],

    "dex": [
        "You do a sick spin move. Nothing happens.",
        "You can't think of a way to come at this problem using your dexterity.",
        "This will require something substantially different from the ability to twist yourself into a pretzel.",
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
        self._messages:dict[bool, dict[str,list]] = {True: {}, False: {}}
        self._passed = False
        self._end_messages:list[str] = []
        self._damage_header = ""
        self._loot = {
            "xp": 0,
            "gold": 0,
            "drops": []
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
    @property
    def damage_header(self) -> str:
        return self._damage_header
    
    #methods

    #ADD
    def add_stat(self, stat:str, dc:int) -> None:
        """Adds a stat to the events stat list"""
        self._stats[stat] = dc

    def add_text(self, text:str) -> None:
        """Sets the event's text to a given string"""
        self._text = text

    def add_message(self, type:bool, message_dict:dict[str, str]) -> None:
        """
        Adds a message to the event's message list. 
        
        type: a bool indicating if the messages in the dict are for
        success (True) or failure (False)

        message_dict: a dictionary of messsages, with stats as keys
        (ie 'str', 'dex', etc) and message text as values

        Returns nothing
        """
        for stat in message_dict:
            if stat in self._messages[type]:
                self._messages[type][stat].append(message_dict[stat])
            else:
                self._messages[type][stat] = message_dict[stat]

    def add_end_message(self, msg) -> None:
        """Adds an end message to the event"""
        if isinstance(msg, list):
            self._end_messages = msg
            return None
        self._end_messages.append(msg)


    #SETTERS
    def set_id(self, id:str):
        self._id = id
    
    def set_tries(self, tries:int) -> None:
        self._tries = tries

    def set_loot(self, loot:dict) -> None:
        """Adds loot to the event"""
        for idx, entry in enumerate(self._loot):
            self._loot[entry] = loot[idx]

    def set_gold(self, num:int) -> None:
        self._loot["gold"] = num

    def set_xp(self, num:int) -> None:
        self._loot["xp"] = num

    def add_drop(self, item) -> None:
        if self._loot["drops"] is None:
            self.set_drop(item)
        else:
            self._loot["drops"].append(item)

    def set_passed(self, val:bool) -> None:
        self._passed = val

    #EVENT INFO
    def has_stat(self, stat:str) -> bool:
        """Checks to see if the event has a stat in its stat list."""
        for key in self._stats:
            if key == stat:
                return True
        return False
    
    def stat_dc(self, stat:str) -> int:
        """Returns the DC associated with a given stat"""
        if stat not in self._stats:
            return 0
        return self._stats[stat]

    #RUN
    def start(self) -> None:
        """Prints the start text and associated formatting of the event"""
        global_commands.type_text(self._text)

    def success(self, code:str) -> None:
        """Runs if the player has passed the event"""
        self._passed = True
        self._tries = -1#set self.tries to False by setting _tries to -1
        if self._loot["xp"] <= 0:#set xp if it hasnt been
            self.set_xp(int(self.stat_dc(code) / 1.5))
        global_commands.type_text(random.choice(self._messages[True][code]))#print a random success message
        return None
    
    def try_again(self, code) -> None:
        """Runs if the player fails the event"""
        global_commands.type_text(random.choice(self._messages[False][code]))#print failure line

    def not_that_stat(self, code:str):
        """Runs if the player tries the event with the wrong stat """
        global_commands.type_text(random.choice(FAILURE_LINES[code]))#print failure line
    
    def run(self, code:str, roll: int):
        """Runs the event for a given stat code and roll. Returns the number of tries left on the event"""
        if self.tries is False:
            raise ValueError("No more tries")
        self._tries -= 1#1
        if self.has_stat(code) is True:
            if roll >= self.stat_dc(code):#if roll beats the DC
                self.success(code)
            else:
                self.try_again(code)
        else:
            self.not_that_stat(code)
        return self.tries

    def failure(self):
        """Runs if the event has been failed twice (ie its over)"""
        self._tries = -1
        global_commands.type_text(random.choice(self._end_messages))
