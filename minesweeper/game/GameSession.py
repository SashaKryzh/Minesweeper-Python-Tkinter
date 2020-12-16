from minesweeper.game.Tile import Tile, TileType, TileStatus
import tkinter as tk
import random
from functools import partial
from enum import Enum
from minesweeper.game.GameStatsWidget import GameStatsWidgets
import time
from tkinter import messagebox


class DifficultyLevel(Enum):
    EASY = 'Новачок'
    MEDIUM = 'Любитель'
    HARD = 'Професіонал'


class GameSession:
    def __init__(self, difficulty):
        self.difficulty = difficulty

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

        # For testing
        if True:
            self.num_rows = 4
            self.num_cols = 4
            self.num_mines = 2

        self.board = None

        self.seconds_elapsed = 0
        self.is_mines_inited = False
        self.flags_left = self.num_mines
        self.flags_correct = 0

        self.wdg_stats = None

        self.master = None
        self.on_end = None
        self.on_stop = None

    def clear_tk(self):
        self.master = None
        self.on_end = None
        self.on_stop = None
        self.wdg_stats = None
        for row in self.board:
            for tile in row:
                tile.clear_tk()

    def start(self, master, on_end, on_stop):
        self.master = master
        self.on_end = on_end
        self.on_stop = on_stop

        self.__top_widget()
        self.__board_widget()
        self.__stats_widget()

    def __top_widget(self):
        def update_time():
            string = time.strftime('%M:%S', time.gmtime(self.seconds_elapsed))
            lbl_time.configure(text=string)
            self.seconds_elapsed += 1
            lbl_time.after(1000, update_time)

        f = tk.Frame(self.master)
        f.pack()

        btn_exit = tk.Button(f, text='Вихід', command=self.__on_exit)
        btn_exit.pack()

        lbl_time = tk.Label(f)
        lbl_time.pack()
        update_time()

    def __board_widget(self):
        frm_board = tk.Frame(self.master)
        frm_board.pack()

        if self.board is None:
            self.board = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]

        for y in range(self.num_rows):
            for x in range(self.num_cols):
                if self.board[y][x] == 0:
                    tile = Tile(x, y)
                    self.board[y][x] = tile
                else:
                    tile = self.board[y][x]

                tile.init_button(frm_board)
                tile.button.grid(row=y, column=x, padx=0, pady=0, sticky="nsew")
                act_on_left_tap = partial(self.__on_lft_btn_tap, x, y)
                act_on_right_tap = partial(self.__on_rgt_btn_tap, x, y)
                tile.button.bind('<Button-1>', act_on_left_tap)
                tile.button.bind('<Button-2>', act_on_right_tap)
                tile.button.bind('<Button-3>', act_on_right_tap)

    def __stats_widget(self):
        frm_stats = tk.Frame(self.master)
        frm_stats.pack()
        self.wdg_stats = GameStatsWidgets(frm_stats, self.num_mines, self.flags_left)

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
                else:
                    self.wdg_stats.update(self.flags_left)
            else:
                tile.change_status(TileStatus.CLEAR)

        else:
            tile.change_status(TileStatus.CLEAR)
            self.flags_left += 1
            self.flags_correct -= tile.type == TileType.MINE
            self.wdg_stats.update(self.flags_left)

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

    def __end_on_mine(self):
        for row in self.board:
            for tile in row:
                self.__unbind_tile(tile)
                if tile.is_opened:
                    pass
                elif tile.type is TileType.MINE and tile.status is not TileStatus.SURE:
                    tile.open(is_safe=True)
                elif tile.type is not TileType.MINE and tile.status is TileStatus.SURE:
                    tile.wrong_flag()
        self.on_end(self.difficulty, False, time.gmtime(self.seconds_elapsed))

    def __end_on_success(self):
        for row in self.board:
            for tile in row:
                self.__unbind_tile(tile)
                if tile.status is not TileStatus.SURE:
                    tile.open(is_safe=True)
        self.on_end(self.difficulty, True, time.gmtime(self.seconds_elapsed))

    def __on_exit(self):
        is_save = messagebox.askyesno("Сапер", "Зберегти гру?")
        self.on_stop(is_save)
