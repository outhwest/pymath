from rational import MyRational
from primes import Factorizer, lcm
import functools

class MyVector():
    __slots__ = ["dim","type", "_list"]

    def __init__(self, iterable=None, myType=None):
        self._list = list(iterable)
        self.dim = len(self._list)
        if self.dim > 0:
            if myType:
                self.type = myType
            else:
                self.type = type(self._list[0])
            for item in self._list:
                if not isinstance(item, self.type):
                    raise TypeError("All items must be of type %s" % self.type)
        else:
            self.type = myType

    def __repr__(self):
        retList = ["MyVector(["]
        for item in self._list:
            retList.append(repr(item))
            retList.append(', ')
        retList[-1] = '])'
        return ''.join(retList)

    def __str__(self):
        retList = ["%d-length v(["]
        for item in self._list:
            retList.append(str(item))
            retList.append(', ')
        retList[-1] = '] of type %s)'
        return ''.join(retList) % (self.dim, self.type)

    def __len__(self):
        return self.dim

    def __add__(self, other):
        if not isinstance(other, MyVector):
            raise TypeError("Other type was %s but should be a MyVector" % type(other))

        if self.dim != other.dim:
            raise TypeError("Both vectors should be of same length")

        return type(self)([self._list[i] + other._list[i] for i in range(self.dim)])

    __radd__ = __add__

    def scale(self, scalar):
        for i in range(self.dim):
            self._list[i] *= scalar
        self.type = type(self._list[0])
        return self

    def __mul__(self, other):
        if isinstance(other, (int, MyRational)):
            insides = [other * component for component in self._list]
            return type(self)(insides)
        return NotImplemented

    def __matmul__(self,other):
        if isinstance(other, MyVector):
            if self.dim != other.dim:
                raise TypeError("Both vectors should be of same length")
            return sum(s * o for (s,o) in zip(self._list, other._list))
        return NotImplemented
    __rmul__ = __mul__
    __rmatmul__ = __matmul__

    def __getitem__(self, key):
        if isinstance(key, slice):
            sliceRange = range(key.start or 0, key.stop or self.dim, key.step or 1)
            return type(self)(self._list[i] for i in sliceRange)
        return self._list[key]



class MyPolynomial(MyVector):

    def __repr__(self):
        retList = ["MyPolynomial(["]
        for item in self._list:
            retList.append(repr(item))
            retList.append(', ')
        retList[-1] = '])'
        return ''.join(retList)

    def __str__(self):
        retList = ["( "]
        for i in range(self.dim):
            if self._list[i] != 0:
                retList.append(str(self._list[i]))
                if i == 1:
                    retList.append("x")
                if i > 1:
                    retList.append("x^%d" % i)
                retList.append(" + ")
        retList[-1] = ' )'
        if len(retList) == 1:
            return '(0)'
        return ''.join(retList)

    def _leftShift(self):
        if self.dim > 0:
            self._list.pop(0)
        self.dim -= 1
        return self
    
    def derivative(self):
        return MyPolynomial([i*item for (i, item) in enumerate(self._list)])._leftShift()
        
    def evaluate(self, x=0, verbose=False):
        if x==0:
            return self._list[0]
        total = 0
        xn = 1
        for i, coeff in enumerate(self._list):
            
            if i==0:
                additional = coeff
            else:
                xn *= x
                additional = xn*coeff
                
            if verbose:
                workList = [MyRational(0)]*self.dim
                workList[i] = MyRational(coeff)
                print(i, MyPolynomial(workList), "evaluates to", additional)

            total += additional
            
        return total

    def ratRoots(self, pg=None):
        roots = []
        an = 0
        for a in self._list[::-1]:
            if a != 0:
                an = a
                break
        if not an:
##            print("Empty Polynomial")
            return []
        #Scale into an integer-coefficient polynomial
        if self.type == MyRational:
            dens = [a.fraction[1] for a in self._list]
##            print([den for den in dens if den != 1])
            scale = functools.reduce(lcm, dens)
            a0 = self._list[0] * scale
            an *= scale
##            print("Scaled by", scale)
        else:
            a0 = self._list[0]
        #print(a0,an)    
        #build candidates list with Rational Root Theorem (Naive)
        f0 = Factorizer(a0, pg)
        fn = Factorizer(an, pg)
        #print(f0,fn)
        div0 = f0.divisors()
        divn = fn.divisors()
##        print(div0,divn)
        candidates = [MyRational(d0,dn, False, True) for d0 in div0 for dn in divn]
        negs = [-1*c for c in candidates]
        candidates.extend(negs)
        if a0 == 0:
            candidates.append(0)
        #test candidates
        for c in candidates:
##            print(c)
            if self.evaluate(c) == 0:
##                print("\tWorks")
                roots.append(c)
        return roots

