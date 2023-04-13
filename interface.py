import sys

import questionary

import controller
import database


def setup_user():
    print(
        "\nWelcome to Pokepy! First, you will need to register or load your account.\n"
    )
    userslist = controller.get_all_users()
    print(f"Accounts present:\n{userslist}\n")

    hasusername = questionary.select(
        "Do you have an account already?", choices=["Yes", "No", "Quit"]
    ).ask()
    if hasusername == "Yes":
        username = input("Enter your username: ")
        password = questionary.password("\nEnter your password: ").ask()

        userobject = controller.get_user(username, password)
        start_interface(userobject)

    elif hasusername == "No":
        print("let's create a new user...")
        username = input("\nEnter your username: ")

        password = questionary.password("\nEnter your password: ").ask()
        passwordcheck = questionary.password("Re-enter your password: ").ask()
        if password != passwordcheck:
            print("\nThese passwords do not match!\nPlease try again")
            controller.restart_program()

        # database.User.check_for_user(username)
        userobject = controller.create_user(username, password)
        start_interface(userobject)

    elif hasusername == "Quit":
        print("Goodbye")
        sys.exit(0)

    else:
        controller.restart_program()


def start_interface(userobject):
    question = questionary.select(
        "What do you want to do?",
        choices=[
            "See one Pokemon",
            "See all Pokemon",
            "See your team",
            "Learn more",
            "Exit",
        ],
    ).ask()

    if question == "See one Pokemon":
        monname = input("Which pokemon do you want to see more about? ")
        mon = controller.get_single_mon(monname)
        if mon:
            print(mon)
        start_interface(userobject)

    elif question == "See all Pokemon":
        controller.get_all_mons()
        start_interface(userobject)

    elif question == "See your team":
        build_team(userobject)

    elif question == "Learn more":
        controller.learn_more()
        start_interface(userobject)

    elif question == "Exit":
        print("\n'Goodbye Butterfree, I'll always remember you...'")
        sys.exit(1)


def build_team(userobject):
    teamobject = controller.get_team(userobject)
    teamsize = database.Team.team_size(teamobject)
    print(f"\n{userobject.username.capitalize()}'s team:\n{teamobject}")

    if teamsize == 6:
        print("\nYour team is full!")
        print("You will need to remove a mon before adding a new one")
    else:
        print(f"\nYour team currently has {teamsize}/6 members")
        print(f"You can add {6 - teamsize} more.\n")
    question = questionary.select(
        "What do you want to do?",
        choices=[
            "See your team",
            "Add a Pokemon to your team",
            "Remove a Pokemon from your team",
            "Delete your team",
            "Get a random team",
            "See a list of all Pokemon",
            "See a single Pokemon",
            "Go back",
        ],
    ).ask()

    if question == "See your team":
        print(f"\n{userobject.username.capitalize()}'s team:\n{teamobject}")
        build_team(userobject)

    elif question == "Add a Pokemon to your team":
        montoadd = input("What mon do you want to add? ")
        monobject = controller.get_single_mon(montoadd)
        database.Team.add_mon_to_team(teamobject, monobject)
        build_team(userobject)

    elif question == "Remove a Pokemon from your team":
        remove_mon_from_team(userobject, teamobject)

    elif question == "Delete your team":
        print("Deleting team!")
        database.Team.delete_team(teamobject)
        build_team(userobject)

    elif question == "Get a random team":
        controller.make_random_team(userobject, teamobject)

    elif question == "See a list of all Pokemon":
        monslist = controller.get_all_mons()
        mon_id = 1
        for item in monslist:
            print(str(mon_id) + " - " + item["name"])
            mon_id += 1

        build_team(userobject)

    elif question == "See a single Pokemon":
        monname = input("Which pokemon do you want to see more about? ")
        controller.get_single_mon(monname)
        build_team(userobject)

    elif question == "Go back":
        start_interface(userobject)


def remove_mon_from_team(userobject, teamobject):
    print(f"\n{userobject.username}'s current team:\n{teamobject}")
    print("\n***")
    choices = []
    teamsize = database.Team.team_size(teamobject)
    if teamsize == 0:
        print("\nYou have no mons to remove!\n")
        build_team(userobject)
    else:
        for i in range(teamsize):
            choices.append(getattr(teamobject, f"mon{i + 1}"))  # TODO: fix this

        question = questionary.checkbox(
            "Select mon(s) to remove:",
            choices,
        ).ask()

        for position, montoremove in enumerate(choices):
            if montoremove in question:
                position += 1
                database.Team.remove_mon_from_team(teamobject, position)
        build_team(userobject)
