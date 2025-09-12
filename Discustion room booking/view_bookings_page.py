import tkinter as tk
from tkinter import ttk
from styled_button import styled_button

class ViewBookingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")
        self.controller = controller

        container = tk.Frame(self, bg="#f2f8ff")
        container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = tk.Frame(container, bg="#f2f8ff")
        center_frame.grid(row=0, column=0)

        tk.Label(center_frame, text="View All Bookings", font=("Arial", 20, "bold"), bg="#f2f8ff", fg="#003366").pack(pady=20)

        # 表格
        columns = ("Name", "Student ID", "Venue", "Date", "Time", "Pax")
        self.tree = ttk.Treeview(center_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")

        self.tree.pack(pady=20)

        # 按钮
        button_frame = tk.Frame(center_frame, bg="#f2f8ff")
        button_frame.pack(pady=10)

        styled_button(button_frame, "Refresh", self.refresh, color="blue").grid(row=0, column=0, padx=10)
        styled_button(button_frame, "Back", lambda: controller.show_frame("HomePage"), color="red").grid(row=0, column=1, padx=10)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for b in self.controller.bookings:
            self.tree.insert("", tk.END, values=b.to_tuple())
