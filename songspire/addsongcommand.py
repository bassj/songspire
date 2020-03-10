import os

class AddSongCommand:
    def __init__(self, song_store, context, cache_path, songs_path):
        self.context = context
        self.song_store = song_store
        self.cache_path = cache_path
        self.songs_path = songs_path

    def Aliases(self):
        return ["add", "a", "c", "catalog"]

    def Handle(self, command_string):

        if not self.context["result_type"] == "MUSIC_FILES":
            print("Invalid result type")
            return

        split_command = command_string.split(" ")

        index = int(split_command[1])

        songpath = self.context["results"][index]

        title = input("Song title: ")
        author = input("Author: ")
        album = input("Album: ")

        self.song_store.InsertSongRecord(songpath, title, author, album)

        os.rename(os.path.join(self.cache_path, songpath), os.path.join(self.songs_path, songpath))
