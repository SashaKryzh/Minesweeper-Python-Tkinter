import tkinter as tk
from tkinter import ttk
import time


class Leaderboard:
    def __init__(self, master, auth, on_back):
        self.ALL = 'All'

        self.master = master
        self.auth = auth

        self.results = self.auth.get_all_results()
        self.user_logins = set(map(lambda a: a[0].login, self.results))

        self.cmbb_user = None
        self.lstb_results = None

        self.__setup(on_back)

    def __setup(self, on_back):
        self.master.pack(fill=tk.BOTH, expand=True)

        frm_left = tk.Frame(self.master)
        frm_left.pack(side=tk.LEFT, fill=tk.BOTH)

        btn_back = tk.Button(frm_left, text='Назад', command=on_back)
        btn_back.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.W))

        options = [self.ALL] + list(self.user_logins)
        self.cmbb_user = ttk.Combobox(frm_left, values=options, state="readonly")
        self.cmbb_user.current(0)
        self.cmbb_user.bind("<<ComboboxSelected>>", self.__on_update_list)
        self.cmbb_user.grid(column=0, row=1, sticky=(tk.N))

        self.lstb_results = tk.Listbox(self.master, height=22, width=37)
        self.__on_update_list()
        self.lstb_results.pack(side=tk.LEFT)

    def __on_update_list(self, event=None):
        self.lstb_results.delete(0, tk.END)

        login = self.cmbb_user.get()
        if login == self.ALL:
            results = self.results
        else:
            results = list(filter(lambda a: a[0].login == login, self.results))

        for result in results:
            u = result[0]
            r = result[1]
            win = 'ВИГРАВ' if r.is_win else 'ПРОГРАВ'
            t_string = time.strftime('%M:%S', r.time_elapsed)
            string = '{} {} {} {}'.format(u.login, win, r.difficulty.value, t_string)
            self.lstb_results.insert(tk.END, string)
