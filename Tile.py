import tkinter as tk
from enum import IntEnum, Enum

from TileImages import TileImages


class TileStatus(IntEnum):
    CLEAR = 0
    PROBABLY = 1
    SURE = 2


class TileType(Enum):
    NOT_DETERMINED = 0
    CLEAR = 1
    MINE = 2


class Tile:
    def __init__(self, frame, x, y):
        self.images = TileImages().images

        self.type = TileType.NOT_DETERMINED
        self.mines_around = 0
        self.is_opened = False

        self.status = TileStatus.CLEAR
        self.coords = x, y
        self.button = tk.Label(frame, image=self.images['plain'], bd=1)

    def open(self, is_safe=False):
        """
        :param is_safe: if True - mines will not detonate
        """
        self.is_opened = True

        if self.type == TileType.MINE:
            if is_safe:
                image = self.images['mine']
            else:
                # TODO: detonated mine
                image = self.images['mine']
        elif self.mines_around != 0:
            image = self.images['numbers'][self.mines_around - 1]
        else:
            image = self.images['clicked']
        self.button.configure(image=image)

    def change_status(self, status):
        self.status = status
        if self.status == TileStatus.CLEAR:
            image = self.images['plain']
        elif self.status == TileStatus.PROBABLY:
            # TODO: question image !!!
            self.button.configure(text='?', image='')
            return
        else:
            image = self.images['flag']
        self.button.configure(image=image)
