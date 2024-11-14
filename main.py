import numpy as np
import tkinter as tk
from tkinter import *
from math import trunc
from icecream import ic
from scipy.stats import norm
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk


from transformations import display_function_list
from trend_functions import sign_criterion, mann_criterion, series_criterion, rise_n_fall_criterion, abbe_criterion



array: list = []
sample_data: dict = {}
samplesGroup: dict = {}
sample_checkbuttons: list = []


def openFile() -> None:
    """
    function that opens file and put it to the sample_data
    :return: None
    """


    root.filename = fd.askopenfilename(initialdir="/", title="Select file", filetypes=[('All Files', '*.*'),
                                                                                       ('Python Files', '*.py'),
                                                                                       ('Text Document', '*.txt'),
                                                                                       ('CSV files', "*.csv")])
    global array
    t = []
    if root.filename.split('.')[1] == 'txt':
        array = np.loadtxt(root.filename, dtype='float')

        if len(array.shape) == 1:
            t.append(array)
        elif len(array.shape) > 1:
            for i in range(len(array[0])):
                t_buff = []
                for j in range(len(array)):
                    t_buff.append(array[j][i])
                t.append(t_buff)

    for i in range(len(t)):
        sample_num = len(sample_data) + 1
        sample_name = f"Вибірка {sample_num}"
        sample_var = tk.IntVar()
        arr = t[i]
        sample_data[sample_name] = {"data": arr, "var": sample_var}
        checkbutton = Checkbutton(text=sample_name, variable=sample_var)
        sample_checkbuttons.append(checkbutton)
        sample_menu.add_checkbutton(label=sample_name, variable=sample_var)

    # print(sample_data)
    print(type(root))
    # print(type(sample_menu))

def visualization() -> None:
    """
    function that visualizes time series
    :return: None
    """


    for i in range(1, len(sample_data) + 1):
        str = f"Вибірка {i}"
        if sample_data[str]['var'].get() == 1:
            s_n = str

    t = [i for i in range(1, len(sample_data[s_n]["data"]) + 1)]
    x_t = sample_data[s_n]["data"]

    fig1, ax1 = plt.subplots(figsize=(9, 5), dpi=100)

    plt.grid(color='grey', linestyle='-', linewidth=0.5)
    plt.xlabel('X')
    plt.ylabel('Y')

    ax1.plot(t, x_t)


    def on_left_click(event):
        print(f"Left click at ({event.xdata}, {event.ydata})")
        print(type(event))


    def on_right_click(event):
        display_function_list(event, root, sample_data, sample_menu, sample_checkbuttons) #, x, y)

    fig1.canvas.mpl_connect('button_press_event', on_left_click)
    fig1.canvas.mpl_connect('button_press_event', on_right_click)


    variation_series_out = FigureCanvasTkAgg(fig1, master=root)
    variation_series_out.get_tk_widget().grid(row=0, column=0, sticky='nw')
    toolbar = NavigationToolbar2Tk(variation_series_out, root, pack_toolbar=False)
    toolbar.update()
    toolbar.grid(row=1, column=0)


def characteristics(tau: int = 5) -> None:
    """
    function that calculates characteristics of time series
    :param tau: int - value for autocovariation and autocorrelation functions
    :return: None
    """


    for i in range(1, len(sample_data) + 1):
        samp = f"Вибірка {i}"
        if sample_data[samp]['var'].get() == 1:
            s_n = samp

    t = [i for i in range(1, len(sample_data[s_n]["data"]) + 1)]
    x_t = sample_data[s_n]["data"]

    N = len(x_t)
    text_frame = Frame(root)
    text_frame.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=5)

    """Time series output"""
    T1 = Text(master=text_frame, height=15, width=20)
    T1.pack(side=LEFT, padx=(0, 5))
    T1.delete('1.0', END)
    T1.insert(END, 'Часовий ряд:\n\n')

    T1.insert(END, f't   x(t)\n')
    for i in range(len(t)):
        T1.insert(END, f'{t[i]}   {x_t[i]:.4f}\n')



    """Characteristics of time series"""
    T2 = Text(master=text_frame, height=15, width=30)
    T2.pack(side=LEFT, padx=(0, 5))
    T2.delete('1.0', END)
    T2.insert(END, 'Характеристики часового ряду:\n\n')

    mean = np.mean(x_t)
    std = np.std(x_t)
    T2.insert(END, f'hat(m): {mean:.4f}\n')
    T2.insert(END, f'hat(σ): {std:.4f}\n')


    autocovariation = sum([(x_t[i] - mean) * (x_t[i + tau] - mean) for i in range(N - tau)]) / (N - tau)
    autocorelation = autocovariation / std

    T2.insert(END, f'\u03B3({tau}): {autocovariation:.4f}\n')
    T2.insert(END, f'r({tau}): {autocorelation:.4f}\n')




    """trend"""
    T3 = Text(master=text_frame, height=15, width=50)
    T3.pack(side=LEFT)
    T3.delete('1.0', END)
    T3.insert(END, 'Аналіз тренду:\n\n')

    critical_value = norm.ppf(1 - 0.05 / 2)

    T3.insert(END, 'Критерій знаків:\n')

    C = sign_criterion(x_t)

    if C > critical_value:
        T3.insert(END, f"Тенденція на спадання: C = {C:.3f}, критичне значення = ±{critical_value:.3f}\n")
    elif C < -critical_value:
        T3.insert(END, f"Тенденція на зростання: C = {C:.3f}, критичне значення = ±{critical_value:.3f}\n")
    else:
        T3.insert(END, f"Процес стаціонарний: C = {C:.3f}, критичне значення = ±{critical_value:.3f}\n")


    T3.insert(END, '\nКритерій Манна:\n')

    u1 = mann_criterion(x_t)

    if u1 > critical_value:
        T3.insert(END, f"Тенденція на спадання: u = {u1:.3f}, критичне значення = ±{critical_value:.3f}\n")
    elif u1 < -critical_value:
        T3.insert(END, f"Тенденція на зростання: u = {u1:.3f}, критичне значення = ±{critical_value:.3f}\n")
    else:
        T3.insert(END, f"Процес стаціонарний: u = {u1:.3f}, критичне значення = ±{critical_value:.3f}\n")


    T3.insert(END, '\nКритерій серій:\n')

    v1, d1 = series_criterion(x_t)

    v1_check = trunc((N + 1 - 1.96 * np.sqrt(N - 1)) / 2)
    d1_check = trunc(3.3 * np.log(N + 1))
    if v1 > v1_check and d1 < d1_check:
        T3.insert(END, f"Процес стаціонарний: (V(N), D(N)) = ({v1:.3f}, {d1:.3f}), критичні значення = ({v1_check}, {d1_check})\n")
    else:
        T3.insert(END, f"Тренд існує: (V(N), D(N)) = ({v1:.3f}, {d1:.3f}), критичні значення = ({v1_check}, {d1_check})\n")



    T3.insert(END, '\nКритерій \'зростаючих\' і \'спадаючих\' серій:\n')

    v2, d2 = rise_n_fall_criterion(x_t)

    v2_check = trunc(((2 * N - 1) / 3 - 1.96 * np.sqrt((16 * N - 29) / 90)) / 2)
    d2_check = 0
    if N <= 26:
        d2_check = 5
    elif 26 < N <= 153:
        d2_check = 6
    elif N > 153:
        d2_check = 7


    if v2 > v2_check and d2 < d2_check:
        T3.insert(END,
                  f"Процес стаціонарний: (V(N), D(N)) = ({v2:.3f}, {d2:.3f}), критичні значення = ({v2_check}, {d2_check})\n")
    else:
        T3.insert(END,
                  f"Тренд існує: (V(N), D(N)) = ({v1:.3f}, {d1:.3f}), критичні значення = ({v1_check}, {d1_check})\n")


    T3.insert(END, '\nКритерій Аббе:\n')

    u2 = abbe_criterion(x_t)


    if u2 > critical_value:
        T3.insert(END, f"Тенденція на спадання: u = {u2:.3f}, критичне значення = ±{critical_value:.3f}\n")
    elif u2 < -critical_value:
        T3.insert(END, f"Тенденція на зростання: u = {u2:.3f}, критичне значення = ±{critical_value:.3f}\n")
    else:
        T3.insert(END, f"Процес стаціонарний: u = {u2:.3f}, критичне значення = ±{critical_value:.3f}\n")




def showSample() -> None:
    """
    function that calls visualization and characteristics functions
    :return: None
    """


    visualization()
    characteristics()


root = Tk()

root.geometry("1200x800")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
root.config(menu=menubar)
menubar.add_cascade(label="Меню", menu=filemenu)
filemenu.add_command(label="Відкрити файл", command=openFile)

sample_menu = Menu(menubar, tearoff=0)
filemenu.add_cascade(label="Вибірки", menu=sample_menu)

filemenu.add_command(label='Відобразити', command=showSample)

root.mainloop()









