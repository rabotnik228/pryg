import sqlite3
import os


class CreateMpDb:
    def __init__(self):
        self.database = sqlite3.connect(r'C:\pryg\users_songs.db')
        self.database.execute("""create table if not exists tablo (id INTEGER PRIMARY KEY, map_name TEXT NOT NULL, 
        song TEXT UNIQUE);""")
        self.list_of_names = [self.all_maps()]

    def add_to_database(self, map_name, song):
        self.database.execute("""INSERT OR IGNORE INTO tablo(map_name, song) VALUES(?, ?);""",
                              (map_name, song))
        self.database.commit()

    def all_maps(self):
        con = self.database
        cursor = con.cursor()
        cursor.execute("SELECT map_name FROM tablo;")
        return cursor.fetchall()

    def open_a_song(self, name):
        current_song = self.database.execute(f"""SELECT song FROM tablo WHERE map_name="{name}";""")
        return current_song.fetchall()

    def get_names_of_song(self):
        return self.list_of_names

    def get_song_name(self, audio):
        current_song = self.database.execute(f"""SELECT map_name FROM tablo WHERE song="{audio}";""")
        return current_song.fetchall()


class AchivementDb:
    def __init__(self):
        self.database = sqlite3.connect(r'C:\pryg\users_achivements.db')
        self.database.execute("""create table if not exists tablo (id INTEGER PRIMARY KEY, achiv_name TEXT UNIQUE, 
                yes_or_not TEXT NOT NULL);""")
        self.list_of_achiv = ("Catch -1 fruit", "Catch 100000", "Catch 2000000", "Catch 100000 in inverted",
                              "Catch 2000000 in inverted", "Catch 100000 in flashlight",
                              "Catch 2000000 in flashlight")

    def set_complete(self, idi):
        pass

    def tutorial_check(self):
        pass
