from tkinter import *
from tkinter import ttk


class ChangeTimeForm:
    def __init__(self, root) -> None:
        self.form_window = TopLevel(root)

    def close(self) -> None:
        self.form_window.destroy()
