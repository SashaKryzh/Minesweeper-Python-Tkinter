import time
import tkinter as tk

from minesweeper.game.GameSession import DifficultyLevel
import settings
from minesweeper.languages.language import text_messages


class Screens:
    @staticmethod
    def home_scr(master, on_new_game, on_continue, on_leaderboard, on_exit):
        def button(text, command):
            return tk.Button(master, text=text, command=command, width=20)

        btn_new = button(text=text_messages[settings.language.lower()].home_scr.new_game, command=on_new_game)
        btn_new.pack()

        if on_continue is not None:
            btn_con = button(text=text_messages[settings.language.lower()].home_scr.continue_btn, command=on_continue)
            btn_con.pack()

        btn_lea = button(text=text_messages[settings.language.lower()].home_scr.table_of_result, command=on_leaderboard)
        btn_lea.pack()

        btn_exi = button(text=text_messages[settings.language.lower()].home_scr.entrance, command=on_exit)
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
