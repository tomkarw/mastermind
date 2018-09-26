#!/usr/bon/python3

import random
import re

class Mastermind(object):
    """ Class to represent the board """
    
    def __init__(self,numPegs,numTries,availPegs,pattern=None):
        """ Initialize all necessary attribute 
            numPegs - width of the board, how many pegs in a pattern
            numTries - maximum number of attempts to solve the pattern
            avail_pegs - range of avalible pegs colors
            pattern - used for setting a fixed pattern (debugging tool)
        """
        
        self._availPegs = availPegs
        self._numPegs = numPegs
        self._numTries = numTries
        self._listHistory = []
        self._turn = 0
        self._time = 0
        
        
        if not pattern:
            self._pattern = tuple(random.sample(self.availPegs,self.numPegs))
        else:
            self._pattern = pattern
    
    @property
    def availPegs(self):
        return self._availPegs
    
    @property
    def numPegs(self):
        return self._numPegs
        
    @property
    def numTries(self):
        return self._numTries
        
    @property
    def listHistory(self):
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
    
    def appendToHistory(self,record):
        self._listHistory.append(record)
        
    def nextTurn(self):
        self._turn += 1
        
    def addTime(self,time):
        self._time += time
    
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
            
        regex = r'[^'+''.join(self.availPegs)+']'
        pattern = re.sub(regex,'',pattern.upper())
        return pattern
        
        
    def validate_pattern(self,pattern):
        """ Check if input pattern is valid 
            pattern - string cleard of unvalid characters
            Return True if string is a viable pattern, else False """
            
        if len(pattern) != self.numPegs:
            return False
        for p in pattern:
            if p not in self.availPegs:
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
            for p in self.listHistory[i][0]:
                print(p+' ',end='')
            print('|',end='')
            print(" pos=%i col=%i" % (self.listHistory[i][1][0], self.listHistory[i][1][1]))

