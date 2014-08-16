# -*- coding: utf-8 -*-
#########################
#       MAIN            
#########################


#########################
# IMPORTS               #
#########################
from random import randint




#########################
# PRE-DECLARATIONS      #
#########################
def getNByN(n, text):
    """
    n: integer > 0
    text: string with size >= n
    Generate: string of n-uplets of given text
    """
    assert(n > 0)
    assert(len(text) >= n)
    index = n
    while index <= len(text):
        yield text[index-n:index]
        index += 1
    return 





#########################
# CLASS                 #
#########################
class NGram(object):
    """"""
# CONSTRUCTOR #################################################################
    def __init__(self, n, text = None):
        """
        n: number used for prediction (integer > 1)
        text: string used for learning, can be None
        """
        self.n = n
        self.freqs = {}
        if text is not None: self.learn(text)
        
# PUBLIC METHODS ##############################################################
    def learn(self, text):
        """
        text: string of text
        """
        # get frequency of apparition for each n-uplet
        for uplet in getNByN(self.n, text):
            self.freqs[uplet] = 1 + self.freqs.get(uplet, 0)

        # get frequency of apparition for each (n-1) first letters in freqs table
        self.firsts_freqs = {}
        for uplet in self.freqs.keys():
            first = uplet[:-1]
            self.firsts_freqs[first] = self.freqs[uplet] + self.firsts_freqs.get(first, 0)
        # add these frequency to self table of freqs
        #self.freqs.update(firsts_freqs)

        # compute probs of apparition
        self.probs = {}
        for uplet in self.freqs.keys():
            first = uplet[:-1]
            last  = uplet[-1]
            # probability of last given first
            #self.probs[last, first] = self.freqs[uplet] / self.firsts_freqs[first]
            d = self.probs.setdefault(first, {})
            d[last] = self.freqs[uplet] / self.firsts_freqs[first]
            # NB: sum of frequencies for each key of self.probs must be equal to 1


    def generate(self, q, start = None):
        """
        q: quantity of n-uplet to generate
        Return: string of q n-uplet, according to probs
        """
        if isinstance(start, str): start = tuple(start)
        if start is None or len(start) < self.n:
            ret = self.randomAccessToUplet()[:-1]
        else:   ret = start
        for i in range(q):
            tmp = self.getRandomLetterAfter(ret[-self.n+1:])
            if tmp == "":       
                ret += self.randomAccessToUplet()[:-1]
            else:               ret += (tmp,)
            #print(str(tmp) + ">>>>" + str(ret[-self.n+1:]) + "<<<<")
            
        return ret
            


# PRIVATE METHODS #############################################################
# PREDICATS ###################################################################
# ACCESSORS ###################################################################
    def getRandomLetterAfter(self, muplet):
        """
        muplet: string of n-1 letters
        Return: a random letter, randomly choosen in possible successor of muplet, or "" if unknow muplet
        """
        assert(len(muplet) == self.n - 1)
        succs = self.probs.get(muplet, None)
        if succs is None:
            return ""
        else:
            return NGram.randomKeyInFrequencyDict(succs, 100000)


    def randomAccessToUplet(self):
        """
        Return: a random uplet in the redondant list of uplets
        """
        return NGram.randomKeyInFrequencyDict(self.freqs)
    

    @staticmethod
    def randomKeyInFrequencyDict(d, coeff = 1):
        """
        d: dict with number as values
        coeff: multiply all freqs by coeff for treatment; useful for floats freqs (default is 1)
        Return: a key of d, randomly choosen according to frequency
        """
        total_freqs = sum([freq * coeff for freq in d.values()])
        counter = randint(1, int(total_freqs))
        ret_key = None
        for key, freq in d.items():
            counter -= freq * coeff
            if counter <= 0:
                ret_key = key
                break
        return ret_key


# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################
if __name__ == "__main__":
    #with open("main.py", "r") as f:
    with open("filin", "r") as f:
        txt = tuple(f.read())
    g = NGram(12, txt)
    #print(g.freqs)
    #print(g.probs)
    print("\nGenerated text :\n")
    print("".join(g.generate(10000)))

    #with open("filin", "r") as f:
        #txt = tuple(f.read().split())
    #g = NGram(6, txt)
    #print("\nGenerated text :\n")
    #print(" ".join(g.generate(1000)))


