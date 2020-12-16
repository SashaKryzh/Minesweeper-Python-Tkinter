import tkinter as tk


class GameStatsWidgets:
    def __init__(self, master, num_mines, flags_left):
        self.master = master

        self.lbl_num_mines = tk.Label(master, text='Мін: {}'.format(num_mines))
        self.lbl_num_mines.pack(side=tk.LEFT)

        self.lbl_flags = tk.Label(master)
        self.update(flags_left)
        self.lbl_flags.pack(side=tk.RIGHT)

    def update(self, flags):
        self.lbl_flags.configure(text='Залишилося флагів: {}'.format(flags))
