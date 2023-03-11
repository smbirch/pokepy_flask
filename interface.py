import sys

import questionary

import controller
import database

    
def start_interface():
    question = questionary.select(
        "What do you want to do?",
        choices = [
            "See one Pokemon",
            "See all Pokemon",  
            "Make a team, or see a team you've made",        
            "Learn more",
            "Exit"
            ]
        ).ask()
    
    if question == "See one Pokemon": 
        monname = input("Which pokemon do you want to see more about? ")
        controller.get_single_mon(monname)
        
    elif question == "See all Pokemon":
       controller.get_all_mons()
       
    elif question == "Make a team, or see a team you've made":
        start_team() 
    
    elif question == "Learn more":
        controller.learn_more()
    
    elif question == "Exit":
        print("\n'Goodbye Butterfree, I'll always remember you...'")
        sys.exit(1)
        
        
# start_team() is the interface portion of the team builder 
def start_team():
    print("\nHere you can select 6 Pokemon to join you on your quest. Gotta catch 'em all!")
    hasusername = questionary.select(
    "Do you have an account already?",
    choices = [
        "Yes", 
        "No",
        "Go back"
        ]
    ).ask()
    # Do I need to move this out into the controller module? 
    if hasusername == "Yes":
        username = input("Enter your username: ")
        userobject = controller.get_user(username)
        build_team(userobject)
    
    elif hasusername == "No":
        print("let's create a new user...")
        username = input("Enter your username: ")
        userobject = controller.create_user(username)
        build_team(userobject)
        
    elif hasusername == "Go back":
        controller.restart_program()
        
    else:
        controller.restart_program()

def build_team(userobject):
    teamobject = controller.get_team(userobject)
    question = questionary.select(
        "What do you want to do?",
        choices = [
            "See your team",
            "Add a pokemon to your team",
            "Remove a pokemon from your team",
            "Delete your team",
            "See a list of all Pokemon",  
            "See a single Pokemon",        
            "Go back"
            ]
        ).ask()
    
    if question == "See your team":
        print(f"{userobject.username.capitalize()}'s team:\n{teamobject}")
        pass
        
    elif question == "Add a pokemon to your team":
        pass
        
    elif question == "See a list of all Pokemon":
        controller.get_all_mons()
        # start_team()
        
    elif question == "See a single Pokemon":
        monname = input("Which pokemon do you want to see more about? ")
        controller.get_single_mon(monname)
        # start_team()
        
    elif question == "Go back":
        controller.restart_program()
    

# show current mons in team by name and ID
# allow user to add a new mon if they have less than 6
# allow user to remove a mon
# allow user to delete entire team

