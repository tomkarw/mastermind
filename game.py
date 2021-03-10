#!/usr/bin/python3

import os
import time

import pickle
import json

import collections

from mastermind import Mastermind

Config = collections.namedtuple('Config', ['num_pegs', 'num_tries', 'avail_pegs'])


class Game(object):
    """ Class where all the logic happens """

    def __init__(self, save_file=".save.bin", stats_file=".stats.json", config_file=".config"):
        """ Initialize attributes, check available files """

        self.load_file, self.save_file = self.init_save_file(save_file)
        self.stats, self.stats_file = self.init_stats_file(stats_file)
        self.config, self.config_file = self.init_config_file(config_file)
        self.current_game = None

    @staticmethod
    def init_save_file(save_file):
        """
        See if save file is available to load from
        Set it to True if there is, else False
        """

        try:
            fh = open(save_file, 'rb')
            fh.close()
        except IOError:
            return False, None

        return True, save_file

    @staticmethod
    def init_stats_file(stats_file):
        """ See if statistics file is available to load from
            If not, create zeroed stats """

        try:
            with open(stats_file, 'r') as fh:
                stats = json.loads(fh.read())
        except IOError:
            stats = {"gamesWon": 0, "gamesLost": 0, "numGuesses": 0, "timeInGame": 0}

        return stats, stats_file

    @staticmethod
    def init_config_file(config_file):
        try:
            with open(config_file, 'rb') as fh:
                config = pickle.load(fh)
        except IOError:
            config = Config(4, 12, ('C', 'Z', 'P', 'N', 'Ż', 'V', 'S'))

        return config, config_file

    def main_menu(self):
        """ Main program loop, main menu and game options """

        print("Welcome to MASTERMIND")
        while True:

            # print menu and get some input data
            menu_options, options_dic = self.print_menu()

            # get proper user input
            i = self.menu_input(menu_options)

            # interpret input based on options given in print_menu
            d = options_dic[i]
            if d == 'new game':
                self.new_game()
            elif d == 'continue game':
                self.continue_game()
            elif d == 'save game':
                self.save_game()
            elif d == 'load game':
                self.load_game()
            elif d == 'see stats':
                self.statistics()
            elif d == 'change config':
                self.change_configurations()
            elif d == 'quit':
                os.system('clear')
                print("Goodbye!")
                exit()

            os.system('clear')

    def print_menu(self):
        """ Print main menu """
        i = 2
        d = {1: 'new game'}
        print('1. Play new game')

        if self.current_game:
            print(f'{i}. Continue game')
            d[i] = 'continue game'
            i += 1
        if self.load_file:
            print(f'{i}. Load game from file')
            d[i] = 'load game'
            i += 1
        if self.current_game:
            print(f'{i}. Save game to file')
            d[i] = 'save game'
            i += 1
        if self.stats_file:
            print(f'{i}. See your statistics')
            d[i] = 'see stats'
            i += 1
        print(f'{i}. Change game configuration')
        d[i] = 'change config'
        i += 1
        print(f'{i}. Quit')
        d[i] = 'quit'

        return i, d

    def menu_input(self, menu_options):
        """ Loop until proper input is given
            Return input for main menu options """
        i = 0
        while i < 1 or i > menu_options:
            i = input()
            try:
                i = int(i)
                if 0 < i <= menu_options:
                    break
            except ValueError:
                os.system('clear')
                self.print_menu()
                print(f"'{i}' is not an option, choose again.")
                i = 0
                continue
            os.system('clear')
            self.print_menu()
            print(f"'{i}' is not an option, choose again.")
        return i

    def new_game(self):
        """ Create new board and start game """
        self.current_game = Mastermind(*self.config)
        self.game()

    def continue_game(self):
        """ Continue game at previous board """
        self.game()

    def load_game(self):
        try:
            with open(self.save_file, 'rb') as fh:
                self.current_game = pickle.load(fh)
            self.continue_game()
        except IOError:
            os.system('clear')
            print('Error occurred while loading the file!')
            time.sleep(1)

    def save_game(self):
        try:
            with open(self.save_file, 'wb') as fh:
                pickle.dump(self.current_game, fh)
            self.load_file = True
            os.system('clear')
            print('Successfully saved the game to file!')
        except IOError:
            os.system('clear')
            print('Error occurred while saving the file!')
        finally:
            time.sleep(1)

    def game(self):
        """ Mastermind game loop """

        m = self.current_game

        while True:
            begin_time = time.time()
            os.system('clear')
            m.print_board()

            pattern = self.game_input()
            if pattern == 'q':
                return

            comparison = m.compare_pattern(pattern)
            m.append_to_history((pattern, comparison))

            m.add_time(time.time() - begin_time)
            m.next_turn()

            if comparison[0] == m.num_pegs or m.turn == m.num_tries:
                os.system('clear')
                m.print_board()
                if comparison[0] == m.num_pegs:
                    print("Congratulations, you have won!")
                    self.add_statistics(m, True)
                else:
                    print("Game over.")
                    self.add_statistics(m, False)
                self.save_statistics()
                self.current_game = None
                input()
                return

    def game_input(self):
        """ In-game input """

        m = self.current_game

        pattern = input("Make a guess. " + str(m.avail_pegs) + '\n' + "'q' for main menu\n")

        if pattern in ('q', 'Q', 'quit'):
            return 'q'

        pattern = m.clean_pattern(pattern)

        while not m.validate_pattern(pattern):
            os.system('clear')
            m.print_board()
            pattern = input('Improper input, try again. ' + str(m.avail_pegs) + '\n' + "'q' for main menu\n")
            if pattern in ('q', 'quit'):
                return 'q'
            pattern = m.clean_pattern(pattern)

        return pattern

    def add_statistics(self, m, is_won):
        """ Update statistics with current game """

        s = self.stats

        if is_won:
            s["gamesWon"] += 1
            s["numGuesses"] += m.turn
        else:
            s["gamesLost"] += 1

        s["timeInGame"] += m.time

    def save_statistics(self):
        try:
            with open(self.stats_file, 'w') as fh:
                fh.write(json.dumps(self.stats))
        except IOError:
            print("Failed to update statistics data!")

    def statistics(self):
        """ Print out statistics """

        s = self.stats

        os.system('clear')
        print("STATISTICS")
        print(f"Games Won : {s['gamesWon']}")
        print(f"Games Lost : {s['gamesLost']}")
        try:
            print(f"Winning percentage : {s['gamesWon'] / s['gamesLost']}")
        except ZeroDivisionError:
            pass
        try:
            print(f"Average number of guesses when won : {s['numGuesses'] / s['gamesWon']}")
        except ZeroDivisionError:
            pass

        print(f"Time spent in game : {s['timeInGame']} seconds")
        input()

    def change_configurations(self):
        # ('Config',['num_pegs','num_tries','avail_pegs'])
        os.system('clear')
        num_pegs = int(input(f'Number of pegs (currently {self.config.num_pegs}): '))
        num_tries = int(input(f'Number of tries per game (currently {self.config.num_tries}): '))
        avail_pegs = tuple(input(f'Available pegs (currently {self.config.avail_pegs}): '))

        self.config = Config(num_pegs, num_tries, avail_pegs)

        try:
            with open(self.config_file, 'wb') as fh:
                pickle.dump(self.config, fh)
            os.system('clear')
            print('Successfully changed the configurations')
        except IOError:
            os.system('clear')
            print('Error while saving new configurations!')
        finally:
            time.sleep(1)


if __name__ == "__main__":
    g = Game()
    g.main_menu()
