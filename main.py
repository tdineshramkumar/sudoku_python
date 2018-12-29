import tkinter as tk
import numpy as np
import sudoku_solver as sudoku
from tkinter import messagebox

entries = np.empty((9, 9), dtype=object)
texts = np.empty((9, 9), dtype=object)
gray = '#AAAAAA'
white = '#FFFFFF'
black = '#000000'
entry_to_text = {}


def validate_entry(string_var):
    _data = string_var.get()
    if len(_data) == 0 or (len(_data) == 1 and _data.isdigit()):
        return
    _digit = ''
    for i in range(len(_data)):
        if _data[i].isdigit():
            _digit = _data[i]
    string_var.set(_digit)


def get_values():
    values = np.zeros((9, 9), np.int)
    for i in range(9):
        for j in range(9):
            if texts[i, j].get():
                values[i, j] = int(texts[i, j].get())
    sudoku.print_sudoku(values)
    return values


def set_values(values):
    for i in range(9):
        for j in range(9):
            if values[i, j] != 0:
                texts[i, j].set(str(values[i, j]))


def reset_entries():
    for i in range(9):
        for j in range(9):
            texts[i][j].set('')


def solve_puzzle():
    problem = get_values()

    try:
        solution = sudoku.solve_sudoku(problem)
        if solution is None:
            messagebox.showerror('Error Solving Sudoku', 'No Solution Found')
        else:
            set_values(solution)
    except Exception as e:
        messagebox.showerror('Error Solving Sudoku', e)


def main():
    master = tk.Tk()
    for r in range(9):
        for c in range(9):
            texts[r][c] = tk.StringVar()
            texts[r][c].trace_add('write', lambda *args, var=texts[r][c]: validate_entry(var))
            bg = white if (r//3 + c//3) % 2 else gray
            entries[r][c] = tk.Entry(master, width=2, textvariable=texts[r][c], fg=black, bg=bg)
            entry_to_text[entries[r][c]] = texts[r][c]
            entries[r][c].grid(row=r, column=c)
    tk.Button(master, text='Solve', justify=tk.CENTER, command=solve_puzzle).grid(row=9, columnspan=9, sticky=tk.EW)
    tk.Button(master, text='Reset', justify=tk.CENTER, command=reset_entries).grid(row=10, columnspan=9, sticky=tk.EW)
    master.mainloop()


main()
