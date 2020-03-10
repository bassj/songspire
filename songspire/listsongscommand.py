class ListSongsCommand:
    def __init__(self, song_store, context):
        self.song_store = song_store
        self.context = context

    def Aliases(self):
        return ["ls", "list"]

    def Handle(self, command_string):
        self.context["result_type"] = "SONG_ENTRIES"
        self.context["results"] = self.song_store.SearchSongRecords()

        for index, song in enumerate(self.context["results"]):
            song_title = song[1]
            song_artist = song[2]
            song_album = song[3]

            print("[%d] { %s | %s | %s }" % (index, song_artist, song_title, song_album))
