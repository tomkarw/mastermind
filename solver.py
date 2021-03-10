#!/usr/bin/python3

import itertools
import re
import pickle
import collections
import sys

Config = collections.namedtuple('Config', ['num_pegs', 'num_tries', 'avail_pegs'])


def init_config_file(config_file):
    try:
        with open(config_file, 'rb') as fh:
            return pickle.load(fh)
    except IOError:
        print('No such file!')


def compare_pattern(pattern0, pattern):
    right_pos, right_col = 0, 0
    for index, p in enumerate(pattern):
        if p == pattern0[index]:
            right_pos += 1
    for p in set(pattern):
        if p in set(pattern0):
            right_col += 1
    right_col -= right_pos
    return right_pos, right_col


def parse_result(line_input):
    pos_col_regex = re.compile(r'.*pos=(\d) col=(\d).*')
    match = pos_col_regex.match(line_input)
    if match:
        return match[1], match[2]
    else:
        return None, None


config = init_config_file('.mastermind.config')

all_patterns = list(itertools.permutations(config.avail_pegs, config.num_pegs))

output = open('output.log', 'w')

# New game
print(1)
print(1, file=output)

for turn in range(config.num_tries):

    if turn == 0:
        pat = config.avail_pegs[:config.num_pegs]
    elif turn == 1:
        pat = config.avail_pegs[-config.num_pegs:]
    else:
        pat = all_patterns[0]

    print(''.join(pat))
    print(''.join(pat), file=output)
    pos, col = None, None
    while pos is None or col is None:
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

    all_patterns = list(filter(lambda t: compare_pattern(t, pat) == (pos, col), all_patterns))
    print('solver: len = ', len(all_patterns), file=output)

    if len(all_patterns) <= 1:
        pat = all_patterns[0]
        # print(''.join(pat))
        print('q')
        print('q')
        print(5)
        # print(''.join(pat),file=output)
        print('q', file=output)
        print('q', file=output)
        print(5, file=output)
        exit()
