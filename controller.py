import asyncio
import requests
import time
import sys
import random

import database
import app

allmons = []


def get_all_mons():
    """Gets a list of the names of each mon.

    Returns:
        list: list of strings containing mon names.
    """

    global allmons
    if len(allmons) == 0:
        try:
            response = requests.get(
                "https://pokeapi.co/api/v2/pokemon?limit=151&offset=0"
            )
            response.raise_for_status()

        except Exception as err:
            app.errorlogs.error(f"all_mons: {err}")
            return "error"

        data = response.json()

        for item in data["results"]:
            allmons.append(item["name"])
    return allmons


def get_single_mon(monname):
    """Get a single mon from API or DB.

    Args:
        monname (string): string of a mon name

    Returns:
        class object: instance of the Pokemon class. See database.py.
    """

    url = f"https://pokeapi.co/api/v2/pokemon/{monname.lower()}/"

    dbmon = database.Pokemon.get_mon(monname)
    if not dbmon:
        try:
            response = requests.get(url)
            response.raise_for_status()

        except Exception as err:
            app.errorlogs.error(f"get_single_mon {monname}: {err}")
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
    """Gets an class instance of a user's team.

    Args:
        userid (string): Hex string generated when the user object was created.

    Returns:
        class: Returns a class instance of a user's team.
    """

    teamobject = database.Team.get_team(userid)
    return teamobject


def make_random_team(teamobject):
    """Generate a random team of mons for a user.

    Args:
        teamobject (class): An instance of the Team class.

    Returns:
        class: An instance of the Team class.
    """

    database.Team.delete_team(teamobject)

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
    """Gets a user from database.

    Args:
        username (string): String of a user's username.
        password (string): A user's plaintext passwor, usually given at login.

    Returns:
        class: An instance of the User class.
    """

    user = database.User.get_user(username, password)

    if not user:
        return "404"

    elif user == "401_unauthorized":
        return "401"
    else:
        return user


# This method is used to pull users who are already authenticated
def get_user_session(username):
    """Gets users who are already authenticated.

    Args:
        username (string)

    Returns:
        class: An instance of the User class.
    """

    user = database.User.get_user_session(username)

    if not user:
        return "404"
    else:
        return user


def get_all_users():
    """Gets a list of all users.

    Returns:
        list: A list of strings containing usernames.
    """

    userslist = database.User.get_all_users()
    if not userslist:
        return None
    return userslist


def create_user(username, password):
    """Creates a new user.

    Args:
        username (string): A username string given during registration.
        password (string): A user's plaintext password given during registration.

    Returns:
        class: An instance of the User class.
    """

    userobject = database.User.get_user(username.lower(), password)
    if userobject:
        return "duplicateaccounterror"

    userobject = database.User.create_user(username, password)
    # Ideally you would never receive None here...
    if userobject == None:
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


def delete_account(username):
    """Delete a user account.

    Args:
        username (string): a username, which should always be unique.

    Returns:
        None
    """
    userobject = database.User.get_user_session(username)
    if database.User.delete_account(userobject) == "Error deleting account":
        return "delete_error"
