import sys
import globals

def run():
    import game_objects, controllers, compendiums, game
    from compendiums import event_compendium as events

    ev = events.dict["smog"]()

    ev.start()

    ev.run("cha")

    ev.run("int")

    sys.exit()