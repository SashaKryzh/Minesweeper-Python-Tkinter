from minesweeper.auth.User import User
from tkinter import messagebox
import pickle
import os
import settings
from minesweeper.languages.language import text_messages

class Auth:
    def __init__(self):
        self.__path = 'minesweeper/data/users.pickle'

        self.current_user = None
        self.users = []

        self.text_messages = text_messages
        try:
            with open(self.__path, 'rb') as f:
                self.users = pickle.load(f)
        except:
            print('"users.pickle" doesn\'t exists')

    def __new_user(self, login, password):
        user = User(login, password)
        self.users.append(user)
        self.__save()
        return user

    def __save(self):
        os.makedirs(os.path.dirname(self.__path), exist_ok=True)
        with open(self.__path, 'wb') as f:
            pickle.dump(self.users, f, pickle.HIGHEST_PROTOCOL)

    def sign_in(self, login, password):
        if login == 'admin':
            if password == 'admin':
                return 'admin'
            else:
                return self.text_messages[settings.language.lower()].auth.sign_in.invalid_admin_password

        user = next((user for user in self.users if user.login == login), None)

        if user is not None:
            password_match = user.password == password
            if password_match:
                self.current_user = user
                return self.current_user
            else:
                return self.text_messages[settings.language.lower()].auth.sign_in.invalid_password
        else:
            if messagebox.askyesno(self.text_messages[settings.language.lower()].auth.sign_in.authorization, '{}{}{}{}?'.format(self.text_messages[settings.language.lower()].auth.sign_in.create_new_player, login, self.text_messages[settings.language.lower()].auth.sign_in.with_password, password)):
                self.current_user = self.__new_user(login, password)
                return self.current_user
            else:
                return None

    def sign_out(self):
        self.current_user = None

    def delete_user(self, user):
        self.users.remove(user)
        self.__save()

    def update_unfinished_game(self, game_session):
        self.current_user.unfinished_game = game_session
        self.__save()

    def update_users_results(self, difficulty, is_win, time_elapsed):
        self.current_user.add_result(difficulty, is_win, time_elapsed)
        self.__save()

    def get_all_results(self):
        results = []
        for user in self.users:
            results += map(lambda a: (user, a), user.last_results)
        return results
