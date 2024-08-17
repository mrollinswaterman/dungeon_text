import random
import event as ev
import events

#STRENGTH_LINES = [f'You come across a gnomish miner. He is struggling to break a rock with a pickaxe that is far too large for his small frame.', f'You come to the edge of a small chasm. It looks jumpable...',

    #f'The path abruptly ends in a sheer rock wall.'
#]

def spawn_event(name:str):
    try:
        return events.dict[name]()
    except KeyError:
        raise ValueError(f"No event by id '{name}'.")

def spawn_random_event():
    return random.choice(list(events.dict.values()))()