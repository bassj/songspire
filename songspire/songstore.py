import sqlite3
import os

class SongStore:
    def __init__(self, database_path):
        self.database_path = database_path


        database_exists = os.path.isfile(database_path)

        self.database = sqlite3.connect(database_path)

        self.cursor = self.database.cursor()

        if not database_exists:
            self.cursor.execute('''CREATE TABLE songs
                                    (songid INTEGER PRIMARY KEY, name TEXT, author TEXT, album TEXT, filepath TEXT)''')
            self.database.commit()
    
    def InsertSongRecord(self, filename, title, author, album):
        query = ('''INSERT INTO songs(songid, name, author, album, filepath) SELECT NULL, '%s', '%s', '%s', '%s' WHERE NOT EXISTS(SELECT 1 FROM songs WHERE filepath='%s')''' % (title, author, album, filename, filename))
    
        self.cursor.execute(query)

        self.database.commit()

    def SearchSongRecords(search_terms = None):
        self.cursor.execute("SELECT * FROM songs")
        
        rows = self.cursor.fetchall()

        return rows

    def Close(self):
        self.database.commit();
        self.database.close()
