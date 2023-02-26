import sqlite3
from sqlite3 import Error
import os

def init_db():
    if not os.path.exists("data/pokepy.db"):
        try:
            connection = sqlite3.connect("data/pokepy.db")
            print("DB connected!")
            print(sqlite3.version)
            cursor = connection.cursor()
            
            # create users table
            try:
                cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    userid INTEGER PRIMARY KEY,
                    username TEXT,
                    date_created INTEGER,
                    has_team INTEGER);
                    """)
                print("users table created")
            except Error as e:
                print("users table creation error")
                print(e)
                
            # create mons table
            # cache data about monsters that have previously been called upon: 
            try:
                cursor.execute("""CREATE TABLE IF NOT EXISTS mons(
                    monid INTEGER PRIMARY KEY,
                    name TEXT,
                    height INTEGER,
                    weight INTEGER,
                    type1 TEXT,
                    type2 TEXT)
                    """)
                print("mons table created")
            except Error as e:
                print("mons table creation error")
                print(e)
                
            # create teams table
            # links user ID and monster IDs
            try:
                cursor.execute("""CREATE TABLE IF NOT EXISTS teams(
                    userid INTEGER PRIMARY KEY,
                    mon1 INTEGER,
                    mon2 INTEGER,
                    mon3 INTEGER,
                    mon4 INTEGER,
                    mon5 INTEGER,
                    mon6 INTEGER);
                    """)
                print("teams table created")
            except Error as e:
                print("teams table creation error")
                print(e)
                
            try:
                connection.commit()
            except Error as e:
                print("db commit error")
                print(e)
                
        except Error as e:
            print("DB connection error")
            print(e)
        
        finally:
            if connection:
                connection.close()
        
        

    
def get_team():
    pass

def add_mons():
    pass
# add mons to list 
# one by one or as a batch? 


# users table:
# userid - int, username - text, date_created - integer (unix time), has_team - integer
    # INSERT INTO users (date_created)
    # VALUES(strftime('%s','now'));
# userid will not be a number less than 151: no conflict with pokemon IDs

#mons table:
# store data about monsters that have previously been called upon: 
    # this will help cut down on calls in future - this data will not ever change

# monID, name, height, weight, type1, type2


# teams table:
# stores teams of each user
# this can just store mon ID number, then pull from mons table

# userID, mon1, mon2, mon3, mon4, mon5, mon6 -- All INT type