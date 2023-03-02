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
        # print(self.montype)
        return f"ID: {self.id}\nName: {self.name.capitalize()}\nHeight: {self.height}\nWeight: {self.weight}\nType: {(self.montype)}"
    
    # adds a single mon to database mons table
    def add_mon_todb(self):
        try:
            connection = sqlite3.connect("data/pokepy.db")
            cursor = connection.cursor()
            # This section below can probably be done more smoothly
            # Do I really need to convert the whole object to tuple each time?
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
    @staticmethod
    def get_mon(monname):
        # see if this mon exists in DBs
        try:
            query = "SELECT EXISTS(SELECT 1 from mons where name = ?);"
            connection = sqlite3.connect("data/pokepy.db")
            cursor = connection.cursor()
            cursor.execute(query, (monname,))
           
            # if row exists in DB
            if cursor.fetchone():
                query = "SELECT * FROM mons where name = ?;"
                cursor.execute(query, (monname,))
                
                for row in cursor:
                    monobject = Pokemon(*row)
                    print("from DB: ")
                    return monobject
            else:
                return None

        except Error as e:
            print("Error getting mon from DB")
            print(e)

        finally:
            if connection:
                connection.close()
            
            
def create_db():
    if not os.path.exists("data/pokepy.db"):
        try:
            connection = sqlite3.connect("data/pokepy.db")
            print("DB connected!")
            print(sqlite3.version)
            cursor = connection.cursor()
            
            # create users table
            # userID should be 5 digits
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