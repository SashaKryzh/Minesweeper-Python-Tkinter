from utils.SingletonMeta import SingletonMeta
import tkinter as tk


class TileImages(metaclass=SingletonMeta):
    def __init__(self):
        self.images = {
            "plain": tk.PhotoImage(file="../images/tile_plain.gif"),
            "clicked": tk.PhotoImage(file="../images/tile_clicked.gif"),
            "mine": tk.PhotoImage(file="../images/tile_mine.gif"),
            "flag": tk.PhotoImage(file="../images/tile_flag.gif"),
            "wrong": tk.PhotoImage(file="../images/tile_wrong.gif"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(tk.PhotoImage(file="images/tile_" + str(i) + ".gif"))
