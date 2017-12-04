from array import array
from math import gcd

class MyRational:

    __slots__ = ['fraction', 'neg']

    def __init__(self, num=1, den=1, neg=False, reduce=False):
        self.fraction = array('L', (num,den))
        self.neg = neg
        if reduce:
            self.reduced()
    
    def __str__(self):
        if self.neg:
            retStr = "(-%d/%d)"
        else:
            retStr = "(%d/%d)"
        return retStr % (self.fraction[0], self.fraction[1])

    def __repr__(self):
        return "MyRational(%d,%d,neg=%r)" % (self.fraction[0], self.fraction[1], self.neg)
        
    def __float__(self):
        return float(self.fraction[0])/self.fraction[1]

    def __int__(self):
        return int(float(self))
    
    def reduced(self, gcd=gcd):
        factor = gcd(self.fraction[0], self.fraction[1])
        self.fraction[0] //= factor
        self.fraction[1] //= factor
        return self

    def __neg__(self):
        self.neg ^= True

    def __add__(self,other):
        if not isinstance(other, MyRational):
            raise TypeError("Other argument should be of type MyRational")
        a,b = self.fraction
        c,d = other.fraction
        if self.neg:
            a *= -1
        if other.neg:
            c *= -1
        numerator = a*d + b*c
        negative = (numerator < 0)
        if negative:
            numerator *= -1
            
        #calculation (a/b) + (c/d) = (ad + bc)/bd but reduced
        return MyRational(numerator, b*d, negative, True)

    def __sub__(self, other):
        a,b = other.fraction
        return self + MyRational(a, b, True, True)
        
    def __abs__(self):
        a,b = self.fraction
        return MyRational(a,b, False)

    def __eq__(self, other):
        diff = self - other
        return diff.fraction[0] == 0

    def __lt__(self, other):
        diff = self - other
        if diff.fraction[0] == 0:
            return False
        return diff.neg

    def __le__(self, other):
        diff = self - other
        return diff.neg or diff.fraction[0] == 0
