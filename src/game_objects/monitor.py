import effects
import game_objects

class Monitor():
    def __init__(self, parent):
        self.parent:game_objects.Game_Object = parent
        self._effects:dict[str, effects.Effect] = {}
        #self._cleanse_pool:set[mechanics.Mechanic] = set()

    """@property
    def active(self) -> list[mechanics.Mechanic]:
        return list(self._effects.values())
    
    @property
    def active_ids(self) -> list[str]:
        return list(self._effects.keys())"""
    
    @property #List of all effect objects
    def effects_list(self) -> list[effects.Effect]:
        return list(self._effects.values())
    
    @property #List of all effect IDs
    def effect_ids(self) -> list[str]:
        return list(self._effects.keys())
    
    def get(self, effect_id:str) -> effects.Effect | None:
        if effect_id in self._effects:
            return self._effects[effect_id]
        else: return None

    def add(self, obj:"effects.Effect"):
        print(f"adding effect: {obj.id}")
        if obj in self.effects_list:
            current = self._effects[obj.id]
            obj.refresh()
        else:
            self._effects[obj.id] = obj
            obj.start()

    def update(self):
        actives = self.effects_list
        for effect in actives:
            if effect.active:
                effect.update()
            if not effect.active:
                del self._effects[effect.id]

    def cleanse(self, obj:"str | effects.Effect"):
        match obj:
            case str(): 
                my_effect = self._effects[obj]
            case effects.Effect():
                my_effect = self._effects[obj.id]
        
        my_effect.end()
        del self._effects[my_effect.id]

    def cleanse_all(self):
        cleanse_pool = self.effects_list
        for effect in cleanse_pool:
            self.cleanse(effect)
        self._effects = {}
