#Hobgoblin mob file
import effects
import game_objects, globals

class Hobgoblin(game_objects.Mob):
    def __init__(self):
        super().__init__(id="Hobgoblin")

        #base gold & xp
        self.gold += 10
        self.xp += 5

    @property
    def save_dc(self):
        return self.stats.base_save_dc + self.bonus("cha")

    def trigger(self):
        """Return True if the player's evasion is >= 10, and the 
        player is not currently suffering from a Hobgoblin's taunt"""
        return False
        if not super().trigger():
            return False
        return self.target.evasion() >= 10 and self.target.monitor.get("Taunted") is None

    def special(self) -> None:
        """Taunt: Reduces the player's evasion by 2 points for 2 turns if they fail a charisma check"""
        self.spend_ap(0)
        globals.type_text(f"The {self.id} hurls enraging insults at you.")

        if self.target.roll_a_check("cha") >= self.save_dc:
            globals.type_text(f"Your mind is an impenetrable fortess. The {self.id}'s words have no effect.")
        else:
            #apply the taunt
            pass
        return None
    
    def roll_narration(self):
        base = super().roll_narration()        
        me = [
            f"The {self.id} swings it's club at you.",
            f"The {self.id} tries to bash your head in.",
            f"The {self.id} winds up for a strike.",
            f"The {self.id} charges you, it's club raised.",
            f"The {self.id} lets out a fierce battle cry, and hoists it's club in preperation..."
        ]
        return base + me

    def hit_narration(self):
        base = super().hit_narration()
        me = [
            f"The {self.id}'s club smashes through your defense.",
            f"You can't dodge its club's powerful smash.",
            f"The {self.id}'s club catches your arm.",
            f"The club moves fast for something so cumbersome looking..."
        ]
        return base + me

    def miss_narration(self):
        base = super().miss_narration()
        me = [
            f"You manage to dash of the club's strike radius",
            f"The {self.id}'s attack is strong, but slow. You step out of it's way.",
            f"You dodge the club's wide arc."
        ]
        return base + me
    
#add taunt status_effect

object = Hobgoblin