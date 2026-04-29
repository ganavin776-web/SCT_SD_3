import tkinter as tk
from tkinter import ttk
import random

# ---------- SOLVER ----------
def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    r, c = empty

    for num in range(1, 10):
        if valid(board, num, (r, c)):
            board[r][c] = num
            if solve(board):
                return True
            board[r][c] = 0
    return False

def valid(board, num, pos):
    for i in range(9):
        if board[pos[0]][i] == num or board[i][pos[1]] == num:
            return False

    box_x, box_y = pos[1]//3, pos[0]//3
    for i in range(box_y*3, box_y*3+3):
        for j in range(box_x*3, box_x*3+3):
            if board[i][j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# ---------- GENERATOR ----------
def generate_full():
    board = [[0]*9 for _ in range(9)]
    solve(board)
    return board

def remove_numbers(board, level):
    remove = {"Easy":30, "Medium":40, "Hard":50}[level]
    while remove:
        r, c = random.randint(0,8), random.randint(0,8)
        if board[r][c] != 0:
            board[r][c] = 0
            remove -= 1
    return board

# ---------- UI ----------
root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("600x750")
root.configure(bg="#0a192f")

tk.Label(root, text="🧩 SUDOKU SOLVER",
         font=("Segoe UI", 24, "bold"),
         fg="#38bdf8", bg="#0a192f").pack(pady=10)

top = tk.Frame(root, bg="#0a192f")
top.pack()

tk.Label(top, text="Difficulty:", fg="white", bg="#0a192f").pack(side="left")
difficulty = ttk.Combobox(top, values=["Easy","Medium","Hard"], width=10)
difficulty.current(0)
difficulty.pack(side="left", padx=5)

# ---------- MAIN FRAME ----------
main = tk.Frame(root, bg="#0a192f")
main.pack(pady=20)

cells = [[None]*9 for _ in range(9)]

# ---------- GRID WITH PERFECT ALIGNMENT ----------
for br in range(3):
    for bc in range(3):

        # rounded-looking box
        box = tk.Frame(main,
                       bg="#1e293b",
                       highlightbackground="#38bdf8",
                       highlightthickness=2,
                       bd=0)
        box.grid(row=br, column=bc, padx=8, pady=8)

        for i in range(3):
            for j in range(3):
                r = br*3 + i
                c = bc*3 + j

                e = tk.Entry(box,
                             width=2,
                             font=("Segoe UI", 20, "bold"),
                             justify="center",
                             bd=0,
                             bg="#0f172a",
                             fg="#7dd3fc",
                             insertbackground="white")

                e.grid(row=i, column=j, padx=4, pady=4)

                cells[r][c] = e

# ---------- FUNCTIONS ----------
def generate():
    board = generate_full()
    board = remove_numbers(board, difficulty.get())

    for i in range(9):
        for j in range(9):
            cells[i][j].delete(0, tk.END)
            if board[i][j] != 0:
                cells[i][j].insert(0, str(board[i][j]))
                cells[i][j].config(fg="#94a3b8")
            else:
                cells[i][j].config(fg="#38bdf8")

def solve_ui():
    board = [[0]*9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            val = cells[i][j].get()
            if val.isdigit():
                board[i][j] = int(val)

    if solve(board):
        for i in range(9):
            for j in range(9):
                cells[i][j].delete(0, tk.END)
                cells[i][j].insert(0, str(board[i][j]))
                cells[i][j].config(fg="#22c55e")

def clear():
    for i in range(9):
        for j in range(9):
            cells[i][j].delete(0, tk.END)

# ---------- BUTTONS ----------
btn = tk.Frame(root, bg="#0a192f")
btn.pack(pady=20)

tk.Button(btn, text="🎲 Generate", command=generate,
          bg="#3b82f6", fg="white").grid(row=0, column=0, padx=10)

tk.Button(btn, text="⚡ Solve", command=solve_ui,
          bg="#22c55e", fg="white").grid(row=0, column=1, padx=10)

tk.Button(btn, text="🗑 Clear", command=clear,
          bg="#ef4444", fg="white").grid(row=0, column=2, padx=10)

root.mainloop()