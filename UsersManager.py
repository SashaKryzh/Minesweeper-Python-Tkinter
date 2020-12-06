from User import User
import pickle


class UsersManager:
    def __init__(self):
        self.current_user = None
        self.users = []

        try:
            with open('users.pickle', 'rb') as f:
                self.users = pickle.load(f)
                print(self.users)
        except:
            print('No saved users')

    def sign_in(self, login, password):
        """
        :param login:
        :param password:
        :return: Text if error or User if success
        """
        user = next((user for user in self.users if user.login == login), None)
        if user is not None:
            password_match = user.password == password
            if password_match:
                self.current_user = user
                print('Logged')
                return self.current_user
            else:
                return 'Wrong password'
        else:
            self.current_user = self.__new_user(login, password)
            print('New user')
            return self.current_user

    def __new_user(self, login, password):
        user = User(login, password)
        self.users.append(user)
        self.save()
        return user

    def save(self):
        with open('users.pickle', 'wb') as f:
            pickle.dump(self.users, f, pickle.HIGHEST_PROTOCOL)
