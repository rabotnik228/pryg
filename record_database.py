import sqlite3
import os



class MapDb:
    pass


class CreateMpDb:
    def __init__(self):
        self.database = sqlite3.connect(r'C:\pryg\users_songs.db')
        self.database.execute("""create table if not exists tablo (id INTEGER PRIMARY KEY, map_name TEXT NOT NULL, 
        song TEXT UNIQUE);""")

    def add_to_database(self, map_name, song):
        self.database.execute("""INSERT OR IGNORE INTO tablo(map_name, song) VALUES(?, ?);""",
                              (map_name, song))
        self.database.commit()

    def all_maps(self):
        con = self.database
        cursor = con.cursor()
        cursor.execute("SELECT * FROM sqlite_master WHERE type='tablo';")
        return cursor.fetchall()

    def open_a_song(self, name):
        current_song = self.database.execute(f"""SELECT song FROM tablo WHERE map_name='{name}';""")
        return current_song.fetchall()
