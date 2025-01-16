import effects

class DamageOverTime(effects.Repeated_Effect):

    def __init__(self, source):
        super().__init__(source)

    def update(self):
        self.deal_damage(globals.XdY(self.potency))
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

class DecreasingDoT(effects.Repeated_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.max_potency = self.potency

    def update(self):
        self.potency = self.potency // 2  #halve potency each tick
        self.potency = max(1, self.potency)  #minimum of 1 damage
        self.deal_damage(self.potency) #damage target
        super().update()
