import effects
import game_objects
import globals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import items

class DamageOverTime(effects.Repeated_Effect):
    """
    Deals damage to its target every turn.

    Increase and Decrease potency functions are adjust the effect's potency
    up or down the dice progression scale based on the specifications
    of the status effect that the DoT object is attached to
    """

    def __init__(self, source):
        super().__init__(source)
        self.max_potency = globals.XdY(self.potency, max=True)

    def decrease_potency(self):
        match self.potency:
            case str(): 
                idx = globals.DICE_PROGRESSION.index(self.potency)
                self.potency = globals.DICE_PROGRESSION[idx - 1]
            case int():
                self.potency = self.potency // 2
                self.potency = max(1, self.potency)
        return None

    def increase_potency(self):
        match self.potency:
            case str():
                idx = globals.DICE_PROGRESSION.index(self.potency)
                if idx > len(globals.DICE_PROGRESSION):
                    return None
                self.potency = globals.DICE_PROGRESSION[idx + 1]
            case int():
                self.potency += 2

        return None

    def update(self):
        self.deal_damage(globals.XdY(self.potency))
        super().update()

class StackingDoT(effects.Repeated_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.stacks = 3
        self.max_stacks = 10

    def check_stacks(self):
        """
        Checks to make sure the stacking DoT effect is not at 0 stacks

        If it is at 0, end the effect.
        """
        if self.stacks <= 0:
            self.end()
    
    def update(self):
        damage = 0
        for _ in range(self.stacks):
            damage += globals.XdY(self.potency)

        if self.stacks >= self.max_stacks: # at max stacks, deal large amount of damage and cleanse
            self.stacks = self.max_stacks
            self.deal_damage(damage + self.stacks)  
            return self.end()
        else: # If not at max stacks, damage target, scaling with stacks, then decrease stacks
            self.deal_damage(damage)
            self.stacks -= 1

        self.check_stacks()

        super().update()

    def end(self):
        self.stacks = 0
        super().end()

class Status_Effect(effects.Repeated_Effect):
    """
    A Status Effect is a type of Repeated Effect, but it is also a wrapper for other repeated effects.
    The Status Effect's 'repeated effect' is applying each of the effects attached to it.

    Status Effects have specific names, unlike other effects (eg. Poisoned, Bleeding, etc)
    """
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__

        # Status Effects have their own headers with custom values for damage
        #self._header = self.source.header
        self._header = game_objects.Header(self)
        self._header._damage = ""

        self._effects_list:list[effects.Repeated_Effect] = []  # might need to make this a dictionary so effects can be accessed by name
        self.switch_word = ""
        self.save_DC = 12


    @property
    def active(self) -> bool:
        return len(self._effects_list) > 0

    @property
    def base_msg(self) -> str:
        return f"{self.target.header.action} {self.switch_word} {self.id}."
    
    @property
    def effects_list(self) -> list[effects.Effect]:
        return self._effects_list

    @property
    def end_msg(self) -> str:
        self.switch_word = "no longer"
        return self.base_msg

    @property
    def refresh_msg(self) -> str:
        self.switch_word = "already"
        return self.base_msg

    @property
    def start_msg(self) -> str:
        self.switch_word = "now"
        return self.base_msg

    def start(self):
        globals.type_text(self.start_msg)
        actives = self.effects_list
        for effect in actives:
            effect.start()
            if not effect.active:
                self._effects_list.remove(effect)
        if not self.active:
            self.end()

    def update(self):
        actives = self.effects_list
        for effect in actives:
            if effect.active:
                effect.update()
            elif not effect.active:
                self._effects_list.remove(effect)

        if not self.active:
            self.end()
        else:
            super().update()

    def refresh(self):
        globals.type_text(self.refresh_msg)

    def end(self):
        globals.type_text(self.end_msg)
        for effect in self.effects_list:
            effect.end()
        self._effects_list = []

    def save_attempt(self) -> bool:
        return None

