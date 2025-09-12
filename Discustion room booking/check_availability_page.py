import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar
from booking import VENUES
from home_page import styled_button

class CheckAvailabilityPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")
        self.controller = controller
        self.room_labels = {}

        tk.Label(self, text="🔍 Check Available Venues", font=("Arial", 16, "bold"), bg="#f2f8ff").pack(pady=10)
        form = tk.Frame(self, bg="#f2f8ff")
        form.pack(pady=5)

        # 日期选择
        tk.Label(form, text="Date:", bg="#f2f8ff").grid(row=0, column=0, sticky="e")
        frame_date = tk.Frame(form, bg="#f2f8ff")
        frame_date.grid(row=0, column=1, padx=10)

        years = [str(y) for y in range(datetime.today().year, datetime.today().year + 3)]
        self.year_combo = ttk.Combobox(frame_date, values=years, state="readonly", width=6)
        self.year_combo.grid(row=0, column=0, padx=2)
        self.year_combo.current(0)

        months = [str(m) for m in range(1, 13)]
        self.month_combo = ttk.Combobox(frame_date, values=months, state="readonly", width=4)
        self.month_combo.grid(row=0, column=1, padx=2)
        self.month_combo.current(datetime.today().month - 1)

        self.day_combo = ttk.Combobox(frame_date, state="readonly", width=4)
        self.day_combo.grid(row=0, column=2, padx=2)
        self.update_days()
        self.day_combo.current(datetime.today().day - 1)

        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.update_days())
        self.month_combo.bind("<<ComboboxSelected>>", lambda e: self.update_days())

        # 时间选择
        times = [f"{h:02d}:{m:02d}" for h in range(9, 20) for m in (0, 30)]
        tk.Label(form, text="Start Time:", bg="#f2f8ff").grid(row=1, column=0, sticky="e")
        self.start_combo = ttk.Combobox(form, values=times, state="readonly", width=10)
        self.start_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="End Time:", bg="#f2f8ff").grid(row=2, column=0, sticky="e")
        self.end_combo = ttk.Combobox(form, values=times, state="readonly", width=10)
        self.end_combo.grid(row=2, column=1, padx=10, pady=5)

        styled_button(self, "Check", self.show_available).pack(pady=10)

        # 外层容器（用来居中显示房间表格）
        self.center_frame = tk.Frame(self, bg="#f2f8ff")
        self.center_frame.pack(fill="both", expand=True)

        self.venue_frame = tk.Frame(self.center_frame, bg="#f2f8ff")
        self.venue_frame.pack(pady=10)

        # 状态说明
        Notice_frame = tk.Frame(self, bg="#f2f8ff")
        Notice_frame.pack(pady=10)
        tk.Label(Notice_frame, text="Notice:", font=("Arial", 12, "bold"), bg="#f2f8ff").pack(side="left", padx=5)
        tk.Label(Notice_frame, text="Available", bg="white", width=10, relief="groove").pack(side="left", padx=5)
        tk.Label(Notice_frame, text="Booked", bg="#4a90e2", fg="white", width=10, relief="groove").pack(side="left", padx=5)

        styled_button(self, "⬅ Back", lambda: controller.show_frame("HomePage"), color="red").pack(pady=10)

    def update_days(self):
        try:
            year = int(self.year_combo.get())
            month = int(self.month_combo.get())
            days_in_month = calendar.monthrange(year, month)[1]
            self.day_combo["values"] = [str(d) for d in range(1, days_in_month + 1)]
        except Exception:
            pass

    def show_available(self):
        year = self.year_combo.get()
        month = self.month_combo.get()
        day = self.day_combo.get()
        start = self.start_combo.get()
        end = self.end_combo.get()
        if not year or not month or not day or not start or not end:
            messagebox.showerror("Error", "Please select date and time first.")
            return
        date = f"{year}-{int(month):02d}-{int(day):02d}"

        # 清空旧内容
        for widget in self.venue_frame.winfo_children():
            widget.destroy()
        self.room_labels.clear()

        row = 0
        for venue, rooms in VENUES.items():
            tk.Label(self.venue_frame, text=venue, font=("Arial", 14, "bold"), bg="#f2f8ff").grid(row=row, column=0, sticky="w", pady=5, columnspan=len(rooms))
            row += 1
            for i, room in enumerate(rooms):
                status = "Available"
                color = "white"
                booking_info = None
                for b in self.controller.bookings:
                    if b.date == date and b.venue == venue and b.room == room:
                        if not (end <= b.start or start >= b.end):
                            status = "Booked"
                            color = "#4a90e2"
                            booking_info = b
                            break
                lbl = tk.Label(self.venue_frame, text=room, width=10, height=2,
                               bg=color, relief="groove", font=("Arial", 10, "bold"))
                lbl.grid(row=row, column=i, padx=5, pady=5)
                lbl.bind("<Button-1>", lambda e, s=status, v=venue, r=room, b=booking_info, d=date, st=start, et=end: self.show_details(s, v, r, b, d, st, et))
                self.room_labels[(venue, room)] = lbl
            row += 1

    def show_details(self, status, venue, room, booking_info, date, start, end):
        if status == "Available":
            messagebox.showinfo("Room Available", f"✅ {venue}-{room} is available!\n\nDate: {date}\nTime: {start} - {end}")
        else:
            messagebox.showinfo("Room Booked", f"❌ {venue}-{room} is already booked!\n\n"
                                               f"Name: {booking_info.name}\n"
                                               f"ID: {booking_info.sid}\n"
                                               f"Date: {booking_info.date}\n"
                                               f"Time: {booking_info.start} - {booking_info.end}\n"
                                               f"Pax: {booking_info.pax}")
