import requests
import interface
import time
import sys
import random

import database


def get_all_mons():
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151&offset=0")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...\n")
        time.sleep(2)
        interface.start_interface()
        
    data = response.json()
    mon_id = 1
    for item in data["results"]:
        print(str(mon_id) + " - " + item["name"])
        mon_id += 1
    print()
    interface.start_interface()    
    
    
def get_single_mon(monname): 
    # todo: check if mon is in DB already
    dbmon = database.Pokemon.get_mon(monname)
    if not dbmon:
        # print("trying request")
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{monname}/")
            response.raise_for_status()
            
        except requests.exceptions.HTTPError:
            print("There was an error processing the request...")
            print("Please check your spelling and try again.\n")
            time.sleep(1)
            interface.start_interface()
        
        # extract data from json and store it in DB, then print for user  
        data = response.json()
        montype = ""
        for attr in data["types"]:
            montype += attr["type"]["name"] + " "
        monobject = database.Pokemon(data["id"], data["name"], data["height"], data["weight"], montype)
        print(monobject)
        monobject.add_mon_todb()
        interface.start_interface()
        
    else:
        print(dbmon)
        

def get_team(username):
    userobject = database.User.get_team(username)
    if not userobject:
            print("User not found")
            return
            # make them create a user or go back
    else:
        team = database.get_team(userobject.id)
        return team



def make_team():
    pass        
        
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
    interface.start_interface()
