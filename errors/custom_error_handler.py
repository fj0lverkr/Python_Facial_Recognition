import tkinter as tk
from tkinter.messagebox import showerror


class Ntk(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))
