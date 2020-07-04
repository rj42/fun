#!/usr/bin/env python3
import heapq
import sys
import time
from functools import reduce # don't use numpy due to integer overflow
from itertools import combinations_with_replacement

BASE_NUMBERS = [
    '237',
    '357'
]

RECORD = str(277_777_788_888_899)

# -- Helpers - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - - -

def _self_product(number):
    return reduce((lambda x, y: x * y), map(int, number))

def _get_age_of_number(number, age):
    #print(age, number)
    if number < 10:
        return age

    number = str(number) # I'm tooo lazy
    next_gen = _self_product(number)
    return _get_age_of_number(next_gen, age + 1)

def get_age_of_number(number):
    #print(0, number)
    next_gen = _self_product(number)
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
    MAX_DIGIT_COUNT = 1500
    REPORT_TIMEOUT = 300 # 5 minutes

    def add_candidate(num, age):
        num = int(''.join(num))
        if len(OLDEST_NUMBERS) < TOP_SIZE:
            heapq.heappush(OLDEST_NUMBERS, (age, -num))
        else:
            heapq.heappushpop(OLDEST_NUMBERS, (age, -num))

    def report(i, elapsed):
        print('=' * 20, f'Step={i} Elapsed: {elapsed:.2f}', '=' * 20)
        for i, (age, num) in enumerate(sorted(OLDEST_NUMBERS, key=lambda x:(-x[0], -x[1]))):
            print(f'{i+1}:age={age} num={-num}')
        print('=' * 60)


    start_time = time.time()
    reported_time = start_time
    for i in range(1, MAX_DIGIT_COUNT + 1):
        now = time.time()
        elapsed = now - start_time
        if i % 10 == 0:
            print(f'Processed: {i} digits. Elapseds: {elapsed:.2f}s', file=sys.stderr)

        if i % 100 == 0 or now - reported_time >= REPORT_TIMEOUT:
            report(i, elapsed)
            reported_time = now

        for num in generate_possible_numbers(i):
            num = collapse_number(num)
            age = get_age_of_number(num)
            add_candidate(num, age)

    report(i)

if __name__ == '__main__':
    main()
