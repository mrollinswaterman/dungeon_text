#Goblin Gang mob file
import game_objects.mob as mob

class Goblin_Gang(mob.Mob):
    def __init__(self):
        super().__init__(id="Goblin Gang")
        
        #goblin_gang gets +5 HP
        self.stats.max_hp += 5
        self.stats.max_hp = int(self.stats.max_hp)
        self.hp = self.stats.max_hp
        
        self.gold += 20
        self.xp += 10

    def special(self) -> bool:
        return False

object = Goblin_Gang