#Boulder Event class
import events

object = events.Event()

success = {
    "str": ["You push the boulder aside and continue on your way.", 
            "You smash the boulder to rubble for daring to stand in your way."],

    "dex": ["You manage to squeeze by the boulder.", "You're flexible enough to make it past."]
}
failure = {
    "str": ["You push with all your might, but the boulder doesn't budge. You'll need to push a little harder.", 
            "You punch the boulder. Nothing happens. Maybe if you punched it harder?"],

    "dex": ["You do a backflip. The boulder is unimpressed. You think you might be able to squeezing past it, if you tried.",
            "You try to squeeze past, but don't quite make it. You wriggle yourself out before you get stuck."]
}

object.add_stat(("str", 10))
object.add_stat(("dex", 15))
#event text
object.add_text(' A boulder blocks your way.')

#success lines
object.add_message((True, "str", success["str"]))
object.add_message((True, "dex", success["dex"]))

#failure lines
object.add_message((False, "str", failure["str"]))
object.add_message((False, "dex", failure["dex"]))

#out of tries
object.add_end_message("You are forced to double back and find another way through.")