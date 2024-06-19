

import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

def Variables(df):
    def calculate_stats(column):
        col_data = df[column]
        if pd.api.types.is_numeric_dtype(col_data):
            stats = {
                'Distinct': col_data.nunique(),
                'Distinct (%)': col_data.nunique() / len(col_data) * 100,
                'Missing': col_data.isnull().sum(),
                'Missing (%)': col_data.isnull().mean() * 100,
                'Mean': col_data.mean(),
                'Minimum': col_data.min(),
                'Maximum': col_data.max(),
                'Zeros': (col_data == 0).sum(),
                'Zeros (%)': (col_data == 0).mean() * 100,
                'Negative': (col_data < 0).sum(),
                'Negative (%)': (col_data < 0).mean() * 100,
                'Memory Size (bytes)': col_data.memory_usage(deep=True)
            }
        else:
            stats = {
                'Distinct': col_data.nunique(),
                'Distinct (%)': col_data.nunique() / len(col_data) * 100,
                'Missing': col_data.isnull().sum(),
                'Missing (%)': col_data.isnull().mean() * 100,
                'Memory Size (bytes)': col_data.memory_usage(deep=True)
            }
        return pd.DataFrame(stats, index=[column])

    def update_stats(event):
        selected_column = column_dropdown.get()
        if selected_column == "Select Column":
            # Clear label and statistics display
            stats_text.delete('1.0', tk.END)
            return

        stats_df = calculate_stats(selected_column)
        stats_df_transposed = stats_df.T

        # Clear previous statistics
        stats_text.delete('1.0', tk.END)

        # Display statistics for the selected column
        stats_text.insert(tk.END, f"Statistics for Column: {selected_column}\n\n")
        for i, (stat, value) in enumerate(stats_df_transposed.iterrows()):
            bg_color = "#f0f0f0" if i % 2 == 0 else "#d9d9d9"
            stats_text.insert(tk.END, f"{stat}: {value[0]}\n", "normal")
            stats_text.tag_add(str(i), f"{i + 2}.0", f"{i + 2}.0 lineend")
            stats_text.tag_config(str(i), background=bg_color)

        # If the column is non-numeric, display value counts with colored bars
        if not pd.api.types.is_numeric_dtype(df[selected_column]):
            stats_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            stats_text.insert(tk.END, f"Value Counts for Column: {selected_column}\n\n")

            value_counts = df[selected_column].value_counts()
            max_count = value_counts.max()

            # Define colors for each unique value
            colors = ["#FF6347", "#7B68EE", "#32CD32", "#FFD700", "#4169E1", "#FFA500", "#6A5ACD", "#00FFFF", "#FF69B4", "#DAA520"]
            color_index = 0

            for i, (value, count) in enumerate(value_counts.items()):
                bar_length = int((count / max_count) * 30)
                bar = "█" * bar_length
                value_str = f"{bar} ({count})  {value}\n"

                # Add the value with a colored background
                stats_text.insert(tk.END, value_str, "normal")
                stats_text.tag_add(f"value_{i}", tk.END)
                stats_text.tag_config(f"value_{i}", background=colors[color_index % len(colors)])
                color_index += 1

    # Create the Variables window
    variables_window = tk.Toplevel()
    variables_window.title("Variables Statistics")
    variables_window.configure(bg="black")

    label = tk.Label(variables_window, text="Variables:", bg="black", fg="white", font=("Helvetica", 14))
    label.pack(pady=10)

    column_names = ["Select Column"] + list(df.columns)
    column_dropdown = ttk.Combobox(variables_window, values=column_names, state="readonly")
    column_dropdown.current(0)
    column_dropdown.pack(pady=10)
    column_dropdown.bind("<<ComboboxSelected>>", update_stats)

    stats_text = tk.Text(variables_window, wrap='word', height=20, width=60, bg="white", fg="black", font=("Helvetica", 12))
    stats_text.pack(pady=10)

# If you want to test Variables.py independently, you can add this block:
if __name__ == "__main__":
    # Example DataFrame creation
    np.random.seed(0)
    df = pd.DataFrame({
        'Category': np.random.choice(['A', 'B', 'C'], size=100),
        'Numeric': np.random.randint(0, 100, size=100),
        'Boolean': np.random.choice([True, False], size=100)
    })

    Variables(df)