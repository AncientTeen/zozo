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

    # Ensure v does not exceed available components
    v = min(v, A.shape[1], Y.shape[0])

    X_hat = A[:, :v] @ Y[:v, :]

    reconstructed_series = diagonal_averaging(X_hat)

    return reconstructed_series


def forecasting(Y: np.ndarray, A: np.ndarray, M: int, v: int, h: int) -> list[float]:
    """
    ssa forecasting
    """

    v = min(v, A.shape[1], Y.shape[0])

    # Select the components to use
    A_v = A[:, :v]
    Y_v = Y[:v, :]

    # Reconstruct the series using selected components
    X_v = A_v @ Y_v  # Reconstructed trajectory matrix using v components

    # Forecasting
    # Step 1: Identify the linear recurrence coefficients
    # Use the reconstructed series to estimate the coefficients

    # Average the reconstructed trajectory matrix along the anti-diagonals
    reconstructed_series = diagonal_averaging(X_v)

    # Determine the coefficients of the linear recurrence relation
    # Using the last M points of the reconstructed series
    K = M
    last_M_points = reconstructed_series[-K:]
    hankel_matrix = np.column_stack([reconstructed_series[i:-K + i] for i in range(K)])

    # Right-hand side vector
    rhs = reconstructed_series[K:]

    # Solve for the coefficients
    coeffs = np.linalg.lstsq(hankel_matrix, rhs, rcond=None)[0]

    # Use the coefficients to forecast future values
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

    # global

    if Y is None or eigenvectors is None or M is None:
        messagebox.showerror("Error", "Please perform decomposition first.")
        return

    v = simpledialog.askinteger("v", f"Enter number of principal components to use (1 ≤ v ≤ {len(eigenvectors)}):")
    if v is None or v < 1 or v > len(eigenvectors):
        messagebox.showerror("Error", f"Invalid number of components.")
        return

    h = simpledialog.askinteger("h", "Enter number of steps ahead to forecast:")
    if h is None or h < 1:
        messagebox.showerror("Error", f"Invalid number of steps.")
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
    print(t)
    print(forecast)
    ax1.plot(t, forecast, c='red')
    fig1.canvas.draw()
    fig1.canvas.flush_events()



