from minesweeper.auth.GameResult import GameResult


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.unfinished_game = None
        self.last_results = []

    def add_result(self, difficulty, is_win, time_elapsed):
        self.last_results.insert(0, GameResult(difficulty, is_win, time_elapsed))
        if len(self.last_results) > 10:
            self.last_results.pop()

    def save_game(self, game):
        self.unfinished_game = game

    def __repr__(self):
        return self.login
