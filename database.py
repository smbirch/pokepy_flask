import sqlite3
from sqlite3 import Error
import os
import datetime
import uuid

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
    def __init__(self, userid, username, date_created):
        self.userid = userid
        self.username = username
        self.date_created = date_created

    def __str__(self):
        return self.username

    @staticmethod
    def get_user(username):
        print(f"check user! - {username}")
        with DBConnection() as db:
            query = "SELECT * FROM users WHERE username = ?"
            db.execute_query(query, username)
            if db.cursor == None:
                return None
            else:
                for row in db.cursor:
                    userobject = User(*row)
                    return userobject

    @staticmethod
    def get_all_users():
        users = []
        with DBConnection() as db:
            query = "SELECT * FROM users"
            db.execute_query(query)
            if db.cursor == None:
                return None
            else:
                for row in db.cursor:
                    users.append(row[1])
                return users

    @staticmethod
    def create_user(username):
        with DBConnection() as db:
            userid = uuid.uuid4().hex
            now = datetime.datetime.now()
            date_created = f"{now.date()} {now.time()}"

            create_user_sql = """INSERT INTO users(
                userid, username, date_created)
                VALUES(?, ?, ?);"""
            userdata = (userid, username, date_created)
            db.execute_query(create_user_sql, *userdata)
            userobject = User(userid, username, date_created)
        # Now we will create an empty team for this user at the same time using their uuid to link them
        # print("user inserted into DB")
        return userobject


class Pokemon:
    def __init__(self, id, name, height, weight, montype):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.montype = montype

    def __str__(self):
        return f"ID: {self.id}\nName: {self.name.capitalize()}\nHeight: {self.height}\nWeight: {self.weight}\nType: {self.montype.title()}\n"

    # adds a single mon to database mons table
    def add_mon_todb(self):
        with DBConnection() as db:
            insert_with_params = """INSERT INTO mons(
                    monid, name, height, weight, type)
                    VALUES(?, ?, ?, ?, ?);"""
            mondata = (
                self.id,
                self.name.lower(),
                self.height,
                self.weight,
                self.montype,
            )
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
                    return monobject


class Team:
    def __init__(self, userid, mon1, mon2, mon3, mon4, mon5, mon6):
        self.teamid = userid
        self.mon1 = mon1
        self.mon2 = mon2
        self.mon3 = mon3
        self.mon4 = mon4
        self.mon5 = mon5
        self.mon6 = mon6

    def __str__(self):
        return f"1: {self.mon1}\n2: {self.mon2}\n3: {self.mon3}\n4: {self.mon4}\n5: {self.mon5}\n6: {self.mon6}"

    def delete_team(self):
        with DBConnection() as db:
            db.execute_query("DELETE FROM teams WHERE teamid=?", self.teamid)

        newteam = Team.create_team(self.teamid)
        return newteam

    def team_size(self):
        size = 0
        mons = [self.mon1, self.mon2, self.mon3, self.mon4, self.mon5, self.mon6]
        for mon in mons:
            if mon != "None":
                size += 1

        return size

    def add_mon_to_team(self, monobject):
        monposition = Team.team_size(self) + 1
        nextmonposition = f"mon{monposition}"

        with DBConnection() as db:
            query = "UPDATE teams SET {0}='{1}' WHERE teamid='{2}';".format(
                nextmonposition, monobject.name, self.teamid
            )
            db.execute_query(query)

    @staticmethod
    def get_team(teamid):
        # get team by searching for userID
        with DBConnection() as db:
            db.execute_query("SELECT * FROM teams WHERE teamid = ?", teamid)
            if db.cursor == None:
                return Team.create_team(teamid)
            else:
                for row in db.cursor:
                    teamobject = Team(*row)
                    return teamobject

    @staticmethod
    def create_team(teamid):
        # Creates and empty team, usually at the time of user creation
        print("creating team")
        with DBConnection() as db:
            create_team_sql = """INSERT INTO teams(
                teamid, mon1, mon2, mon3,
                mon4, mon5, mon6)
                VALUES(?, ?, ?, ?, ?, ?, ?);"""
            params = (teamid, "None", "None", "None", "None", "None", "None")
            db.execute_query(create_team_sql, *params)
            print("team created")
            db.execute_query("SELECT * FROM teams WHERE teamid = ?", teamid)
            for row in db.cursor:
                teamobject = Team(*row)
                return teamobject


def create_db():
    if os.path.exists("data/pokepy.db"):
        return

    # create users table
    with DBConnection() as db:
        users_table = """CREATE TABLE IF NOT EXISTS users(
            userid TEXT PRIMARY KEY, 
            username TEXT UNIQUE,
            date_created INTEGER);
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
            teamid TEXT PRIMARY KEY,
            mon1 INTEGER,
            mon2 INTEGER,
            mon3 INTEGER,
            mon4 INTEGER,
            mon5 INTEGER,
            mon6 INTEGER);
            """
        db.execute_query(teams_table)
        print("teams table created")
