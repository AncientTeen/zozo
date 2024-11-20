import numpy as np
import tkinter as tk
from tkinter import *




def remove_anomalous(sample_data: dict, sample_menu: tk.Menu, sample_checkbuttons: list) -> None:
    """
    function that detects and replaces anomalous in the time series
    """

    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]

    mean = np.mean(x_t)
    std = np.std(x_t)
    k = 4  # recommended to set k from the interval [3, 9]

    temp = [x_t[0], x_t[1]]
    for i in range(2, len(x_t)):
        if mean - k * std < x_t[i] < mean + k * std:
            temp.append(x_t[i])
        else:
            print('*')
            x_new = 2 * x_t[i - 1] - x_t[i - 2]
            temp.append(x_new)

    sample_num = len(sample_data) + 1
    sample_name = f"Вибірка {sample_num}"
    sample_var = tk.IntVar()
    sample_data[sample_name] = {"data": temp, "var": sample_var}
    checkbutton = Checkbutton(text=sample_name, variable=sample_var)
    sample_checkbuttons.append(checkbutton)
    sample_menu.add_checkbutton(label=sample_name, variable=sample_var)


# Data smoothing
# 1. median +
# 2. SMA +
# 3. WMA +
# 4. EMA +
# 5. DMA +
# 6. TMA +

def median_smoothing(sample_data: dict, fig1, ax1) -> None:
    """
    function for smoothing data using median
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)

    m0 = (4 * x_t[0] + x_t[1] + 2 * x_t[2]) / 3
    mN = (4 * x_t[-1] + x_t[-2] + 2 * x_t[-3]) / 3
    M = [m0]
    for i in range(1, N - 1):
        m_temp = (x_t[i - 1] + x_t[i] + x_t[i + 1]) / 3
        M.append(m_temp)

    M.append(mN)

    t = [i for i in range(1, len(M) + 1)]

    ax1.plot(t, M, c='red')
    fig1.canvas.draw()
    fig1.canvas.flush_events()


def sma(sample_data: dict, fig1, ax1) -> None:
    """
    simple moving average function for smoothing data with window size of 3
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)

    n = 3


    s0 = x_t[0] / n
    s1 = x_t[1] / n
    S = [s0, s1]


    for i in range(2, N):
        s_next = (x_t[i - 2] + x_t[i - 1] + x_t[i]) / n
        S.append(s_next)

    t = [i for i in range(1, N + 1)]

    ax1.plot(t, S, c='green')
    fig1.canvas.draw()
    fig1.canvas.flush_events()

def wma(sample_data: dict, fig1, ax1) -> None:
    """
    weighted moving average function for smoothing data with window size of 3
    """

    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]
    N = len(x_t)

    weights = [1, 2, 3]
    weight_sum = sum(weights)

    w0 = x_t[0]
    w1 = (x_t[0] * weights[0] + x_t[1] * weights[1]) / (weights[0] + weights[1])
    W = [w0, w1]

    for i in range(2, N):
        weighted_sum = (x_t[i - 2] * weights[0] +
                        x_t[i - 1] * weights[1] +
                        x_t[i] * weights[2])
        w_next = weighted_sum / weight_sum
        W.append(w_next)

    t = [i for i in range(1, N + 1)]

    ax1.plot(t, W, c='magenta')
    fig1.canvas.draw()
    fig1.canvas.flush_events()


def ema(sample_data: dict, fig1, ax1) -> None:
    """
    exponential moving average function for smoothing data with window size of 3
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]

    N = len(x_t)
    n = 4
    alpha = 2 / (n + 1)

    e0 = x_t[0]
    E = [e0]
    for i in range(1, N):
        e_next = alpha * x_t[i] + (1 - alpha) * E[i - 1]
        E.append(e_next)




    t = [i for i in range(1, N + 1)]

    ax1.plot(t, E, c='black')
    fig1.canvas.draw()
    fig1.canvas.flush_events()


def dema(sample_data: dict, fig1, ax1) -> None:
    """
    double Exponential moving average function for smoothing data with window size of 3
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]

    N = len(x_t)
    n = 4
    alpha = 2 / (n + 1)

    e0 = x_t[0]
    E = [e0]
    D = [e0]

    for i in range(1, N):
        e_next = alpha * x_t[i] + (1 - alpha) * E[i - 1]
        E.append(e_next)

        d_next = alpha * e_next + (1 - alpha) * D[i - 1]
        D.append(d_next)

    t = [i for i in range(1, N + 1)]

    ax1.plot(t, D, c='brown')
    fig1.canvas.draw()
    fig1.canvas.flush_events()


def tema(sample_data: dict, fig1, ax1) -> None:
    """
    triple Exponential moving average function for smoothing data with window size of 3
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]

    N = len(x_t)
    n = 4
    alpha = 2 / (n + 1)

    e0 = x_t[0]
    E = [e0]
    D = [e0]
    T = [e0]

    for i in range(1, N):
        e_next = alpha * x_t[i] + (1 - alpha) * E[i - 1]
        E.append(e_next)

        d_next = alpha * e_next + (1 - alpha) * D[i - 1]
        D.append(d_next)

        t_next = alpha * d_next + (1 - alpha) * T[i - 1]
        T.append(t_next)



    t = [i for i in range(1, N + 1)]

    ax1.plot(t, T, c='gray')
    fig1.canvas.draw()
    fig1.canvas.flush_events()