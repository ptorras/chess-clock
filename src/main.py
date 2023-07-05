"""Simple Raspberry pi chess clock implementation"""

import tkinter as tk
from tkinter import ttk

import time


class ClockStatus:
    def __init__(
        self,
        left_time: int = 3000,
        left_inc: int = 0,
        right_time: int = 3000,
        right_inc: int = 0,
    ):
        self.left_time = left_time
        self.left_inc = left_inc
        self.right_time = right_time
        self.right_inc = right_inc


class ChessClockApplication:
    GRAY_COLOR = "#bfbdbd"

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(640, 480)

        self.status = ClockStatus()

        self.menu_bar = tk.Menu(self.root)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(menu=self.settings_menu, label="Configuració")
        self.settings_menu.add_command(
            label="Configura Rellotge...",
            command=lambda: ConfigureScreen(
                self.status,
            ),
        )

        self.root.config(menu=self.menu_bar)
        # self.config_dialog = ConfigureScreen(self.status)

        self.leftside = tk.Frame(self.root)
        self.rightside = tk.Frame(self.root)

        self.clock_text_left_content = tk.StringVar()
        self.clock_text_right_content = tk.StringVar()
        self.clock_text_left = ttk.Label(
            self.leftside,
            textvariable=self.clock_text_left_content,
            font=("Consolas", 50),
        )
        self.clock_text_right = ttk.Label(
            self.rightside,
            textvariable=self.clock_text_right_content,
            font=("Consolas", 50),
        )

        self.leftside.configure(bg=self.GRAY_COLOR)
        self.rightside.configure(bg=self.GRAY_COLOR)

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

        self._draw_time()

    def _draw_time(self):
        self.clock_text_left_content.set(
            self._format_time(self.status.left_time),
        )
        self.clock_text_right_content.set(
            self._format_time(self.status.right_time),
        )

    @staticmethod
    def _format_time(ticks: int) -> str:
        """Formats time from integer to mm:ss:d.

        Parameters
        ----------
        time : int
            The time value in integer form (tenths of second).

        Returns
        -------
        str
            An output string in format mm:ss:d.
        """
        minutes = ticks // 600
        seconds = (ticks % minutes) // 10
        tenths = ticks % 10

        return f"{minutes:02d}:{seconds:02d}:{tenths:01d}"

    def main(self) -> None:
        self.root.mainloop()


class ConfigureScreen(tk.Toplevel):
    def __init__(self, status: ClockStatus) -> None:
        super().__init__()
        self.title = "Configuració"
        self.clock_status = status

        self.left_area = tk.Frame(self)

        self.left_minutes_dialog = tk.Entry(self.left_area)
        self.left_seconds_dialog = tk.Entry(self.left_area)
        self.left_tenths_dialog = tk.Entry(self.left_area)
        self.left_increment_dialog = tk.Entry(self.left_area)

        self.left_minutes_label = tk.Label(self.left_area, text="Minuts")
        self.left_seconds_label = tk.Label(self.left_area, text="Segons")
        self.left_tenths_label = tk.Label(self.left_area, text="Dècimes")
        self.left_increment_label = tk.Label(self.left_area, text="Increment")

        self.right_area = tk.Frame(self)

        self.right_minutes_dialog = tk.Entry(self.right_area)
        self.right_seconds_dialog = tk.Entry(self.right_area)
        self.right_tenths_dialog = tk.Entry(self.right_area)
        self.right_increment_dialog = tk.Entry(self.right_area)

        self.right_minutes_label = tk.Label(self.right_area, text="Minuts")
        self.right_seconds_label = tk.Label(self.right_area, text="Segons")
        self.right_tenths_label = tk.Label(self.right_area, text="Dècimes")
        self.right_increment_label = tk.Label(self.right_area, text="Increment")

        self.left_area.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.S, tk.E))
        self.right_area.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.S, tk.E))

        self.left_minutes_dialog.grid(row=0, column=1, padx=10, pady=10)
        self.left_seconds_dialog.grid(row=1, column=1, padx=10, pady=10)
        self.left_tenths_dialog.grid(row=2, column=1, padx=10, pady=10)
        self.left_increment_dialog.grid(row=3, column=1, padx=10, pady=10)

        self.left_minutes_label.grid(row=0, column=0, padx=10, pady=10)
        self.left_seconds_label.grid(row=1, column=0, padx=10, pady=10)
        self.left_tenths_label.grid(row=2, column=0, padx=10, pady=10)
        self.left_increment_label.grid(row=3, column=0, padx=10, pady=10)

        self.right_minutes_dialog.grid(row=0, column=1, padx=10, pady=10)
        self.right_seconds_dialog.grid(row=1, column=1, padx=10, pady=10)
        self.right_tenths_dialog.grid(row=2, column=1, padx=10, pady=10)
        self.right_increment_dialog.grid(row=3, column=1, padx=10, pady=10)

        self.right_minutes_label.grid(row=0, column=0, padx=10, pady=10)
        self.right_seconds_label.grid(row=1, column=0, padx=10, pady=10)
        self.right_tenths_label.grid(row=2, column=0, padx=10, pady=10)
        self.right_increment_label.grid(row=3, column=0, padx=10, pady=10)

        self.cancel = tk.Button(self, text="Descarta")
        self.accept = tk.Button(self, text="Accepta")

        self.accept.grid(row=1, column=1)
        self.cancel.grid(row=1, column=0)


if __name__ == "__main__":
    app = ChessClockApplication()
    app.main()
