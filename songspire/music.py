from youtube_search import YoutubeSearch
import json
import subprocess
import sqlite3
import os
import pygame
import mutagen.mp3
from os import listdir

home_path = os.path.join(os.path.expanduser("~"), ".songspire/")
database_path = os.path.join(home_path, "songstore.db")
cache_path = os.path.join(home_path, "cache/")
songs_path = os.path.join(home_path, "songs/");

song_store = None;
songs = None;

is_running = True
result_type = None
results = []

def DestroyDatabase():
    song_store.commit()
    song_store.close()

def CreateDatabase():
    songs.execute('''CREATE TABLE songs
                                    (songid INTEGER PRIMARY KEY, name TEXT, author TEXT, album TEXT, filepath TEXT)''')
    song_store.commit()

def InitDatabase():
    global song_store
    global songs

    database_exists = os.path.isfile(database_path)
    
    song_store = sqlite3.connect(database_path)
    
    songs = song_store.cursor()

    if not database_exists:
        CreateDatabase()

def InsertSongRecord(filename, title, author, album):
    query = ('''INSERT INTO songs(songid, name, author, album, filepath) SELECT NULL, '%s', '%s', '%s', '%s' WHERE NOT EXISTS(SELECT 1 FROM songs WHERE filepath='%s')''' % (title, author, album, filename, filename))

    songs.execute(query)

    song_store.commit()

def SearchSongRecords(search_terms = None):
    songs.execute("SELECT * FROM songs")

    rows = songs.fetchall()

    return rows

def PlayMusicFile(music_file): 
    mp3 = mutagen.mp3.MP3(song_path) 

    pygame.mixer.quit()
    pygame.mixer.init(mp3.info.sample_rate)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()


def QuitCommand():
    global is_running

    is_running = False
    DestroyDatabase()

def SearchCommand(args):
    global results
    global result_type
    
    argstring = " ".join(args) 

    result_type = "YOUTUBE_SOURCES"
    results = YoutubeSearch(argstring, max_results=10).to_dict();

    for index, video in enumerate(results):
        print("[%d] %s" % (index, video["title"]))

    print(home_path)
    print(cache_path)
def DownloadCommand(asongs_path, songpathrgs):
    
    index = int(args[0])

    video = results[index]

    print("Downloading \"%s\"" % video["title"]) 

    video_url = "https://www.youtube.com%s" % video['link'] 

    ytdl_out = subprocess.Popen(['youtube-dl', '-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '0', video_url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cache_path) 

    print("Download finished")

def AddCommand(args):
   
    index = int(args[0])

    print(results[index])

    songpath = results[index]

    title = input("Song title: ")
    author = input("Author: ")
    album = input("Album: ")

    InsertSongRecord(songpath, title, author, album)

    os.rename(os.path.join(cache_path, songpath), os.path.join(songs_path, songpath))

def ListCacheCommand(args):
    global results
    global result_type


    results = listdir(cache_path)
    result_type = "MUSIC_FILES"

    for index, song in enumerate(results):
        print('[%d] %s' % (index, song))

def ListSongsCommand(args):
    global results
    global result_type

    results = SearchSongRecords();
    result_type = "SONG_ENTRIES"

    for index, song in enumerate(results):  
        song_title = song[1]
        song_artist = song[2]
        song_album = song[3]
        
        print("[%d] Song: %s Album: %s by %s" % (index, song_title, song_album, song_artist))

def PlaySongCommand(args):    
    if not (result_type == "SONG_ENTRIES" or result_type == "MUSIC_FILES"):
        print("Invalid result type")
        return
    
    
    index = int(args[0])
    
    song = results[index]

    if result_type == "SONG_ENTRIES":
        song_file = song[4]
        print("Playing %s" % song_file)
        
        song_path = os.path.join(songs_path, song_file)

        PlayMusicFile(song_path)    

def ProcessCommand(command, args):    
    if (command == "q"):
        QuitCommand()
    elif command == "s": 
        SearchCommand(args)
    elif command == "d":
        DownloadCommand(args)
    elif command == "a":
        AddCommand(args)
    elif command == "lc":
        ListCacheCommand(args)
    elif command == "ls":
        ListSongsCommand(args)
    elif command == "p":
        PlaySongCommand(args)
    else:
        print("Unknown command \"%s\"" % command)


def Init():   

    print(home_path)
    print(cache_path)
    print(songs_path)
    print(database_path)

    if not os.path.exists(os.path.dirname(home_path)):
        os.makedirs(os.path.dirname(home_path))
    if not os.path.exists(os.path.dirname(cache_path)):
        os.makedirs(os.path.dirname(cache_path));
    if not os.path.exists(os.path.dirname(songs_path)):
        os.makedirs(os.path.dirname(songs_path))

    InitDatabase()

    while is_running:
        raw_command = input(">")

        split_command = raw_command.split(" ")

        command = split_command[0]

        command_args = split_command[1:len(split_command)]

        ProcessCommand(command, command_args)
     

if __name__ == "__main__":
    Init()
