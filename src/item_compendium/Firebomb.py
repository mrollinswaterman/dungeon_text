#Firebomb
import items, status_effect, global_commands
from conditions import On_Fire

class Firebomb(items.Consumable):
    
    def __init__(self, id="Firebomb", rarity="Uncommon", quantity=0):
        import mob
        super().__init__(id, rarity, quantity)
        self._unit_value = 20 * self._numerical_rarity
        self._unit_weight = 1 
        self._target:mob.Mob = None
        self._damage = self._strength
        #self._type = "Firebomb"

    @property
    def damage_header(self) -> str:
        return self._id
    @property
    def damage_type(self) -> str:
        return "Physical"

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
                self.set_on_fire()
            return True
        
        if throw > dodge:
            global_commands.type_text(f"You hit the {self._target.id}.")
            taken = self._target.take_damage(int(self._damage), self)
            if global_commands.probability(75):#--> if statement is a formattting thing the message doesn't change 
                self.set_on_fire()

        return True

    def set_on_fire(self) -> None:
        fire:status_effect.Status_Effect = On_Fire(self._owner, self._target)
        fire.set_duration(2)
        fire.set_potency(self._numerical_rarity)
        self._target.add_status_effect(fire)
        return None
       
    def update(self) -> None:
        super().update()
        self._damage = self._strength
        self._unit_value = 20 * self._numerical_rarity
        self._unit_weight = 1

def craft(num=1):
    fb = Firebomb()
    fb.set_quantity(num)
    return fb

object = Firebomb