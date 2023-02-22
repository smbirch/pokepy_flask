import requests
import interface
import time


def get_all_mons():
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151&offset=0")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...")
        time.sleep(2)
        interface.start_interface()
        
    data = response.json()
    mon_id = 1
    for item in data["results"]:
        print(str(mon_id) + " - " + item["name"])
        mon_id += 1
    
    
def get_single_mon(monname):    
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{monname}/")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...")
        print("Please check your spelling and try again.")
        time.sleep(2)
        interface.start_interface()
        
    data = response.json()
    
    print("\nName: " + data["name"])
    print("ID: " + str(data["id"]))
    print("Height: " + str(data["height"]))
    print("Weight: " + str(data["weight"]))
    for attr in data["types"]:
        print("Type: " + attr["type"]["name"])
        
        
def make_team():
    
    pass        
        
def learn_more():
    print("\nThis project utilizes the PokeApi, which can be found at https://pokeapi.co/")
    print("For more info about Pokemon, please visit https://www.serebii.net/")
    # print("\n\nThis project was made for the author's personal use and should not be cloned, forked, or otherwise distributed or monetized in any way without the author's permission.")
    print("...\n")
    time.sleep(3)
    interface.start_interface()
