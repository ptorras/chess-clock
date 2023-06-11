import tkinter as tk
from tkinter import ttk


class ChessClockApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(640, 480)
        self.leftside = tk.Frame(self.root)
        self.rightside = tk.Frame(self.root)
        self.clock_text_left = ttk.Label(
            self.leftside,
            text="Test Left",
            font=("Consolas", 50),
        )
        self.clock_text_right = ttk.Label(
            self.rightside,
            text="Test Right",
            font=("Consolas", 50),
        )

        self.leftside.configure(bg="#bfbdbd")
        self.rightside.configure(bg="#bfbdbd")

        self.leftside.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.S, tk.E))
        self.rightside.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.S, tk.E))

        self.clock_text_left.grid(column=0, row=0, padx=10, pady=10)
        self.clock_text_right.grid(column=0, row=0, padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.leftside.columnconfigure(0, weight=1)
        self.leftside.rowconfigure(0, weight=1)
        self.rightside.columnconfigure(0, weight=1)
        self.rightside.rowconfigure(0, weight=1)

    def main(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = ChessClockApplication()
    app.main()
