import tkinter as tk

from game_session import GameSession


class Game:
    def __init__(self, window):
        self.game_session = None

        self.window = window
        self.window.protocol('WM_DELETE_WINDOW', self.__window_deleted)
        self.__hello_screen()

    def __hello_screen(self):
        start_b = tk.Button(self.window, text='Start', command=self.__start_game)
        start_b.pack()

    def __start_game(self):
        self.game_session = GameSession(self.window)

    def __window_deleted(self):
        print('Closing')
        self.window.quit()
