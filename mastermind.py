import random
import re

class Mastermind(object):
    """ Class to represent the board """
    
    def __init__(self,numPegs=4,numTries=12,pattern=None):
        self.numPegs = numPegs
        self.numTries = numTries
        self.history = []
        self.turn = 0
        self.avail_pegs = ('R','G','Y','P','B','W')
        if pattern == None:
            self.pattern = tuple(random.sample(self.avail_pegs,4))
        else:
            self.pattern = pattern
        
    def compare_pattern(self,pattern):
        """ Compare guess with pattern """
        rightPos,rightCol = 0, 0
        #self.history[0].append(pattern)
        for index,p in enumerate(pattern):
            if p == self.pattern[index]:
                rightPos += 1
        for p in set(pattern):
            if p in set(self.pattern):
                rightCol += 1
        rightCol -= rightPos
        return rightPos,rightCol
    
    def clean_pattern(self,pattern):
        """ Clean pattern from non-peg characters """
        regex = r'[^'+''.join(self.avail_pegs)+']'
        pattern = re.sub(regex,'',pattern.upper())
        return pattern
        
    def validate_pattern(self,pattern):
        """ Check if input pattern is valid """
        if len(pattern) != self.numPegs:
            return False
        for p in pattern:
            if p not in self.avail_pegs:
                return False
        return True
        
    def print_board(self):
        """ Print current board """        
        for i in range(self.numTries-self.turn):
            print('| ',end='')
            print('_ '*self.numPegs,end='')
            print('|')
        
        for i in range(self.turn):
            print('| ',end='')
            for p in self.history[i][0]:
                print(p+' ',end='')
            print('|',end='')
            print(" pos=%i col=%i" % (self.history[i][1][0], self.history[i][1][1]))
