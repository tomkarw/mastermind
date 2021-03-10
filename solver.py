#!/usr/bin/python3

import itertools
import re
import pickle
import collections
import sys

Config = collections.namedtuple('Config', ['numPegs', 'numTries', 'availPegs'])


def init_config_file(config_file):
    try:
        with open(config_file, 'rb') as fh:
            return pickle.load(fh)
    except IOError:
        print('No such file!')


def compare_pattern(pattern0, pattern):
    rightPos, rightCol = 0, 0
    for index, p in enumerate(pattern):
        if p == pattern0[index]:
            rightPos += 1
    for p in set(pattern):
        if p in set(pattern0):
            rightCol += 1
    rightCol -= rightPos
    return rightPos, rightCol


def parse_result(line_input):
    poscolRegex = re.compile(r'.*pos=(\d) col=(\d).*')
    match = poscolRegex.match(line_input)
    if match:
        return match[1], match[2]
    else:
        return None, None


config = init_config_file('.mastermind.config')

allPatterns = list(itertools.permutations(config.availPegs, config.numPegs))

output = open('output.log', 'w')

# New game
print(1)
print(1, file=output)

for turn in range(config.numTries):

    if turn == 0:
        pat = config.availPegs[:config.numPegs]
    elif turn == 1:
        pat = config.availPegs[-config.numPegs:]
    else:
        pat = allPatterns[0]

    print(''.join(pat))
    print(''.join(pat), file=output)
    pos, col = None, None
    while (pos == None or col == None):
        board_print = input()
        print('master:', board_print, file=output)
        pos, col = parse_result(board_print)
        # print('solver:',pos,col,file=output)
    for _ in range(turn):
        board_print = input()
        print('master:', board_print, file=output)
        pos, col = parse_result(board_print)
        print('solver', pos, col, file=output)
    pos = int(pos)
    col = int(col)

    allPatterns = list(filter(lambda tupl: compare_pattern(tupl, pat) == (pos, col), allPatterns))
    print('solver: len = ', len(allPatterns), file=output)

    if len(allPatterns) <= 1:
        pat = allPatterns[0]
        # print(''.join(pat))
        print('q')
        print('q')
        print(5)
        # print(''.join(pat),file=output)
        print('q', file=output)
        print('q', file=output)
        print(5, file=output)
        exit()
