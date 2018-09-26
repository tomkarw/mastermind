#!/usr/bin/python3

import itertools
import re
import pickle
import collections

Config = collections.namedtuple('Config',['numPegs','numTries','availPegs'])

def init_config_file(config_file):
        try:
            with open(config_file,'rb') as fh:
                return pickle.load(fh)
        except IOError:
            print('No such file!')

def compare_pattern(pattern0,pattern):

        rightPos,rightCol = 0, 0
        for index,p in enumerate(pattern):
            if p == pattern0[index]:
                rightPos += 1
        for p in set(pattern):
            if p in set(pattern0):
                rightCol += 1
        rightCol -= rightPos
        return rightPos,rightCol

def parse_result(board_print):
    poscolRegex = re.compile(r'pos=(\d) col=(\d)')
    return poscolRegex.findall(board_print)[-1]

config = init_config_file('.mastermind.config')

allPatterns = list(itertools.permutations(config.availPegs,config.numPegs))

print(1)

for turn in range(config.numTries):
    
    if turn==0:
        pat = config.availPegs[:config.numPegs]
    elif turn==1:
        pat = config.availPegs[-config.numPegs:]
    else:
        pat = allPatterns[0]
    print(''.join(pat))
    
    board_print = input()
    print(board_print)
    pos,col = parse_result(board_print)
    pos = int(pos)
    col = int(col)
    
    allPatterns = list(filter(lambda tupl : compare_pattern(tupl,pat) == (pos,col),allPatterns))
    
    if len(allPatterns) == 1:
        exit()
    #print(allPatterns)
