from aloe import step, world
from Matrix import Matrix
from maths import equals
from Tuple4 import Tuple4


@step(r'the following (\d+)x(\d+) matrix (\S+):')
def _m_is_a_matrix(self, rows, cols, name):
    setattr(world, name, Matrix(self.table))


@step(r'(\S+)\[(\d+),\s*(\d+)\]\s*=\s*([-+]?\d*\.?\d+)')
def _check_matrix_element(self, name, row, col, value):
    assert equals(getattr(world, name)[int(row)][int(col)], float(value))


@step(r'matrix ([A-Za-z0-9]+)\s*=\s*matrix ([A-Za-z0-9]+)')
def _matrix_equal(self, name1, name2):
    assert getattr(world, name1) == getattr(world, name2)


@step(r'matrix ([A-Za-z0-9]+)\s*!=\s*matrix ([A-Za-z0-9]+)')
def _matrix_not_equal(self, name1, name2):
    assert getattr(world, name1) != getattr(world, name2)


@step(r'([A-Za-z0-9]+)\s*\*\s*([A-Za-z0-9]+) is the following '
      r'(\d+)x(\d+) matrix:')
def _matrix_multiplication(self, name1, name2, rows, cols):
    test_matrix = Matrix(self.table)
    assert getattr(world, name1) * getattr(world, name2) == test_matrix


@step(r'([A-Za-z0-9]+)\s*\*\s*([A-Za-z0-9]+)\s*=\s*tuple\('
      r'([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)'
      r'\s*,\s*([-+]?\d*\.?\d+)\)')
def _matrix_mutiplied_by_tuple(self, name1, name2, x, y, z, w):
    test_tuple = Tuple4(float(x), float(y), float(z), float(w))
    assert getattr(world, name1) * getattr(world, name2) == test_tuple
