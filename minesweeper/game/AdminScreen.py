import tkinter as tk
from tkinter import messagebox


class AdminScreen(tk.Frame):
    def __init__(self, master, auth, on_back, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.auth = auth

        self.frm_left = tk.Frame(self)
        self.frm_left.pack(side=tk.LEFT, fill=tk.Y)

        self.btn_back = tk.Button(self.frm_left, text='Назад', command=on_back, width=15)
        self.btn_back.pack(pady=2, padx=2)

        self.btn_delete = tk.Button(self.frm_left, text='Видалити', command=self.__on_delete, width=15)
        self.btn_delete.pack(pady=2, padx=2)

        self.list = tk.Listbox(self, selectmode=tk.SINGLE, height=22, width=54)
        self.list.pack(side=tk.LEFT, padx=4)

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
