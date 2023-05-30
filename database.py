import sqlite3
from sqlite3 import Error
import os
import datetime
import uuid

import bcrypt

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
                return "db_query_execution_error"

    def commit(self):
        try:
            self.conn.commit()
        except Error as e:
            print("db commit error")
            print(e)

    def rollback(self):
        self.conn.rollback()
        print("db rollback")

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
    def __init__(self, userid, username, password, date_created):
        self.userid = userid
        self.username = username
        self.password = password
        self.date_created = date_created

    def __str__(self):
        return self.username.capitalize()

    @staticmethod
    def get_user(username, password):
        with DBConnection() as db:
            query = "SELECT * FROM users WHERE username = ?;"
            db.execute_query(query, username)
            userobject = None

            for row in db.cursor:
                userobject = User(*row)
            if not userobject:
                return None

            elif (
                bcrypt.hashpw(str.encode(password), userobject.password)
                != userobject.password
            ):
                return "401_unauthorized"

            else:
                return userobject

    # This method is used to pull users who are already authenticated
    @staticmethod
    def get_user_session(username):
        with DBConnection() as db:
            query = "SELECT * FROM users WHERE username = ?;"
            db.execute_query(query, username)
            userobject = None

            for row in db.cursor:
                userobject = User(*row)
            if not userobject:
                return None
            else:
                return userobject

    @staticmethod
    def get_all_users():
        users = []
        with DBConnection() as db:
            query = "SELECT * FROM users;"
            db.execute_query(query)

            for row in db.cursor:
                users.append(row[1])
            if not users:
                return None
            return users

    @staticmethod
    def create_user(username, password):
        with DBConnection() as db:
            userid = uuid.uuid4().hex
            now = datetime.datetime.now()
            date_created = f"{now.date()} {now.time()}"

            pwByte = password.encode()
            pwHash = bcrypt.hashpw(pwByte, bcrypt.gensalt())

            create_user_sql = """INSERT INTO users(
                userid, username, password, date_created)
                VALUES(?, ?, ?, ?);"""
            userdata = [userid, username, pwHash, date_created]
            if (
                db.execute_query(create_user_sql, *userdata)
                == "db_query_execution_error"
            ):
                print("ERROR creating user")
                return None
            else:
                userobject = User(userid, username.lower(), password, date_created)

        return userobject

    def delete_account(self):
        with DBConnection() as db:
            queryone = """DELETE from users WHERE userid = ?"""
            querytwo = """DELETE FROM teams WHERE teamid = ?"""
            if (
                db.execute_query(queryone, self.userid)
                or db.execute_query(querytwo, self.userid) == "db_query_execution_error"
            ):
                print("\nrolling back...\n")
                db.rollback()
                return "Error deleting account"
            else:
                return


class Pokemon:
    def __init__(self, id, name, height, weight, montype, sprite):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.montype = montype
        self.sprite = sprite

    def __str__(self):
        return f"\nID: {self.id}\nName: {self.name.capitalize()}\nHeight: {self.height}\nWeight: {self.weight}\nType: {self.montype.title()}\nSprite: {self.sprite}\n"

    # adds a single mon to database mons table
    def add_mon_todb(self):
        if dbmon := self.get_mon(self.name):
            return dbmon
        with DBConnection() as db:
            insert_with_params = """INSERT INTO mons(
                    monid, name, height, weight, type, sprite)
                    VALUES(?, ?, ?, ?, ?, ?);"""
            mondata = (
                self.id,
                self.name.lower(),
                self.height,
                self.weight,
                self.montype,
                self.sprite,
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
        return f"\n1: {self.mon1}\n2: {self.mon2}\n3: {self.mon3}\n4: {self.mon4}\n5: {self.mon5}\n6: {self.mon6}"

    def delete_team(self):
        teamsize = 0
        for attr, _ in self.__dict__.items():
            if attr == "teamid":
                continue
            elif attr != "None":
                teamsize += 1
        if teamsize == 0:
            return "empty_team"

        teamid = self.teamid
        rows = ["mon1", "mon2", "mon3", "mon4", "mon5", "mon6"]
        for mon in rows:
            with DBConnection() as db:
                query = "UPDATE teams SET {0}='None' WHERE teamid='{1}';".format(
                    mon, teamid
                )
                db.execute_query(query)
        # Updating current object with new empty team
        for attr, _ in self.__dict__.items():
            if attr == "teamid":
                continue
            setattr(self, attr, "None")

        return

    def team_size(self):
        size = 0
        mons = [self.mon1, self.mon2, self.mon3, self.mon4, self.mon5, self.mon6]
        for mon in mons:
            if mon != "None":
                size += 1

        return size

    def add_mon_to_team(self, monobject):
        # gets current size of team, calculates mon position in team roster
        monposition = Team.team_size(self) + 1
        # wraps around if team is already full
        if monposition == 7:
            return "428_team_full"

        nextmonposition = f"mon{monposition}"

        with DBConnection() as db:
            query = "UPDATE teams SET {0}='{1}' WHERE teamid='{2}';".format(
                nextmonposition, monobject.name, self.teamid
            )
            db.execute_query(query)
            # This updates the team object to reflect new mon
            for attr, value in self.__dict__.items():
                if value == "None":
                    setattr(self, attr, monobject.name)
                    break

            return self

    def update_team(self, montoupdate_pos, newstring):
        # makes a string to represent column name in db
        column_pos = f"mon{montoupdate_pos}"
        with DBConnection() as db:
            query = "UPDATE teams SET {0}='{1}' WHERE teamid='{2}';".format(
                column_pos, newstring, self.teamid
            )
            db.execute_query(query)

    @staticmethod
    def get_team(teamid):
        # get team by searching for userID
        with DBConnection() as db:
            db.execute_query("SELECT * FROM teams WHERE teamid = ?;", teamid)
            if db.cursor == None:
                return Team.create_team(teamid)
            else:
                for row in db.cursor:
                    teamobject = Team(*row)
                    return teamobject

    @staticmethod
    def create_team(teamid):
        # Creates and empty team, usually at the time of user creation
        with DBConnection() as db:
            create_team_sql = """INSERT INTO teams(
                teamid, mon1, mon2, mon3,
                mon4, mon5, mon6)
                VALUES(?, ?, ?, ?, ?, ?, ?);"""
            params = (teamid, "None", "None", "None", "None", "None", "None")
            db.execute_query(create_team_sql, *params)
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
            password TEXT,
            date_created INTEGER);
            """
        db.execute_query(users_table)
        print("users table created")

        # create mons table
        # caches data about monsters that have previously been called upon:
        mons_table = """CREATE TABLE IF NOT EXISTS mons(
            monid INTEGER PRIMARY KEY NOT NULL,
            name TEXT,
            height INTEGER,
            weight INTEGER,
            type TEXT,
            sprite TEXT);
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
