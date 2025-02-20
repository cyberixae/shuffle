"""
Reversible Shuffle

Shuffles a list

>>> shuffle(list(range(8)))
[4, 1, 5, 2, 0, 3, 7, 6]

Unshuffles a list

>>> unshuffle([4, 1, 5, 2, 0, 3, 7, 6])
[0, 1, 2, 3, 4, 5, 6, 7]

Gives different shufflings based on seed

>>> show(shuffle(list('ELVIS'), 0x0_faded_ace))
'LIVES'
>>> show(shuffle(list('ELVIS'), 0x0_ace_added))
'ILVES'

Unshuffles seeded shuffles

>>> show(unshuffle(list('LIVES'), 0x0_faded_ace))
'ELVIS'
>>> show(unshuffle(list('ILVES'), 0x0_ace_added))
'ELVIS'

"""

from collections import deque
from itertools import islice
from random import Random

def forward_swaps(seed):
    random = Random(seed)
    def swaps(deck_size):
        i = deck_size
        while (i > 0):
            i -= 1
            yield [i, random.randint(0, i)]
    return swaps

def backward_swaps(seed):
    fw_swaps = forward_swaps(seed)
    def swaps(deck_size):
        buffer = deque()
        for swap in fw_swaps(deck_size):
            buffer.appendleft(swap)
        yield from buffer
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
