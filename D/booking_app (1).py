import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

VENUES = {
    "Library": ["L001", "L002", "L003", "L004", "L005"],
    "Cyber Centre": ["C001", "C002", "C003", "C004", "C005"]
}


# booking class
class Booking:
    def __init__(self, name, sid, venue, room, date, start, end, pax):
        self.name = name.strip()
        self.sid = sid.strip()
        self.venue = venue.strip()
        self.room = room.strip()
        self.date = date.strip()
        self.start = start.strip()
        self.end = end.strip()
        self.pax = pax

    def to_tuple(self):
        return (self.name, self.sid, f"{self.venue}-{self.room}",
                self.date, f"{self.start}-{self.end}", self.pax)


class BookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TarUMT Discussion Room Booking System")
        self.geometry("900x650")
        self.minsize(700, 500)
        self.configure(bg="#f2f8ff")

        self.bookings = []
        self.frames = {}

        container = tk.Frame(self, bg="#f2f8ff")
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (HomePage, CheckAvailabilityPage, BookRoomPage, ViewBookingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()


def styled_button(master, text, command):
    return tk.Button(master, text=text, command=command,
                     bg="#4a90e2", fg="white",
                     activebackground="#357ABD", activeforeground="white",
                     font=("Arial", 12, "bold"),
                     relief="flat", padx=10, pady=5, width=18)


# Homepage
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = tk.Frame(self, bg="#f2f8ff")
        center_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(center_frame, text="📚 Welcome to TarUMT Discussion Room Booking",
                 font=("Arial", 20, "bold"), bg="#f2f8ff", fg="#333").pack(pady=40)

        styled_button(center_frame, "Check Venues", lambda: controller.show_frame(CheckAvailabilityPage)).pack(pady=10)
        styled_button(center_frame, "Book a Room", lambda: controller.show_frame(BookRoomPage)).pack(pady=10)
        styled_button(center_frame, "View Bookings", lambda: controller.show_frame(ViewBookingsPage)).pack(pady=10)


# Check Availability
class CheckAvailabilityPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")
        self.controller = controller
        self.room_buttons = {}

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="🔍 Check Available Venues",
                 font=("Arial", 16, "bold"), bg="#f2f8ff").grid(row=0, column=0, pady=10)

        # legend (green/red)
        legend = tk.Frame(self, bg="#f2f8ff")
        legend.grid(row=1, column=0, pady=5)
        tk.Label(legend, text="🟩 Available", bg="#f2f8ff", fg="green", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        tk.Label(legend, text="🟥 Booked", bg="#f2f8ff", fg="red", font=("Arial", 10, "bold")).pack(side="left", padx=10)

        form = tk.Frame(self, bg="#f2f8ff")
        form.grid(row=2, column=0, sticky="n")

        tk.Label(form, text="Date (YYYY-MM-DD):", bg="#f2f8ff").grid(row=0, column=0, sticky="e")
        self.date_entry = tk.Entry(form, width=25)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        times = [f"{h:02d}:{m:02d}" for h in range(9, 20) for m in (0, 30)]
        tk.Label(form, text="Start Time:", bg="#f2f8ff").grid(row=1, column=0, sticky="e")
        self.start_combo = ttk.Combobox(form, values=times, state="readonly", width=23)
        self.start_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="End Time:", bg="#f2f8ff").grid(row=2, column=0, sticky="e")
        self.end_combo = ttk.Combobox(form, values=times, state="readonly", width=23)
        self.end_combo.grid(row=2, column=1, padx=10, pady=5)

        styled_button(self, "Check", self.show_available).grid(row=3, column=0, pady=10)

        self.venue_frame = tk.Frame(self, bg="#f2f8ff")
        self.venue_frame.grid(row=4, column=0, sticky="nsew", pady=10)
        self.grid_rowconfigure(4, weight=1)

        styled_button(self, "⬅ Back", lambda: controller.show_frame(HomePage)).grid(row=5, column=0, pady=10)

    def show_available(self):
        date = self.date_entry.get()
        start = self.start_combo.get()
        end = self.end_combo.get()

        if not date or not start or not end:
            messagebox.showerror("Error", "Please enter date and time first.")
            return

        # 🔽 sort bookings by date + start time before checking availability
        self.controller.bookings.sort(
            key=lambda x: (datetime.strptime(x.date, "%Y-%m-%d"), x.start)
        )

        for widget in self.venue_frame.winfo_children():
            widget.destroy()
        self.room_buttons.clear()

        row = 0
        for venue, rooms in VENUES.items():
            tk.Label(self.venue_frame, text=venue,
                     font=("Arial", 14, "bold"), bg="#f2f8ff").grid(row=row, column=0, columnspan=5, pady=5)
            row += 1

            for i, room in enumerate(rooms):
                status = "Available"
                color = "#27ae60"  # green
                for b in self.controller.bookings:
                    if b.date == date and b.venue == venue and b.room == room:
                        if not (end <= b.start or start >= b.end):
                            status = "Booked"
                            color = "#e74c3c"  # red
                            break

                btn = tk.Button(self.venue_frame, text=room,
                                width=10, height=2, bg=color, fg="white",
                                font=("Arial", 10, "bold"),
                                command=lambda v=venue, r=room, s=status: self.show_info(v, r, s))
                btn.grid(row=row, column=i, padx=10, pady=5)
                self.room_buttons[(venue, room)] = btn
            row += 1

    def show_info(self, venue, room, status):
        messagebox.showinfo("Room Info", f"Venue: {venue}\nRoom: {room}\nStatus: {status}")


# Book Venue
class BookRoomPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")
        self.controller = controller

        tk.Label(self, text="📝 Book a Room", font=("Arial", 16, "bold"), bg="#f2f8ff").pack(pady=10)

        form = tk.Frame(self, bg="#f2f8ff")
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
                e = tk.Entry(form, width=25)
                e.grid(row=i, column=1, padx=10)
                self.entries[lbl] = e
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

        styled_button(self, "✅ Book Now", self.book_room).pack(pady=15)
        styled_button(self, "⬅ Back", lambda: controller.show_frame(HomePage)).pack()

    def book_room(self):
        name = self.entries["Name:"].get()
        sid = self.entries["Student ID:"].get()
        venue = self.venue_combo.get()
        date = self.entries["Date:"].get()
        start = self.entries["Start Time:"].get()
        end = self.entries["End Time:"].get()
        pax = self.entries["Pax:"].get()

        if not all([name, sid, venue, date, start, end, pax]):
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

        # 🔽 sort bookings by date + start time after adding
        self.controller.bookings.sort(
            key=lambda x: (datetime.strptime(x.date, "%Y-%m-%d"), x.start)
        )

        messagebox.showinfo("Booking Successful",
                            f"✅ Successful!\n\n"
                            f"Venue: {venue}-{assigned_room}\n"
                            f"Date: {date}\n"
                            f"Time: {start} - {end}\n"
                            f"Pax: {pax}")


# Check Booking
class ViewBookingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f8ff")
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="📑 Booking Records", font=("Arial", 16, "bold"), bg="#f2f8ff").grid(row=0, column=0, pady=10)

        columns = ("Name", "ID", "Venue", "Date", "Time", "Pax")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew", pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        btn_frame = tk.Frame(self, bg="#f2f8ff")
        btn_frame.grid(row=2, column=0, pady=5)

        styled_button(btn_frame, "🔄 Refresh", self.load_records).grid(row=0, column=0, padx=5)
        styled_button(btn_frame, "✏ Edit", self.edit_record).grid(row=0, column=1, padx=5)
        styled_button(btn_frame, "❌ Delete", self.delete_record).grid(row=0, column=2, padx=5)
        styled_button(btn_frame, "⬅ Back", lambda: controller.show_frame(HomePage)).grid(row=0, column=3, padx=5)

    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 🔽 sort before showing (date + start time)
        self.controller.bookings.sort(
            key=lambda x: (datetime.strptime(x.date, "%Y-%m-%d"), x.start)
        )

        for b in self.controller.bookings:
            self.tree.insert("", "end", values=b.to_tuple())

    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a record")
            return None
        index = self.tree.index(sel[0])
        return index

    def edit_record(self):
        idx = self.get_selected()
        if idx is None:
            return
        booking = self.controller.bookings[idx]

        new_name = simpledialog.askstring("Edit", "Enter new name:", initialvalue=booking.name)
        if new_name:
            booking.name = new_name
        new_pax = simpledialog.askstring("Edit", "Enter new pax:", initialvalue=booking.pax)
        if new_pax:
            booking.pax = new_pax

        # 🔽 re-sort after editing
        self.controller.bookings.sort(
            key=lambda x: (datetime.strptime(x.date, "%Y-%m-%d"), x.start)
        )
        self.load_records()

    def delete_record(self):
        idx = self.get_selected()
        if idx is None:
            return
        confirm = messagebox.askyesno("Confirm", "Delete this record?")
        if confirm:
            del self.controller.bookings[idx]
            self.load_records()


if __name__ == "__main__":
    app = BookingApp()
    app.mainloop()