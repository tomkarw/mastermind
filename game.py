#!/usr/bin/python3

import os
import time

import pickle
import json

import collections

from mastermind import Mastermind

Config = collections.namedtuple('Config', ['numPegs', 'numTries', 'availPegs'])


class Game(object):
    """ Class where all the logic happens """

    def __init__(self, save_file=".save.bin", stats_file=".stats.json", config_file=".config"):
        """ Initialize attributes, check available files """

        self.init_save_file(save_file)
        self.init_stats_file(stats_file)

        self.Config = Config
        self.init_config_file(config_file)

        self.current_game = None

    def init_save_file(self, save_file):
        """
        See if save file is available to load from
        Set it to True if there is, else False
        """

        try:
            fH = open(save_file, 'rb')
            fH.close()
            self.load_file = True
        except IOError:
            self.load_file = False
        finally:
            self.save_file = save_file

    def init_stats_file(self, stats_file):
        """ See if statistics file is available to load from
            If not, create zeroed stats """

        try:
            with open(stats_file, 'r') as fh:
                self.stats = json.loads(fh.read())
        except IOError:
            self.stats = {"gamesWon": 0, "gamesLost": 0, "numGuesses": 0, "timeInGame": 0}
        finally:
            self.stats_file = stats_file

    def init_config_file(self, config_file):
        try:
            with open(config_file, 'rb') as fh:
                self.config = pickle.load(fh)
        except IOError:
            self.config = self.Config(4, 12, ('C', 'Z', 'P', 'N', 'Ż', 'V', 'S'))
        finally:
            self.config_file = config_file

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
        while (i < 1 or i > menu_options):
            i = input()
            try:
                i = int(i)
                if i > 0 and i <= menu_options:
                    break
            except:
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
            print('Error occured while loading the file!')
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
            print('Error occured while saving the file!')
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
            m.appendToHistory((pattern, comparison))

            m.addTime(time.time() - begin_time)
            m.nextTurn()

            if comparison[0] == m.numPegs or m.turn == m.numTries:
                os.system('clear')
                m.print_board()
                if comparison[0] == m.numPegs:
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

        pattern = input("Make a guess. " + str(m.availPegs) + '\n' + "'q' for main menu\n")

        if pattern in ('q', 'Q', 'quit'):
            return 'q'

        pattern = m.clean_pattern(pattern)

        while not m.validate_pattern(pattern):
            os.system('clear')
            m.print_board()
            pattern = input('Inproper input, try again. ' + str(m.availPegs) + '\n' + "'q' for main menu\n")
            if pattern in ('q', 'quit'):
                return 'q'
            pattern = m.clean_pattern(pattern)

        return pattern

    def add_statistics(self, m, isWon):
        """ Update statistics with current game """

        s = self.stats

        if isWon:
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
        # ('Config',['numPegs','numTries','availPegs'])
        os.system('clear')
        numPegs = int(input(f'Number of pegs (currently {self.config.numPegs}): '))
        numTries = int(input(f'Number of tries per game (currently {self.config.numTries}): '))
        availPegs = tuple(input(f'Available pegs (currently {self.config.availPegs}): '))

        self.config = self.Config(numPegs, numTries, availPegs)

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