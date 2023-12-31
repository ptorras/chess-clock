"""Simple Raspberry pi chess clock implementation"""

import tkinter as tk
from tkinter import ttk

import time
import re

RE_NUMBER = re.compile(r"[0-9]*")


class ClockStatus:
    def __init__(
        self,
        left_time: int = 3000,
        left_inc: int = 0,
        right_time: int = 3000,
        right_inc: int = 0,
        left_plays: bool = True,
        running: bool = False,
    ):
        self._left_time = left_time
        self._left_inc = left_inc
        self._right_time = right_time
        self._right_inc = right_inc

        self._left_plays = left_plays
        self._running = running

        self._last_toggle = 0

    def tick(self):
        if self._running:
            delta = (int(time.time_ns()) - self._last_toggle) // int(1e8)
            self._last_toggle = int(time.time_ns())

            if self._left_plays:
                self._left_time -= delta

                if self._left_time <= 0:
                    self._left_time = 0
                    self._running = False
            else:
                self._right_time -= delta

                if self._right_time <= 0:
                    self._right_time = 0
                    self._running = False

    @property
    def left_minutes(self) -> int:
        return self._left_time // 600

    @left_minutes.setter
    def left_minutes(self, value: int) -> None:
        self._left_time = (self._left_time % 600) + (600 * value)

    @property
    def left_seconds(self) -> int:
        return (self._left_time % 600) // 10

    @left_seconds.setter
    def left_seconds(self, value: int) -> None:
        self._left_time = (
            (self._left_time // 600) * 600 + (value * 10) + (self._left_time % 10)
        )

    @property
    def left_tenths(self) -> int:
        return self._left_time % 10

    @left_tenths.setter
    def left_tenths(self, value: int) -> None:
        self._left_time = (self._left_time // 10) * 10 + value

    @property
    def left_increment(self) -> int:
        return self._left_inc // 10

    @left_increment.setter
    def left_increment(self, value: int) -> None:
        self._left_inc = value * 10

    @property
    def right_minutes(self) -> int:
        return self._right_time // 600

    @right_minutes.setter
    def right_minutes(self, value: int) -> None:
        self._right_time = (self._right_time % 600) + (600 * value)

    @property
    def right_seconds(self) -> int:
        return (self._right_time % 600) // 10

    @right_seconds.setter
    def right_seconds(self, value: int) -> None:
        self._right_time = (
            (self._right_time // 600) * 600 + (value * 10) + (self._right_time % 10)
        )

    @property
    def right_tenths(self) -> int:
        return self._right_time % 10

    @right_tenths.setter
    def right_tenths(self, value: int) -> None:
        self._right_time = (self._right_time // 10) * 10 + value

    @property
    def right_increment(self) -> int:
        return self._right_inc // 10

    @right_increment.setter
    def right_increment(self, value: int) -> None:
        self._right_inc = value * 10

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, value: bool) -> None:
        if self._left_time > 0 and self._right_time > 0:
            if value:
                self._last_toggle = int(time.time_ns())
            else:
                self.tick()
            self._running = value

    @property
    def left_plays(self) -> bool:
        return self._left_plays

    @left_plays.setter
    def left_plays(self, val: bool) -> None:
        self.tick()
        if self._running:
            if self._left_plays and self._left_time > 0:
                self._left_time += self._left_inc
            if not self._left_plays and self._right_time > 0:
                self._right_time += self._right_inc
        self._left_plays = val


class ChessClockApplication:
    GRAY_COLOR = "#bfbdbd"
    ACTIVE_COLOR = "#f58318"

    FONT_SIZE = 120

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(640, 480)
        self.root.title("Rellotge d'Escacs")

        self.status = ClockStatus()

        self.menu_bar = tk.Menu(self.root)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(menu=self.settings_menu, label="Configuració")
        self.settings_menu.add_command(
            label="Configura Rellotge...",
            command=self.configure,
        )

        self.root.config(menu=self.menu_bar)
        self.root.bind("<Return>", self._toggle_clock)
        self.root.bind("<space>", self._toggle_side)
        # self.config_dialog = ConfigureScreen(self.status)

        self.leftside = tk.Frame(self.root)
        self.rightside = tk.Frame(self.root)

        self.clock_text_left_content = tk.StringVar()
        self.clock_text_right_content = tk.StringVar()
        self.clock_text_left = ttk.Label(
            self.leftside,
            textvariable=self.clock_text_left_content,
            font=("Consolas", self.FONT_SIZE),
        )
        self.clock_text_right = ttk.Label(
            self.rightside,
            textvariable=self.clock_text_right_content,
            font=("Consolas", self.FONT_SIZE),
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

        self._update_clock()

    def configure(self) -> None:
        self.status.running = False
        self._draw_time()
        self._set_background()
        ConfigureScreen(self, self.status)
        return None

    def _draw_time(self) -> None:
        self.clock_text_left_content.set(
            f"{self.status.left_minutes:02d}"
            f":{self.status.left_seconds:02d}"
            f":{self.status.left_tenths: 01d}"
        )
        self.clock_text_right_content.set(
            f"{self.status.right_minutes:02d}"
            f":{self.status.right_seconds:02d}"
            f":{self.status.right_tenths: 01d}"
        )

    def _set_background(self) -> None:
        if self.status.running:
            if self.status.left_plays:
                self.leftside.configure(bg=self.ACTIVE_COLOR)
                self.rightside.configure(bg=self.GRAY_COLOR)
            else:
                self.leftside.configure(bg=self.GRAY_COLOR)
                self.rightside.configure(bg=self.ACTIVE_COLOR)
        else:
            self.leftside.configure(bg=self.GRAY_COLOR)
            self.rightside.configure(bg=self.GRAY_COLOR)

    def refresh_screen(self) -> None:
        self._draw_time()
        self._set_background()

    def _toggle_clock(self, event) -> None:
        self.status.running = not self.status.running
        self.refresh_screen()

    def _update_clock(self) -> None:
        self.status.tick()
        self.root.after(100, self._update_clock)
        self.refresh_screen()

    def _toggle_side(self, event) -> None:
        if self.status.running:
            self.status.left_plays = not self.status.left_plays
            self.refresh_screen()
        return None

    def main(self) -> None:
        self.root.mainloop()


class ConfigureScreen(tk.Toplevel):
    def __init__(self, parent: ChessClockApplication, status: ClockStatus) -> None:
        super().__init__()
        self.grab_set()
        self.resizable(False, False)
        self.title("Configuració")
        self.parent = parent
        self.clock_status = status
        self.validation_wrapper = (self.register(self._validate_input), "%P")

        self.left_area = tk.Frame(self)
        self.left_area["borderwidth"] = 2
        self.left_area["relief"] = "sunken"

        self.left_minutes_var = tk.StringVar()
        self.left_seconds_var = tk.StringVar()
        self.left_tenths_var = tk.StringVar()
        self.left_increment_var = tk.StringVar()

        self.left_minutes_var.set(f"{self.clock_status.left_minutes}")
        self.left_seconds_var.set(f"{self.clock_status.left_seconds}")
        self.left_tenths_var.set(f"{self.clock_status.left_tenths}")
        self.left_increment_var.set(f"{self.clock_status.left_increment}")

        self.left_minutes_dialog = tk.Entry(
            self.left_area,
            textvariable=self.left_minutes_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )
        self.left_seconds_dialog = tk.Entry(
            self.left_area,
            textvariable=self.left_seconds_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )
        self.left_tenths_dialog = tk.Entry(
            self.left_area,
            textvariable=self.left_tenths_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )
        self.left_increment_dialog = tk.Entry(
            self.left_area,
            textvariable=self.left_increment_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )

        self.left_minutes_label = tk.Label(self.left_area, text="Minuts")
        self.left_seconds_label = tk.Label(self.left_area, text="Segons")
        self.left_tenths_label = tk.Label(self.left_area, text="Dècimes")
        self.left_increment_label = tk.Label(self.left_area, text="Increment")

        self.right_area = tk.Frame(self)
        self.right_area["borderwidth"] = 2
        self.right_area["relief"] = "sunken"

        self.right_minutes_var = tk.StringVar()
        self.right_seconds_var = tk.StringVar()
        self.right_tenths_var = tk.StringVar()
        self.right_increment_var = tk.StringVar()

        self.right_minutes_var.set(f"{self.clock_status.right_minutes}")
        self.right_seconds_var.set(f"{self.clock_status.right_seconds}")
        self.right_tenths_var.set(f"{self.clock_status.right_tenths}")
        self.right_increment_var.set(f"{self.clock_status.right_increment}")

        self.right_minutes_dialog = tk.Entry(
            self.right_area,
            textvariable=self.right_minutes_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )
        self.right_seconds_dialog = tk.Entry(
            self.right_area,
            textvariable=self.right_seconds_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )
        self.right_tenths_dialog = tk.Entry(
            self.right_area,
            textvariable=self.right_tenths_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )
        self.right_increment_dialog = tk.Entry(
            self.right_area,
            textvariable=self.right_increment_var,
            validatecommand=self.validation_wrapper,
            validate="key",
        )

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

        self.cancel = tk.Button(self, text="Descarta", command=self._close_window)
        self.accept = tk.Button(self, text="Accepta", command=self._update_and_close)

        self.accept.grid(row=1, column=1)
        self.cancel.grid(row=1, column=0)

        self.radio_var = tk.StringVar()
        self.radio_var.set("left" if self.clock_status.left_plays else "right")
        self.radio_left = ttk.Radiobutton(
            self.left_area,
            text="<---",
            variable=self.radio_var,
            value="left",
        )
        self.radio_right = ttk.Radiobutton(
            self.right_area,
            text="--->",
            variable=self.radio_var,
            value="right",
        )
        self.radio_left.grid(row=4, column=0, padx=10, pady=10)
        self.radio_right.grid(row=4, column=0, padx=10, pady=10)

    def _close_window(self) -> None:
        self.grab_release()
        self.destroy()

    def _update_and_close(self) -> None:
        self.clock_status.left_increment = int(self.left_increment_var.get())
        self.clock_status.left_minutes = int(self.left_minutes_var.get())
        self.clock_status.left_seconds = int(self.left_seconds_var.get())
        self.clock_status.left_tenths = int(self.left_tenths_var.get())
        self.clock_status.right_increment = int(self.right_increment_var.get())
        self.clock_status.right_minutes = int(self.right_minutes_var.get())
        self.clock_status.right_seconds = int(self.right_seconds_var.get())
        self.clock_status.right_tenths = int(self.right_tenths_var.get())

        self.clock_status.left_plays = True if self.radio_var.get() == "left" else False

        self.parent._draw_time()
        self._close_window()

    @staticmethod
    def _validate_input(value: str) -> bool:
        match = RE_NUMBER.fullmatch(value)
        if match is not None:
            return True
        else:
            return False


if __name__ == "__main__":
    app = ChessClockApplication()
    app.main()
