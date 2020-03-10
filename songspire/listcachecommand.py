import os

class ListCacheCommand:
    def __init__(self, context, cache_path):
        self.cache_path = cache_path
        self.context = context

    def Aliases(self):
        return ["lc", "cache"]

    def Handle(self, command_string):
        
        self.context["result_type"] = "MUSIC_FILES"
        self.context["results"] = os.listdir(self.cache_path)

        for index, song in enumerate(self.context["results"]):
            print("[%d] %s" % (index, song))
