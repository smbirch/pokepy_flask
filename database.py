import sqlite3
from sqlite3 import Error
import os

database_file = "data/pokepy.db"


class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        
    def __enter__(self):
        return self
                   
    def execute_query(self, query, *args):
        if self.conn:
            try:
                self.cursor.execute(query, args)
                
            except Error as e:
                print("Error executing db query")
                print(e)
                
    def commit(self):
        try:
            self.conn.commit()
        except Error as e:
            print("db commit error")
            print(e)
        
    def close(self):
        if self.conn:
            self.conn.close()
        
    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.conn.rollback()
            
        else:
            self.commit()
            self.close()
        

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
        return f"ID: {self.id}\nName: {self.name.capitalize()}\nHeight: {self.height}\nWeight: {self.weight}\nType: {self.montype.title()}"
    
    # adds a single mon to database mons table
    def add_mon_todb(self):
        with DBConnection() as db:
            insert_with_params = """INSERT INTO mons(
                    monid, name, height, weight, type)
                    VALUES(?, ?, ?, ?, ?);""" 
            mondata = (self.id, self.name.lower(), self.height, self.weight, self.montype)
            db.execute_query(insert_with_params, *mondata)
        
    # This should return either the pokemon object from DB, or None 
    @staticmethod
    def get_mon(monname):
        # see if this mon exists in DB
        with DBConnection() as db:
            query = "SELECT * FROM mons where name = ?;"
            db.execute_query(query, monname)
            if db.cursor == None:
                return None

            else:
                for row in db.cursor:
                    monobject = Pokemon(*row)
                    # print("from DB: ")
                    return monobject
    
         
def create_db():
    if os.path.exists("data/pokepy.db"):
        return
    
    # create users table
    # userID should be 5 digits
    with DBConnection() as db:
        users_table = """CREATE TABLE IF NOT EXISTS users(
            userid INTEGER PRIMARY KEY, 
            username TEXT,
            date_created INTEGER,
            has_team INTEGER);
            """
        db.execute_query(users_table)
        print("users table created")

        # create mons table
        # cache data about monsters that have previously been called upon: 
        mons_table = """CREATE TABLE IF NOT EXISTS mons(
            monid INTEGER PRIMARY KEY NOT NULL,
            name TEXT,
            height INTEGER,
            weight INTEGER,
            type TEXT);
            """
        db.execute_query(mons_table)
        print("mons table created")
       
        # create teams table
        # links user ID and monster IDs
        teams_table = """CREATE TABLE IF NOT EXISTS teams(
            userid INTEGER PRIMARY KEY,
            mon1 INTEGER,
            mon2 INTEGER,
            mon3 INTEGER,
            mon4 INTEGER,
            mon5 INTEGER,
            mon6 INTEGER);
            """
        db.execute_query(teams_table)
        print("teams table created")
        

def get_team():
    pass