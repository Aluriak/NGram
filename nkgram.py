# -*- coding: utf-8 -*-
"""
NK-gram object definition.

NK-gram instances have their own orders and model,
and are able to generates random data according to the model..
"""


#########################
# IMPORTS               #
#########################
from collections import defaultdict, deque
import itertools
import random




#########################
# PRE-DECLARATIONS      #
#########################
def window(text, n):
    """
    n: integer > 0
    text: string with size >= n
    Generate: string of n-uplets of given text, sliding on the text
    """
    assert(n > 0)
    assert(len(text) >= n)
    index = n
    while index <= len(text):
        yield text[index-n:index]
        index += 1





#########################
# NKGRAM                #
#########################
class NKGram(object):
    """
    Model is described by a dict of dict as:

        (tuple(str), tuple(str)):(str:int)

    Key tuple(str), tuple(str) is the n previous and k next lexems.
    Value is the word between previous and next lexems,
     that appeared int times in learning process.

    """
# CONSTRUCTOR #################################################################
    def __init__(self, n, k=0):
        """
        """
        assert(n >= 0)
        assert(k >= 0)
        self.n, self.k = n, k
        self.model = defaultdict(lambda: defaultdict(int))
        self.counter = 0


    def learn(self, iterable):
        """Learn from given iterable

        Return self for functionnal convenience.
        """
        assert(hash(iterable))
        window_size = self.n + self.k + 1
        for slide in window(iterable, window_size):
            previous = slide[0:self.n]
            lexem    = slide[self.n]
            nexts    = slide[self.n+1:]
            # print(previous, lexem, nexts, sep='·')
            assert(isinstance(previous, tuple) and isinstance(nexts, tuple))
            self.model[previous, nexts][lexem] += 1
        return self


    def generate(self, m, previous, nexts=tuple()):
        """Generate m lexems, based on previous and nexts lexems

        if K is not equals to zero, the generation is impossible in
         linear treatment. (impossible to found the next lexem
         without knows what is the k nexts, that are not generated)
         In this case, the generation will be like a N-Gram.
        """
        prev_lexems = deque(previous, self.n)
        assert(len(prev_lexems) == self.n)
        assert(m >= len(prev_lexems))
        for lexem in prev_lexems: yield lexem
        generated_size = self.n
        while generated_size < m:
            lexem = self.random_lexem(tuple(prev_lexems), nexts)
            if lexem:
                prev_lexems.append(lexem)
                generated_size += 1
                yield lexem
            else:  # no lexem found : it's a tail-end !
                generated_size = m


    def random_lexem(self, previous, nexts):
        """
        """
        # take all candidates
        assert(isinstance(previous, tuple) and isinstance(nexts, tuple))
        candidates = tuple((k,v) for k,v in self.model[previous, nexts].items())
        if len(candidates) == 0:
            # no candidate : no random lexem : return None
            return None
        # take a random element
        counts, candidates = itertools.tee(candidates)
        threshold = random.randint(0, sum((count for _, count in counts)))
        for candidate, count in candidates:
            print('candidats:', candidate, count)
            threshold -= count
            if threshold <= 0:
                return candidate
        # it's impossible to be here
        raise NotImplementedError


    @property
    def random_lexems(self):
        """Return a tuple of two tuples of n and k lexems
        """
        return random.choice(tuple(self.model.keys()))





if __name__ == '__main__':
    text = tuple("les abribus volants sont nos amis")

    with open("filin", "r") as f:
        txt = tuple(f.read().split())
    order = 3
    g = NKGram(order).learn(txt)
    # print(g.model)
    print(' '.join(g.generate(200, g.random_lexems[0])))


