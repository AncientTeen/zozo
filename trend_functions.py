import numpy as np
import tkinter as tk
from tkinter import *

from numerical_functions import mean, median

"""This file is used to calculate trend criteria"""


def sign_criterion(x_t: list) -> float:
    """
    sign criterion function
    """
    n = len(x_t)
    y = []

    for i in range(n - 1):
        if x_t[i + 1] > x_t[i]:
            y.append(1)
        else:
            y.append(0)

    one = 0
    zeros = 0
    for i in y:
        if i == 1:
            one += 1
        else:
            zeros += 1
    c = sum(y)
    E_c = (n - 1) / 2
    D_c = (n + 1) / 12

    C = (c - E_c) / np.sqrt(D_c)

    return C


def mann_criterion(x_t: list) -> float:
    """
    mann criterion function
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
    """
    n = len(x_t)
    median_series = median(x_t)

    """"""
    y = [1 if x_t[i] >= median_series else -1 for i in range(n)]

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
    """

    n = len(x_t)
    mean_series = mean(x_t)

    q_square = sum([(x_t[i] - x_t[i + 1]) ** 2 for i in range(n - 1)]) / (n - 2)
    s_square = sum([(x_t[i] - mean_series) ** 2 for i in range(n)]) / (n - 1)

    gamma = q_square / (2 * s_square)
    u = (gamma - 1) * np.sqrt((n ** 2 - 1) / (n - 2))

    return u


def identification_lin_trend(sample_data: dict, fig1, ax1) -> None:
    """
    function for identification a linear trend
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Ряд {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)
    t = [i for i in range(1, N + 1)]

    mean_x = mean(x_t)
    mean_t = mean(t)

    mean_t_sq = mean([t[i] ** 2 for i in range(N)])
    mean_tx = mean([(x_t[i] * t[i]) for i in range(N)])

    a_0 = (mean_x * mean_t_sq - mean_t * mean_tx) / (mean_t_sq - mean_t ** 2)
    a_1 = (mean_tx - mean_t * mean_x) / (mean_t_sq - mean_t ** 2)

    x_t_new = [(a_0 + a_1 * t[i]) for i in range(N)]

    ax1.plot(t, x_t_new, c='red')
    fig1.canvas.draw()
    fig1.canvas.flush_events()


def remove_lin_trend(sample_data: dict, sample_menu: tk.Menu, sample_checkbuttons: list) -> None:
    """
    function for extracting a linear trend
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Ряд {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)
    t = [i for i in range(1, N + 1)]

    mean_x = mean(x_t)
    mean_t = mean(t)

    mean_t_sq = mean([t[i] ** 2 for i in range(N)])
    mean_tx = mean([(x_t[i] * t[i]) for i in range(N)])

    a_0 = (mean_x * mean_t_sq - mean_t * mean_tx) / (mean_t_sq - mean_t ** 2)
    a_1 = (mean_tx - mean_t * mean_x) / (mean_t_sq - mean_t ** 2)

    x_trend = [(a_0 + a_1 * t[i]) for i in range(N)]

    x_t_new = [x_t[i] - x_trend[i] for i in range(N)]

    sample_num = len(sample_data) + 1
    sample_name = f"Ряд {sample_num}"
    sample_var = tk.IntVar()
    sample_data[sample_name] = {"data": x_t_new, "var": sample_var}
    checkbutton = Checkbutton(text=sample_name, variable=sample_var)
    sample_checkbuttons.append(checkbutton)
    sample_menu.add_checkbutton(label=sample_name, variable=sample_var)


def identification_parab_trend(sample_data: dict, fig1, ax1) -> None:
    """
    function for identification a polynomial trend
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Ряд {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)
    t = [i for i in range(1, N + 1)]

    mean_x = mean(x_t)
    mean_t = mean(t)

    mean_t_sq = mean([t[i] ** 2 for i in range(N)])
    mean_t_trd = mean([t[i] ** 3 for i in range(N)])
    mean_t_frth = mean([t[i] ** 4 for i in range(N)])

    mean_tx = mean([(x_t[i] * t[i]) for i in range(N)])
    mean_tx_sq = mean([(x_t[i] * (t[i] ** 2)) for i in range(N)])

    D = (mean_t_sq * mean_t_frth - mean_t_trd ** 2) - mean_t * (
            mean_t * mean_t_frth - mean_t_sq * mean_t_trd) + mean_t_sq * (mean_t * mean_t_trd - mean_t_sq ** 2)

    a_0 = (mean_x * (mean_t_sq * mean_t_frth - mean_t_trd ** 2) - mean_t * (
            mean_tx * mean_t_frth - mean_t_trd * mean_tx_sq) + mean_t_sq * (
                   mean_tx * mean_t_trd - mean_t_sq * mean_tx_sq)) / D
    a_1 = ((mean_tx * mean_t_frth - mean_t_trd * mean_tx_sq) - mean_x * (
            mean_t * mean_t_frth - mean_t_sq * mean_t_trd) + mean_t_sq * (
                       mean_t * mean_tx_sq - mean_tx * mean_t_sq)) / D
    a_2 = ((mean_t_sq * mean_tx_sq - mean_tx * mean_t_trd) - mean_t * (
                mean_t * mean_tx_sq - mean_tx * mean_t_sq) + mean_x * (mean_t * mean_t_trd - mean_t_sq ** 2)) / D

    x_t_new = [(a_0 + a_1 * t[i] + a_2 * t[i] ** 2) for i in range(N)]

    ax1.plot(t, x_t_new, c='green')
    fig1.canvas.draw()
    fig1.canvas.flush_events()


def remove_parab_trend(sample_data: dict, sample_menu: tk.Menu, sample_checkbuttons: list) -> None:
    """
    function for extracting a polynomial trend
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Ряд {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)
    t = [i for i in range(1, N + 1)]

    mean_x = mean(x_t)
    mean_t = mean(t)

    mean_t_sq = mean([t[i] ** 2 for i in range(N)])
    mean_t_trd = mean([t[i] ** 3 for i in range(N)])
    mean_t_frth = mean([t[i] ** 4 for i in range(N)])

    mean_tx = mean([(x_t[i] * t[i]) for i in range(N)])
    mean_tx_sq = mean([(x_t[i] * (t[i] ** 2)) for i in range(N)])

    D = (mean_t_sq * mean_t_frth - mean_t_trd ** 2) - mean_t * (
            mean_t * mean_t_frth - mean_t_sq * mean_t_trd) + mean_t_sq * (mean_t * mean_t_trd - mean_t_sq ** 2)

    a_0 = (mean_x * (mean_t_sq * mean_t_frth - mean_t_trd ** 2) - mean_t * (
            mean_tx * mean_t_frth - mean_t_trd * mean_tx_sq) + mean_t_sq * (
                   mean_tx * mean_t_trd - mean_t_sq * mean_tx_sq)) / D
    a_1 = ((mean_tx * mean_t_frth - mean_t_trd * mean_tx_sq) - mean_x * (
            mean_t * mean_t_frth - mean_t_sq * mean_t_trd) + mean_t_sq * (
                       mean_t * mean_tx_sq - mean_tx * mean_t_sq)) / D
    a_2 = ((mean_t_sq * mean_tx_sq - mean_tx * mean_t_trd) - mean_t * (
                mean_t * mean_tx_sq - mean_tx * mean_t_sq) + mean_x * (mean_t * mean_t_trd - mean_t_sq ** 2)) / D

    x_trend = [(a_0 + a_1 * t[i] + a_2 * t[i] ** 2) for i in range(N)]

    x_t_new = [x_t[i] - x_trend[i] for i in range(N)]

    sample_num = len(sample_data) + 1
    sample_name = f"Ряд {sample_num}"
    sample_var = tk.IntVar()
    sample_data[sample_name] = {"data": x_t_new, "var": sample_var}
    checkbutton = Checkbutton(text=sample_name, variable=sample_var)
    sample_checkbuttons.append(checkbutton)
    sample_menu.add_checkbutton(label=sample_name, variable=sample_var)
