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
            "Add a pokemon to your team",
            "Remove a pokemon from your team",
            "Delete your team",
            "See a list of all Pokemon",  
            "See a single Pokemon",        
            "Go back"
            ]
        ).ask()
    
    if question == "See your team":
        user_team()
        
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
        start_interface()
    
    
def user_team():
    # database.User.check_user()
    hasusername = questionary.select(
    "Do you have an account already?",
    choices = [
        "Yes", 
        "No",
        "Go back"
        ]
    ).ask()
    
    if hasusername == "Yes":
        username = input("Enter your username: ")
        team = controller.get_team(username)
        print(team)
        

    elif hasusername == "No":
        username = input("Enter your username: ")
        database.User.create_user(username)
    
    elif hasusername == "Go back":
        start_interface()
# show current mons in team by name and ID
# allow user to add a new mon if they have less than 6
# allow user to remove a mon
# allow user to delete entire team

