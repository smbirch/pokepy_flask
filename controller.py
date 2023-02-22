import requests
import interface
import time
import sys


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
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{monname}/")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...")
        print("Please check your spelling and try again.\n")
        time.sleep(2)
        interface.start_interface()
        
    data = response.json()
    
    print("\nName: " + data["name"])
    print("ID: " + str(data["id"]))
    print("Height: " + str(data["height"]))
    print("Weight: " + str(data["weight"]))
    for attr in data["types"]:
        print("Type: " + attr["type"]["name"])
    print()
        
    interface.start_interface()
        
        
def make_team():
    
    pass        
        
def learn_more():
    text = "This project utilizes the PokeApi, which can be found at https://pokeapi.co/\nFor more info about Pokemon, please visit https://www.serebii.net/\n"
    for item in text:
        print(item, end='')
        sys.stdout.flush()
        time.sleep(0.05)
    
    
    # print("\nThis project utilizes the PokeApi, which can be found at https://pokeapi.co/")
    # print("For more info about Pokemon, please visit https://www.serebii.net/")
    ellipsis = "..."
    time.sleep(1)
    for item in ellipsis:
        print(item, end='')
        sys.stdout.flush()
        time.sleep(1)
    print()
    interface.start_interface()
