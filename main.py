import os
from mastermind import Mastermind

class Game(object):
    """ Class where all the logic happens """
    
    def __init__(self,continue_file=None,history_file=None):
        #self.menu_options = len(re.findall(r'\n',getsource(self.print_menu)))-1
        self.menu_options = 2
        
    def start(self):
        """ Main program loop, main menu and game options """
        
        print("Welcome to MASTERMIND")
        while True:
            self.print_menu()
            
            i = int(input())
            while(i<0 or i>self.menu_options):
                print('Unknown option, choose again')
                i = int(input())
            
            if i == 1:
                self.game()
            if i == 2:
                exit()
        
    def game(self):
        """ New mastermind game loop """
        
        m = Mastermind()
        
        while True:
            os.system('clear')
            m.print_board()
            print(m.pattern)
            pattern = input('Make a guess. '+str(m.avail_pegs)+'\n')
            pattern = m.clean_pattern(pattern)
            while not m.validate_pattern(pattern):
                pattern = input('Inproper input, try again. '+str(m.avail_pegs)+'\n')
                pattern = m.clean_pattern(pattern)
                
            comparison = m.compare_pattern(pattern)
            m.history.append((pattern,comparison))
            
            m.turn += 1
            if comparison[0] == m.numPegs or m.turn == m.numTries:
                if comparison[0] == m.numPegs:
                    print("Congratulations, you have won!")
                else:
                    print("Game over.")
                input()
                os.system('clear')
                return

    def print_menu(self):
        print('1. Play new game')
        print('2. Quit')

g = Game()
g.start()
