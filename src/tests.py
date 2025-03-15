import sys
import globals

def run():
    import game_objects, controllers, compendiums, game
    from compendiums import event_compendium as events

    ev = events.dict["glyphs"]()

    ev.start()

    ev.run("cha")

    ev.run("dex")

    sys.exit()