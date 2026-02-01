"""
Reversible Shuffle 2

Shuffles a list

>>> shuffle(list(range(8)))
[4, 2, 7, 6, 3, 5, 1, 0]

Unshuffles a list

>>> unshuffle([4, 2, 7, 6, 3, 5, 1, 0])
[0, 1, 2, 3, 4, 5, 6, 7]

"""

from math import floor, ceil
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
    def __init__(self, a, c, m):
        self.a = Mod(a, m)
        self.v = self.a.inverse()
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

    _size = 8
    _max = pow(2, _size * 8)

    def __init__(self, seed=0, skip=0):
        self.prng = LCG(
            6364136223846793005,
            1442695040888963407,
            self._max,
        )
        self.state = self.prng.next(seed, skip)

    def _next(self):
        ret = self.state
        self.state = self.prng.next(self.state)
        return sha512(ret.to_bytes(self._size)).digest()

    def _prev(self):
        self.state = self.prng.prev(self.state)
        ret = self.state
        return sha512(ret.to_bytes(self._size)).digest()

    def next_ratio(self):
        return int.from_bytes(self._next()[:self._size]) / self._max

    def prev_ratio(self):
        return int.from_bytes(self._prev()[:self._size]) / self._max

    def next_int(self, a, b):
        return a + floor(self.next_ratio() * (1 + b - a))

    def prev_int(self, a, b):
        return a + floor(self.prev_ratio() * (1 + b - a))


def forward_swaps(seed):
    def swaps(deck_size):
        random = Random(seed)
        i = deck_size
        while (i > 0):
            i -= 1
            yield [i, random.next_int(0, i)]
    return swaps

def backward_swaps(seed):
    def swaps(deck_size):
        random = Random(seed, deck_size)
        i = 0
        while (i < deck_size):
            yield [i, random.prev_int(0, i)]
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
