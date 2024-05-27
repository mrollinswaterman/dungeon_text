from event_guide import Boulder, RockWall, Berries

#STRENGTH_LINES = [f'You come across a gnomish miner. He is struggling to break a rock with a pickaxe that is far too large for his small frame.', f'You come to the edge of a small chasm. It looks jumpable...',

    #f'The path abruptly ends in a sheer rock wall.'
#]

EVENTS = {}

EVENTS[Boulder.object.id] = (Boulder.object)
EVENTS[RockWall.object.id] = (RockWall.object)
EVENTS[Berries.object.id] = (Berries.object)