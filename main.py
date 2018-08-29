import os
import pickle
import time
from mastermind import Mastermind

class Game(object):
    """ Class where all the logic happens """
    
    def __init__(self,save_file="save.mastermind-bin",stats_file="stats.mastermind-txt"):
        """ Initailize attributes, check avaliable files """
        
        self.init_save_file(save_file) # current issue, saving mechanism
        self.init_stats_file()
        self.current_game = None
    
    def init_save_file(self,save_file):
        """ See if save file is avalible to load from
            Set it to True if there is, else Fasle """
        try:
            fH = open(save_file,'rb')
            fH.close()
            self.load_file = True
        except:
            self.load_file = False
        finally:
            self.save_file = save_file
    
    def init_stats_file(self):
        """ See if save file is avalible to load from
            Set it to file name if there is, else set to None """
        try:
            fH = open(stats_file,'r')
            fH.close()
            self.stats_file = stats_file
        except:
            self.stats_file = None
            
    def start(self):
        """ Main program loop, main menu and game options """
        
        print("Welcome to MASTERMIND")
        while True:
            
            # print menu and get some input data
            menu_options,options_dic = self.print_menu()
            
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
            elif d == 'quit':
                os.system('clear')
                print("Goodbye!")
                exit()
                
            os.system('clear')
    
    def print_menu(self):
        """ Print main menu """
        i = 2
        d = {1:'new game'}
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
        print(f'{i}. Quit')
        d[i] = 'quit'
        
        return i,d
    
    def menu_input(self,menu_options):
        """ Loop untill proper input is given
            Return input for main menu options """
        i = 0
        while(i<1 or i>menu_options):
            i = input()
            try:
                i = int(i)
                if i>0 and i<=menu_options:
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
        self.current_game = Mastermind()
        self.game()
    
    def continue_game(self):
        """ Continue game at previous board """
        self.game()
    
    def load_game(self):
        try:
            with open(self.save_file,'rb') as fh:
                self.current_game = pickle.load(fh)
            self.continue_game()
        except:
            os.system('clear')
            print('Error occured while loading the file!')
            time.sleep(1)
        
    def save_game(self):
        try:
            with open(self.save_file,'wb') as fh:
                pickle.dump(self.current_game, fh)
            self.load_file = True
            os.system('clear')
            print('Successfully saved the game to file!')
        except:
            os.system('clear')
            print('Error occured while saving the file!')
        finally:
            time.sleep(1)
            
        
    def game(self):
        """ Start new Mastermind game """
        
        m = self.current_game
        
        while True:
            os.system('clear')
            m.print_board()
            
            pattern = self.game_input()
            if pattern == 'q':
                return
            
            comparison = m.compare_pattern(pattern)
            m.history.append((pattern,comparison))
            
            m.turn += 1
            if comparison[0] == m.numPegs or m.turn == m.numTries:
                os.system('clear')
                m.print_board()
                if comparison[0] == m.numPegs:
                    print("Congratulations, you have won!")
                else:
                    print("Game over.")
                self.current_game = None
                input()
                return
                
    def game_input(self):
        """ In-game input """ 
        m = self.current_game
        
        pattern = input("Make a guess. "+str(m.avail_pegs)+'\n'+"'q' for main menu\n")
        if pattern in ('q','Q','quit'):
            return 'q'
        pattern = m.clean_pattern(pattern)
        while not m.validate_pattern(pattern):
            os.system('clear')
            m.print_board()
            pattern = input('Inproper input, try again. '+str(m.avail_pegs)+'\n'+"'q' for main menu\n")
            if pattern in ('q','quit'):
                return 'q'
            pattern = m.clean_pattern(pattern)
                
        return pattern
        

g = Game()
g.start()
