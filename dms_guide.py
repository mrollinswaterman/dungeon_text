import events

boulder = events.Event()

boulder.add_stat(("str", 10))
boulder.add_stat(("dex", 20))

boulder.add_tries(2)

boulder.add_text(f'A boulder blocks your way.')

boulder.add_message((True, "str", f"\nYou push the boulder aside and continue on your way."))
boulder.add_message((True, "str", f"\nYou smash the boulder to rubble for daring to stand in your way."))
boulder.add_message((True, "dex", f"\nYou manage to squeeze by the boulder."))
boulder.add_message((True, "dex", f"\nYou're flexible enough to make it past."))

boulder.add_message((False, "str", f"\nYou push with all your might, but the boulder doesn't budge. You'll need to push a little harder"))
boulder.add_message((False, "str", f"\nYou punch the boulder. Nothing happens. Surely punching it harder will do something!"))
boulder.add_message((False, "dex", f"\nYou do a sick spin move. The boulder is unimpressed. Maybe try squeezing past it?"))
boulder.add_message((False, "dex", f"\nYou try to squeeze past, but don't quite make it. You wriggle yourself out before you get stuck."))

print(boulder.run("con", 22))
print(boulder.run("con", 22))
print(boulder.run("con", 22))


#STRENGTH_LINES = [f'You come across a gnomish miner. He is struggling to break a rock with a pickaxe that is far too large for his small frame.', f'You come to the edge of a small chasm. It looks jumpable...',

    #f'The path abruptly ends in a sheer rock wall.'
#]

