import tkinter as tk
from tkinter import messagebox


class AdminScreen(tk.Frame):
    def __init__(self, master, auth, on_back, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.auth = auth

        self.frm_left = tk.Frame(self)
        self.frm_left.grid(column=0, row=0)

        self.btn_back = tk.Button(self.frm_left, text='Назад', command=on_back)
        self.btn_back.pack()

        self.btn_delete = tk.Button(self.frm_left, text='Видалити', command=self.__on_delete)
        self.btn_delete.pack()

        self.frm_right = tk.Frame(self)
        self.frm_right.grid(column=1, row=0)

        self.list = tk.Listbox(self.frm_right, selectmode=tk.SINGLE)
        self.list.pack()

        self.__update_users()

    def __update_users(self):
        for user in self.auth.users:
            string = 'Логін: {}, Пароль: {}'.format(user.login, user.password)
            self.list.insert(tk.END, string)

    def __on_delete(self):
        index = self.list.curselection()[0]
        user = self.auth.users[index]
        is_delete = messagebox.askyesno("Сапер", "Видалити: {}?".format(user.login))
        if is_delete:
            self.auth.delete_user(user)
            self.list.delete(index)
