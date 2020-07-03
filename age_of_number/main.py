#!/usr/bin/env python3
import numpy as np
import heapq
import sys
from itertools import combinations_with_replacement

BASE_NUMBERS = [
    '237',
    '357'
]

RECORD = str(277_777_788_888_899)
NEW_RECORD = str(277777777777777777777777778888888888888888999999999999999999999999)

# -- Helpers - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - -

def _get_age_of_number(number, age):
    #print(age, number)
    if number < 10:
        return age

    number = str(number) # I'm tooo lazy
    next_gen = np.product(list(map(int, number)))
    return _get_age_of_number(next_gen, age + 1)

def get_age_of_number(number):
    #print(0, number)
    next_gen = np.product(list(map(int, number)))
    return _get_age_of_number(next_gen, 1)

def generate_possible_numbers(len):
    for base in BASE_NUMBERS:
        yield from combinations_with_replacement(base, len)

def collapse_number(num):
    # IT'S TERRRRRRRIBLE.
    #
    num = ''.join(num)
    twos = num.count('2')
    threes = num.count('3')
    fives = num.count('5')
    sevens = num.count('7')

    # Deal with 2: 4, 8
    #
    eights = twos // 3
    twos %= 3

    fours = twos // 2
    twos %= 2

    # Deal with 3: 9
    #
    nines = threes // 2
    threes %= 2

    # Deal with 6.
    #
    if twos == threes == 1:
        sixs = 1
        twos = threes = 0
    else:
        sixs = 0

    digit_count = {
        '2': twos,
        '3': threes,
        '4': fours,
        '5': fives,
        '6': sixs,
        '7': sevens,
        '8': eights,
        '9': nines
    }

    ret = ''
    for digit, count in digit_count.items():
        ret += digit * count
    return ret


# - - Main - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def main():
    OLDEST_NUMBERS = []
    TOP_SIZE = 50
    MAX_DIGIT_COUNT = 150

    def add_candidate(num, age):
        num = int(''.join(num))
        if len(OLDEST_NUMBERS) < TOP_SIZE:
            heapq.heappush(OLDEST_NUMBERS, (age, -num))
        else:
            heapq.heappushpop(OLDEST_NUMBERS, (age, -num))

    for i in range(1, MAX_DIGIT_COUNT + 1):
        if i % 10 == 0:
            print(f'Processed: {i} digits', file=sys.stderr)
        for num in generate_possible_numbers(i):
            num = collapse_number(num)
            age = get_age_of_number(num)
            add_candidate(num, age)

    # World record.
    #add_candidate(RECORD, get_age_of_number(RECORD))

    for i, (age, num) in enumerate(sorted(OLDEST_NUMBERS, key=lambda x:(-x[0], -x[1]))):
        print(f'{i}:age={age} num={-num}')

if __name__ == '__main__':
    main()
