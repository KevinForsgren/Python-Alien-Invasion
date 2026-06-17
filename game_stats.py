class GameStats:
    '''Track statistics for Alien Invasion.'''

    def __init__(self, ai_game):
        '''Initialize statistics.'''
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset
        self.high_score = self.read_calculated_highscore()

    def reset_stats(self):
        '''Initialize statistic that can change during the game.'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def read_calculated_highscore(self):
        '''Read the highscore from the txt file.'''
        with open("score.txt", "r") as file:
            score = file.read().strip()
            if not score:
                high_score = 0
            else:
                high_score = score
            return int(high_score)
