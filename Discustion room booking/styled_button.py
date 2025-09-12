import tkinter as tk

def styled_button(master, text, command, color="blue"):
    if color == "red":
        bg, abg = "#e74c3c", "#c0392b"
    elif color == "green":
        bg, abg = "#27ae60", "#1e8449"
    elif color == "orange":
        bg, abg = "#e67e22", "#ca6f1e"
    else:
        bg, abg = "#4a90e2", "#357ABD"
    return tk.Button(master, text=text, command=command,
                     bg=bg, fg="white",
                     activebackground=abg, activeforeground="white",
                     font=("Arial", 12, "bold"),
                     relief="flat", padx=10, pady=5, width=18)