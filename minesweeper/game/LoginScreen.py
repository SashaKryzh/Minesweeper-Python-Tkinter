import tkinter as tk
from tkinter import messagebox
from minesweeper.auth.User import User
from minesweeper.game.AdminScreen import AdminScreen


class LoginScreen:
    def __init__(self, root, auth, on_logged):
        self.root = root

        self.master = tk.Frame(root)
        self.auth = auth
        self.on_logged = on_logged

        self.ent_login = None
        self.ent_password = None

        self.__setup()

    def __setup(self):
        self.master.pack(expand=True)

        lbl = tk.Label(self.master, text='Who are you?')
        lbl.grid(row=0, columnspan=2)

        lbl_login = tk.Label(self.master, text='login: ')
        self.ent_login = tk.Entry(self.master, width=20)
        lbl_login.grid(row=1, column=0, sticky='e')
        self.ent_login.grid(row=1, column=1)

        lbl_password = tk.Label(self.master, text='password:')
        self.ent_password = tk.Entry(self.master, width=20, show='*')
        lbl_password.grid(row=2, column=0, sticky='e')
        self.ent_password.grid(row=2, column=1)

        btn_login = tk.Button(self.master, text='Login / Register', command=self.__on_login_tap)
        btn_login.grid(row=3, column=1, sticky='e')

    def __on_login_tap(self):
        login = self.ent_login.get()
        password = self.ent_password.get()
        print('login: "{}" - password: "{}"'.format(login, password))
        if login == '' or password == '':
            messagebox.showerror('Login', 'Fields can\'t be empty')
            return
        res = self.auth.sign_in(login, password)
        if isinstance(res, User):
            self.on_logged()
        elif res == 'admin':
            self.__on_admin()
        else:
            messagebox.showerror('Login', res)

    def __on_admin(self):
        self.master.destroy()
        self.master = AdminScreen(self.root, self.auth, self.__on_back)
        self.master.pack(fill=tk.BOTH, expand=True)

    def __on_back(self):
        self.master.destroy()
        self.master = tk.Frame(self.root)
        self.__setup()
