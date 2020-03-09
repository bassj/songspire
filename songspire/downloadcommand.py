class DownloadCommand:
    def __init__(self, context, download_queue):
        self.context = context
        self.download_queue = download_queue

    def Aliases(self):
        return ["d", "download"]

    def Handle(self, command_string):
        args = command_string.split(" ")

        #TODO: validate input

        index = int(args[1])

        if not (self.context["result_type"] == "YOUTUBE_SOURCES"):
            print("Invalid result type")
            return

        video = self.context["results"][index]
    
        print("Adding %s to the download queue..." % video["title"])

        self.download_queue.put(video)
