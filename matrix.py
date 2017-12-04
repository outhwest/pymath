from rational import MyRational
from array import array

class ListMatrix:
    __slots__ = ['dim', '_list']

    def __init__(self, init=None, mrows=0, ncols=0):
        self._list = []
        if init:
            if mrows != 0 or ncols != 0:
                raise TypeError("if init given, mrows and ncols must be default 0")

            for row in init:
                mrows += 1
                #first row determines number of columns
                rowLen = 0
                for value in row:
                    self._list.append(value)
                    rowLen += 1
                if mrows == 1:
                    ncols = rowLen
                else:
                    if ncols != rowLen:
                        raise TypeError("init should be an iterable of equal-length iterables")
        else:
            for i in range(mrows):
                for j in range(ncols):
                    if i == j:
                        self._list.append(MyRational(1))
                    else:
                        self._list.append(MyRational(0))
        
        self.dim = array('L', (mrows, ncols))

    def __str__(self):
        retList = ['']
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                retList.append(str(self._list[i*self.dim[1] + j]))
            retList.append('\n')
        return ' '.join(retList)
    
    def __repr__(self):
        retList = ["ListMatrix(%d by %d): ["]
        for item in self._list:
            retList.append(str(item))
            retList.append(',')
        retList[-1] = ']'
        return ''.join(retList) % tuple(self.dim)

    def __len__(self):
        return self.dim[0] * self.dim[1]

    def scale(self, scalar):
        for i in range(len(self)):
            self._list[i] *= scalar
        return self

    def __mul__(self, other):
        if isinstance(other, (int,MyRational)):
            newList = []
            for i in range(len(self)):
                newList.append(other * self._list[i])
            newMat = ListMatrix(None, self.dim[0], self.dim[1])
            newMat._list = newList
            return newMat
        else:
            print("other's type:", type(other))
            raise TypeError("Multiplication can only be performed with scalars")
        
    __rmul__ = __mul__
        
    def __imul__(self, other):
        if isinstance(other, (int,MyRational)):
            return self.scale(other)
        else:
            raise TypeError("Multiplication can only be performed with scalars")


def eyesn(n):
    return ListMatrix(None, n, n)
