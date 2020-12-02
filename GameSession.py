from tile import Tile, TileType, TileStatus
import tkinter as tk
import random
from functools import partial


class GameSession:
    def __init__(self, window):
        self.board = None
        self.window = window
        self.frm_board = tk.Frame(window)
        self.frm_board.pack()

        self.is_mines_inited = False

        self.__setup()

    def __setup(self):
        self.board = [[0 for j in range(9)] for i in range(9)]
        for y in range(9):
            for x in range(9):
                tile = Tile(self.frm_board, x, y)
                tile.button.grid(row=y, column=x)

                act_on_left_tap = partial(self.__on_lft_btn_tap, x, y)
                act_on_right_tap = partial(self.__on_rgt_btn_tap, x, y)
                tile.button.bind('<Button-1>', act_on_left_tap)
                tile.button.bind('<Button-2>', act_on_right_tap)
                tile.button.bind('<Button-3>', act_on_right_tap)

                self.board[y][x] = tile

    def __on_lft_btn_tap(self, x, y, event=None):
        if self.board[y][x].status != TileStatus.CLEAR:
            return
        if self.is_mines_inited is False:
            self.__init_mines(x, y)
        self.__open_tile(x, y)

    def __on_rgt_btn_tap(self, x, y, event=None):
        self.board[y][x].change_status()

    def __open_tile(self, x, y):
        # To prevent open when auto opening free of mines field
        if self.board[y][x].status == TileStatus.SURE:
            return

        tile = self.board[y][x]
        tile.button.unbind('<Button-1>')
        tile.button.unbind('<Button-2>')
        tile.button.unbind('<Button-3>')
        tile.open()

        if tile.type == TileType.MINE:
            print('end')
        elif tile.mines_around == 0:
            closed_tiles_around = self.__get_closed_tiles_around(x, y)
            for tile in closed_tiles_around:
                self.__open_tile(tile.coords[0], tile.coords[1])
        else:
            pass

    def __init_mines(self, n_x, n_y):
        self.is_mines_inited = True
        mines_left = 9

        while mines_left != 0:
            x = random.randint(0, 9 - 1)
            y = random.randint(0, 9 - 1)
            if x == n_x and y == n_y:
                pass
            elif self.board[y][x].type == TileType.NOT_DETERMINED:
                self.board[y][x].type = TileType.MINE
                mines_left -= 1

        for y in range(9):
            for x in range(9):
                tile = self.board[y][x]
                if tile.type != TileType.MINE:
                    tile.type = TileType.CLEAR
                    tile.mines_around = self.__count_mines_around(x, y)

    def __get_closed_tiles_around(self, x, y):
        around = self.__get_tiles_around(x, y, diagonals=False)
        closed = list(filter(lambda t: t.is_opened is False, around))
        return closed

    def __count_mines_around(self, x, y):
        around = self.__get_tiles_around(x, y)
        mines = list(filter(lambda t: t.type == TileType.MINE, around))
        return len(mines)

    def __get_tiles_around(self, x, y, diagonals=True):
        if diagonals:
            directions = [(-1, -1), (0, -1), (1, -1),
                          (-1, 0), (1, 0),
                          (-1, 1), (0, 1), (1, 1)]
        else:
            directions = [(0, -1),
                          (-1, 0), (1, 0),
                          (0, 1)]

        tiles = []
        for d in directions:
            cx, cy = x + d[0], y + d[1]
            if 0 <= cy < 9:
                if 0 <= cx < 9:
                    tiles.append(self.board[cy][cx])
        return tiles
