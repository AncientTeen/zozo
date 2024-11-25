import numpy as np
from tkinter import simpledialog, messagebox

from numerical_functions import *

"""
SSA - singular spectrum analysis
"""


# set M (2 < M < [N / 2])


def decomposition(x_t: dict, M: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    SSA decomposition function.
    """

    N = len(x_t)

    """implemented standardization before decomposition"""
    mean_series = mean(x_t)
    std_series = std(x_t)
    x_t = (x_t - mean_series) / std_series

    k = M
    l = N - M + 1
    X = np.zeros((k, l))
    for i in range(k):
        X[i, :] = x_t[i:i + l]

    S = matrix_multiply(X, transpose(X))

    eigenvals, eigenvectors = eig_decomposition(S)

    eigenvectors = np.array(eigenvectors)

    idx = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[idx]
    eigenvectors = eigenvectors[:, idx]

    Y = matrix_multiply(transpose(eigenvectors), X)

    return Y, eigenvectors, eigenvals, X


def diagonal_averaging(X: np.ndarray) -> np.ndarray:
    """
    Perform diagonal averaging on the trajectory matrix to reconstruct the time series.
    """
    X = np.array(X)

    M, L = X.shape
    N = M + L - 1
    reconstructed_series = np.zeros(N)
    counts = np.zeros(N)

    for i in range(M):
        for j in range(L):
            reconstructed_series[i + j] += X[i, j]
            counts[i + j] += 1

    reconstructed_series /= counts

    return reconstructed_series


def recomposition(Y: np.ndarray, A: np.ndarray, component_option: str, components: list[int] = None) -> np.ndarray:
    """
    Recomposition function of SSA with user-selected components.
    Allows:
    1. Exact reconstruction using all components.
    2. Reconstruction using several selected components (low-pass filtering).
    3. Reconstruction using a single components.
    """
    Y = np.array(Y)

    if component_option == '1':
        X_hat = matrix_multiply(A, Y)
    elif component_option == '2':
        if not components:
            raise ValueError("For 'first' option, components (number of components to use) must be specified.")
        v = min(components[0], A.shape[1], Y.shape[0])
        X_hat = matrix_multiply(A[:, :v], Y[:v, :])
    elif component_option == '3':
        if not components:
            raise ValueError("For 'specific' option, components (indices of components to use) must be specified.")
        selected_eigenvectors = A[:, components]
        selected_Y = Y[components, :]
        X_hat = matrix_multiply(selected_eigenvectors, selected_Y)
    else:
        raise ValueError("Invalid component_option. Use 'all', 'first', or 'specific'.")

    X_hat = np.array(X_hat)

    reconstructed_series = diagonal_averaging(X_hat)
    return reconstructed_series



def forecasting(Y: np.ndarray, A: np.ndarray, M: int, v: int, h: int, forecast_start_index: int) -> list[float]:
    """
    SSA forecasting with user-defined forecast start index.
    """
    Y = np.array(Y)
    v = min(v, A.shape[1], Y.shape[0])

    A_v = A[:, :v]
    Y_v = Y[:v, :]

    X_v = matrix_multiply(A_v, Y_v)

    reconstructed_series = diagonal_averaging(X_v)

    truncated_series = reconstructed_series[:forecast_start_index]

    K = M
    last_M_points = truncated_series[-K:]
    hankel_matrix = np.column_stack([truncated_series[i:-K + i] for i in range(K)])

    rhs = truncated_series[K:]

    coeffs = solve_least_squares(hankel_matrix, rhs)

    forecast = []
    last_values = last_M_points.copy()

    for _ in range(h):
        next_value = dot_product(coeffs, last_values[::-1])
        forecast.append(next_value)
        last_values = np.append(last_values[1:], next_value)

    return forecast



def ssa_forecasting(Y: np.ndarray, eigenvectors: np.ndarray, M: np.ndarray, sample_data: dict, fig1, ax1) -> None:
    """
    Function to perform SSA forecasting
    """
    s_n = None
    for i in range(1, len(sample_data) + 1):
        samp = f"Ряд {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp
            break

    if not s_n:
        messagebox.showerror("Помилка", "Не вибрано жодного ряду")
        return

    if Y is None or eigenvectors is None or M is None:
        messagebox.showerror("Помилка", "Спершу зробіть декомпозицію")
        return

    v = simpledialog.askinteger("v", f"Введіть кількість головних компонент (1 ≤ v ≤ {len(eigenvectors)}):")
    if v is None or v < 1 or v > len(eigenvectors):
        messagebox.showerror("Помилка", f"Невірне значення для компонент")
        return

    h = simpledialog.askinteger("h", "Введіть кількість кроків для прогнозування:")
    if h is None or h < 1:
        messagebox.showerror("Помилка", f"Невірне значення для кількості кроків")
        return

    forecast_start_index = simpledialog.askinteger(
        "Індекс початку прогнозу",
        "Введіть індекс останнього значення часового ряду для прогнозування:"
    )
    if forecast_start_index is None or forecast_start_index >= len(sample_data[s_n]["data"]) + 1:
        messagebox.showerror("Помилка",
                             f"Індекс початку прогнозу повинен бути меншим за довжину серії ({len(sample_data[s_n]['data'])}).")
        return

    Y = np.array(Y)


    x_t = sample_data[s_n]["data"]

    mean_series = mean(x_t[:forecast_start_index])
    std_series = std(x_t[:forecast_start_index])

    forecast = forecasting(Y, eigenvectors, M, v, h, forecast_start_index)

    forecast = np.array(forecast)
    forecast = (forecast * std_series) + mean_series

    forecast = [x_t[forecast_start_index - 1]] + forecast.tolist()



    t = [i for i in range(forecast_start_index, forecast_start_index + len(forecast))]

    ax1.plot(t, forecast, c='red', label='Forecast')
    ax1.legend()
    fig1.canvas.draw()
    fig1.canvas.flush_events()





