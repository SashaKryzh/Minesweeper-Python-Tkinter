from tile import Tile
import tkinter as tk


class GameSession:
    def __init__(self, window):
        self.board = None
        self.window = window
        self.board_f = tk.Frame(window)
        self.board_f.pack()

        self.setup()

    def setup(self):
        self.board = [[0 for j in range(9)] for i in range(9)]
        for y in range(9):
            for x in range(9):
                tile = Tile(self.board_f, x, y)
                tile.button.grid(row=y, column=x)
                self.board = tile


