from songstore import SongStore
from commandprocessor import CommandProcessor
from quitcommand import QuitCommand
from searchcommand import SearchCommand
from downloadcommand import DownloadCommand

from queue import Queue

import os


home_path = os.path.join(os.path.expanduser("~"), ".songspire/")
database_path = os.path.join(home_path, "songstore.db")
cache_path = os.path.join(home_path, "cache/")
songs_path = os.path.join(home_path, "songs/");

song_store = None
command_processor = None
context = {}
download_queue = Queue() 

def InitSongStore():
    global song_store

    song_store = SongStore(database_path)

def InitCmdProcessor():
    global command_processor

    command_processor = CommandProcessor()

def DestroySongStore():
    song_store.Close()

def InitFolders():
    if not os.path.exists(os.path.dirname(home_path)):
        os.makedirs(os.path.dirname(home_path))
    if not os.path.exists(os.path.dirname(cache_path)):
        os.makedirs(os.path.dirname(cache_path));
    if not os.path.exists(os.path.dirname(songs_path)):
        os.makedirs(os.path.dirname(songs_path))

def CreateCommands():
    command_processor.AddCommand(QuitCommand(command_processor))
    command_processor.AddCommand(SearchCommand(context))
    command_processor.AddCommand(DownloadCommand(context, download_queue))
    
def Init():
    InitFolders()    
    InitSongStore()
    InitCmdProcessor()

    CreateCommands()

    while not command_processor.ShouldQuit():
        command_string = input(">")
         
        command_processor.ProcessCommand(command_string);


    DestroySongStore()
