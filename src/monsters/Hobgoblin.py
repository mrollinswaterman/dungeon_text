#Hobgoblin mob file
import random
import mob, player, global_commands

print("GOBLIN DEEZ NTS")

stats = mob.Statblock("Hobgoblin")

stats.set_hp(6)
stats.set_damage(5)
stats.set_evasion(9)
stats.set_armor(1)
stats.set_gold(8)
stats.set_xp(6)
stats.set_dc(14)
stats.set_min_max((1, 5))

def special(source: mob.Mob, target: player.Player) -> bool:
    """
    Taunt: Reduces the player's evasion by 2 points for 2 turns if they fail a charisma check
    """
    global_commands.type_with_lines(f" The {source.id} hurls enraging insults at you.\n")

    if target.roll_a_check("cha") >= source.dc:
        global_commands.type_text(f" Your mind is an impenetrable fortess. The {source.id}'s words have no effect.")

    else:
        global_commands.type_text(f" The {source.id}'s insults distract you, making you an easier target.\n")
        taunt = player.Status_Effect("Taunt", source, "evasion", target)
        taunt.set_duration(3)
        taunt.set_power(-2)
        taunt.set_message(f" Your Evasion has been redcued by 2 by the {source.id}'s Taunt!")
        target.add_status_effect(taunt)

def conditions(target: player.Player) -> bool:
    if target.evasion > 10:
        return True
    return False

stats.set_special(special)
stats.special.set_conditions(conditions, True)




