import random

class Statblock():

    def __init__(self, id, hp, damage, evasion, armor, loot):
        self._id = id
        self._hp = hp
        self._damage = damage
        self._evasion = evasion
        self._armor = armor
        self._loot = loot

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def damage(self) -> int:
        return self._damage
    @property
    def evasion(self) -> int:
        return self._evasion
    @property
    def armor(self) -> int:
        return self._armor
    @property
    def loot(self):
        return self._loot


class Mob():

    def __init__(self, level, statblock: Statblock):
        self._id = statblock.id
        self._level = level
        #base stats
        self._stat_block = statblock

        #calculated stats
        self._hp = random.randrange(1, statblock.hp) * level
        self._damage: int = statblock.damage * level
        self._evasion: int = statblock.evasion * level
        self._armor:int = statblock.armor * level

        self._loot = []
        for item in statblock.loot:
            self._loot.append(item*level)

    #properties
    @property
    def dead(self) -> bool:
        return self.hp <= 0
    @property
    def level(self) -> int:
        return self._level
    @property
    def damage(self) -> int:
        return self._damage
    @property
    def evasion(self) -> int:
        return self._evasion
    @property
    def armor(self) -> int:
        return self._armor
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def loot(self):
        return self._loot
    @property
    def id(self) -> str:
        return self._id
        
    #methods
    def roll_attack(self) -> int:
        """
        Rolls an attack (d20)
        """
        roll = random.randrange(1,20)

        if roll == 1:
            return 1
        if roll == 20:
            return 0
        
        return roll + self.level
    
    def roll_damage(self) -> int:
        """
        Rolls damage (damage dice)
        """
        return random.randrange(1, self.damage)
    
    def take_damage(self, damage:int) -> int:
        """
        Takes a given amount of damage, reduced by armor
        """
        if damage - self.armor < 0:
            return 0
        else:
            self._hp -= damage - self.armor
            return damage - self.armor