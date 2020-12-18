import tkinter as tk
from minesweeper.game.Game import Game

if __name__ == '__main__':
    window = tk.Tk()
    window.title("Сапер")
    window.geometry('600x400+400+200')

    Game(window)

    window.mainloop()
