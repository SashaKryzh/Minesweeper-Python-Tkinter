import time


class GameResult:
    def __init__(self, difficulty, is_win, time_elapsed):
        self.difficulty = difficulty
        self.is_win = is_win
        self.time_elapsed = time_elapsed
        self.date = time.localtime()

    def __repr__(self):
        elapsed = time.strftime('%M:%S', self.time_elapsed)
        date = time.strftime('%d.%m %H:%M:%S', self.date)
        return '{} {} {} ({})'.format(self.is_win, elapsed, self.difficulty, date)
