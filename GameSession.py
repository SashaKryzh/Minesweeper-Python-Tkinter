from Tile import Tile, TileType, TileStatus
import tkinter as tk
import random
from functools import partial
from enum import Enum
from GameStatsWidget import GameStatsWidgets


class DifficultyLevel(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class GameSession:
    def __init__(self, window, difficulty):
        self.window = window
        if difficulty is DifficultyLevel.EASY:
            self.num_rows = 9
            self.num_cols = 9
            self.num_mines = 10
        elif difficulty is DifficultyLevel.MEDIUM:
            self.num_rows = 16
            self.num_cols = 16
            self.num_mines = 40
        else:
            self.num_rows = 16
            self.num_cols = 30
            self.num_mines = 90

        # For testing purposes
        if True:
            self.num_rows = 4
            self.num_cols = 4
            self.num_mines = 2

        self.frm_board = tk.Frame(window)
        self.frm_board.pack()

        self.frm_stats = tk.Frame(window)
        self.stats = GameStatsWidgets(self.frm_stats, self.num_mines)
        self.frm_stats.pack()

        self.board = None
        self.is_mines_inited = False

        self.flags_left = self.num_mines
        self.flags_correct = 0

        self.__setup()

    def __setup(self):
        self.board = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                tile = Tile(self.frm_board, x, y)
                tile.button.grid(row=y, column=x, padx=0, pady=0, sticky="nsew")

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
        tile = self.board[y][x]
        if tile.status == TileStatus.CLEAR:
            tile.change_status(TileStatus.PROBABLY)

        elif tile.status == TileStatus.PROBABLY:
            if self.flags_left != 0:
                tile.change_status(TileStatus.SURE)
                self.flags_left -= 1
                self.flags_correct += tile.type == TileType.MINE
                if self.flags_correct == self.num_mines:
                    self.__end_on_success()
                self.stats.update(self.flags_left)
            else:
                tile.change_status(TileStatus.CLEAR)

        else:
            tile.change_status(TileStatus.CLEAR)
            self.flags_left += 1
            self.flags_correct -= tile.type == TileType.MINE
            self.stats.update(self.flags_left)

    def __open_tile(self, x, y):
        tile = self.board[y][x]

        # To prevent open when auto opening free of mines field
        if tile.status == TileStatus.SURE:
            return

        self.__unbind_tile(tile)
        tile.open()

        if tile.type == TileType.MINE:
            self.__end_on_mine()
            return
        elif tile.mines_around == 0:
            closed_tiles_around = self.__get_closed_tiles_around(x, y)
            for tile in closed_tiles_around:
                self.__open_tile(tile.coords[0], tile.coords[1])
        else:
            pass

    @staticmethod
    def __unbind_tile(tile):
        tile.button.unbind('<Button-1>')
        tile.button.unbind('<Button-2>')
        tile.button.unbind('<Button-3>')

    def __end_on_mine(self):
        print('YOU LOSE')
        for row in self.board:
            for tile in row:
                self.__unbind_tile(tile)
                if tile.type is TileType.MINE and tile.status is not TileStatus.SURE:
                    tile.open()

    def __end_on_success(self):
        print('YOU WIN')
        for row in self.board:
            for tile in row:
                self.__unbind_tile(tile)
                if tile.status is not TileStatus.SURE:
                    tile.open()

    def __init_mines(self, n_x, n_y):
        self.is_mines_inited = True
        mines_left = self.num_mines

        while mines_left != 0:
            x = random.randint(0, self.num_cols - 1)
            y = random.randint(0, self.num_rows - 1)
            if x == n_x and y == n_y:
                pass
            elif self.board[y][x].type == TileType.NOT_DETERMINED:
                self.board[y][x].type = TileType.MINE
                mines_left -= 1

        for y in range(self.num_rows):
            for x in range(self.num_cols):
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
            if 0 <= cy < self.num_rows:
                if 0 <= cx < self.num_cols:
                    tiles.append(self.board[cy][cx])
        return tiles
