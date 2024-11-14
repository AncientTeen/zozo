import numpy as np

"""This file is used to calculate trend criteria"""

def sign_criterion(x_t: list) -> float:
    """
    sign criterion function
    :param x_t: list - time series data
    :return: tuple[float, float] - C value and normal distribution quantile
    """
    n = len(x_t)
    y = []

    for i in range(n - 1):
        if x_t[i + 1] > x_t[i]:
            y.append(1)
        else:
            y.append(0)

    c = sum(y)
    E_c = (n - 1) / 2
    D_c = (n + 1) / 12

    C = (c - E_c) / np.sqrt(D_c)

    return C


def mann_criterion(x_t: list) -> float:
    """
    mann criterion function
    :param x_t: list - time series data
    :return: float - u value
    """
    n = len(x_t)
    T_matrix = [[0 for j in range(n)] for i in range(n - 1)]
    for i in range(n):
        for j in range(i + 1, n):
            if x_t[i] > x_t[j]:
                T_matrix[i][j] = 0
            elif x_t[i] == x_t[j]:
                T_matrix[i][j] = 1 / 2
            else:
                T_matrix[i][j] = 1
    T = sum(sum(T_matrix, []))
    E_T = n * (n - 1) / 4
    D_T = n * (2 * n + 5) * (n - 1) / 72
    u = (T + 0.5 - E_T) / np.sqrt(D_T)

    return u

def series_criterion(x_t: list) -> tuple[int, int]:
    """
    series criterion function
    :param x_t: list - time series data
    :return: tuple[int, int] - v and u values
    """
    n = len(x_t)
    median = np.median(x_t)

    """"""
    y = [1 if x_t[i] >= median else -1 for i in range(n)]

    series_count = 1
    max_series_length = 1
    current_series_length = 1

    for i in range(1, n):
        if y[i] == y[i - 1]:
            current_series_length += 1
        else:
            # End of the current series
            series_count += 1
            max_series_length = max(max_series_length, current_series_length)
            current_series_length = 1  # Reset for the new series

    # Final check for the last series
    max_series_length = max(max_series_length, current_series_length)

    v = series_count
    d = max_series_length

    return v, d


def rise_n_fall_criterion(x_t: list) -> tuple[int, int]:
    """
     "rising" and "falling" series criterion function
     :param x_t: list - time series data
     :return: tuple[int, int] - v and u values
     """
    n = len(x_t)
    y = [1 if (x_t[i + 1] - x_t[i]) >= 0 else -1 for i in range(n - 1)]

    series_count = 1
    max_series_length = 1
    current_series_length = 1

    for i in range(1, n - 1):
        if y[i] == y[i - 1]:
            current_series_length += 1
        else:
            series_count += 1
            max_series_length = max(max_series_length, current_series_length)
            current_series_length = 1

    max_series_length = max(max_series_length, current_series_length)

    v = series_count
    d = max_series_length

    return v, d


def abbe_criterion(x_t: list) -> float:
    """
    abbe criterion function
    :param x_t: list - time series data
    :return: tuple[float, float] - gamma and u values
    """

    n = len(x_t)
    mean = np.mean(x_t)

    q_square = sum([(x_t[i] - x_t[i + 1]) ** 2 for i in range(n - 1)]) / (n - 2)
    s_square = sum([(x_t[i] - mean) ** 2 for i in range(n)]) / (n - 1)

    gamma = q_square / (2 * s_square)
    u = (gamma - 1) * np.sqrt((n ** 2 - 1) / (n - 2))

    return u
