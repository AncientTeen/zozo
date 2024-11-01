import numpy as np
import tkinter as tk
from tkinter import *
from icecream import ic
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk



array = []
sample_data = {}
samplesGroup = {}
sample_checkbuttons = []

def openFile() -> None:
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


def showSample() -> None:
    for i in range(1, len(sample_data) + 1):
        str = f"Вибірка {i}"
        if sample_data[str]['var'].get() == 1:
            s_n = str

    arr = [[i for i in range(1, len(sample_data[s_n]["data"]) + 1)], sample_data[s_n]["data"]]


    fig1, ax1 = plt.subplots(figsize=(7, 5), dpi=100)

    plt.grid(color='grey', linestyle='-', linewidth=0.5)
    plt.xlabel('X')
    plt.ylabel('Y')

    ax1.plot(arr[0], arr[1])

    variation_series_out = FigureCanvasTkAgg(fig1, master=root)
    variation_series_out.get_tk_widget().grid(row=0, column=0)
    toolbar = NavigationToolbar2Tk(variation_series_out, root, pack_toolbar=False)
    toolbar.update()
    toolbar.grid(row=1, column=0)




root = Tk()

root.geometry("1200x700")

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
root.config(menu=menubar)
menubar.add_cascade(label="Меню", menu=filemenu)
filemenu.add_command(label="Відкрити файл", command=openFile)

sample_menu = Menu(menubar, tearoff=0)
filemenu.add_cascade(label="Вибірки", menu=sample_menu)

filemenu.add_command(label='Відобразити', command=showSample)





root.mainloop()
