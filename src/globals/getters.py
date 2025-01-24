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
    bases = obj.__class__.__bases__
    return bases[0].__name__