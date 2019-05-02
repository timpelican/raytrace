Feature: Matrix operations

As a programmer
I want to work with matrices
So I can build a ray-tracer

Scenario: Constructing and inspecting a 4x4 matrix
  Given the following 4x4 matrix M:
    | 1     | 2     | 3     | 4     |
    | 5.5   | 6.5   | 7.5   | 8.5   |
    | 9     | 10    | 11    | 12    |
    | 13.5  | 14.5  | 15.5  | 16.5  |
  Then M[0, 0] = 1
  And M[0, 3] = 4
  And M[1, 0] = 5.5
  And M[1, 2] = 7.5
  And M[2, 2] = 11
  And M[3, 0] = 13.5
  And M[3, 2] = 15.5

Scenario: A 2x2 matrix should be representable
  Given the following 2x2 matrix M:
    | -3    | 5     |
    | 1     | -2    |
  Then M[0, 0] = -3
  And M[0, 1] = 5
  And M[1, 0] = 1
  And M[1, 1] = -2

Scenario: A 3x3 matrix should be representable
  Given the following 3x3 matrix M:
    | -3    | 5     | 0     |
    | 1     | -2    | -7    |
    | 0     | 1     | 1     |
  Then M[0, 0] = -3
  And M[1, 1] = -2
  And M[2, 2] = 1

Scenario: Matrix equality with identical matrices
  Given the following 4x4 matrix A:
    | 1     | 2     | 3     | 4     |
    | 5     | 6     | 7     | 8     |
    | 9     | 8     | 7     | 6     |
    | 5     | 4     | 3     | 2     |
  And the following 4x4 matrix B:
    | 1     | 2     | 3     | 4     |
    | 5     | 6     | 7     | 8     |
    | 9     | 8     | 7     | 6     |
    | 5     | 4     | 3     | 2     |
  Then matrix A = matrix B

Scenario: Matrix equality with different matrices
  Given the following 4x4 matrix A:
    | 1     | 2     | 3     | 4     |
    | 5     | 6     | 7     | 8     |
    | 9     | 8     | 7     | 6     |
    | 5     | 4     | 3     | 2     |
  And the following 4x4 matrix B:
    | 2     | 3     | 4     | 5     |
    | 6     | 7     | 8     | 9     |
    | 8     | 7     | 6     | 5     |
    | 4     | 3     | 2     | 4     |
  Then matrix A != matrix B

Scenario: Multiplying two matrices
  Given the following 4x4 matrix A:
    | 1     | 2     | 3     | 4     |
    | 5     | 6     | 7     | 8     |
    | 9     | 8     | 7     | 6     |
    | 5     | 4     | 3     | 2     |
  And the following 4x4 matrix B:
    | -2    | 1     | 2     | 3     |
    | 3     | 2     | 1     | -1    |
    | 4     | 3     | 6     | 5     |
    | 1     | 2     | 7     | 8     |
  Then A * B is the following 4x4 matrix:
    | 20    | 22    | 50    | 48    |
    | 44    | 54    | 114   | 108   |
    | 40    | 58    | 110   | 102   |
    | 16    | 26    | 46    | 42    |

Scenario: A matrix multipled by a tuple
  Given the following 4x4 matrix A:
    | 1     | 2     | 3     | 4     |
    | 2     | 4     | 4     | 2     |
    | 8     | 6     | 4     | 1     |
    | 0     | 0     | 0     | 1     |
  And b <- tuple(1, 2, 3, 1)
  Then A * b = tuple(18, 24, 33, 1)

Scenario: Multiplying a matrix by the identity matrix
  Given the following 4x4 matrix A:
    | 0     | 1     | 2     | 4     |
    | 1     | 2     | 4     | 8     |
    | 2     | 4     | 8     | 16    |
    | 4     | 8     | 16    | 32    |
  Then A * identity_matrix = A

Scenario: Multiplying the identity matrix by a tuple
  Given a <- tuple(1, 2, 3, 4)
  Then identity_matrix * a = a

Scenario: Transposing a matrix
  Given the following 4x4 matrix A:
    | 0 | 9 | 3 | 0 |
    | 9 | 8 | 0 | 8 |
    | 1 | 8 | 5 | 3 |
    | 0 | 0 | 5 | 8 |
  Then transpose(A) is the following 4x4 matrix:
    | 0 | 9 | 1 | 0 |
    | 9 | 8 | 8 | 0 |
    | 3 | 0 | 5 | 5 |
    | 0 | 8 | 3 | 8 |

Scenario: Transposing the identity matrix
  Given A <- transpose(identity_matrix)
  Then A is the identity_matrix