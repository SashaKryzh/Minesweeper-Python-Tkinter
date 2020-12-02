import tkinter as tk


class GameStatsWidgets:
    def __init__(self, master, num_mines):
        self.master = master

        self.lbl_num_mines = tk.Label(master, text='All mines: {}'.format(num_mines))
        self.lbl_num_mines.pack(side=tk.LEFT)

        self.flags = 0
        self.lbl_flags = tk.Label(master, textvariable=self.flags)
        self.lbl_flags.pack(side=tk.LEFT)

    def update(self, flags):
        self.flags = flags
