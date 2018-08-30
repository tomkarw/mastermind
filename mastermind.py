import random
import re

class Mastermind(object):
    """ Class to represent the board """
    
    def __init__(self,numPegs=4,numTries=12,avail_pegs=('R','G','Y','P','B','W'),pattern=None):
        """ Initialize all necessary attribute 
            numPegs - width of the board, how many pegs in a pattern
            numTries - maximum number of attempts to solve the pattern
            avail_pegs - range of avalible pegs colors
            pattern - used for setting a fixed pattern (debugging tool)
        """
        
        self.numPegs = numPegs
        self.numTries = numTries
        self.history = []
        self.turn = 0
        self.time = 0
        self.avail_pegs = avail_pegs
        
        if pattern == None:
            self.pattern = tuple(random.sample(self.avail_pegs,4))
        else:
            self.pattern = pattern
        
        
    def compare_pattern(self,pattern):
        """ Compare guess with pattern 
            pattern - valid pattern
            Return tuple (rightly positioned pegs, rightly colored pegs)"""
            
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
        """ Clean pattern from non-peg characters
            pattern - any string
            Return string of only valid characters """
            
        regex = r'[^'+''.join(self.avail_pegs)+']'
        pattern = re.sub(regex,'',pattern.upper())
        return pattern
        
        
    def validate_pattern(self,pattern):
        """ Check if input pattern is valid 
            pattern - string cleard of unvalid characters
            Return True if string is a viable pattern, else False """
            
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

