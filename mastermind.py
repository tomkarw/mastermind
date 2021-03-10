import random
import re


class Mastermind(object):
    """ Class to represent the board """

    def __init__(self, num_pegs, num_tries, avail_pegs, pattern=None):
        """ Initialize all necessary attribute 
            num_pegs - width of the board, how many pegs in a pattern
            num_tries - maximum number of attempts to solve the pattern
            avail_pegs - range of available pegs colors
            pattern - used for setting a fixed pattern (debugging tool)
        """

        self._avail_pegs = avail_pegs
        self._num_pegs = num_pegs
        self._num_tries = num_tries
        self._listHistory = []
        self._turn = 0
        self._time = 0

        if not pattern:
            self._pattern = tuple(random.sample(self.avail_pegs, self.num_pegs))
        else:
            self._pattern = pattern

    @property
    def avail_pegs(self):
        return self._avail_pegs

    @property
    def num_pegs(self):
        return self._num_pegs

    @property
    def num_tries(self):
        return self._num_tries

    @property
    def list_history(self):
        return self._listHistory

    @property
    def turn(self):
        return self._turn

    @property
    def time(self):
        return self._time

    @property
    def pattern(self):
        return self._pattern

    def append_to_history(self, record):
        self._listHistory.append(record)

    def next_turn(self):
        self._turn += 1

    def add_time(self, time):
        self._time += time

    def compare_pattern(self, pattern):
        """ Compare guess with pattern 
            pattern - valid pattern
            Return tuple (rightly positioned pegs, rightly colored pegs)"""

        right_pos, right_col = 0, 0
        # self.history[0].append(pattern)
        for index, p in enumerate(pattern):
            if p == self.pattern[index]:
                right_pos += 1
        for p in set(pattern):
            if p in set(self.pattern):
                right_col += 1
        right_col -= right_pos
        return right_pos, right_col

    def clean_pattern(self, pattern):
        """ Clean pattern from non-peg characters
            pattern - any string
            Return string of only valid characters """

        regex = r'[^' + ''.join(self.avail_pegs) + ']'
        pattern = re.sub(regex, '', pattern.upper())
        return pattern

    def validate_pattern(self, pattern):
        """ Check if input pattern is valid 
            pattern - string cleared of invalid characters
            Return True if string is a viable pattern, else False """

        if len(pattern) != self.num_pegs:
            return False
        for p in pattern:
            if p not in self.avail_pegs:
                return False
        return True

    def print_board(self):
        """ Print current board """
        print_string = ''

        for i in range(self.num_tries - self.turn):
            print_string += '| '
            print_string += '_ ' * self.num_pegs
            print_string += '|\n'

        for i in range(self.turn):
            print_string += '| '
            for p in self.list_history[i][0]:
                print_string += str(p) + ' '
            print_string += '|'
            print_string += f" pos={self.list_history[i][1][0]} col={self.list_history[i][1][1]}\n"

        print(print_string, end='')
