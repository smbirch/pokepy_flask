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
        
        
# start_team() is the interface portion of the team builder 
def start_team():
    print("\nHere you can select 6 Pokemon to join you on your quest. Gotta catch 'em all!")
    question = questionary.select(
        "What do you want to do?",
        choices = [
            "See your team",
            "See a list of all Pokemon",  
            "Check out a single Pokemon",        
            "Go back"
            ]
        ).ask()
    
    if question == "See your team":
        user_team()
        
    elif question == "See a list of all Pokemon":
        controller.get_all_mons()
        start_team()
        
    elif question == "Check out a single Pokemon":
        monname = input("Which pokemon do you want to see more about? ")
        controller.get_single_mon(monname)
        start_team()
        
    elif question == "Go back":
        start_interface()
    
    
def user_team():
    pass
# show current mons in team by name and ID
# allow user to add a new mon if they have less than 6
# allow user to remove a mon
# allow user to delete entire team

# will need a model.py file to start working this out