#Clockwork Hound mob file
import mob, global_commands, items

stats = {
    "str": 16,
    "dex": 14,
    "con": 14,
    "int": 18,
    "wis": 10,
    "cha": 7,
    "base_evasion": 10,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 3,
    "damage": 8,
    "dc": 10,
    "hit_dice": 10,
    "loot": {
        "gold": 30,
        "xp": 15,
        "drops": []
    }
}

class Clockwork_Hound(mob.Mob):
    def __init__(self, id="Clockwork Hound", level = (6,13), statblock=stats):
        super().__init__(id, level, statblock)

        if global_commands.probability(50):
            scrap:items.Item = items.Item("Clockwork Scrap", "Uncommon")
            scrap.set_weight(1.5)
            self._loot["drops"].append(scrap)

        if global_commands.probability(3):
            heart = items.Item("Clockwork Heart", "Epic")
            heart.set_weight(2)
            self._loot["drops"].append(heart)
            
    def trigger(self) -> bool:
        return self._hp < self.max_hp // 2

    def special(self) -> None:
        self.spend_ap()

        if self._player is None:
            raise ValueError("No Target.")
        
        weapon:items.Weapon = self._player.equipped["Weapon"]
        armor:items.Armor = self._player.equipped["Armor"]

        meal:items.Item = weapon
        if weapon.durability < armor.durability:
            meal = armor
        
        global_commands.type_text(f"The {self.id} lunges for your {meal.id}.")
        if self.roll_attack() > self._player.evasion:
            global_commands.type_text(f"It gulps down a chunk, then darts back looking satisfied.")
            meal.remove_durability(self.bonus("str"))
            self.heal(self.bonus("str"))
        else:
            global_commands.type_text("It missed.")

object = Clockwork_Hound
