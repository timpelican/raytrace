from __future__ import print_function
from aloe import step, world
from Matrix import Matrix, IdentityMatrix
from maths import equals
from Tuple4 import Tuple4


@step(r'the following (\d+)x(\d+) matrix (\S+):')
def _m_is_a_matrix(self, rows, cols, name):
    setattr(world, name, Matrix(self.table))


@step(r'(\S+)\[(\d+),\s*(\d+)\]\s*=\s*([-+]?\d*\.?\d+)')
def _check_matrix_element(self, name, row, col, value):
    print("\n" + name + '[' + str(row) + '][' + str(col) + ']')
    print("-----")
    print("\nExpected:")
    print(value)
    print("\nGot:")
    print(getattr(world, name)[int(row)][int(col)])
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


@step(r'([A-Za-z0-9]+)\s*\*\s*identity_matrix\s*=\s*([A-Za-z0-9]+)')
def _matrix_times_identity(self, name1, name2):
    id = IdentityMatrix(getattr(world, name1).rows)
    print("identity_matrix is:")
    print(str(id))
    print("\nExpected:")
    print(str(getattr(world, name2)))
    print("\nGot:")
    print(str(getattr(world, name2) * id))
    assert getattr(world, name1) * id == getattr(world, name2)


@step(r'identity_matrix\s*\*\s*([A-Za-z0-9]+)\s*=\s*([A-Za-z0-9]+)')
def _identity_times_tuple(self, name1, name2):
    id = IdentityMatrix(4)
    print("identity_matrix is:")
    print(str(id))
    print("\nExpected:")
    print(str(getattr(world, name2)))
    print("\nGot:")
    print(str(id * getattr(world, name2)))
    assert id * getattr(world, name1) == getattr(world, name2)


@step(r'transpose\(([A-Za-z][A-Za-z0-9]*)\) is the following (\d+)x(\d+)'
      r' matrix:')
def _transpose_matrix(self, name, rows, cols):
    test_matrix = Matrix(self.table)
    print("Expected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name).transpose())
    assert getattr(world, name).transpose() == test_matrix


@step(r'([A-Za-z][A-Za-z0-9]*) <- transpose\(identity_matrix\)')
def _create_transpose_identity_matrix(self, name):
    setattr(world, name, IdentityMatrix(4))


@step(r'[^a-z0-9\.]([A-Za-z][A-Za-z0-9]*) is the identity_matrix')
def _check_identity_matrix(self, name):
    id = IdentityMatrix(getattr(world, name).rows)
    print("Expected:")
    print(id)
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) == id


@step(r'determinant\(([A-Za-z][A-Za-z0-9]*)\)\s*=\s*([-+]?\d*\.?\d+)')
def _check_determinant(self, name, determinant):
    print("\ndeterminant(" + name + ")")
    print("-----")
    print("\nExpected:")
    print(float(determinant))
    print("\nGot:")
    print(getattr(world, name).determinant())
    assert equals(getattr(world, name).determinant(), float(determinant))


@step(r'submatrix\(([A-Za-z][A-Za-z0-9]*)\s*,\s*(\d+)\s*,\s*(\d+)\) is the '
      r'following (\d+)x(\d+) matrix:')
def _check_submatrix(self, name, subrow, subcol, rows, cols):
    test_matrix = Matrix(self.table)
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name).submatrix(int(subrow), int(subcol)))
    assert getattr(world, name).submatrix(int(subrow), int(subcol)) ==\
        test_matrix


@step(r'([A-Za-z][A-Za-z0-9]*) <- submatrix\(([A-Za-z][A-Za-z0-9]*)\s*,\s*'
      r'(\d+)\s*,\s*(\d+)\)')
def _get_submatrix(self, name1, name2, subrow, subcol):
    setattr(world, name1,
            getattr(world, name2).submatrix(int(subrow), int(subcol)))


@step(r'minor\(([A-Za-z][A-Za-z0-9]*)\s*,\s*(\d+)\s*,\s*(\d+)\)\s*=\s*'
      r'([-+]?\d*\.?\d+)')
def _check_minor(self, name, row, col, minor):
    print("\nExpected:")
    print(float(minor))
    print("\nGot:")
    print(getattr(world, name).minor(int(row), int(col)))
    assert equals(getattr(world, name).minor(int(row), int(col)),
                  float(minor))


@step(r'cofactor\(([A-Za-z][A-Za-z0-9]*)\s*,\s*(\d+)\s*,\s*(\d+)\)\s*=\s*'
      r'([-+]?\d*\.?\d+)')
def _check_cofactor(self, name, row, col, cofactor):
    print("\ncofactor(" + name + ", " + row + ", " + col + ")")
    print("-----")
    print("\nExpected:")
    print(float(cofactor))
    print("\nGot:")
    print(getattr(world, name).cofactor(int(row), int(col)))
    assert equals(getattr(world, name).cofactor(int(row), int(col)),
                  float(cofactor))


@step(r'([A-Za-z][A-Za-z0-9]*) is (not)?\s?invertible')
def _check_invertible(self, name, isnot):
    if isnot == "not":
        assert not getattr(world, name).isInvertible()
    else:
        assert getattr(world, name).isInvertible()


@step(r'([A-Za-z][A-Za-z0-9]*) <- inverse\(([A-Za-z][A-Za-z0-9]*)\)')
def _get_inverse(self, name1, name2):
    setattr(world, name1, getattr(world, name2).inverse())


@step(r'matrix ([A-Za-z][A-Za-z0-9]*) is the following (\d+)x(\d+) matrix:')
def _matrix_is_the_following(self, name, rows, cols):
    test_matrix = Matrix(self.table)
    print("\nMatrix " + name)
    print("-----")
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(getattr(world, name))
    assert getattr(world, name) == test_matrix


@step(r'inverse\(([A-Za-z][A-Za-z0-9]*)\) is the following (\d+)x(\d+)'
      r' matrix:')
def _inverse_matrix_is_the_following(self, name, rows, cols):
    test_matrix = Matrix(self.table)
    inv = getattr(world, name).inverse()
    print("\ninverse(" + name + ")")
    print("-----")
    print("\nExpected:")
    print(test_matrix)
    print("\nGot:")
    print(inv)
    assert inv == test_matrix


@step(r'([A-Za-z][A-Za-z0-9]*) <- ([A-Za-z][A-Za-z0-9]*)\s*\*\s*'
      r'([A-Za-z][A-Za-z0-9]*)')
def _mutiply_matrices(self, name1, name2, name3):
    setattr(world, name1, getattr(world, name2) * getattr(world, name3))


@step(r'([A-Za-z][A-Za-z0-9]*)\s*\*\s*inverse\(([A-Za-z][A-Za-z0-9]*)\)'
      r'\s*=\s*([A-Za-z][A-Za-z0-9]*)')
def _multiply_inverse_matrix(self, name1, name2, name3):
    inv = getattr(world, name2).inverse()
    print("\n" + name1 + " * inverse(" + name2 + ")")
    print("-----")
    print("\nExpected:")
    print(getattr(world, name3))
    print("\nGot:")
    print(getattr(world, name1) * inv)
    assert getattr(world, name1) * inv == getattr(world, name3)


@step(r'([A-Za-z][A-Za-z0-9]*) <- chain3 ([A-Za-z][A-Za-z0-9]*)\s*\*\s*'
      r'([A-Za-z][A-Za-z0-9]*)\s*\*\s*([A-Za-z][A-Za-z0-9]*)')
def _mutiply_matrices_chain3(self, name1, name2, name3, name4):
    setattr(world, name1, getattr(world, name2) * getattr(world, name3)
            * getattr(world, name4))
