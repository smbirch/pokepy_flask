import main
import questionary


def testfunc():
    print("testestestestest")
    
    
def start_interface():
   test = questionary.select(
        "What do you want to do?",
        choices = [
            "Make a team",
            "See all Pokemon",
            "See one Pokemon"
            ]
    ).ask()
   print(type(test))
    
 
    # if answer == "Make a team":
    #     make_team()
    # elif answer == "See all Pokemon":
    #     get_all_mons()
    # elif answer == "See one Pokemon":
    #     monname = input("Name of the Pokemon: ")
    #     main.get_single_mon(monname)
        
        
        
        
def make_team():
    pass
    

def get_all_mons():
    pass