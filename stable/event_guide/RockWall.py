#Rock Wall Event class
import event

object = event.Event("RockWall")

success = {
    "str": ["With nothing but your own brute strength, you haul yourself up the wall.", 
            "You manage to clamber over the wall."],

    "dex": ["You find hand and footholds in wall's nooks and crannies, enough to make your way up.", 
            "You scurry up the wall with ease."]
}

failure = {
    "str": ["You try a few times to pull yourself up the wall, but you aren't quite strong enough this time."],
 

    "dex": ["You try your hand at freesoloing the wall. It doesn't go well."]
}

end = ["You are forced to double back and find another way through.", 
       "You turn back, dejected."
       "It's no use, better find another way.", 
       "Not this time.", 
       "Your skills failed you on this one.",
       "Time to throw in the towel.", 
       "Better luck next time champ."]

object.add_stat("str", 20)
object.add_stat("dex", 10)

object.add_text("The path abruptly ends in a sheer rock wall.")

object.add_message(True, success)

object.add_message(False, failure)

object.add_end_message(end)