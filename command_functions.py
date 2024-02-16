



def exit_game():
        RUNNING = False
        sys.exit()
    def attack(enemy: mob.Mob) -> None:

        print(f'\nYou attack the {enemy.id}.\n')
        if GOD_MODE is True:
            attack_roll = 1000000
        else:
            attack_roll = PLAYER.roll_attack_roll()
        print(f'You rolled a {attack_roll}.\n')

        if attack_roll == 20:
            print("Critical Hit!\n")

        if attack_roll == 1:
            print("Crtical Fail!\n")

        if attack_roll >= enemy.evasion:
            if GOD_MODE is True:
                taken = enemy.take_damage(1000)
            else:
                taken = enemy.take_damage(PLAYER.roll_damage())
            
            print(f'You hit the {enemy.id}, dealing {taken} damage.\n')
            if enemy.dead is False:
                enemy_turn()
            elif enemy.dead is True:
                end_scene()
        elif attack_roll < enemy.evasion:
            print("You missed.\n")
            enemy_turn()

    
    def hp():
        narrator.display_hp(PLAYER)
        player_turn()

    def inventory():
        print(f'\nGold: {PLAYER.gold}\n')
        PLAYER.print_inventory()
        player_turn()