import time
import tkinter as tk

from GameSession import GameSession, DifficultyLevel


class Game:
    def __init__(self, window):
        self.window = window
        self.window.protocol('WM_DELETE_WINDOW', self.__window_deleted)

        # Select difficulty
        self.frm_select_difficulty = None

        # Game session
        self.game_session = None
        self.frm_game_session = None

        # End of game

        self.__select_difficulty()

    def __select_difficulty(self):
        f = tk.Frame(self.window)
        self.frm_select_difficulty = f

        btn_e = tk.Button(f, text='Новачок', command=lambda: self.__start_game(DifficultyLevel.EASY))
        btn_m = tk.Button(f, text='Любитель', command=lambda: self.__start_game(DifficultyLevel.MEDIUM))
        btn_h = tk.Button(f, text='Професіонал', command=lambda: self.__start_game(DifficultyLevel.HARD))

        btn_e.pack()
        btn_m.pack()
        btn_h.pack()
        f.pack(fill=tk.NONE, expand=True)

    def __start_game(self, difficulty):
        self.frm_select_difficulty.pack_forget()
        self.frm_select_difficulty.destroy()

        self.frm_game_session = tk.Frame(self.window)
        self.frm_game_session.pack()
        self.game_session = GameSession(self.frm_game_session, difficulty=difficulty, on_end=self.__end_of_game)

    def __end_of_game(self, stats):
        """
        :param stats: [is_win (TRUE / FALSE), seconds elapsed (int)]
        """
        self.frm_game_session.pack_forget()
        self.frm_game_session.destroy()



        print('WIN' if stats[0] else 'LOSE')
        print(time.gmtime(stats[1]))



    def __window_deleted(self):
        print('Closing')
        self.window.quit()
