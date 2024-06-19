
import tkinter as tk
from tkinter import ttk
import pandas as pd

def truncate_col_name(col_name, max_length=20):
    """Truncate column names that are too long."""
    return (col_name[:max_length] + '...') if len(col_name) > max_length else col_name

def show_overview(df):
    overview_window = tk.Toplevel()
    overview_window.title("Overview Statistics")
    overview_window.configure(bg="black")
    overview_window.geometry("875x400")  # Set the fixed size of the window
    overview_window.minsize(875, 400)  # Set minimum size to prevent resizing smaller
    overview_window.maxsize(875, 400)  # Set maximum size to prevent resizing larger

    # Main frame to hold both statistics and column analysis
    main_frame = tk.Frame(overview_window, bg="black")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame for statistics on the left
    stats_frame = tk.Frame(main_frame, bg="black")
    stats_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    bold_font = ("Helvetica", 14, "bold")

    # Calculate statistics
    stats = {}

    # Number of columns and types
    stats['Number of Columns'] = df.shape[1]
    stats['Numeric Columns'] = df.select_dtypes(include=['number']).shape[1]
    stats['Categorical Columns'] = df.select_dtypes(include=['category', 'object']).shape[1]
    stats['Boolean Columns'] = df.select_dtypes(include=['bool']).shape[1]

    # Number of rows and duplicates
    stats['Number of Rows'] = df.shape[0]
    stats['Duplicate Rows'] = df.duplicated().sum()
    stats['Duplicate Rows %'] = round((df.duplicated().sum() / df.shape[0]) * 100, 4)

    # Missing cells
    stats['Number of Missing Cells'] = df.isnull().sum().sum()
    stats['Missing Cells %'] = round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 4)

    # Memory usage
    stats['Memory Usage (KB)'] = round(df.memory_usage(deep=True).sum() / 1024, 2)

    # Display statistics in the stats frame
    for key, value in stats.items():
        tk.Label(stats_frame, text=f"{key}: {value}", bg="black", fg="white", font=bold_font).pack(anchor="w", pady=2)

    # Frame for column analysis on the right with scrollbar and mouse wheel scrolling
    analysis_frame = tk.Frame(main_frame, bg="black")
    analysis_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(analysis_frame, bg="black")
    scrollbar = tk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Column analysis table headers
    headers = ["#", "Column Name", "Zeros Count", "Zeros %", "Null Count", "Null %"]

    for i, header in enumerate(headers):
        header_label = ttk.Label(scrollable_frame, text=header, font=("Helvetica", 12, "bold"))
        header_label.grid(row=0, column=i, padx=1, pady=1)

    # Column analysis data
    zeros_count = pd.Series({col: (df[col] == 0).sum() for col in df.columns})
    zeros_per = pd.Series({col: round((df[col] == 0).sum() / len(df) * 100, 2) for col in df.columns})
    missing_count = df.isnull().sum()
    missing_per = (df.isnull().sum() / len(df)) * 100

    for i, col in enumerate(df.columns):
        truncated_col = truncate_col_name(col)
        ttk.Label(scrollable_frame, text=str(i+1), font=("Helvetica", 12)).grid(row=i+1, column=0, padx=5, pady=2)
        ttk.Label(scrollable_frame, text=truncated_col, font=("Helvetica", 12)).grid(row=i+1, column=1, padx=5, pady=2)
        ttk.Label(scrollable_frame, text=zeros_count[col], font=("Helvetica", 12)).grid(row=i+1, column=2, padx=5, pady=2)
        ttk.Label(scrollable_frame, text=zeros_per[col], font=("Helvetica", 12)).grid(row=i+1, column=3, padx=5, pady=2)
        ttk.Label(scrollable_frame, text=missing_count[col], font=("Helvetica", 12)).grid(row=i+1, column=4, padx=5, pady=2)
        ttk.Label(scrollable_frame, text=round(missing_per[col], 2), font=("Helvetica", 12)).grid(row=i+1, column=5, padx=5, pady=2)

if __name__ == "__main__":
    # For testing purpose
    # df = pd.read_csv("BankChurners.csv")
    show_overview(df)
