import tkinter as tk
from enum import IntEnum, Enum

from minesweeper.helpers.TileImages import TileImages


class TileStatus(IntEnum):
    CLEAR = 0
    PROBABLY = 1
    SURE = 2


class TileType(Enum):
    NOT_DETERMINED = 0
    CLEAR = 1
    MINE = 2


class Tile:
    def __init__(self, x, y):
        self.coords = x, y

        self.status = TileStatus.CLEAR
        self.type = TileType.NOT_DETERMINED
        self.mines_around = 0
        self.is_opened = False
        self.image_str = 'plain'

        self.images = None
        self.button = None

    def init_button(self, frame):
        self.images = TileImages()
        self.button = tk.Label(frame, image=self.images.get(self.image_str, self.mines_around - 1), bd=1)

    def clear_tk(self):
        self.images = None
        self.button.destroy()
        self.button = None

    def open(self, is_safe=False):
        """
        :param is_safe: if True - mines will not detonate
        """
        self.is_opened = True

        if self.type == TileType.MINE:
            if is_safe:
                self.image_str = 'mine'
            else:
                self.image_str = 'detonated'
        elif self.mines_around != 0:
            self.image_str = 'numbers'
        else:
            self.image_str = 'clicked'
        self.button.configure(image=self.images.get(self.image_str, self.mines_around - 1))

    def change_status(self, status):
        self.status = status
        if self.status == TileStatus.CLEAR:
            self.image_str = 'plain'
        elif self.status == TileStatus.PROBABLY:
            self.image_str = 'question'
        else:
            self.image_str = 'flag'
        self.button.configure(image=self.images.get(self.image_str))

    def wrong_flag(self):
        self.image_str = 'wrong'
        self.button.configure(image=self.images.get(self.image_str))
