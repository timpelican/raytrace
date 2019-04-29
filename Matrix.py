# Matrix operations
from maths import equals


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
