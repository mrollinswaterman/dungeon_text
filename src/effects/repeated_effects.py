import effects
import game
import globals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import items


class DamageOverTime(effects.Repeated_Effect):

    def __init__(self, source):
        super().__init__(source)

    def update(self):
        self.deal_damage(globals.XdY(self.potency))
        super().update()

class DecreasingDoT(effects.Repeated_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.max_potency = self.potency

    def update(self):
        self.potency = self.potency // 2  #halve potency each tick
        self.potency = max(1, self.potency)  #minimum of 1 damage
        self.deal_damage(self.potency) #damage target
        super().update()

class StackingDoT(effects.Repeated_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.stacks = 1
        self.max_stacks = 10
    
    def update(self):
        damage = globals.XdY(self.potency)

        if self.stacks >= self.max_stacks: # at max stacks, deal large amount of damage and cleanse
            self.stacks = self.max_stacks
            self.deal_damage((damage * self.stacks) + self.stacks)  
            return self.end()
        else: # damage target, scaling with stacks
            self.deal_damage(damage * self.stacks)
            self.stacks -= 1

        super().update()
    
    def end(self):
        self.stacks = 0
        super().end()

class Status_Effect(effects.Repeated_Effect):
    
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__
        self.header = game_objects.Header(self)
        self._effects:list[effects.Repeated_Effect] = []  # might need to make this a dictionary so effects can be accessed by name
        self.switch_word = ""
        self.save_DC = 12

    @property
    def active(self) -> bool:
        return len(self._effects) > 0

    @property
    def base_msg(self) -> str:
        return f"{self.target.header.action} {self.switch_word} {self.id}."
    
    @property
    def effects(self) -> list[effects.Effect]:
        return self._effects

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
        actives = self.effects
        for effect in actives:
            effect.start()
            if not effect.active:
                self._effects.remove(effect)
        if not self.active:
            self.end()

    def update(self):
        actives = self.effects
        for effect in actives:
            if effect.active:
                effect.update()
            elif not effect.active:
                self._effects.remove(effect)
        super().update()

    def refresh(self):
        globals.type_text(self.refresh_msg)

    def end(self):
        globals.type_text(self.end_msg)
        for effect in self.effects:
            effect.end()
        self._effects = []

    def save_attempt(self) -> bool:
        return None

