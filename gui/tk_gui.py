import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Create main window
root = tk.Tk()
root.title("Analysis System")
root.geometry("400x200")

# Add a label
label = tk.Label(root, text="Welcome to Tkinter!", font=("Arial", 14))
label.pack(pady=10)

# Add an entry widget
entry = tk.Entry(root)
entry.pack(pady=5)

# Add a button
def greet():
    label.config(text=f"Hello, {entry.get()}!")

button = tk.Button(root, text="Greet", command=greet)
button.pack(pady=5)

# Add a combobox
combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"])
combo.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()