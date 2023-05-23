import requests
import time
import sys
import random

import database

allmons = []


def get_all_mons():
    global allmons
    if len(allmons) == 0:
        try:
            response = requests.get(
                "https://pokeapi.co/api/v2/pokemon?limit=151&offset=0"
            )
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            print("There was an error processing the request...\n")
            print("restarting")

        data = response.json()

        for item in data["results"]:
            allmons.append(item["name"])

    return allmons


def get_single_mon(monname):
    monname = monname.lower()

    dbmon = database.Pokemon.get_mon(monname)
    if not dbmon:
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{monname}/")
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            print("\nThere was an error processing the request...")
            print("Please check your spelling and try again.\n")
            return None

        # extract data from json and store it in DB
        data = response.json()

        montype = ""
        for attr in data["types"]:
            montype += attr["type"]["name"] + " "
        sprite = data["sprites"]["front_default"]
        monobject = database.Pokemon(
            data["id"],
            data["name"],
            data["height"],
            data["weight"],
            montype,
            sprite,
        )
        monobject.add_mon_todb()
        return monobject
    else:
        return dbmon


def get_team(userid):
    teamobject = database.Team.get_team(userid)
    return teamobject


def make_random_team(teamobject):
    database.Team.delete_team(teamobject)
    global allmons
    if len(allmons) == 0:
        allmons = get_all_mons()

    shuffled_mons = []
    for mon in allmons:
        shuffled_mons.append(mon)
    random.shuffle(shuffled_mons)

    for _ in range(6):
        randmon = shuffled_mons.pop()
        monobject = get_single_mon(randmon)
        teamobject = database.Team.add_mon_to_team(teamobject, monobject)
    return teamobject


def update_team(teamobject, position, newmon):
    mons = [
        teamobject.mon1,
        teamobject.mon2,
        teamobject.mon3,
        teamobject.mon4,
        teamobject.mon5,
        teamobject.mon6,
    ]

    # move mon in question to end of list and then replace it
    mons[position] = newmon
    mons.append(mons.pop(position))

    for index, mon in enumerate(mons):
        database.Team.update_team(teamobject, index + 1, mon)


def get_user(username, password):
    user = database.User.get_user(username, password)

    if not user:
        print("\nUser not found!")
        return "404"

    elif user == "401_unauthorized":
        print("Incorrect password!\nPlease try again")
        # restart_program()
        return "401"
    else:
        return user


# This method is used to pull users who are already authenticated
def get_user_session(username):
    user = database.User.get_user_session(username)

    if not user:
        print("\nUser not found!")
        return "404"
    else:
        return user


def get_all_users():
    userslist = database.User.get_all_users()
    if not userslist:
        return None
    return userslist


def create_user(username, password):
    userobject = database.User.get_user(username.lower(), password)
    if userobject:
        print("There is already a user with that username!")
        return "duplicateaccounterror"
        restart_program()

    userobject = database.User.create_user(username, password)
    # Ideally you would never receive None here...
    if userobject == None:
        print("This username is already taken!\n")
        return "duplicateaccounterror"

    database.Team.create_team(userobject.userid)
    return userobject


def learn_more():
    text = "\nThis project utilizes the PokeApi, which can be found at https://pokeapi.co/\nFor more information about Pokemon, please visit https://www.serebii.net/\n"
    for item in text:
        print(item, end="")
        sys.stdout.flush()
        sleeptimer = random.uniform(0.03, 0.099)
        time.sleep(sleeptimer)

    ellipsis = "..."
    time.sleep(0.5)
    for item in ellipsis:
        print(item, end=" ")
        sys.stdout.flush()
        time.sleep(0.4)
    print()


def delete_account(userid):
    userobject = database.User.get_user_session(userid)
    if database.User.delete_account(userobject) == "Error deleting account":
        return "delete_error"
    else:
        print(f"\n***{userobject.username}'s account has been deleted***\n")


# Passing this function for now to test web API
def restart_program():
    # os.execv(sys.executable, ["python"] + sys.argv)
    pass
