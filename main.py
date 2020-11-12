import tkinter as tk
from game import Game


def main(name):
    window = tk.Tk()

    window.title("Minesweeper")
    window.geometry('500x400')

    game = Game(window)

    window.mainloop()


if __name__ == '__main__':
    main('Minesweeper')
