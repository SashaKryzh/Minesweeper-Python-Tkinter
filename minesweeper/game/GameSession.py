from minesweeper.game.Tile import Tile, TileType, TileStatus
import tkinter as tk
import random
from functools import partial
from enum import Enum
import time
from tkinter import messagebox
import settings

class DifficultyLevel(Enum):
    if settings.language.lower() == 'english':
        EASY = 'Easy'
        MEDIUM = 'Medium'
        HARD = 'Hard'
    elif settings.language.lower() == 'russian':
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
        # self.num_rows = 4
        # self.num_cols = 4
        # self.num_mines = 2

        self.board = None

        self.is_playing = None
        self.seconds_elapsed = 0
        self.is_mines_inited = False
        self.flags_left = self.num_mines
        self.flags_correct = 0

        self.master = None
        self.on_end = None
        self.on_stop = None

        self.lbl_flags = None

    def clear_tk(self):
        self.master = None
        self.on_end = None
        self.on_stop = None
        self.lbl_flags = None
        for row in self.board:
            for tile in row:
                tile.clear_tk()

    def start(self, master, on_end, on_stop):
        self.is_playing = True

        self.master = master
        self.on_end = on_end
        self.on_stop = on_stop

        self.__menu_widget()
        self.__board_widget()

    def __menu_widget(self):
        def update_time():
            if settings.language.lower() == 'english':
                string = time.strftime('Time: %M:%S', time.gmtime(self.seconds_elapsed))
            elif settings.language.lower() == 'russian':
                string = time.strftime('Час: %M:%S', time.gmtime(self.seconds_elapsed))
            lbl_time.configure(text=string)
            if self.is_playing:
                self.seconds_elapsed += 1
                lbl_time.after(1000, update_time)

        frm = tk.Frame(self.master)
        frm.pack(side=tk.LEFT, fill=tk.Y, pady=2, padx=2)

        if settings.language.lower() == 'english':
            btn_exit = tk.Button(frm, text='Entrance', command=self.__on_exit, width=15)
        elif settings.language.lower() == 'russian':
            btn_exit = tk.Button(frm, text='Вихід', command=self.__on_exit, width=15)
        
        btn_exit.pack()

        tk.Frame(frm, height=15).pack()

        lbl_time = tk.Label(frm, anchor=tk.W)
        lbl_time.pack(fill=tk.X)
        update_time()

        if settings.language.lower() == 'english':
            lbl_num_mines = tk.Label(frm, text='Min: {}'.format(self.num_mines), anchor=tk.W)
        elif settings.language.lower() == 'russian':
            lbl_num_mines = tk.Label(frm, text='Мін: {}'.format(self.num_mines), anchor=tk.W)
        lbl_num_mines.pack(fill=tk.X)

        self.lbl_flags = tk.Label(frm, anchor=tk.W)
        self.lbl_flags.pack(fill=tk.X)
        self.__update_flags()

    def __update_flags(self):
        if settings.language.lower() == 'english':
            self.lbl_flags.configure(text='Remaining flags: {}'.format(self.flags_left))
        elif settings.language.lower() == 'russian':
            self.lbl_flags.configure(text='Залишилося флагів: {}'.format(self.flags_left))

    def __board_widget(self):
        frm_board = tk.Frame(self.master)
        frm_board.pack(side=tk.LEFT, padx=4, pady=2)

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
                    self.__update_flags()
            else:
                tile.change_status(TileStatus.CLEAR)

        else:
            tile.change_status(TileStatus.CLEAR)
            self.flags_left += 1
            self.flags_correct -= tile.type == TileType.MINE
            self.__update_flags()

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
        self.is_playing = False
        for row in self.board:
            for tile in row:
                self.__unbind_tile(tile)
                if tile.is_opened:
                    pass
                elif tile.type is TileType.MINE and tile.status is not TileStatus.SURE:
                    tile.open(is_safe=True)
                elif tile.type is not TileType.MINE and tile.status is TileStatus.SURE:
                    tile.wrong_flag()

        def f():
            if settings.language.lower() == 'english':
                self.__display_message('LOSS')
            elif settings.language.lower() == 'russian':
                self.__display_message('ПРОГРАШ')
            self.on_end(self.difficulty, False, time.gmtime(self.seconds_elapsed))
        self.master.after(200, f)

    def __end_on_success(self):
        self.is_playing = False
        for row in self.board:
            for tile in row:
                self.__unbind_tile(tile)
                if tile.status is not TileStatus.SURE:
                    tile.open(is_safe=True)

        def f():
            if settings.language.lower() == 'english':
                self.__display_message('VICTORY')
            elif settings.language.lower() == 'russian':
                self.__display_message('ПЕРЕМОГА')
            self.on_end(self.difficulty, True, time.gmtime(self.seconds_elapsed))
        self.master.after(200, f)

    def __display_message(self, text):
        gmt = time.gmtime(self.seconds_elapsed)
        time_string = time.strftime('%M:%S', gmt)
        if settings.language.lower() == 'english':
            messagebox.showinfo('Сапер', '{}\nTime: {}'.format(text, time_string))
        elif settings.language.lower() == 'russian':
            messagebox.showinfo('Сапер', '{}\nЧас: {}'.format(text, time_string))

    def __on_exit(self):
        if settings.language.lower() == 'english':
            is_save = messagebox.askyesno("Сапер", "Save game?")
        elif settings.language.lower() == 'russian':
            is_save = messagebox.askyesno("Сапер", "Зберегти гру?")
        self.on_stop(is_save)
