import tkinter as tk
from tkinter import ttk

def apply_dark_theme(window):
    style = ttk.Style(window)

    window.configure(bg="#2e2e2e")
    style.theme_use("clam")

    style.configure("TLabel", background="#2e2e2e", foreground="white")
    style.configure("TButton", background="#444444", foreground="white")
    style.configure("TEntry", fieldbackground="#3e3e3e", foreground="white")
    style.configure("TCombobox", fieldbackground="#3e3e3e", foreground="white")

    # Treeview dark theme
    style.configure("Treeview",
                    background="#3e3e3e",
                    fieldbackground="#3e3e3e",
                    foreground="white",
                    bordercolor="#3e3e3e",
                    borderwidth=1)
    style.configure("Treeview.Heading", background="#444444", foreground="white")
