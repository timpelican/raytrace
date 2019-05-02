# Matrix operations
from maths import equals
from Tuple4 import Tuple4


class Matrix(object):
    def __init__(self, data_in):
        self.rows = len(data_in)
        self.cols = len(data_in[0])
        self.data = []
        for y in range(0, self.rows):
            self.data.append([])
            for x in range(0, self.cols):
                self.data[y].append(float(data_in[y][x]))

    def __getitem__(self, index):
        return self.data[index]

    def __eq__(self, other):
        if self.rows == other.rows and self.cols == other.cols:
            for r in range(0, self.rows):
                for c in range(0, self.cols):
                    if not equals(self[r][c], other[r][c]):
                        return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not(self == other)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise MatrixError('A.columns must equal B.rows to '
                                  'multiply matrices.')
            data = []
            for r in range(0, self.rows):
                data.append([])
                for c in range(0, other.cols):
                    total = 0
                    for m in range(0, self.cols):
                        total += (self[r][m] * other[m][c])
                    data[r].append(total)
            return Matrix(data)
        elif isinstance(other, Tuple4):
            m1 = Matrix([[other.x], [other.y], [other.z], [other.w]])
            m2 = self * m1
            return Tuple4(m2[0][0], m2[1][0], m2[2][0], m2[3][0])
        else:
            raise MatrixError('Cannot mutiply a matrix by a '
                              + type(other).__name__)

    def __str__(self):
        m = '[ '
        first_row = True
        for r in range(0, self.rows):
            if first_row:
                first_row = False
            else:
                m += ',\n  '
            m += '[ '
            first_col = True
            for c in range(0, self.cols):
                if first_col:
                    first_col = False
                else:
                    m += ', '
                m += str(self[r][c])
            m += ']'
        m += ' ]\n'
        return m

    def transpose(self):
        m = ZeroMatrix(self.cols, self.rows)
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                m[c][r] = self[r][c]
        return m


class MatrixError(Exception):
    def __init__(self, message):
        self.message = message


def IdentityMatrix(size):
    m = ZeroMatrix(size, size)
    for r in range(0, size):
        m[r][r] = 1
    return m


def ZeroMatrix(rows, cols):
    data = []
    for r in range(0, rows):
        data.append([])
        for c in range(0, cols):
            data[r].append(0)
    return Matrix(data)
