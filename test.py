from random import randint
from rational import MyRational, contFracToRat
from vector import MyVector, MyPolynomial
from matrix import ListMatrix
from fractions import Fraction

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

if __name__ == "__main__":
    i = randr()
    p = randp(pSkip=10)
    print(p,"where x=",i)
    print(p.evaluate(i, True))
    truths = []
    for j in range(100):
        r = randr()
        cf = r.toContFrac()
        r2 = contFracToRat(cf)
        truth = (r==r2)
        truths.append(truth)
        if not truth:
            print("\n\nUh oh, r=%s, r2=%s, cf=%s:\n" % (r,r2,cf))
            r.toContFrac(verbose=True)
            contFracToRat(cf, True)
    print("Does i = its own continued fraction in 100 tries:", sum(truths))
    
