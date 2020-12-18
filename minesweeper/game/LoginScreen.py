import tkinter as tk
from tkinter import messagebox
from minesweeper.auth.User import User
from minesweeper.game.AdminScreen import AdminScreen
import settings

class LoginScreen:
    def __init__(self, root, auth, on_logged):
        self.root = root

        self.master = None
        self.frm_hint = None
        self.auth = auth
        self.on_logged = on_logged

        self.ent_login = None
        self.ent_password = None

        self.__setup()

    def __setup(self):
        self.master = tk.Frame(self.root)
        self.master.pack(expand=True)

        if settings.language.lower() == 'english':
            lbl = tk.Label(self.master, text='Who are you?')
            lbl_login = tk.Label(self.master, text='Login: ')
            lbl_password = tk.Label(self.master, text='Password:')
            btn_login = tk.Button(self.master, text='Login / Register', command=self.__on_login_tap)
        elif settings.language.lower() == 'russian':
            lbl = tk.Label(self.master, text='Хто ти?')
            lbl_login = tk.Label(self.master, text='Логін: ')
            lbl_password = tk.Label(self.master, text='Пароль:')
            btn_login = tk.Button(self.master, text='Увійти / Зареєструватися', command=self.__on_login_tap)
            

        lbl.grid(row=0, columnspan=2)

        self.ent_login = tk.Entry(self.master, width=20)
        lbl_login.grid(row=1, column=0, sticky='e')
        self.ent_login.grid(row=1, column=1)

        self.ent_password = tk.Entry(self.master, width=20, show='*')
        lbl_password.grid(row=2, column=0, sticky='e')
        self.ent_password.grid(row=2, column=1)

        btn_login.grid(row=3, column=0, columnspan=2, sticky='ew')
 
        self.frm_hint = tk.Frame(self.root)
        self.frm_hint.pack(fill=tk.BOTH)
        lbl_admin = tk.Label(self.frm_hint, text='admin - admin', fg='gray')
        lbl_admin.pack(side=tk.BOTTOM, pady=4)

    def __on_login_tap(self):
        login = self.ent_login.get()
        password = self.ent_password.get()

        if login == '' or password == '':
            if settings.language.lower() == 'english':
                messagebox.showerror('Authorization', 'Fields cannot be empty')
            elif settings.language.lower() == 'russian':
                messagebox.showerror('Авторизація', 'Поля не можуть бути порожніми')
            return

        res = self.auth.sign_in(login, password)
        if isinstance(res, User):
            self.on_logged()
        elif res == 'admin':
            self.__on_admin()
        elif isinstance(res, str):
            if settings.language.lower() == 'english':
                messagebox.showerror('Authorization', res)
            elif settings.language.lower() == 'russian':
                messagebox.showerror('Авторизація', res)

    def __on_admin(self):
        self.master.destroy()
        self.frm_hint.destroy()
        self.master = AdminScreen(self.root, self.auth, self.__on_back)
        self.master.pack(fill=tk.BOTH, expand=True)

    def __on_back(self):
        self.master.destroy()
        self.__setup()
