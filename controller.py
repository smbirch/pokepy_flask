import requests
import time
import sys
import random
import os

import bcrypt
import interface

import database


def get_all_mons():
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151&offset=0")
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        print("There was an error processing the request...\n")
        print("restarting")
        ellipsis = "..."
        time.sleep(0.5)
        for item in ellipsis:
            print(item, end=" ")
            sys.stdout.flush()
            time.sleep(0.4)
        print()
        restart_program()

    data = response.json()
    mon_id = 1
    for item in data["results"]:
        print(str(mon_id) + " - " + item["name"])
        mon_id += 1
    print("\n")
    return


# 3/25: issue: calling a pokemon that doesnt exist restarts program completely
def get_single_mon(monname):
    if monname == "" or monname == " ":
        print("Please check your spelling and try again.\n")
        return

    dbmon = database.Pokemon.get_mon(monname)
    if not dbmon:
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{monname}/")
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            print("There was an error processing the request...")
            print("Please check your spelling and try again.\n")
            time.sleep(1)
            restart_program()

        # extract data from json and store it in DB, then print for user
        data = response.json()
        montype = ""
        for attr in data["types"]:
            montype += attr["type"]["name"] + " "
        monobject = database.Pokemon(
            data["id"], data["name"], data["height"], data["weight"], montype
        )
        monobject.add_mon_todb()
        return monobject
    else:
        return dbmon


def get_team(userobject):
    teamobject = database.Team.get_team(userobject.userid)
    return teamobject


def make_team():
    pass


def get_user(username, password):
    user = database.User.get_user(username, password)

    if not user:
        print("\nUser not found!")
        restart_program()
    elif user == "401_unauthorized":
        print("Incorrect username or password!\nPlease try again")
        restart_program()
    else:
        return user


def get_all_users():
    userslist = database.User.get_all_users()
    if not userslist:
        print("No accounts found\n")
        return None
    return userslist


def create_user(username, password):
    userobject = database.User.check_for_user(username)
    if userobject:
        print("There is already a user with that username!")
        restart_program()

    userobject = database.User.create_user(username, password)
    if userobject == None:
        print("This username is already taken!\n")
        restart_program()
    database.Team.create_team(userobject.userid)
    return userobject


# This function literally just prints the text to stdout, but with a randomized delay so it scrolls in a cooler way
def learn_more():
    text = "This project utilizes the PokeApi, which can be found at https://pokeapi.co/\nFor more information about Pokemon, please visit https://www.serebii.net/\n"
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


def restart_program():
    os.execv(sys.executable, ["python"] + sys.argv)
