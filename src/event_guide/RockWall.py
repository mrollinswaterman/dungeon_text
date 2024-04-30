#Rock Wall Event class
import events

object = events.Event()
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
object.add_stat(("str", 20))
object.add_stat(("dex", 10))

object.add_text(' The path abruptly ends in a sheer rock wall.')

object.add_message((True, "str", rock_wall_lines_true["str"]))
object.add_message((True, "dex", rock_wall_lines_true["dex"]))

object.add_message((False, "str", rock_wall_line_false["str"]))
object.add_message((False, "dex", rock_wall_line_false["dex"]))

object.add_end_message("You are forced to double back and find another way through.")