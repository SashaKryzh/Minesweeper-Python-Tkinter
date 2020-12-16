import tkinter as tk
from minesweeper.game.Game import Game

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Сапер")
    window.geometry('500x400')

    Game(window)

    window.mainloop()
