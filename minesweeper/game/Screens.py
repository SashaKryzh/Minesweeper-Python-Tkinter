import time
import tkinter as tk

from minesweeper.game.GameSession import DifficultyLevel


class Screens:
    @staticmethod
    def home_scr(master, on_new_game, on_continue, on_leaderboard, on_exit):
        btn_new = tk.Button(master, text='New Game', command=on_new_game)
        btn_new.pack()

        if on_continue is not None:
            btn_con = tk.Button(master, text='Continue', command=on_continue)
            btn_con.pack()

        btn_lea = tk.Button(master, text='Leaderboard', command=on_leaderboard)
        btn_lea.pack()

        btn_exi = tk.Button(master, text='Exit', command=on_exit)
        btn_exi.pack()

        master.pack(fill=tk.NONE, expand=True)

    @staticmethod
    def sel_difficulty_scr(master, on_select):
        btn_e = tk.Button(master, text='Новачок', command=lambda: on_select(DifficultyLevel.EASY))
        btn_m = tk.Button(master, text='Любитель', command=lambda: on_select(DifficultyLevel.MEDIUM))
        btn_h = tk.Button(master, text='Професіонал', command=lambda: on_select(DifficultyLevel.HARD))

        btn_e.pack()
        btn_m.pack()
        btn_h.pack()
        master.pack(fill=tk.NONE, expand=True)

    @staticmethod
    def end_of_game_scr(master, is_win, time_elapsed, on_ok):
        # TODO: translate
        result_string = 'WIN' if is_win else 'LOSE'
        lbl_result = tk.Label(master, text=result_string)
        lbl_result.pack()

        time_string = time.strftime('%M:%S', time_elapsed)
        lbl_time = tk.Label(master, text=time_string)
        lbl_time.pack()

        btn_ok = tk.Button(master, text='OK', command=on_ok)
        btn_ok.pack()

        master.pack(fill=tk.NONE, expand=True)
