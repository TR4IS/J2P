Here’s your file with the easter egg fully removed and no remaining references to it.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image(s) to PDF stitcher (Tkinter + Pillow)
- Select PNG/JPG images, auto-fit to A4 pages, export a multi-page PDF.
- Minimal PAGE-generated UI integration via J2P.Toplevel1.
"""

import os  # OS utilities for username and path ops
import tkinter as tk  # Tkinter core
from tkinter import filedialog as fd  # File picker dialogs
from datetime import datetime  # Timestamp-based output name
from PIL import Image  # Pillow image handling

# Global state for selected/composed pages
imgs = []  # List[Image.Image] holding composed page-sized PIL images


def main():
    """Create root window, PAGE toplevel, and wire callbacks."""
    global root, _w1
    root = tk.Tk()  # Root Tk window
    root.protocol("WM_DELETE_WINDOW", root.destroy)  # Graceful close

    # Build PAGE-generated top-level UI
    import J2P  # Local PAGE-generated module containing Toplevel1 and start_up
    _w1 = J2P.Toplevel1(root)  # Construct UI under root

    # Disable editing in the log ListBox-like Text widget
    _w1.ListBox.config(state="disabled")

    # Wire UI buttons to functions
    _w1.TButton1.configure(command=convert)       # "Convert" button
    _w1.TButton2.configure(command=select_files)  # "Select Files" button
    _w1.TButton3.configure(command=clear_files)   # "Clear Files" button

    root.mainloop()  # Start Tk event loop


def convert():
    """Export selected/composed images as a single multi-page PDF."""
    global imgs

    # No images selected case
    if not imgs:
        _set_log("No Files to Convert.")
        return

    # Resolve output path
    user = os.getlogin()  # Current Windows user name
    # Read desired filename from Entry (user-provided name)
    name_of_file = _w1.Entry1.get().strip()
    # Fallback to timestamp-based name if entry is blank
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Final output destination under Downloads/image
    base_dir = f"C:/Users/{user}/Downloads/image"  # Output folder
    os.makedirs(base_dir, exist_ok=True)  # Ensure directory exists
    output_path = os.path.join(
        base_dir,
        f"{name_of_file if name_of_file else stamp}.pdf"
    )

    # Save multi-page PDF; imgs[0] is first page, rest are appended
    imgs[0].save(output_path, save_all=True, append_images=imgs[1:])

    # Notify user and open the resulting PDF with default app
    _set_log("Done!")

    # Clear the list after converting
    imgs = []
    try:
        os.startfile(output_path)  # Windows-specific open
    except Exception:
        # Silently ignore if shell open fails (e.g., restricted env)
        pass


def clear_files():
    """Clear selected images/pages and reset state."""
    global imgs

    if not imgs:
        _set_log("No Files to Clear.")
        return

    imgs = []  # Reset the in-memory pages list
    _set_log("Done!")


def select_files():
    """Open a file dialog, load images, fit each onto an A4 page, and queue."""
    # Ask for multiple image files (PNG/JPG/JPEG)
    file_paths = fd.askopenfilenames(
        title="Select Images",
        initialdir="~",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )
    # Clear before printing the files
    _set_log("")

    # If user cancels, do nothing
    if not file_paths:
        return

    # Append each selected image as a centered, resized A4 page
    for idx, path in enumerate(file_paths, start=1):
        img = Image.open(path).convert("RGB")  # Ensure RGB for PDF
        page = _compose_on_a4(img)  # Fit onto A4 canvas
        imgs.append(page)  # Store page in global queue

        # Append a log line with file name
        _append_log_line(f" - File {idx} : {os.path.basename(path)}")


def _compose_on_a4(img, bg="white"):
    """Return a new A4-sized RGB page with the image centered and fitted."""
    # A4 at 300 DPI: 2480x3508 pixels (width x height)
    a4_w, a4_h = 2480, 3508
    fitted = _resize_fit(img, a4_w, a4_h)  # Maintain aspect ratio
    page = Image.new("RGB", (a4_w, a4_h), bg)  # Create blank A4 canvas
    # Compute top-left anchor to center the fitted image on the page
    x = (a4_w - fitted.width) // 2
    y = (a4_h - fitted.height) // 2
    page.paste(fitted, (x, y))  # Paste image onto the page
    return page


def _resize_fit(image, max_width, max_height):
    """Resize image to fit within max dimensions while preserving aspect ratio."""
    img_ratio = image.width / image.height  # Original aspect ratio
    target_ratio = max_width / max_height   # Target area aspect ratio

    # Choose scaling by width or height depending on which dimension limits first
    if img_ratio > target_ratio:
        # Wider than target: limit by width
        new_width = max_width
        new_height = int(max_width / img_ratio)
    else:
        # Taller/narrower than target: limit by height
        new_height = max_height
        new_width = int(max_height * img_ratio)

    # High-quality down/up-sampling with LANCZOS filter
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def _set_log(text, auto_clear_ms=None):
    """Replace entire log with text and optionally auto-clear after delay."""
    _w1.ListBox.config(state="normal")          # Make editable for programmatic write
    _w1.ListBox.delete("1.0", "end")            # Clear all text
    _w1.ListBox.insert("1.0", text)             # Insert message
    _w1.ListBox.config(state="disabled")        # Lock editing again
    if auto_clear_ms:
        _w1.ListBox.after(auto_clear_ms, _clear_log)  # Schedule clear


def _append_log_line(text):
    """Append a line to the log (keeps existing content)."""
    _w1.ListBox.config(state="normal")          # Make editable
    _w1.ListBox.insert("end", text + "\n")      # Append line
    _w1.ListBox.config(state="disabled")        # Lock editing


def _clear_log():
    """Clear the log text area."""
    _w1.ListBox.config(state="normal")          # Make editable
    _w1.ListBox.delete("1.0", "end")            # Remove all content
    _w1.ListBox.config(state="disabled")        # Lock editing


if __name__ == "__main__":
    # Boot the PAGE-generated app start-up, which should call main()
    # If J2P.start_up() already creates the UI and calls main,
    # keep this as-is per the PAGE workflow used by the project.
    import J2P  # Local PAGE-generated module
    J2P.start_up()  # Delegates to PAGE runner which should invoke main()
```
