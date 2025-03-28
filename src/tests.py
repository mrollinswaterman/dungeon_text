import sys
import globals
from mechanics import damage, magic

def run():
    import game
    global SPEED
    player_tests()

    print("All tests passed successfully!\n")
    globals.set_SPEED(3)
    #sys.exit()

def item_tests():
    pass

def player_tests():
    import game_objects
    globals.set_SPEED(0)

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

    #Weapon
    wep = globals.craft_item("Longsword", "Common")
    assert(p1.equip(wep))
    assert(globals.get_TEXTBOX() == "Longsword equipped.")

    enemy = globals.spawn_mob("Goblin")
    
    pots = globals.craft_item("Health_Potion", "Common")
    pots.set_quantity(5)

    p1.pick_up(pots)

    print(p1.get_item(pots.id).quantity)

    p1.load_inventory("inventory.csv")

    print(p1.get_item(pots.id).quantity)

    sys.exit()

def event_tests():
    import game_objects, controllers, compendiums, game
    from compendiums import event_compendium as events

    ev = events.dict["Glyphs"]()

    ev.start()

    ev.run("cha")

    ev.run("dex")