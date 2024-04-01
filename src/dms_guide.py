import events

#BOULDER EVENT
boulder = events.Event()
boulder_lines_true = {
    "str": ["You push the boulder aside and continue on your way.", 
            "You smash the boulder to rubble for daring to stand in your way."],

    "dex": ["You manage to squeeze by the boulder.", "You're flexible enough to make it past."]
}
boulder_line_false = {
    "str": ["You push with all your might, but the boulder doesn't budge. You'll need to push a little harder.", 
            "You punch the boulder. Nothing happens. Maybe if you punched it harder?"],

    "dex": ["You do a backflip. The boulder is unimpressed. You think you might be able to squeezing past it, if you tried.",
            "You try to squeeze past, but don't quite make it. You wriggle yourself out before you get stuck."]
}
boulder.add_stat(("str", 10))
boulder.add_stat(("dex", 15))

boulder.add_text(' A boulder blocks your way.')
boulder.add_message((True, "str", boulder_lines_true["str"]))
boulder.add_message((True, "dex", boulder_lines_true["dex"]))
boulder.add_message((False, "str", boulder_line_false["str"]))
boulder.add_message((False, "dex", boulder_line_false["dex"]))
boulder.add_end_message("You are forced to double back and find another way through.")

#ROCKCLIMBING EVENT
rock_wall = events.Event()
rock_wall_lines_true = {
    "str": ["With nothing but your own brute strength, you haul yourself up the wall.", 
            "You manage to clamber over the wall."],

    "dex": ["You find hand and footholds in wall's nooks and crannies, enough to make your way up.", 
            "You scurry up the wall with ease."]
}
rock_wall_line_false = {
    "str": ["You try a few times to pull yourself up the wall, but you aren't quite strong enough this time."],
 

    "dex": ["You try your hand at freesoloing the wall. It doesn't go well."]
}
rock_wall.add_stat(("str", 20))
rock_wall.add_stat(("dex", 10))

rock_wall.add_text(' The path abruptly ends in a sheer rock wall.')
rock_wall.add_message((True, "str", rock_wall_lines_true["str"]))
rock_wall.add_message((True, "dex", rock_wall_lines_true["dex"]))
rock_wall.add_message((False, "str", rock_wall_line_false["str"]))
rock_wall.add_message((False, "dex", rock_wall_line_false["dex"]))
rock_wall.add_end_message("You are forced to double back and find another way through.")

#STRENGTH_LINES = [f'You come across a gnomish miner. He is struggling to break a rock with a pickaxe that is far too large for his small frame.', f'You come to the edge of a small chasm. It looks jumpable...',

    #f'The path abruptly ends in a sheer rock wall.'
#]

EVENT_LIST = []

EVENT_LIST.append(boulder)
EVENT_LIST.append(rock_wall)



