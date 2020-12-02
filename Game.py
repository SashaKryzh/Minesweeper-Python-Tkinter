import tkinter as tk

from GameSession import GameSession, DifficultyLevel


class Game:
    def __init__(self, window):
        self.window = window
        self.window.protocol('WM_DELETE_WINDOW', self.__window_deleted)

        self.game_session = None
        self.frm_select_difficulty = None

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
        self.game_session = GameSession(self.window, difficulty=difficulty)

    def __window_deleted(self):
        print('Closing')
        self.window.quit()
