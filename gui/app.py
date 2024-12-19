import tkinter as tk
from tkinter import ttk, filedialog
from asammdf import MDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Analysis System")
        self.root.geometry("200x200")

        # Add button to open file dialog
        self.button = tk.Button(self.root, text="Select File", command=self.open_new_window)
        self.button.pack(pady=20)
        self.file_path = None

    def open_file(self):
        """
        Open a file dialog to select a file.
        """
        self.file_path = tk.filedialog.askopenfilename(
            filetypes=[("MF4 files", "*.mf4")],
            title="Select MF4 file"
        )
        print(self.file_path)
        
    def open_new_window(self):
        """
        Open a new window to display the MF4 file.
        """
        self.open_file()
        new_window = mf4ViewerApp(self.file_path, self.root)

    def run(self):
        self.root.mainloop()

class mf4ViewerApp(tk.Toplevel):
    def __init__(self, file_path, master=None):
        super().__init__(master)
        self.data = MDF(file_path)
        self.title("MF4 Viewer")
        self.geometry("800x600")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Treeview to display signals
        self.tree = ttk.Treeview(self, columns=("Name", "Unit"), show="headings")
        self.tree.heading("Name", text="Signal name")
        self.tree.heading("Unit", text="Unit")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.populate_treeview()

        # Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(fill=tk.BOTH, expand=True)

        # Button to plot selected signal
        self.plot_button = ttk.Button(self, text="Plot Signal", command=self.plot_signal)
        self.plot_button.pack(pady=20)

    def populate_treeview(self):
        """
        Populate the treeview with signals from the MF4 file.
        """
        for channel_group in self.data.groups:
            for channel in channel_group.channels:
                self.tree.insert("", "end", values=(channel.name, channel.unit))

    def plot_signal(self):
        """
        Plot the selected signal.
        """
        selected = self.tree.selection()
        if selected:
            signal_name = self.tree.item(selected)["values"][0]
            signal_data = self.data[signal_name].samples
            self.ax.clear()
            self.ax.plot(signal_data)
            self.ax.set_title(signal_name)
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Value")
            self.canvas.draw()