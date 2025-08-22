import tkinter as tk
from tkinter import ttk
import threading
import platform
import os

try:
    from pynput import keyboard
except ImportError:
    import tkinter.messagebox as messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", 'pynput not detected, please install it with the command "pip install pynput"')
    exit()
BG_COLOR = "#f0f0f0"
ACCENT_COLOR = "#4a6fa5"
SUCCESS_COLOR = "#2e8b57"
TEXT_COLOR = "#333333"
LIGHT_TEXT = "#666666"
root = tk.Tk()
root.title("Keyboard Tester")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg=BG_COLOR)
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=BG_COLOR)
style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
style.configure('Title.TLabel', font=("Arial", 16, "bold"), foreground=ACCENT_COLOR)
style.configure('Key.TLabel', font=("Arial", 14, "bold"), foreground=TEXT_COLOR)
style.configure('Status.TLabel', font=("Arial", 12), foreground=LIGHT_TEXT)
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)
title_label = ttk.Label(main_frame, text="Keyboard Tester", style="Title.TLabel")
title_label.pack(pady=(0, 20))
status_frame = ttk.Frame(main_frame)
status_frame.pack(pady=(20, 10))
canvas = tk.Canvas(status_frame, width=60, height=60, bg=BG_COLOR, highlightthickness=0)
canvas.pack()
indicator = canvas.create_oval(10, 10, 50, 50, fill="#cccccc", outline="")
ok_label = ttk.Label(status_frame, text="Press a key", style="Status.TLabel")
ok_label.pack(pady=(10, 0))
key_frame = ttk.Frame(main_frame)
key_frame.pack(pady=(20, 10))
ttk.Label(key_frame, text="Key detected:", style="Status.TLabel").pack()
key_label = ttk.Label(key_frame, text="", style="Key.TLabel")
key_label.pack(pady=(5, 0))
info_frame = ttk.Frame(main_frame)
info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))
version_label = ttk.Label(info_frame, text="Versión: 1.0", style="Status.TLabel")
version_label.pack(side=tk.LEFT)
platform_label = ttk.Label(info_frame, text=f"OS: {platform.system()}", style="Status.TLabel")
platform_label.pack(side=tk.RIGHT)
beep_running = False
def continuous_beep():
    global beep_running
    system_os = platform.system()
    while beep_running:
        if system_os == "Windows":
            import ctypes
            ctypes.windll.kernel32.Beep(1000, 100)
        elif system_os == "Linux":
            os.system('echo -e "\a"')
        root.after(100)
def on_press(key):
    global beep_running
    canvas.itemconfig(indicator, fill=SUCCESS_COLOR)
    ok_label.config(text="Key pressed")
    key_label.config(text=f"{key}")
    if not beep_running:
        beep_running = True
        threading.Thread(target=continuous_beep, daemon=True).start()
def on_release(key):
    global beep_running
    beep_running = False
    canvas.itemconfig(indicator, fill="#cccccc")
    ok_label.config(text="Press a key")
    key_label.config(text="")
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
root.mainloop()