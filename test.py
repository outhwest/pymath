from random import randint
from rational import MyRational, contFracToRat
from vector import MyVector, MyPolynomial
from matrix import *
from fractions import Fraction
from primes import PrimeGenerator
from array import array

def randr(bound = 1000, lowerbound=None):
    if lowerbound == None:
        lowerbound = -1 * bound
    num = randint(lowerbound, bound)
    assert num >= lowerbound
    den = randint(1, bound)
    r = MyRational(num, den)
    return r.reduced()

def randp(a=5, b=100, bound = 1000, pSkip = 3):
    return MyPolynomial(randr(bound) if not randint(0,pSkip) else MyRational(0) for i in range(randint(a,b)))

def randMSqInt(a=3,b=15, maxInt=1000, pSkip = 2):
    matLen = randint(a,b)
    matList = []
    for i in range(matLen**2):
        if randint(0, pSkip):
            matList.append(0)
        else:
            matList.append(randint(1,maxInt))

    mat = ListMatrix()
    mat.dim = array('L', (matLen, matLen))
    mat._list = matList

    return mat

def randMSqRat(a=3,b=20, bound = 1000):
    matLen = randint(a,b)
    matList = []
    for i in range(matLen**2):
        matList.append(randr(bound))

    mat = ListMatrix()
    mat.dim = array('L', (matLen, matLen))
    mat._list = matList

    return mat

if __name__ == "__main__":
##    i = randr()
##    p = randp(pSkip=10)
##    print(p,"where x=",i)
##    print(p.evaluate(i, True))
##    truths = []
##    for j in range(100):
##        r = randr()
##        cf = r.toContFrac()
##        r2 = contFracToRat(cf)
##        truth = (r==r2)
##        truths.append(truth)
##        if not truth:
##            print("\n\nUh oh, r=%s, r2=%s, cf=%s:\n" % (r,r2,cf))
##            r.toContFrac(verbose=True)
##            contFracToRat(cf, True)
##    print("Does i = its own continued fraction in 100 tries:", sum(truths))
##    pg = PrimeGenerator(50000)
##    for i in range(20000):
##        p = randp(a=3, b=20, bound = 75)
##        print(i+1,":",end=' ')
##        roots = p.ratRoots(pg)
##        if len(roots) > 0 and roots != [0]:
##            print("\nPolynomial: 0 =", p)
##            for r in roots:
##                print(r, ": p(r) =", p.evaluate(r))
##
    a = ListMatrix([
        [1,2,3,4,5],
        [2,3,4,5,6],
        [9,8,7,6,5],
        [8,6,4,2,0],
        [0,3,6,9,6]])

    b = ListMatrix([
        [1,0,1,0,1],
        [0,1,0,1,0],
        [1,2,3,4,5],
        [9,8,7,6,5],
        [0,2,4,6,8]])
##    for i in range(10):
##        m = randMSqInt(maxInt=1,pSkip=1)
##        d = m.determinant()
##        if d !=0:
##            wolfram = m.wolframPrint()
##            if len(wolfram) > 190:
##                print("%d. Determinant=%d, Matrix:\n%s" % (i + 1, d, m))
##            else:
##                print("%d. Determinant=%d, Matrix: %s" % (i + 1, d, wolfram))
##        else:
##            print("%d." % (i+1))
