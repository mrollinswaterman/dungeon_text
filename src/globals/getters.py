from typing import Any

def get_cmd() -> str:
    cmd = input(">> ").lower()
    print("")
    return cmd

def get_base_type(obj:Any) -> str:
    """Returns the base type of the given object
        i.e. Item, Game_Object, Mechanic, etc"""
    bases = obj.__class__.__mro__
    return bases[len(bases)-2].__name__

def get_subtype(obj:Any) -> str:
    """Returns the subtype of an object,
        i.e. Equipment, Enchantment, Combat_Trick, etc"""
    bases = obj.__class__.__mro__
    return bases[len(bases)-3].__name__

def get_type(obj: Any) -> str:
    """Returns the type of an object,
        i.e. Weapon, Stackable, Consumable"""
    import compendiums.item_compendium as items
    
    bases = obj.__class__.__mro__
    if bases[0].__name__ in items.dict:
        return bases[1].__name__
    return bases[0].__name__