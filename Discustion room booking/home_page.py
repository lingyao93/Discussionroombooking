import tkinter as tk
from styled_button import styled_button

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")

        # 撑满的容器
        container = tk.Frame(self, bg="#f2f8ff")
        container.grid(row=0, column=0, sticky="nsew")

        # 让 container 居中
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 中心框架
        center_frame = tk.Frame(container, bg="#f2f8ff")
        center_frame.grid(row=0, column=0)

        tk.Label(center_frame, text="Welcome!", font=("Arial", 20, "bold"), bg="#f2f8ff").pack(pady=20)

        styled_button(center_frame, "Check Availability", lambda: controller.show_frame("CheckAvailabilityPage"), "blue").pack(pady=10)
        styled_button(center_frame, "Book Room", lambda: controller.show_frame("BookRoomPage"), "green").pack(pady=10)
        styled_button(center_frame, "View Bookings", lambda: controller.show_frame("ViewBookingsPage"), "orange").pack(pady=10)
