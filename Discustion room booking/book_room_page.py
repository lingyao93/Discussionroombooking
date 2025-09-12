import tkinter as tk
from tkinter import messagebox, ttk
from booking import VENUES, Booking
from datetime import datetime
from styled_button import styled_button   # 改成 styled.py
import calendar 

class BookRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")
        self.controller = controller

        center_frame = tk.Frame(self, bg="#f2f8ff")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="📝 Book a Room", font=("Arial", 16, "bold"), bg="#f2f8ff").pack(pady=10)
        form = tk.Frame(center_frame, bg="#f2f8ff")
        form.pack(pady=5)
        labels = ["Name:", "Student ID:", "Venue Category:", "Date:", "Start Time:", "End Time:", "Pax:"]
        self.entries = {}
        pax_options = [str(i) for i in range(1, 11)]
        for i, lbl in enumerate(labels):
            tk.Label(form, text=lbl, bg="#f2f8ff").grid(row=i, column=0, sticky="e", pady=5)
            if lbl == "Venue Category:":
                self.venue_combo = ttk.Combobox(form, values=list(VENUES.keys()), state="readonly", width=23)
                self.venue_combo.grid(row=i, column=1, padx=10)
                self.venue_combo.current(0)
                self.entries[lbl] = self.venue_combo
            elif lbl == "Date:":
                frame_date = tk.Frame(form, bg="#f2f8ff")
                frame_date.grid(row=i, column=1, padx=10)
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
            elif lbl == "Pax:":
                cb = ttk.Combobox(form, values=pax_options, state="readonly", width=23)
                cb.grid(row=i, column=1, padx=10)
                cb.current(0)
                self.entries[lbl] = cb
            elif "Time" in lbl:
                times = [f"{h:02d}:{m:02d}" for h in range(9, 20) for m in (0, 30)]
                cb = ttk.Combobox(form, values=times, state="readonly", width=23)
                cb.grid(row=i, column=1, padx=10)
                self.entries[lbl] = cb
            else:
                e = tk.Entry(form, width=25)
                e.grid(row=i, column=1, padx=10)
                self.entries[lbl] = e

        styled_button(center_frame, "✅ Book Now", self.book_room, color="blue").pack(pady=15)

        terms_text = (
            "Terms of Use:\n"
            "1. Artwork, role-play, video shooting and/or any other disruptive activities are not allowed in the Library.\n"
            "2. Discussion Rooms are solely intended for written assignments only.\n"
            "3. Presentation Room is strictly to be used for presentation purposes only.\n"
            "4. Users using the Discussion Room and Presentation Room shall discuss softly.\n"
            "5. Library staff reserve the right to conduct occasional spot checks of the rooms.\n"
            "6. Return the room key and complete the check-out process on time.\n"
            "7. Users shall clear all belongings and books from the room while leaving.\n"
            "8. Arrange tables and chairs to their original position.\n"
            "9. Shut down the PC or LCD projector, if applicable.\n"
            "10. Switch off the lights.\n"
            "11. Lock the room upon leaving."
        )
        tk.Label(center_frame, text=terms_text, font=("Arial", 9), bg="#f2f8ff", fg="#555", justify="left", anchor="w").pack(pady=10)

        # ✅ 统一返回按钮，放在底部
        styled_button(self, "⬅ Back", lambda: controller.show_frame("HomePage"), color="red").pack(side="bottom", pady=15)

    def update_days(self):
        try:
            year = int(self.year_combo.get())
            month = int(self.month_combo.get())
            days_in_month = calendar.monthrange(year, month)[1]
            self.day_combo["values"] = [str(d) for d in range(1, days_in_month + 1)]
        except Exception:
            pass

    def book_room(self):
        name = self.entries["Name:"].get()
        sid = self.entries["Student ID:"].get()
        venue = self.venue_combo.get()
        year = self.year_combo.get()
        month = self.month_combo.get()
        day = self.day_combo.get()
        date = f"{year}-{int(month):02d}-{int(day):02d}"
        start = self.entries["Start Time:"].get()
        end = self.entries["End Time:"].get()
        pax = self.entries["Pax:"].get()
        if not all([name, sid, venue, year, month, day, start, end, pax]):
            messagebox.showerror("Error", "All fields are required")
            return
        assigned_room = None
        for room in VENUES[venue]:
            conflict = False
            for b in self.controller.bookings:
                if b.venue == venue and b.room == room and b.date == date:
                    if not (end <= b.start or start >= b.end):
                        conflict = True
                        break
            if not conflict:
                assigned_room = room
                break
        if not assigned_room:
            messagebox.showerror("Error", f"No available rooms in {venue} for this time slot!")
            return
        booking = Booking(name, sid, venue, assigned_room, date, start, end, pax)
        self.controller.bookings.append(booking)
        messagebox.showinfo("Booking Successful",
                            f"✅ Successful!\n\n"
                            f"Venue: {venue}-{assigned_room}\n"
                            f"Date: {date}\n"
                            f"Time: {start} - {end}\n"
                            f"Pax: {pax}")
