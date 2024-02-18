import events

#BOULDER EVENT
boulder = events.Event()
boulder_lines_true = {
    "str": [f"\nYou push the boulder aside and continue on your way.\n", f"\nYou smash the boulder to rubble for daring to stand in your way.\n"],

    "dex": [f"\nYou manage to squeeze by the boulder.\n", f"\nYou're flexible enough to make it past.\n"]
}
boulder_line_false = {
    "str": [f"\nYou push with all your might, but the boulder doesn't budge. You'll need to push a little harder.\n", 
            f"\nYou punch the boulder. Nothing happens. Maybe if you punched it harder?\n"],

    "dex": [f"\nYou do a backflip. The boulder is unimpressed. You think you might be able to squeezing past it, if you tried.\n",
            f"\nYou try to squeeze past, but don't quite make it. You wriggle yourself out before you get stuck.\n"]
}
boulder.add_stat(("str", 10))
boulder.add_stat(("dex", 15))

boulder.add_text(f'A boulder blocks your way.\n')
boulder.add_message((True, "str", boulder_lines_true["str"]))
boulder.add_message((True, "dex", boulder_lines_true["dex"]))
boulder.add_message((False, "str", boulder_line_false["str"]))
boulder.add_message((False, "dex", boulder_line_false["dex"]))
boulder.add_end_message(f"\nYou are forced to double back and find another way through.\n")

#ROCKCLIMBING EVENT
rock_wall = events.Event()
rock_wall_lines_true = {
    "str": [f"\nWith nothing but your own brute strength, you haul yourself up the wall.\n", f"You manage to clamber over the wall.\n"],

    "dex": [f"\nplaceholder dex true\n"]
}
rock_wall_line_false = {
    "str": [f"\nplaceholder str false\n"],
 

    "dex": [f"\nplaceholder dex false\n"]
}
rock_wall.add_stat(("str", 20))
rock_wall.add_stat(("dex", 10))

rock_wall.add_text(f'The path abruptly ends in a sheer rock wall.\n')
rock_wall.add_message((True, "str", rock_wall_lines_true["str"]))
rock_wall.add_message((True, "dex", rock_wall_lines_true["dex"]))
rock_wall.add_message((False, "str", rock_wall_line_false["str"]))
rock_wall.add_message((False, "dex", rock_wall_line_false["dex"]))

#STRENGTH_LINES = [f'You come across a gnomish miner. He is struggling to break a rock with a pickaxe that is far too large for his small frame.', f'You come to the edge of a small chasm. It looks jumpable...',

    #f'The path abruptly ends in a sheer rock wall.'
#]

EVENT_LIST = []

EVENT_LIST.append(boulder)
EVENT_LIST.append(rock_wall)


