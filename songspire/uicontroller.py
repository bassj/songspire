import curses
from curses.textpad import Textbox, rectangle

class UiController:
    def __init__(self, context, command_processor):
        self.context = context
        self.command_processor = command_processor

    def __prompt_input(self):
        self.screen.clear()
        self.screen.nodelay(False)
        self.screen.addstr(">")
        curses.echo()
        
        command_input = self.screen.getstr(0, 1)

        command_input.strip()

        self.screen.nodelay(True)
        return command_input

    def Create(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)

        self.screen.nodelay(True)

        self.screen.clear()





    def Destroy(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def Update(self):
        text = self.__prompt_input().decode("utf-8")
        
        #self.screen.addstr("'%s'" % text)

        if (text == "quit"):
            self.command_processor.should_quit = True
        

        self.screen.refresh()
