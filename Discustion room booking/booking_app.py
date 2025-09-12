import tkinter as tk
from home_page import HomePage
from check_availability_page import CheckAvailabilityPage
from book_room_page import BookRoomPage
from view_bookings_page import ViewBookingsPage

class BookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TarUMT Discussion Room Booking System")
        self.geometry("950x700")
        self.configure(bg="#f2f8ff")

        self.bookings = []
        self.frames = {}

        container = tk.Frame(self, bg="#f2f8ff")
        container.pack(fill="both", expand=True)

        for F in (HomePage, CheckAvailabilityPage, BookRoomPage, ViewBookingsPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
