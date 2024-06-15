"""
A simple and dirty `blosc_reader` file reader and plotter.

The reader can read a `blp` file containing a collection of list and can plot them as per selection.
The `blosc_reader` is made in response to the signal writing capability of `create_gw_signal` in my PhD GW repository.

Created on Jun 15 05:10:48 2024
"""

import pickle
import tkinter as tk
from tkinter import filedialog, ttk
from typing import List

import blosc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = []


def blosc_reader():
    """A simple and dirty `blosc_reader` file reader and plotter."""

    def decompress_and_read(input_file: str) -> list:
        """
        Decompress the selected `blosc_reader` file and read it.

        Parameters
        ----------
        input_file : str
            Path to the compressed file.

        Returns
        -------
        list
            A list of data arrays/lists extracted from the file.
        """
        with open(input_file, 'rb') as temp_:
            compressed_ = temp_.read()

        serialized_ = blosc.decompress(compressed_)
        return pickle.loads(serialized_)

    def browse_file():
        """
        Browse for the `blosc_reader` file and load its data.

        This function opens a file dialog to select a `blosc_reader` file,
        decompresses and reads its contents, and populates the dropdown
        menu with the data lists from the file.
        """

        file_path = filedialog.askopenfilename(filetypes=[("BLP files", "*.blp")])
        if file_path:
            global data
            data = decompress_and_read(file_path)
            populate_dropdown(data)

    def populate_dropdown(data_: List[list]):
        """
        Populate the dropdown menu with data arrays/lists from the blosc_reader file.

        Parameters
        ----------
        data_ : List[list]
            List of data arrays/lists to be added to the dropdown menu.
        """

        options = [f"Data List {i + 1}" for i in range(len(data_))]
        dropdown['values'] = options
        dropdown.current(0)
        plot_data(data_[0])

    def on_dropdown_select(event: tk.Event):
        """
        Handle dropdown menu selection event.

        Parameters
        ----------
        event : tk.Event
            The event object representing the selection event.
        """

        selected_index = dropdown.current()
        plot_data(data[selected_index])

    def plot_data(data_list: list):
        """
        Plot the data from the selected file.

        Parameters
        ----------
        data_list : list
            The data list to be plotted.
        """

        fig, ax = plt.subplots()
        ax.plot(data_list)
        ax.grid('on')
        ax.set_title("Signal Plot")
        ax.set_xlabel("Time")
        ax.set_ylabel("Amplitude")
        fig.tight_layout()

        for widget in plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def on_closing():
        """Close the running task and exit the application when the window is closed."""

        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("BLP File Browser")
    window.protocol("WM_DELETE_WINDOW", on_closing)

    browse_button_frame = tk.Frame(window)
    browse_button_frame.pack(padx=20, pady=20)

    browse_button = tk.Button(browse_button_frame, text="Browse for BLP File", command=browse_file)
    browse_button.pack()

    dropdown_frame = tk.Frame(window)
    dropdown_frame.pack(padx=20, pady=20)

    dropdown = ttk.Combobox(dropdown_frame, state="readonly")
    dropdown.pack()
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

    plot_frame = tk.Frame(window)
    plot_frame.pack(fill=tk.BOTH, expand=1)

    window.mainloop()


if __name__ == '__main__':
    blosc_reader()
