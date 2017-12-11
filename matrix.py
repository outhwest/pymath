from rational import MyRational
from array import array
from oputils import sliceToRange

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
            if mrows==0 or ncols==0:
                mrows, ncols = (0,0)
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
                retList.append(str(self._list[i*self.dim[1] + j]) + '\t')
            retList.append('\n')
        return ' '.join(retList)
    
    def __repr__(self):
        if self.dim[0] == 0:
            return "ListMatrix(0 by 0): []"
        else:
            retList = ["ListMatrix(%d by %d): ["]
            for item in self._list:
                retList.append(str(item))
                retList.append(',')
            retList[-1] = ']'
            return ''.join(retList) % tuple(self.dim)

    def __len__(self):
        return self.dim[0] * self.dim[1]

    def scale(self, scalar, inPlace=False):
        if inPlace and isinstance(scalar, int):
            for i in range(self.__len__):
                self._list[i].scale(scalar)
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

    def rows(self):
        for i in range(0, self.__len__(), self.dim[1]):
            yield self._list[i:i + self.dim[1]]

    def cols(self):
        for i in range(0, self.dim[1]):
            curCol = []
            for j in range(self.dim[0]):
                curCol.append(self._list[i+j*self.dim[1]])
            yield curCol

    def diagonalIter(self):
        for i in range(0, self.__len__(), self.dim[1] + 1):
            yield self._list[i]

    def __add__(self, other):
        if not isinstance(other, ListMatrix):
            return NotImplemented
        if self.dim[0] != other.dim[0] or self.dim[1] != other.dim[1]:
            raise TypeError("Dimensions must match for matrix addition")
        
        newList = [self._list[i] + other._list[i] for i in range(self.__len__())]
        newMat = ListMatrix(None, self.dim[0], self.dim[1])
        newMat._list = newList
        return newMat
    __radd__ = __add__

    def __iadd__(self, other):
        if not isinstance(other, ListMatrix):
            return NotImplemented
        if self.dim[0] != other.dim[0] or self.dim[1] != other.dim[1]:
            raise TypeError("Dimensions must match for matrix addition")
        for i in range(self.__len__()):
            self._list[i] += other._list[i]
        return self

    def __sub__(self, other):
        if not isinstance(other, ListMatrix):
            return NotImplemented
        return self.__add__(-1*other)

    def __isub__(self, other):
        if not isinstance(other, ListMatrix):
            return NotImplemented
        if self.dim[0] != other.dim[0] or self.dim[1] != other.dim[1]:
            raise TypeError("Dimensions must match for matrix addition")
        for i in range(self.__len__()):
            self._list[i] -= other._list[i]

        return self

    def __matmul__(self,other):
        if not isinstance(other, ListMatrix):
            return NotImplemented

        size = self.dim[1]
        if size != other.dim[0]:
            raise TypeError("Dimensions must match properly")
        
        matList = []
        for srow in self.rows():
            for ocol in other.cols():
                matList.append(sum([srow[i]*ocol[i] for i in range(size)]))

        mat = ListMatrix()
        mat.dim = array('L', (self.dim[0], other.dim[1]))
        mat._list = matList

        return mat

    def __imatmul__(self, other):
        if not isinstance(other, ListMatrix):
            return NotImplemented

        size = self.dim[1]
        if size != other.dim[0]:
            raise TypeError("Dimensions must match properly")
        
        matList = []
        for srow in self.rows():
            for ocol in other.cols():
                matList.append(sum([srow[i]*ocol[i] for i in range(size)]))

        self.dim = array('L', (self.dim[0], other.dim[1]))
        self._list = matList

        return self
        

    def __getitem__(self, a):
        # if given M[i] then user wants the i-th row as a list
        if isinstance(a, int):
            if a >= self.dim[0]:
                raise IndexError("Matrix has %d rows, so cannot return %d-th row" % (self.dim[0], a-1))
            rowIter = self.rows()
            for i in range(a):
                next(rowIter)
            return next(rowIter)
        # M[start:stop:step] should give a matrix with rows from self
        #  satisfying the corresponding range object NOT EFFICIENTLY
        if isinstance(a, slice):
            # stop = None means all the rows, where the number of them is dim[0]
            r = sliceToRange(a, self.dim[0])
##            print("%s converted to %s" % (a,r))
            matList = []
            # Ugly from an optimization perspective
            rowList = list(self.rows())
            for i in r:
                matList.append(rowList[i])
            return ListMatrix(matList)

        if isinstance(a, tuple):
            if len(a) > 2:
                raise IndexError("You seem to be indexing a 2D matrix with %d indices." % len(a))
            a,b = a
            if a == None:
                a = slice(None)
            if isinstance(a, int) and isinstance(b, int):
                return self._list[a*self.dim[1] + b]
            
            if isinstance(a, int) and isinstance(b, slice):
                if a >= self.dim[0]:
                    raise IndexError("Matrix has %d rows, so cannot return %d-th row" % (self.dim[0], a-1))
                rowIter = self.rows()
                for i in range(a):
                    next(rowIter)
                row = next(rowIter)
                return row[b]
            
            if isinstance(a, slice) and isinstance(b, int):
                if b >= self.dim[1]:
                    raise IndexError("Matrix has %d columns, so cannot return %d-th column" % (self.dim[1], b-1))
                colIter = self.cols()
                for i in range(b):
                    next(colIter)
                col = next(colIter)
                return col[a]
            
            if isinstance(a, slice) and isinstance(b, slice):
                matList = []
                rowIter = self.rows()
                row = None
                ra = sliceToRange(a, self.dim[0])
                for i in range(self.dim[0]):
                    row = next(rowIter)
                    if i in ra:
                        matList.append(row[b])
                return ListMatrix(matList)

    def transpose(self):
        return ListMatrix(self.cols())

    def __eq__(self, other):
        if not isinstance(other, ListMatrix):
            return False
        sameDim = (self.dim == other.dim)
        sameEntries = (self._list == other._list)

        return sameDim and sameEntries

    def rationalize(self):
        for i in range(self.__len__()):
            self._list[i] = MyRational(self._list[i])
        return self
        
    def __pow__(self, other):
        if not self.isSquare():
            raise TypeError("This is not a square matrix")
        if (not isinstance(other, int)) or other < 0:
            raise TypeError("Power must be a positive integer")
        if other == 0:
            return ListMatrix(None, n, n)

        #Now other is a positive integer
        mat = ListMatrix(self)
        for i in range(1,other):
            mat @= self

        return mat

    def princSub(self,row,col):
        matList = [self._list[i*self.dim[1] + j]
                   for i in range(self.dim[0])
                   for j in range(self.dim[1])
                   if (i != row and j != col)]

        mat = ListMatrix()
        mat.dim = array('L', (self.dim[0]-1, self.dim[1] - 1))
        mat._list = matList

        return mat

    def isSquare(self):
        return self.dim[0] == self.dim[1]

    def determinant(self):
##        print("Evaluating:\n%s" % self)
        if not self.isSquare():
            raise TypeError("This is not a square matrix.")
        if self.dim[0] == 2:
            (a,b,c,d) = self._list
            return a*d - b*c
        total = 0
        odd = False

        #decide to go row-wise or column-wise based on number of zeros
        row = self._list[:self.dim[1]]
        col = self.__getitem__((slice(None), 0))
        row0 = sum(1 for entry in row if entry == 0)
        col0 = sum(1 for entry in col if entry == 0)

        if row0 < col0:
            for i in range(self.dim[1]):
                if self._list[i] != 0:
                    cofactor = self.princSub(0,i).determinant()
                    if odd:
                        cofactor *= -1
                    total += self._list[i] * cofactor
                odd ^= True
        else:
            for j in range(self.dim[0]):
                if col[j] != 0:
                    sub = self.princSub(j,0)
                    cofactor = sub.determinant()
##                    print(sub,cofactor)
                    if odd:
                        cofactor *= -1
                    total += col[j] * cofactor
                odd ^= True
        return total

    def wolframPrint(self):
        retList = ["{"]
        for row in self.rows():
            retList.append("{")
            for entry in row:
                retList.append(str(entry))
                retList.append(',')
            retList[-1] = "}"
            retList.append(",")
        retList[-1] = "}"
        return ''.join(retList)
    
def eyesn(n):
    return ListMatrix(None, n, n)

def constMat(c, m, n=None):
    if not isinstance(n, int):
        n = m
    if not isinstance(m, int) or n < 1 or m < 1:
        raise TypeError("Number of columns and rows must be integers > 0")
    mat = ListMatrix()
    mat.dim = array('L', (m,n))

    if isinstance(c, (int, float)):
        mat._list = [c]*(m*n)
    elif isinstance(c, MyRational):
        mat._list = [MyRational(c) for i in range(m*n)]

    return mat

def zeros(m, n=None):
    return constMat(0, m, n)

zeroes = zeros

def ones(m, n=None):
    return constMat(1, m, n)

def toeplitz(row, col=None):
    rowLen = len(row)
    newMat = ListMatrix(None, rowLen, rowLen)
    if col:
        assert rowLen == len(col)
        assert row[0] == col[0]
    else:
        col = row
    pass
