import requests
import sys
import interface


# Working on now:
# questionary?
# See list of all monsters
# store monsters in db that have already been Get-ted
# Allow users to select up to six mons.
# Store chosen monsters somewhere


def main():
    interface.testfunc()
    print("Strong Pokémon, weak Pokémon, that is only the foolish perception of people. Truly skilled trainers should try to win with their favorites. \n- Karen (Gold, Silver, Crystal)")
    interface.start_interface()


def get_single_mon(monname):
    print("running...")
    
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
        
        


if __name__ == "__main__":
    main()