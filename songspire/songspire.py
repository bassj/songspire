from songstore import SongStore
from commandprocessor import CommandProcessor
from songqueue import SongQueue
from songplayer import SongPlayer
from quitcommand import QuitCommand
from searchcommand import SearchCommand
from downloadcommand import DownloadCommand
from listcachecommand import ListCacheCommand
from addsongcommand import AddSongCommand
from listsongscommand import ListSongsCommand
from queuecommand import QueueCommand

from downloadworker import DownloadWorker

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
download_worker = None
song_player = None
song_queue = None

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

def InitDownloadWorker():
    global download_worker

    download_worker = DownloadWorker(download_queue, cache_path)

    download_worker.Start()

def CleanupDownloadWorker():
    download_worker.should_close = True
    download_worker.Join()

def InitSongQueue():
    global song_queue

    song_queue = SongQueue()

def InitSongPlayer():
    global song_player
    song_player = SongPlayer()

def DestroySongPlayer():
    song_player.Destroy()

def CreateCommands():
    command_processor.AddCommand(QuitCommand(command_processor))
    command_processor.AddCommand(SearchCommand(context))
    command_processor.AddCommand(DownloadCommand(context, download_queue))
    command_processor.AddCommand(ListCacheCommand(context, cache_path))
    command_processor.AddCommand(ListSongsCommand(song_store, context))
    command_processor.AddCommand(AddSongCommand(song_store, context, cache_path, songs_path))
    command_processor.AddCommand(QueueCommand(context, song_queue, songs_path))

def Init():
    InitSongQueue()
    InitFolders()    
    InitSongStore()
    InitCmdProcessor()
    InitDownloadWorker()
    InitSongPlayer()

    CreateCommands()

    while not command_processor.ShouldQuit():
        if not song_queue.Empty():
           song = song_queue.Get()
           print("Queuing %s" % song)
           song_player.PlaySong(song)

        command_string = input(">")
         
        command_processor.ProcessCommand(command_string);

    DestroySongPlayer()
    CleanupDownloadWorker()
    DestroySongStore()
