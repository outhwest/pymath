from array import array
from math import gcd

class MyRational:

    __slots__ = ['fraction', 'neg']

    def __init__(self, num=0, den=1, neg=False, reduce=False):

        if isinstance(num, MyRational):
            den = num.fraction[1]
            neg ^= num.neg
            num = num.fraction[0]

        if num < 0:
            num *= -1
            neg ^= True
            
        try:
            self.fraction = array('L', (num,den))
        except OverflowError:
            self.fraction = [num, den]
        self.neg = neg
        if den == 0:
            raise ZeroDivisionError("Denominator must be nonzero integer")
        if reduce:
            self.reduced()
    
    def __str__(self):
        if self.fraction[0] == 0:
            return "(0)"
        else:
            if self.neg:
                retStr = "(-%d/%d)"
            else:
                retStr = "(%d/%d)"
            return retStr % (self.fraction[0], self.fraction[1])

    def __repr__(self):
        if self.fraction[0] == 0:
            return "MyRational(0)"
        return "MyRational(%d,%d,neg=%r)" % (self.fraction[0], self.fraction[1], self.neg)
        
    def __float__(self):
        return float(self.fraction[0])/self.fraction[1]

    def __int__(self):
        return int(float(self))

    def __hash__(self):
        return hash(float(self))
    
    def reduced(self, gcd=gcd):
        if self.fraction[0] == 0:
            self.neg = False
            self.fraction[1] = 1
        else:
            factor = gcd(self.fraction[0], self.fraction[1])
            self.fraction[0] //= factor
            self.fraction[1] //= factor
        return self

    def __neg__(self):
        self.neg ^= True
        return self

    def scale(self, intScalar, reduce=False):
        if not isinstance(intScalar, int):
            raise TypeError
        try:
            self.fraction[0] *= intScalar
        except OverflowError:
            self.fraction = [self.fraction[0] * intScalar, self.fraction[1]]
        if reduce:
            self.reduced()

    def __add__(self,other):
        if not isinstance(other, MyRational):
            if isinstance(other, int):
                return self + MyRational(other)
            return NotImplemented
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
    __radd__ = __add__

    def __iadd__(self, other):
        if not isinstance(other, MyRational):
            if isinstance(other, int):
                other = MyRational(other)
            else:
                return NotImplemented
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
        try:
            self.fraction[0] = numerator
            self.fraction[1] = b*d
        except OverflowError:
            self.fraction = [numerator, b*d]
        self.neg = negative
        self.reduced()
        return self

    def __sub__(self, other):
        if not isinstance(other, (MyRational,int)):
            return NotImplemented
        if isinstance(other, int):
            other = MyRational(other)
        a,b = other.fraction
        return self + MyRational(a, b, other.neg ^ True, True)
        
    def __abs__(self):
        a,b = self.fraction
        return MyRational(a,b, False)

    def __eq__(self, other):
        if not isinstance(other, MyRational):
            if isinstance(other, int):
                return self == MyRational(other)
            return NotImplemented
        diff = self - other
        return diff.fraction[0] == 0

    def __lt__(self, other):
        if not isinstance(other, MyRational):
            if isinstance(other, int):
                return self < MyRational(other)
            return NotImplemented
        diff = self - other
        if diff.fraction[0] == 0:
            return False
        return diff.neg

    def __le__(self, other):
        if not isinstance(other, MyRational):
            if isinstance(other, int):
                return self <= MyRational(other)
            return NotImplemented
        diff = self - other
        return diff.neg or diff.fraction[0] == 0

    def __gt__(self, other):
        return not self.__le__(other)
    def __ge__(self,other):
        return not self.__lt__(other)
    
    def __mul__(self, other):
        a,b = self.fraction
        if isinstance(other, int):
            numerator = a * other
            negative = (other < 0)
            if negative:
                numerator *= -1
            negative ^= self.neg
            return MyRational(numerator, b, negative, True)
        if isinstance(other, MyRational):
            c,d = other.fraction
            numerator = a*c
            denominator = b*d
            negative = self.neg ^ other.neg
            return MyRational(numerator, denominator, negative, True)
        return NotImplemented

    __rmul__ = __mul__

    def __imul__(self, other):
        if not isinstance(other, (MyRational, int)):
            return NotImplemented
        if isinstance(other, int):
            if other < 0:
                self.__neg__()
                other *= -1
            try:
                self.fraction[0] *= other
            except OverflowError:
                self.fraction = [self.fraction[0] * other, self.fraction[1]]
            self.reduced()
            return self
        a,b = self.fraction
        c,d = other.fraction
        self.neg ^= other.neg
        a *= c
        b *= d
        try:
            self.fraction[0] = a
            self.fraction[1] = b
        except OverflowError:
            self.fraction = [a,b]

        self.reduced()
        return self

    def __truediv__(self, other):
        a,b = self.fraction
        if not isinstance(other, MyRational):
            if isinstance(other, int):
                denominator = b * other
                negative = (other < 0)
                if negative:
                    denominator *= -1
                negative ^= self.neg
                return MyRational(a, denominator, negative, True)
            return NotImplemented
        c,d = other.fraction
        numerator = a*d
        denominator = b*c
        negative = self.neg ^ other.neg
        return MyRational(numerator, denominator, negative, True)

    def __idiv__(self, other):
        if not isinstance(other, (int, MyRational)):
            return NotImplemented
        if isinstance(other, int):
            try:
                self.fraction[1] *= other
            except OverflowError:
                self.fraction = [self.fraction[0], self.fraction[1] * other]
            return self.reduced()
        return self.inverted().__imul__(other)


    def toContFrac(self, limit=1024, verbose=False, initial=True):
        if verbose: print("Finding continued fraction for:",self, end='\t')
##        a = self.fraction[0] // self.fraction[1]
##        f = self.fraction[0] %  self.fraction[1]

        num = self.fraction[0]
        if self.neg: num *= -1
        a = num // self.fraction[1]
        f = num % self.fraction[1]
        if verbose: print("Got %d with %d left over" % (a,f))
        if limit == 1 or f == 0:
            return [a]
        else:
            inverse = MyRational(self.fraction[1], f)
            return [a] + inverse.toContFrac(limit-1, verbose, False)
        

    def inverse(self):
        return MyRational(self.fraction[1],self.fraction[0], self.neg)

    def inverted(self):
        temp = self.fraction[0]
        self.fraction[0] = self.fraction[1]
        self.fraction[1] = temp
        return self

    def isInt(self):
        return (self.fraction[1] == 1)

    def isAbsLessThanOne(self):
        return (self.fraction[0] < self.fraction[1])

    def isOne(self):
        return (self.fraction[0] == self.fraction[1]) and not self.neg


def contFracToRat(contFrac, verbose=False):
    if len(contFrac) == 0:
        return MyRational(0)
    if len(contFrac) == 1:
        return MyRational(contFrac[0])
    result = MyRational(1,contFrac[-1])
    for i in contFrac[-2:0:-1]:
        result += i
        result.inverted()
        if verbose:
            print("After %d, result=%s" % (i, result))
    result += contFrac[0]
    return result 
