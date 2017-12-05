from random import randint
from rational import MyRational
from vector import MyVector, MyPolynomial
from matrix import ListMatrix
from fractions import Fraction

def randr(bound = 1000):
    return MyRational(randint(-1 * bound, bound), randint(1, bound)).reduced()

def randp(a=5, b=100, bound = 1000, pSkip = 3):
    return MyPolynomial(randr(bound) if not randint(0,pSkip) else MyRational(0) for i in range(randint(a,b)))

if __name__ == "__main__":
    i = randr()
    p = randp(pSkip=10)
    print(p,"where x=",i)
    print(p.evaluate(i, True))
