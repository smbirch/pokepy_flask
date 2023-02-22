import questionary
import requests
import sys

    
def start_interface():
    test = questionary.select(
        "What do you want to do?",
        choices = [
            "Make a team",
            "See all Pokemon",
            "See one Pokemon",
            "Learn more"
            ]
        ).ask()
    
    if test == "Make a team":
       make_team()
    elif test == "See all Pokemon":
       get_all_mons()
    elif test == "See one Pokemon": 
        monname = input("Which pokemon do you want to see more about? ")
        get_single_mon(monname)
    elif test == "Learn more":
        learn_more()
        
        
def make_team():
    pass
    

def get_all_mons():
    
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151&offset=0")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...")
        print("Please check your spelling and try again.")
        sys.exit(1)
        
    data = response.json()
    mon_id = 1
    for item in data["results"]:
        print(str(mon_id) + " - " + item["name"])
        mon_id += 1
    
    start_interface()
    
    
def get_single_mon(monname):    
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{monname}/")
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print("There was an error processing the request...")
        print("Please check your spelling and try again.")
        sys.exit(1)
        
    data = response.json()
    
    print("Name: " + data["name"])
    print("ID: " + str(data["id"]))
    print("Height: " + str(data["height"]))
    print("Weight: " + str(data["weight"]))
    for attr in data["types"]:
        print("Type: " + attr["type"]["name"])
        
        
def learn_more():
    pass
