from youtube_search import YoutubeSearch

class SearchCommand:
    def __init__(self, context):
        self.context = context

    def Aliases(self):
        return ["s", "search"]

    def Handle(self, command_string):
        split_command = command_string.split(" ")

        command_args = split_command[1:len(split_command)]

        argstring = " ".join(command_args)

        self.context["result_type"] = "YOUTUBE_SOURCES"
        self.context["results"] = YoutubeSearch(argstring, max_results=10).to_dict()

        for index, video in enumerate(self.context["results"]):
            print("[%d] %s" % (index, video["title"]))
