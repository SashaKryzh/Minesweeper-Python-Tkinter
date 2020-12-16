import time
import tkinter as tk

from minesweeper.game.GameSession import DifficultyLevel


class Screens:
    @staticmethod
    def home_scr(master, on_new_game, on_continue, on_leaderboard, on_exit):
        def button(text, command):
            return tk.Button(master, text=text, command=command, width=20)

        btn_new = button(text='Нова гра', command=on_new_game)
        btn_new.pack()

        if on_continue is not None:
            btn_con = button(text='Продовижити', command=on_continue)
            btn_con.pack()

        btn_lea = button(text='Таблиця результатів', command=on_leaderboard)
        btn_lea.pack()

        btn_exi = button(text='Вихід', command=on_exit)
        btn_exi.pack()

        master.pack(fill=tk.NONE, expand=True)

    @staticmethod
    def sel_difficulty_scr(master, on_select):
        def button(text, command):
            return tk.Button(master, text=text, command=command, width=20)

        btn_e = button(DifficultyLevel.EASY.value, lambda: on_select(DifficultyLevel.EASY))
        btn_e.pack()

        btn_m = button(DifficultyLevel.MEDIUM.value, lambda: on_select(DifficultyLevel.MEDIUM))
        btn_m.pack()

        btn_h = button(DifficultyLevel.HARD.value, lambda: on_select(DifficultyLevel.HARD))
        btn_h.pack()

        master.pack(fill=tk.NONE, expand=True)

    @staticmethod
    def end_of_game_scr(master, is_win, time_elapsed, on_ok):
        # TODO: translate
        result_string = 'ПЕРЕМОГА' if is_win else 'ПРОГРАШ'
        lbl_result = tk.Label(master, text=result_string)
        lbl_result.pack()

        time_string = time.strftime('%M:%S', time_elapsed)
        lbl_time = tk.Label(master, text=time_string)
        lbl_time.pack()

        btn_ok = tk.Button(master, text='ОК', command=on_ok)
        btn_ok.pack()

        master.pack(fill=tk.NONE, expand=True)
