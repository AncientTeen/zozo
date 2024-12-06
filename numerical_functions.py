import numpy as np


def mean(arr: list[float]) -> float:
    """
    function to calculate mean
    """
    sum = 0
    for i in range(len(arr)):
        sum += arr[i]

    res = sum / len(arr)

    return res


def std(arr: list[float]) -> float:
    """
    function to calculate standard deviation
    """

    arr_mean = mean(arr)

    sum = 0
    for i in range(len(arr)):
        sum += (arr[i] - arr_mean) ** 2

    dispersion = sum / (len(arr) - 1)

    res = dispersion ** 0.5

    return res

def median(data: list[float]) -> float:
    """
    Manually compute the median of a list of numbers
    """

    sorted_data = sorted(data)

    n = len(sorted_data)

    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        mid1 = n // 2 - 1
        mid2 = n // 2
        return (sorted_data[mid1] + sorted_data[mid2]) / 2



def matrix_multiply(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """
    function to multiply two matrices
    """

    def dot_product(row, col):
        result = 0
        for a, b in zip(row, col):
            result += a * b
        return result

    return [[dot_product(A_row, B_col) for B_col in zip(*B)] for A_row in A]


def transpose(A: list[list[float]]) -> list[list[float]]:
    """
    function for matrix transpose
    """

    result = []
    for i in range(len(A[0])):
        row = []
        for j in range(len(A)):
            row.append(A[j][i])
        result.append(row)
    return result


def eig_decomposition(A: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    """
    Simple power iteration-based eigen decomposition
    """

    def power_iteration(mat, num_simulations: int = 100):
        n, m = len(mat), len(mat[0])
        vec = [1] * n

        for _ in range(num_simulations):
            new_vec = []
            for i in range(n):
                value = 0
                for j in range(m):
                    value += mat[i][j] * vec[j]
                new_vec.append(value)

            norm = 0
            for x in new_vec:
                norm += x ** 2
            norm = norm ** 0.5
            vec = [x / norm for x in new_vec]

        eigenvalue = 0
        for i in range(n):
            row_sum = 0
            for j in range(m):
                row_sum += mat[i][j] * vec[j]
            eigenvalue += vec[i] * row_sum

        return eigenvalue, vec

    n = len(A)
    eigenvalues = []
    eigenvectors = []

    for _ in range(n):
        eigval, eigvec = power_iteration(A)
        eigenvalues.append(eigval)
        eigenvectors.append(eigvec)

        for i in range(n):
            for j in range(n):
                A[i][j] -= eigval * eigvec[i] * eigvec[j]

    """"""
    eigenvalues = np.array(eigenvalues)
    """"""

    return eigenvalues, transpose(eigenvectors)


def solve_least_squares(A: list[list[float]], b: list[float]) -> list[float]:
    """
    Solve the least squares problem Ax = b using manual computation
    """

    A_T = transpose(A)

    ATA = matrix_multiply(A_T, A)

    ATb = [sum(A_T[i][j] * b[j] for j in range(len(b))) for i in range(len(A_T))]

    n = len(ATA)
    x = [0] * n

    for i in range(n):
        for j in range(i + 1, n):
            factor = ATA[j][i] / ATA[i][i]
            for k in range(i, n):
                ATA[j][k] -= factor * ATA[i][k]
            ATb[j] -= factor * ATb[i]

    for i in range(n - 1, -1, -1):
        x[i] = ATb[i]
        for j in range(i + 1, n):
            x[i] -= ATA[i][j] * x[j]
        x[i] /= ATA[i][i]

    return x


def dot_product(v1: list[float], v2: list[float]) -> float:
    """
    function to compute the dot product of two vectors
    """

    result = 0.0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result
