import sys
import globals
from mechanics import damage, magic

def run():
    player_tests()

    print("All tests passed successfully!\n")

def player_tests():
    import game_objects

    p1 = game_objects.Player()

    #Header
    assert(p1.header.default == "you")
    assert(p1.header.ownership == "your")
    assert(p1.header.action == "you are")
    assert(p1.header.damage == p1.header.default)
    assert(p1.header.tries in ["you try", "you attempt"])

    #Damage Type
    assert(p1.damage_type.physical)
    assert(p1.damage_type.bludgeoning)
    assert(not p1.damage_type.magic)
    assert(not p1.damage_type.slashing)
    assert(not p1.damage_type.piercing)
    assert(p1.damage_type.string == "Physical/Bludgeoning")

    #Immunities/Resistances
    assert(p1.resistances.string == "None")
    assert(p1.immunities.string == "None")

def event_tests():
    import game_objects, controllers, compendiums, game
    from compendiums import event_compendium as events

    ev = events.dict["glyphs"]()

    ev.start()

    ev.run("cha")

    ev.run("dex")

    sys.exit()