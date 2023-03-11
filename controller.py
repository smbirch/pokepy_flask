import requests
import interface
import time
import sys
import random
import os

import database


def get_all_mons():
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151&offset=0")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...\n")
        time.sleep(2)
        restart_program()
        
    data = response.json()
    mon_id = 1
    for item in data["results"]:
        print(str(mon_id) + " - " + item["name"])
        mon_id += 1
    print()
    restart_program()
    
    
    
def get_single_mon(monname):
    if monname == "" or monname == " ":
        print("Please check your spelling and try again.\n")
        restart_program()

        
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
        monobject = database.Pokemon(data["id"], data["name"], data["height"], data["weight"], montype)
        print(monobject)
        monobject.add_mon_todb()
        restart_program()
        
    else:
        print(dbmon)
        restart_program()
        
        

def get_team(userobject):
    teamobject = database.Team.get_team(userobject.userid)
    # print(teamobject)
    return teamobject
    

def make_team():
    pass     


def get_user(username):
    user = database.User.get_user(username)
    if not user:
        print("User not found!")
        interface.start_team()
    print(user.userid)
    return user
    
def create_user(username):
    userobject = database.User.get_user(username)
    if userobject:
        print("There is already a user with that username!")
        interface.start_team()
    userobject = database.User.create_user(username)
    database.Team.create_team(userobject.userid)
    
# This function literally just prints the text to stdout, but with a randomized delay so it *kinda* scrolls like in a game
def learn_more():
    text = "This project utilizes the PokeApi, which can be found at https://pokeapi.co/\nFor more information about Pokemon, please visit https://www.serebii.net/\n"
    for item in text:
        print(item, end='')
        sys.stdout.flush()
        sleeptimer = random.uniform(0.03, 0.099)
        time.sleep(sleeptimer)

    ellipsis = "..."
    time.sleep(.5)
    for item in ellipsis:
        print(item, end=' ')
        sys.stdout.flush()
        time.sleep(.4)
    print()
    restart_program()


def restart_program():
    os.execv(sys.executable, ['python'] + sys.argv)