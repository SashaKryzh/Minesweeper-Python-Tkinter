from SingletonMeta import SingletonMeta
import tkinter as tk
from PIL import Image, ImageTk


class TileImages(metaclass=SingletonMeta):
    def __init__(self):
        self.image_size = 20

        self.images = {
            "plain": self.__open_image("images/tile_plain.gif"),
            "clicked": self.__open_image("images/tile_clicked.gif"),
            "mine": self.__open_image("images/tile_mine.gif"),
            "detonated": self.__open_image("images/tile_mine_detonated.gif"),
            "question": self.__open_image("images/tile_question.gif"),
            "flag": self.__open_image("images/tile_flag.gif"),
            "wrong": self.__open_image("images/tile_wrong.gif"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(self.__open_image("images/tile_" + str(i) + ".gif"))

    def __open_image(self, path):
        return ImageTk.PhotoImage(Image.open(path).resize((self.image_size, self.image_size)))
