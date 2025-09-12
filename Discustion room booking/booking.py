VENUES = {
    "Library": ["L001", "L002", "L003", "L004", "L005"],
    "Cyber Centre": ["C001", "C002", "C003", "C004", "C005"]
}

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
        return (self.name, self.sid, f"{self.venue}-{self.room}", self.date, f"{self.start}-{self.end}", self.pax)
