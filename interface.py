import questionary
import sys
import controller

    
def start_interface():
    question = questionary.select(
        "What do you want to do?",
        choices = [
            "See one Pokemon",
            "See all Pokemon",  
            "Make a team",        
            "Learn more",
            "Exit"
            ]
        ).ask()
    
    if question == "See one Pokemon": 
        monname = input("Which pokemon do you want to see more about? ")
        controller.get_single_mon(monname)
        
    elif question == "See all Pokemon":
       controller.get_all_mons()
       
    elif question == "Make a team":
        start_team() 
    
    elif question == "Learn more":
        controller.learn_more()
    
    elif question == "Exit":
        print("\n'Goodbye Butterfree, I'll always remember you...'")
        sys.exit(1)
        
        
def start_team():
    print("\nHere you can select 6 Pokemon to join you on your quest. Gotta catch 'em all!")
    question = questionary.select(
        "What do you want to do?",
        choices = [
            "Ready to add a Pokemon?",
            "See a list of all Pokemon",  
            "Check out a single Pokemon",        
            "Go back"
            ]
        ).ask()
    
    if question == "Add a Pokemon to your team?":
        ...
    elif question == "See a list of all Pokemon":
        controller.get_all_mons()
        start_team()
    elif question == "Check out a single Pokemon":
        monname = input("Which pokemon do you want to see more about? ")
        controller.get_single_mon(monname)
        start_team()
    elif question == "Go back":
        start_interface()
    
