import os

class QueueCommand:
    def __init__(self, context, song_queue, songs_path):
        self.context = context
        self.song_queue = song_queue
        self.songs_path = songs_path

    def Aliases(self):
        return ["qu", "p"]

    def Handle(self, command_string):
        
        if (not self.context["result_type"] == "SONG_ENTRIES"):
            print("Invalid results.")
            return

        split_command = command_string.split(" ")

        index = int(split_command[1])
        
        #print(self.context["results"][index]);

        results = self.context["results"]

        song_path = results[index][4]

        song_file = os.path.join(self.songs_path, song_path)

        self.song_queue.Add(song_file)

        print("Added %s by %s to queue." % (results[index][1], results[index][2]))

