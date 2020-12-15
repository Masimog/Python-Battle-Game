from classes.game import Person, BColors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 20, 600, "black")
thunder = Spell("Thunder", 24, 720, "black")
blizzard = Spell("Blizzard", 18, 540, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 28, 840, "black")


# Create White Magic
cure = Spell("Cure", 24, 620, "white")
cura = Spell("Cura", 36, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixir", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/Mp of all party members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Ciri       :", 3260, 165, 270, 34, player_spells, player_items)
player2 = Person("Geralt     :", 4160, 165, 180, 34, player_spells, player_items)
player3 = Person("Yennefer   :", 3100, 195, 180, 34, player_spells, player_items)

# Instantiate Enemies
enemy1 = Person("Imp        :", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Coronavirus:", 18200, 700, 525, 25, enemy_spells, [])
enemy3 = Person("Imp        :", 1250, 130, 560, 325, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(BColors.FAIL + BColors.BOLD + "AN ENEMY ATTACKS!" + BColors.ENDC)

while running:
    print("==============================")

    print("\n\n")
    print("NAME                    HP                                      MP")
    for player in players:
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")  # Force the player to only choose specific number
        index = int(choice) - 1

        # Use simple attack
        if index == 0:

            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name.replace(" ", ""), " attacked " + enemies[enemy].name.replace(" ", "") + "for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        # Use magic
        elif index == 1:

            player.choose_magic()
            magic_choice = int(input("    Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            # Check the mana cost for the spell
            if spell.cost > current_mp:
                print(BColors.FAIL + "\nNot enough MP" + BColors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            # Check if its a healing or a damaging spell
            if spell.type == "white":
                player.heal(magic_dmg)
                print(BColors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + BColors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(BColors.OKBLUE + "\n" + spell.name + " deals ", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + BColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        # Use item
        elif index == 2:

            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            # Check item quantity
            if player.items[item_choice]["quantity"] == 0:
                print(BColors.FAIL + "\n" + "None left..." + BColors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            # Check item type
            if item.type == "potion":
                player.heal(item.prop)
                print(BColors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop), "HP" + BColors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(BColors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + BColors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(BColors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + BColors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if battle is over
    if len(enemies) == 0:
        running = False
        print(BColors.OKGREEN + "You win!" + BColors.ENDC)
    elif len(players) == 0:
        running = False
        print(BColors.FAIL + "You lose!" + BColors.ENDC)

    # Enemy actions
    print("\n")
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(BColors.FAIL + BColors.BOLD + enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for "
                  + str(enemy_dmg), "points of damage" + BColors.ENDC)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(BColors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for", str(magic_dmg), "HP." + BColors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)
                print(BColors.OKBLUE + enemy.name.replace(" ", "") + spell.name + " deals", str(magic_dmg), "points of damage to "
                      + players[target].name.replace(" ", "") + BColors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
