#Enraged condition. 
import global_commands, status_effect

class Condition(status_effect.Status_Effect):
    """
    Enraged condition. Gain str and con, lose dex, lose int.
    Gain temp hp equal to con bonus, and enraged creatures
    can't flee combat, and must attack every turn while they remain enraged.
    """

    def __init__(self, src, target, id="Enraged"):
        super().__init__(src, target, id)
        self._old_flee = None

        if src is None: return None
        
        if self.player:
            self._message = "You become Enraged."
            self._cleanse_message = "You are no longer Enraged."
        else:
            self._message = f"The {self._target.id} has become Enraged."
            self._cleanse_message = f"The {self._target.id} is no longer Enraged."
        
        self._buffs = ["con", "str"]
        self._debuffs = ["int, dex"]

        self._duration = 3
        self._potency = 3

    def apply(self):
        super().apply()

        for item in self._buffs:
            self.target.stats[item] += self._potency
        for item in self._debuffs:
            self.target.stats[item] -= self._potency

        self.target.gain_temp_hp(self.target.bonus("con") * 1.5)
        self._old_flee = self.target.flee_threshold
        self.target.set_flee_threshold(0.0)
    
    def additional_effect(self, effect: status_effect.Status_Effect):
        text = f"The {self.target.id} is already Enraged."
        if self.player:
            text = f"You are already Enraged."
        global_commands.type_text(text)
        return None
    
    def cleanse(self) -> None:
        super().cleanse()

        self.target.remove_temp_hp(self.target.bonus("con"))
        for item in self._buffs:
            self.target.stats[item] -= self._potency
        for item in self._debuffs:
            self.target.stats[item] += self._potency

        self.target.set_flee_threshold(self._old_flee)
        return None
