class CommandProcessor:
    def __init__(self):
        self.should_quit = False
        self.commands = []

    def ShouldQuit(self):
        return self.should_quit

    def ProcessCommand(self, command_string):
        split_string = command_string.split(" ")

        command = split_string[0]

        for command_handler in self.commands:
            for alias in command_handler.Aliases():
                if command == alias:
                    command_handler.Handle(command_string)
                    return

        print("Unknown Command: %s" % command)

    def AddCommand(self, command):
        self.commands.append(command)

