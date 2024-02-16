import events


STRENGTH_LINES = [
    f'A boulder blocks your way.',

    f'You come across a gnomish miner. He is struggling 
    to break a rock with a pickaxe that is far too large for his small frame.',

    f'You come to the edge of a small chasm. It looks jumpable...',

    f'The path abruptly ends in a sheer rock wall.'
]

EVENTS_LIST = []

check = events.StatCheck_Event(
    {"str": (10, [], []), "dex": (20, [], [])}
)

[f"You push the boulder aside and continue on your way",
                  f"You pummel the boulder to rubble for daring to stand in your way."]
