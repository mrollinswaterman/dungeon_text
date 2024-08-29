#Firebomb
import items, global_commands

class Firebomb(items.Consumable):
    
    def __init__(self, id="Firebomb", rarity="Uncommon", quantity=0):
        import mob
        super().__init__(id, rarity, quantity)
        self._unit_value = 20 * self._rarity.value
        self._unit_weight = 3
        self._target:mob.Mob = None
        self._damage = self._strength

    @property
    def damage_header(self) -> str:
        return self._id

    def use(self, target=None) -> bool:
        """
        Throws the firebomb at a given target, and checks to
        see if that target is set on fire
        Always returns True
        """
        import mob
        target: mob.Mob = target
        self._target = target

        throw = self._owner.roll_a_check("dex")
        dodge = target.roll_a_check("dex")
       
        self.decrease_quantity(1)

        global_commands.type_text(f"You throw a {self._id} at the {self._target.id}.")

        if dodge >= throw + 10:
            global_commands.type_text(f"The {self._target.id} dodged your {self._id} entirely!")
            return True
        
        if dodge >= throw:
            global_commands.type_text(f"The {self._target.id} partially dodged your {self._id}.")
            taken = self._target.take_damage(int(self._damage // 2), self)
            if global_commands.probability(50 - dodge):
                self.apply_tags()
            return True
        
        if throw > dodge:
            global_commands.type_text(f"You hit the {self._target.id}.")
            taken = self._target.take_damage(int(self._damage), self)
            if global_commands.probability(75):
                self.apply_tags()

        return True

    def apply_tags(self) -> None:
        for tag in self._tags:
            if tag.on_hit:
                tag.apply()
        return None
       
    def update(self) -> None:
        super().update()
        self._damage = self._strength
        self._unit_value = 20 * self._rarity.value
        self._unit_weight = 3

def craft(num=1):
    fb = Firebomb()
    fb.set_quantity(num)
    return fb

object = Firebomb