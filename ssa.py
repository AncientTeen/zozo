import numpy as np
from tkinter import simpledialog, messagebox

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
    mean = np.mean(x_t)
    std = np.std(x_t)
    x_t = (x_t - mean) / std

    k = M
    l = N - M + 1
    X = np.zeros((k, l))
    for i in range(k):
        X[i, :] = x_t[i:i + l]

    S = X @ X.T

    eigenvals, eigenvectors = np.linalg.eig(S)

    idx = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[idx]
    eigenvectors = eigenvectors[:, idx]

    Y = eigenvectors.T @ X

    return Y, eigenvectors, eigenvals, X


def diagonal_averaging(X: np.ndarray) -> np.ndarray:
    """
    Perform diagonal averaging on the trajectory matrix to reconstruct the time series.
    """
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


def recomposition(Y: np.ndarray, A: np.ndarray, v: int) -> np.ndarray:
    """
    Recomposition function of SSA.
    """

    v = min(v, A.shape[1], Y.shape[0])

    X_hat = A[:, :v] @ Y[:v, :]

    reconstructed_series = diagonal_averaging(X_hat)

    return reconstructed_series


def forecasting(Y: np.ndarray, A: np.ndarray, M: int, v: int, h: int) -> list[float]:
    """
    ssa forecasting
    """

    v = min(v, A.shape[1], Y.shape[0])

    A_v = A[:, :v]
    Y_v = Y[:v, :]

    X_v = A_v @ Y_v

    reconstructed_series = diagonal_averaging(X_v)

    K = M
    last_M_points = reconstructed_series[-K:]
    hankel_matrix = np.column_stack([reconstructed_series[i:-K + i] for i in range(K)])

    rhs = reconstructed_series[K:]

    coeffs = np.linalg.lstsq(hankel_matrix, rhs, rcond=None)[0]

    forecast = []
    last_values = last_M_points.copy()

    for _ in range(h):
        next_value = np.dot(coeffs, last_values[::-1])
        forecast.append(next_value)
        last_values = np.append(last_values[1:], next_value)

    return forecast


def ssa_forecasting(Y: np.ndarray, eigenvectors: np.ndarray, M: np.ndarray, sample_data: dict, fig1, ax1) -> None:
    """
    Function to perform SSA forecasting.
    """


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

    forecast = forecasting(Y, eigenvectors, M, v, h)

    s_n = None
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp
            break

    x_t = sample_data[s_n]["data"]

    forecast = [x_t[-1]] + forecast

    t = [i for i in range(len(x_t), len(x_t) + len(forecast))]
    ax1.plot(t, forecast, c='red')
    fig1.canvas.draw()
    fig1.canvas.flush_events()
