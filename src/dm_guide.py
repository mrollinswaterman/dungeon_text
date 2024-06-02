import random
from events import Boulder, Rock_Wall, Berries
from events import Smog, Glyphs, Trap_Room
import event

#STRENGTH_LINES = [f'You come across a gnomish miner. He is struggling to break a rock with a pickaxe that is far too large for his small frame.', f'You come to the edge of a small chasm. It looks jumpable...',

    #f'The path abruptly ends in a sheer rock wall.'
#]

event_scenarios = [
    Boulder.object, Rock_Wall.object, Berries.object, Smog.object,
    Glyphs.object
]

def spawn_event(name:str):
    for entry in event_scenarios:
        event_obj:event.Event = entry() 
        if event_obj.id == name:
            return event_obj
    raise ValueError(f"No event by id '{name}'.")

def spawn_random_event():
    return random.choice(event_scenarios)()