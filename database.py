import sqlite3
from sqlite3 import Error
import os

# working on now:
# creating DB class

# class DB:
#     def __init__(self, db_path):
#         self.connection = sqlite3.connect(db_path)

class User:
    pass

class Pokemon:
    def __init__(self, id, name, height, weight, montype):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.montype = montype
        
    def __str__(self):
        return f"ID: {self.id}\nName: {self.name.capitalize()}\nHeight: {self.height}\nWeight: {self.weight}\nType: {' '.join(str(x).capitalize() for x in self.montype)}"
    
    # adds a single mon to database mons table
    def add_mon(self):
        try:
            connection = sqlite3.connect("data/pokepy.db")
            cursor = connection.cursor()
    
            insert_with_params = """INSERT INTO mons(
                monid, name, height, weight, type)
                VALUES(?, ?, ?, ?, ?);"""
            
            mondata_tuple = (self.id, self.name, self.height, self.weight, ' '.join(str(x).capitalize() for x in self.montype))

            cursor.execute(insert_with_params, mondata_tuple)
            connection.commit()
            print("Mon inserted into DB")            

        except Error as e:
            print("Error while adding mon to DB")
            print(e)
            
            
        finally:
            if connection:
                connection.close()
                
    # This should return either the pokemon object or None 
    def get_mon(self, monname):
        pass
        
        
        
        
def create_db():
    if not os.path.exists("data/pokepy.db"):
        try:
            # DB.__init__("data/pokepy.db")
            connection = sqlite3.connect("data/pokepy.db")
            print("DB connected!")
            print(sqlite3.version)
            cursor = connection.cursor()
            
            # create users table
            # userID here CANNOT be below 151
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
                    type TEXT);
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