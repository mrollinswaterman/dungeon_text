import mechanics
import game_objects

class Condition_Monitor():
    def __init__(self, parent):
        self.parent:game_objects.Game_Object = parent
        self._effects:dict[str, mechanics.Mechanic] = {}
        self._cleanse_pool:set[mechanics.Mechanic] = set()

    @property
    def active(self) -> list[mechanics.Mechanic]:
        return list(self._effects.values())
    
    @property
    def active_ids(self) -> list[str]:
        return list(self._effects.keys())

    def add(self, effect:mechanics.Mechanic):
        assert effect is mechanics.Mechanic()
        if effect in self.active:
            effect = self._effects[effect.id]
            effect.refresh()
        else:
            self._effects[effect.id] = effect
            effect.start()

    def update(self):
        for element in self.active:
            if element.active:
                element.update()
            if not element.active:
                self._cleanse_pool.add(element)

        self.cleanse()
    
    def cleanse(self):
        """Removes all effects in the cleanse pool from effects list,
            ending them if they are active"""
        for element in self._cleanse_pool:
            if element.active:
                element.end()
            del self._effects[element.id]

        self._cleanse_pool = set()

    def cleanse_all(self):
        """Adds all active effects to the cleanse pool, then cleases"""
        self._cleanse_pool.update(self.active)
        self.cleanse()