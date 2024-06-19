from tkinter import ttk, font as tkFont, messagebox
import tkinter as tk
import pandas as pd
import Sample as sp  # Import Sample.py as a module
import Variables as var  # Import Variables.py as a module
import Overview  # Import Overview.py module

def de_analysis(df):  ## Data Engineer Analysis 
    window = tk.Tk()
    window.title("Automatic EDA")
    window.configure(bg="black")
    window.geometry("800x600") 

    bold_font = tkFont.Font(family="Helvetica", size=24, weight="bold")

    overview_button = tk.Button(window, text="Overview", fg="white", bg="green", font=bold_font, cursor="hand2", command=lambda: Overview.show_overview(df), relief='raised', bd=5)
    overview_button.pack(pady=20)

    Missing_values_button = tk.Button(window, text="Missing Values", fg="white", bg="blue", font=bold_font, cursor="hand2", command=lambda: Missing(df), relief='raised', bd=5)
    Missing_values_button.pack(pady=20)

    Variable_button = tk.Button(window, text="Variable", fg="white", bg="#008CBA", font=bold_font, cursor="hand2", command=lambda: var.Variables(df), relief='raised', bd=5)
    Variable_button.pack(pady=20)

    Sample_button = tk.Button(window, text="Sample", command=lambda: sp.Sample(df), bg="#4682B4", fg="white", font=("Arial", 14, "bold"), cursor="hand2", relief='raised', bd=5)
    Sample_button.pack(pady=20, ipadx=20, ipady=10)

    window.mainloop()

if __name__ == "__main__":
    de_analysis(df)
