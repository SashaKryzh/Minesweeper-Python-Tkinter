import time
import tkinter as tk

from GameSession import GameSession, DifficultyLevel
from LoginScreen import LoginScreen
from Screens import Screens


class Game:
    def __init__(self, window):
        self.window = window
        self.window.protocol('WM_DELETE_WINDOW', self.__window_deleted)

        self.frame = None

        self.game_session = None

        self.__login()

    def __login(self):
        self.frame = tk.Frame(self.window)
        LoginScreen(self.frame, on_logged=self.__home_screen)

    def __home_screen(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)
        Screens.home_scr(self.frame,
                         on_new_game=self.__select_difficulty,
                         on_continue=self.__on_continue,
                         on_leaderboard=self.__on_leaderboard,
                         on_exit=self.__on_exit,
                         )

    def __select_difficulty(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)
        Screens.sel_difficulty_scr(self.frame, self.__start_game)

    def __on_continue(self):
        print('continue')

    def __on_leaderboard(self):
        print('leaderboard')

    def __on_exit(self):
        self.__window_deleted()

    def __start_game(self, difficulty):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.game_session = GameSession(self.frame, difficulty=difficulty, on_end=self.__end_of_game)

    def __end_of_game(self, difficulty, is_win, time_elapsed):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)
        if is_win:
            self.save_result(difficulty, time_elapsed)
        self.game_session = None
        Screens.end_of_game_scr(self.frame, is_win, time_elapsed, self.__home_screen)

    def __window_deleted(self):
        print('Closing')
        self.window.quit()

    def save_result(self, difficulty, time_elapsed):
        print('save result')
