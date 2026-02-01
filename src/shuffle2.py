"""
Reversible Shuffle 2

Shuffles a list

>>> shuffle(list(range(8)))
[4, 2, 7, 6, 3, 5, 1, 0]

Unshuffles a list

>>> unshuffle([4, 2, 7, 6, 3, 5, 1, 0])
[0, 1, 2, 3, 4, 5, 6, 7]

>>> a = 12608590619323093763
>>> b = 13819126590027240918
>>> c = 16051947959618044397
>>> omg = LCG()
>>> assert omg.next(a) == b
>>> assert omg.prev(b) == a
>>> assert omg.next(b) == c
>>> assert omg.prev(c) == b
>>> assert omg.next(a, 2) == c
>>> assert omg.prev(c, 2) == a
>>> assert omg.next(a, 0) == a
>>> assert omg.prev(a, 0) == a
"""

from collections import deque
from itertools import islice
from math import floor, ceil
from random import Random
from hashlib import sha512

class Mod:
    def __init__(self, x, m):
        self.m = m
        self.x = x % m

    def __int__(self):
        return self.x

    def __add__(self, y):
        return Mod(self.x + y, self.m)

    def __sub__(self, y):
        return Mod(self.x - y, self.m)

    def __mul__(self, y):
        return Mod(self.x * y, self.m)

    def inverse(self):
        return Mod(pow(self.x, -1, self.m), self.m)


class LCG:
    def __init__(self, a=6364136223846793005, c=1442695040888963407, m=pow(2, 64)):
        self.a = Mod(a, m)
        self.v = Mod(a, m).inverse()
        self.c = c

    def next(self, x, i=1):
        if i < 1:
            return x
        return self.next(int((self.a * x) + self.c), i - 1)

    def prev(self, x, i=1):
        if i < 1:
            return x
        return self.prev(int(self.v * (x - self.c)), i - 1)


class Random:

    def __init__(self, seed=0, skip=0, mix=sha512, prng=LCG()):
        self.mix = mix
        self.prng = prng
        self.state = self.prng.next(seed, skip)

    def next(self):
        ret = self.mix(self.state.to_bytes(8)).digest()
        self.state = self.prng.next(self.state, 1)
        return ret

    def prev(self):
        self.state = self.prng.prev(self.state, 1)
        ret = self.mix(self.state.to_bytes(8)).digest()
        return ret

    def nextrat(self):
        return int.from_bytes(self.next()[:8]) / 2**64

    def prevrat(self):
        return int.from_bytes(self.prev()[:8]) / 2**64

    def nextint(self, a, b):
        foo = floor(a + self.nextrat() * (1 + b - a))
        return foo

    def prevint(self, a, b):
        foo = floor(a + self.prevrat() * (1 + b - a))
        return foo


def forward_swaps(seed):
    def swaps(deck_size):
        random = Random(seed)
        i = deck_size
        while (i > 0):
            i -= 1
            yield [i, random.nextint(0, i)]
    return swaps

def backward_swaps(seed):
    def swaps(deck_size):
        random = Random(seed, deck_size)
        i = 0
        while (i < deck_size):
            yield [i, random.prevint(0, i)]
            i += 1
    return swaps

def execute_swaps(deck, swaps):
    for [a, b] in swaps(len(deck)):
        deck[a], deck[b] = deck[b], deck[a]
    return deck

def shuffle(deck, seed = 0):
    return execute_swaps(deck, forward_swaps(seed))

def unshuffle(deck, seed = 0):
    return execute_swaps(deck, backward_swaps(seed))

def show(deck):
    return str().join(deck)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
