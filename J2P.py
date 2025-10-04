#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
J2P GUI (PAGE-generated) — Tkinter toplevel and widgets.
Defines the window layout and delegates behavior to J2P_support.main().
Adds a gray placeholder to Entry1: "leave empty for default name".
"""

import os  # For locating theme files relative to this file
import sys  # For platform check (Windows styling)
import tkinter as tk  # Tkinter base widgets
import tkinter.ttk as ttk  # Themed Tkinter widgets

# Support module providing main() and logic callbacks
import J2P_support

# Absolute directory of this file (used for optional theme)
_LOCATION = os.path.dirname(__file__)

# Basic colors used by widgets and tooltip
_BGCOLOR = "#d9d9d9"
_FGCOLOR = "#000000"

# Style guard to prevent re-initializing ttk style multiple times
_style_initialized = False


def _init_style(root):
    """Initialize ttk style and optionally load a local theme once."""
    global _style_initialized
    if _style_initialized:
        return

    # Try to source a local default.tcl theme if available (optional)
    try:
        root.tk.call("source", os.path.join(_LOCATION, "themes", "default.tcl"))
    except Exception:
        pass  # It’s fine if themes/default.tcl does not exist

    style = ttk.Style()
    # Prefer native Windows theme if on win32, else default
    style.theme_use("winnative" if sys.platform == "win32" else "default")
    style.configure(".", font="TkDefaultFont")

    _style_initialized = True


def add_placeholder(entry, text="leave empty for default name", color="gray"):
    """
    Add a gray placeholder to a tk.Entry.
    - Inserts placeholder when empty and out-of-focus.
    - Clears on focus if placeholder is present.
    - Restores if left empty on blur.
    """
    normal_fg = entry.cget("fg") or _FGCOLOR

    def on_focus_in(_):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg=normal_fg)

    def on_focus_out(_):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg=color)

    # Initialize with placeholder
    entry.insert(0, text)
    entry.config(fg=color)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


class Toplevel1:
    """
    Configure and populate the main toplevel window (created by PAGE).
    Exposes: Entry1, ListBox, TButton1 (Convert), TButton2 (Select), TButton3 (Clear).
    """

    def __init__(self, top=None):
        # Window geometry and base styling
        top.geometry("320x266+778+304")
        top.minsize(320, 266)
        top.maxsize(3844, 1061)
        top.resizable(True, True)
        top.title("J2P")
        top.configure(background=_BGCOLOR, highlightbackground=_BGCOLOR, highlightcolor=_FGCOLOR)

        # Keep reference to the toplevel
        self.top = top

        # Labeled container for the whole UI
        self.Labelframe1 = tk.LabelFrame(
            self.top,
            text="J2P",
            background=_BGCOLOR,
            foreground=_FGCOLOR,
            highlightbackground=_BGCOLOR,
            highlightcolor=_FGCOLOR,
            relief="groove",
        )
        self.Labelframe1.place(relx=0.033, rely=0.023, relheight=0.94, relwidth=0.915)

        # Bottom control area (Entry + Select/Convert/Clear buttons)
        self.Frame1 = tk.Frame(
            self.Labelframe1,
            background=_BGCOLOR,
            relief="groove",
            borderwidth=2,
            highlightbackground=_BGCOLOR,
            highlightcolor=_FGCOLOR,
        )
        self.Frame1.place(relx=0.036, rely=0.6, relheight=0.356, relwidth=0.911, bordermode="ignore")

        # Label for the PDF name entry
        self.Label2 = tk.Label(
            self.Frame1,
            text="Name of PDF file :",
            anchor="w",
            background=_BGCOLOR,
            foreground=_FGCOLOR,
            highlightbackground=_BGCOLOR,
            highlightcolor=_FGCOLOR,
        )
        self.Label2.place(relx=0.090, rely=0.101, height=13, width=160)

        # Entry where the user can type a target PDF name (optional)
        self.Entry1 = tk.Entry(
            self.Frame1,
            background=_BGCOLOR,
            foreground=_FGCOLOR,
            insertbackground=_FGCOLOR,
            selectbackground=_BGCOLOR,
            selectforeground=_FGCOLOR,
            exportselection=False,
            font="TkDefaultFont",
            cursor="xterm",
        )
        self.Entry1.place(relx=0.100, rely=0.315, height=20, relwidth=0.8)

        # Tooltip text near Entry1 (kept for UX parity)
        self.Entry1_tooltip = ToolTip(self.Entry1, "leave empty for default name")

        # Add gray placeholder behavior to Entry1
        add_placeholder(self.Entry1, "leave empty for default name")

        # Initialize ttk style before creating ttk widgets
        _init_style(self.top)

        # "Select" button
        self.TButton2 = ttk.Button(self.Frame1, text="Select", takefocus=False)
        self.TButton2.place(relx=0.100, rely=0.629, relwidth=0.264, relheight=0.3)

        # "Convert" button
        self.TButton1 = ttk.Button(self.Frame1, text="Convert", takefocus=False)
        self.TButton1.place(relx=0.640, rely=0.629, relwidth=0.264, relheight=0.3)

        # Middle area showing selected files and status messages
        self.Frame2 = tk.LabelFrame(
            self.Labelframe1,
            text="Selected Files :",
            background=_BGCOLOR,
            foreground=_FGCOLOR,
            highlightbackground=_BGCOLOR,
            highlightcolor=_FGCOLOR,
            relief="groove",
            borderwidth=2,
        )
        self.Frame2.place(relx=0.036, rely=0.084, relheight=0.46, relwidth=0.911, bordermode="ignore")

        # Text area used as a simple log for filenames and status
        self.ListBox = tk.Text(
            self.Frame2,
            background=_BGCOLOR,
            foreground=_FGCOLOR,
            highlightbackground=_BGCOLOR,
            highlightcolor=_FGCOLOR,
            font="TkDefaultFont",
        )
        self.ListBox.place(relx=0.039, rely=0.087, relwidth=0.9, relheight=0.8)

        # "Clear" button
        self.TButton3 = ttk.Button(self.Frame1, text="Clear", takefocus=False)
        self.TButton3.place(relx=0.37, rely=0.629, relwidth=0.264, relheight=0.3)


# Lightweight tooltip implementation used by PAGE exports
from time import time as _time


class ToolTip(tk.Toplevel):
    """Simple tooltip that appears near a widget after a small delay."""

    def __init__(self, wdgt, msg=None, msgFunc=None, delay=0.5, follow=True):
        self.wdgt = wdgt               # Widget the tooltip belongs to
        self.parent = self.wdgt.master # Parent window
        super().__init__(self.parent, bg="black", padx=1, pady=1)
        self.withdraw()                # Start hidden
        self.overrideredirect(True)    # No window decorations

        # Message content handling
        self.msgVar = tk.StringVar(value=msg or "No message provided")
        self.msgFunc = msgFunc         # Optional dynamic text provider
        self.delay = delay             # Delay before showing
        self.follow = follow           # Whether tooltip follows mouse
        self.visible = 0               # 0 hidden, 1 pending, 2 shown
        self.lastMotion = 0            # For delay logic

        # The message widget that displays tooltip text
        self.msg = tk.Message(self, textvariable=self.msgVar, bg=_BGCOLOR,
                              fg=_FGCOLOR, font="TkTooltipFont", aspect=1000)
        self.msg.grid()

        # Mouse bindings to control tooltip lifecycle
        self.wdgt.bind("<Enter>", self.spawn, "+")
        self.wdgt.bind("<Leave>", self.hide, "+")
        self.wdgt.bind("<Motion>", self.move, "+")

    def spawn(self, event=None):
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        if self.visible == 1 and _time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        self.lastMotion = _time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        # Position tooltip near cursor
        self.geometry(f"+{event.x_root + 20}+{event.y_root - 10}")
        # Update message from function if provided
        try:
            if self.msgFunc:
                self.msgVar.set(self.msgFunc())
        except Exception:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        self.msgVar.set(msg)

    def configure(self, **kwargs):
        """Optional styling updates for the tooltip message."""
        current_text = self.msgVar.get()
        background = kwargs.pop("background", kwargs.pop("bg", None))
        foreground = kwargs.pop("foreground", kwargs.pop("fg", None))
        fontd = kwargs.pop("font", None)
        text = kwargs.pop("text", None)
        reliefd = kwargs.pop("relief", "flat")
        justifyd = kwargs.pop("justify", "left")
        padxd = kwargs.pop("padx", 1)
        padyd = kwargs.pop("pady", 1)
        borderwidthd = kwargs.pop("borderwidth", 2)

        if text is not None:
            self.msgVar.set(text if text.strip() else current_text)

        wid = self.msg
        if background is not None:
            wid.config(bg=background)
        if foreground is not None:
            wid.config(fg=foreground)
        wid.config(font=fontd, borderwidth=borderwidthd, relief=reliefd,
                   justify=justifyd, padx=padxd, pady=padyd)


def start_up():
    """Entrypoint: delegate to support module main()."""
    J2P_support.main()


if __name__ == "__main__":
    # When run directly, start via the support module
    J2P_support.main()
