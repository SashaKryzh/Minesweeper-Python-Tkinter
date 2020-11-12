import tkinter as tk


class Tile:
    def __init__(self, frame, x, y):
        self.closed_statuses = ['CLOSED', 'PROBABLY', 'SURE']

        self.is_opened = False
        self.is_mine = False
        self.mines_around = 0
        self.status = self.closed_statuses[0]
        self.coords = x, y
        self.button = tk.Button(frame)
