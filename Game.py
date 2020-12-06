import pickle
import time
import tkinter as tk

from GameSession import GameSession, DifficultyLevel
from LoginScreen import LoginScreen
from Screens import Screens
from UsersManager import UsersManager


class Game:
    def __init__(self, window):
        self.window = window
        self.window.protocol('WM_DELETE_WINDOW', self.__window_deleted)

        self.auth = UsersManager()

        self.frame = None

        self.game_session = None

        self.__login()

    def __login(self):
        self.frame = tk.Frame(self.window)
        LoginScreen(self.frame, self.auth, on_logged=self.__home_screen)

    def __home_screen(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)

        if self.auth.current_user.unfinished_game is not None:
            on_continue = self.__on_continue
        else:
            on_continue = None

        Screens.home_scr(self.frame,
                         on_new_game=self.__on_new_game,
                         on_continue=on_continue,
                         on_leaderboard=self.__on_leaderboard,
                         on_exit=self.__on_exit,
                         )

    def __on_new_game(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)

        self.auth.current_user.unfinished_game = None
        self.auth.save()

        Screens.sel_difficulty_scr(self.frame, self.__start_game)

    def __on_continue(self):
        self.__start_game(is_continue=True)

    def __on_leaderboard(self):
        print('leaderboard')

    def __on_exit(self):
        self.__window_deleted()

    def __start_game(self, difficulty=None, is_continue=False):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        if is_continue:
            self.game_session = self.auth.current_user.unfinished_game
        else:
            self.game_session = GameSession(difficulty=difficulty)
        self.game_session.start(self.frame,
                                on_end=self.__end_of_game,
                                on_stop=self.__stop_of_game
                                )

    def __end_of_game(self, difficulty, is_win, time_elapsed):
        self.frame.destroy()
        self.frame = tk.Frame(self.window)
        if is_win:
            self.save_result(difficulty, time_elapsed)
        self.game_session = None
        Screens.end_of_game_scr(self.frame, is_win, time_elapsed, self.__home_screen)

    def __stop_of_game(self, is_save):
        self.frame.destroy()
        if is_save:
            self.game_session.clear_tk()
            self.auth.current_user.unfinished_game = self.game_session
            self.auth.save()
            self.game_session = None
        self.__home_screen()

    def __window_deleted(self):
        print('Closing')
        self.window.quit()

    def save_result(self, difficulty, time_elapsed):
        print('save result')
