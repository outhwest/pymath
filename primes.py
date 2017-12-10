from math import gcd
from array import array
from collections import defaultdict

def sieve(psSoFar, toCheck):
    while len(toCheck) > 0:
        prime = toCheck[0]
        multiples = []
        for odd in toCheck:
            multiple = prime * odd
            if multiple <= toCheck[-1]:
                multiples.append(multiple)
            else:
                break
        psSoFar.append(prime)
##            print("Added %d. Multiples is: %s" % (prime, multiples)) 
        toCheck = [i for i in toCheck[1:] if i not in multiples]
##            print("Odds is length-%d: %s" % (len(odds),odds))
##            if prime % 100 == 1:
##                print(prime)
    return psSoFar

class PrimeGenerator:
    __slots__ = ['primes', 'n']
    def __init__(self, n=100):
        if not isinstance(n,int):
            #Let any type errors come through
            n = int(n)
        self.n = n
        if self.n % 2 == 1:
            self.n += 1
        #Sieve of Eratosthenes, starting with just odds
        odds = range(3,self.n,2)
        #print("odds created")
        if self.n >= 2:
            self.primes = array('L', [2])
        else:
            self.primes = array('L')

        self.primes = sieve(self.primes, odds)


    def newN(self, n):
        if not isinstance(n,int):
            #Let any type errors come through
            n = int(n)
        if n < self.n:
            raise TypeError("You may only increase the bank of primes.\n\t\tFor decreasing, use slicing")

        toCheck = range(self.n + 1, n, 2)
        for p in self.primes:
            toCheck = [i for i in toCheck if i % p != 0]

        #now toCheck serves as odds in the initial sieve
        self.primes = sieve(self.primes, toCheck)
        

        self.n = n
        if self.n % 2 == 1:
            self.n += 1

    def primesUpTo(self, n):
        if not isinstance(n,int):
            #Let any type errors come through
            n = int(n)
        
        if n > self.n:
            self.newN(n)
        if n % 2 == 1:
            n += 1
        for p in self.primes:
            if p < n:
                yield p

def isqrt(n):
    prev = 0
    cur = n
    while (cur - prev) not in (0,1):
        prev = cur
        cur = ( cur + ( n // cur ) ) // 2
    return cur

class Factorizer:
    __slots__ = ["n", "factorDict", "pg"]
    
    def __init__(self, n, pg=None):
        if not isinstance(n, int):
            #Let any type errors come through
            n = int(n)
        n = abs(n)
        maxP = isqrt(n)
        if not pg:
            pg = PrimeGenerator(maxP+1)
        if not isinstance(pg, PrimeGenerator):
            raise TypeError("pg must be a PrimeGenerator or None")
        self.n = n
        self.pg = pg
        self.factorDict = defaultdict(lambda:0)
        
        pIter = pg.primesUpTo(maxP+1)
        while n > 1:
            try:
                divisor = p = next(pIter)
            except StopIteration:
                self.factorDict[n] += 1
                break
##            print(p,n)
            while n % divisor == 0:
                self.factorDict[p] += 1
                divisor *= p
            n //= (divisor // p)
            

    def primes(self):
        return dict(self.factorDict)

    def divisors(self, sort=False):
        divs = [1]
        for p, times in self.factorDict.items():
            pMults = []
            for i in range(times):
##                print(p,times, i, p**i)
                power = p**(i+1)
                for div in divs:
##                    print(div, power*div)
                    pMults.append(power*div)
            divs.extend(pMults)

        if sort:
            return sorted(divs)
        return divs

    def __str__(self):
        if len(self.factorDict) == 0:
            return "1"
        retList = ["%d = " % self.n]
        for p, power in self.factorDict.items():
            if power > 1:
               retList.append("(%d^%d)" % (p, power))
            else:
               retList.append(str(p))
            retList.append("*")
        return ''.join(retList[:-1])
  
def factor(n, pg=None):
    if not isinstance(n, int):
        #Let any type errors come through
        n = int(n)

    maxP = isqrt(n)
    if not pg:
        pg = PrimeGenerator(maxP+1)
    if not isinstance(pg, PrimeGenerator):
        raise TypeError("pg must be a PrimeGenerator or None")

    factorDict = defaultdict(lambda:0)

##    for p in pg.primesUpTo(maxP):
##        divisor = p
##        while n % divisor == 0:
##            factorDict[p] += 1
##            divisor *= p

    pIter = pg.primesUpTo(maxP+1)
    while n > 1:
        divisor = p = next(pIter)
        while n % divisor == 0:
            factorDict[p] += 1
            divisor *= p
        n //= (divisor // p)
    
    return dict(factorDict)

def lcm(a, b):
    return a * b // gcd(a,b)
