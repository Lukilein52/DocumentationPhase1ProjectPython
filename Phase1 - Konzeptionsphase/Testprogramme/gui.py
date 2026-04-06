import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Test Window")
root.geometry("400x200")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

tk.Label(frame, text = "Progress")

# Progress bar test

progress = ttk.Progressbar(frame, orient = "horizontal", length = 200, mode = "determinate")
progress.pack()
progress["value"] = 65

root.mainloop()
