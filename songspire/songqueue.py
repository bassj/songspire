class SongQueue:
    def __init__(self):
        self.song_list = []

    def Add(self, item):
        self.song_list.append(item)

    def PlayNext(self, item):
        self.song_list.insert(0, item)

    def Get(self):
        return self.song_list.pop(0)

    def Empty(self):
        return len(self.song_list) == 0
