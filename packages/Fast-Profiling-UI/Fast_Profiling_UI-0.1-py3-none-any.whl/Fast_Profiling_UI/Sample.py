
import tkinter as tk
from tkinter import ttk
import pandas as pd

def Sample(df):
    def show_sample(event):
        sample_option = sample_dropdown.get()
        if sample_option == "Select Sample":
            return

        for i in tree.get_children():
            tree.delete(i)

        if sample_option == "top_5":
            sample_data = df.head(5)
        elif sample_option == "top_10":
            sample_data = df.head(10)
        elif sample_option == "top_20":
            sample_data = df.head(20)
        elif sample_option == "bottom_5":
            sample_data = df.tail(5)
        elif sample_option == "bottom_10":
            sample_data = df.tail(10)
        elif sample_option == "bottom_20":
            sample_data = df.tail(20)

        for idx, row in sample_data.iterrows():
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=[idx] + list(row), tags=(tag,))

    # Create the Sample window
    sample_window = tk.Toplevel()
    sample_window.title("Sample Data")
    sample_window.configure(bg="black")

    label = tk.Label(sample_window, text="Sample:", bg="black", fg="white", font=("Helvetica", 14))
    label.pack(pady=10)

    sample_options = ["Select Sample", "top_5", "top_10", "top_20", "bottom_5", "bottom_10", "bottom_20"]
    sample_dropdown = ttk.Combobox(sample_window, values=sample_options, state="readonly")
    sample_dropdown.current(0)
    sample_dropdown.pack(pady=10)
    sample_dropdown.bind("<<ComboboxSelected>>", show_sample)

    frame = tk.Frame(sample_window)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    columns = ["Index"] + list(df.columns)
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.pack(side="left", fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(sample_window, orient="horizontal", command=tree.xview)
    hsb.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hsb.set)

    tree.tag_configure('oddrow', background='#f0f0f0')
    tree.tag_configure('evenrow', background='#ffffff')

if __name__ == "__main__":
    Sample(df)
