import tkinter as tk


class GameStatsWidgets:
    def __init__(self, master, num_mines):
        self.master = master

        self.lbl_num_mines = tk.Label(master, text='Mines: {};'.format(num_mines))
        self.lbl_num_mines.pack(side=tk.LEFT)

        self.lbl_flags = tk.Label(master)
        self.update(num_mines)
        self.lbl_flags.pack(side=tk.RIGHT)

    def update(self, flags):
        self.lbl_flags.configure(text='Flags left: {};'.format(flags))
