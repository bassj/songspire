class QuitCommand:
    def __init__(self, command_processor):
        self.command_processor = command_processor

    def Aliases(self):
        return ["q", "quit", "exit"]

    def Handle(self, command_string):
        self.command_processor.should_quit = True
