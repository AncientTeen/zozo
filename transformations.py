import matplotlib
import numpy as np
import tkinter as tk
from tkinter import *
from matplotlib.backend_bases import MouseEvent


def display_function_list(event: matplotlib.backend_bases.MouseEvent, root: tk.Tk, sample_data: dict, sample_menu: tk.Menu, sample_checkbuttons: list):  # , x, y):
    """
    function that displays list of transformation functions when right-clicked on graph
    :param event: matplotlib.backend_bases.MouseEvent - event that handle mouse clicking on the graph
    :param root: tk.Tk - root of window
    :param sample_data: dict - time series samples
    :param sample_menu: tk.Menu - menubar of root
    :param sample_checkbuttons: list - list of checkbuttons
    :return: None
    """

    if event.button == 3:
        function_list = ["Вилучення аномальних значень", "Лінійний тренд"]

        function_list_window = Toplevel(root)

        listbox = Listbox(function_list_window, selectmode=SINGLE, width=40, height=15)
        for function_name in function_list:
            listbox.insert(END, function_name)

        def select_function(event):
            selected_index = listbox.curselection()
            if selected_index:
                selected_function = function_list[selected_index[0]]

                if selected_function == "Вилучення аномальних значень":
                    remove_anomalous(sample_data, sample_menu, sample_checkbuttons)
                    pass
                # elif selected_function == "Лінійний тренд":
                    # linear_trend()
                    # pass

                function_list_window.destroy()

        listbox.bind('<ButtonRelease-1>', select_function)

        listbox.pack()


def remove_anomalous(sample_data: dict, sample_menu: tk.Menu, sample_checkbuttons: list) -> None:
    """
    function that detects and replaces anomalous in the time series
    :param sample_data: dict - time series samples
    :param sample_menu: tk.Menu - menubar of root
    :param sample_checkbuttons: list - list of checkbuttons
    :return: None
    """

    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]

    mean = np.mean(x_t)
    std = np.std(x_t)
    k = 4 #[3, 9]

    temp = [x_t[0], x_t[1]]
    for i in range(2, len(x_t)):
        if mean - k * std < x_t[i] < mean + k * std:
            temp.append(x_t[i])
        else:
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
# 1. median
# 2. SMA
# 3. WMA
# 4. EMA
# 5. DMA
# 6. TMA

def median_smoothing(sample_data: dict, sample_menu: tk.Menu, sample_checkbuttons: list) -> None:
    """
    function smoothing data using median
    :param sample_data: dict - time series samples
    :param sample_menu: tk.Menu - menubar of root
    :param sample_checkbuttons: list - list of checkbuttons
    :return: None
    """
    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    x_t = sample_data[s_n]["data"]

    M = []
    for i in range(2, len(x_t) - 1):
        ...



    pass


