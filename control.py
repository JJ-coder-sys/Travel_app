import sqlite3 as sql
import control as connect
from tkinter import ttk


con = sql.connect("travel.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# Users
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    gender TEXT NOT NULL,
    address TEXT NOT NULL,
    dob TEXT NOT NULL,
    role TEXT NOT NULL
)
""")
#Bookings
cur.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    pickup_location TEXT NOT NULL,
    destination TEXT NOT NULL,
    vehicle_type TEXT NOT NULL,
    fare REAL NOT NULL,
    booking_status TEXT DEFAULT 'Pending',
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# ADD NEW COLUMNS TO THE BOOKINGS TABLE

connect.cur.execute("PRAGMA table_info(bookings)")
columns = [column[1] for column in connect.cur.fetchall()]

if "booking_type" not in columns:
    connect.cur.execute(
        "ALTER TABLE bookings ADD COLUMN booking_type TEXT DEFAULT 'Passenger'"
    )

if "passenger_count" not in columns:
    connect.cur.execute("ALTER TABLE bookings ADD COLUMN passenger_count INTEGER")

if "goods_type" not in columns:
    connect.cur.execute("ALTER TABLE bookings ADD COLUMN goods_type TEXT")

if "load_size" not in columns:
    connect.cur.execute("ALTER TABLE bookings ADD COLUMN load_size TEXT")


# Add new fields
def add_column_if_missing(table_name, column_name, column_type):
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cur.fetchall()]
    if column_name not in columns:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")


add_column_if_missing("users", "availability", "TEXT DEFAULT 'Available'")
add_column_if_missing("bookings", "driver_id", "INTEGER REFERENCES users(id)")
add_column_if_missing("bookings", "pickup_park", "TEXT")
add_column_if_missing("bookings", "estimated_arrival", "TEXT")

cur.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    booking_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT,
    is_read INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS motor_parks (
    park_id INTEGER PRIMARY KEY AUTOINCREMENT,
    town TEXT NOT NULL,
    park_name TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    UNIQUE(town, park_name)
)
""")

# Motor Parks
starter_parks = [
    ("Ado-Ekiti", "New Garage"),
    ("Ado-Ekiti", "Ikare Garage"),
    ("Ado-Ekiti", "Akure Garage"),
    ("Ifaki-Ekiti", "Ifaki Garage"),
    ("Ido-Ekiti", "Ido Central"),
    ("Ikole-Ekiti", "Ikole Central"),
    ("Oye-Ekiti", "Oye Central"),
    ("Ikere-Ekiti", "Old Garage"),
    ("Ijero-Ekiti", "Ijero Central"),
    ("Aramoko-Ekiti", "Aramoko Central"),
    ("Ilawe-Ekiti", "Ilawe Park"),
    ("Ode-Ekiti", "Ode Garage"),
    ("Iworoko-Ekiti", "Iworoko Park"),
    ("Igede-Ekiti", "Igede Park"),
    ("Iyin-Ekiti", "Iyin Park"),
    ("Igbemo-Ekiti", "Igbemo Park"),
    ("Itapa-Ekiti", "Itapa Park"),
    ("Efon-Alaaye", "Efon Central Park"),
    ("Okemesi-Ekiti", "Okemesi Park"),
    ("Ise-Ekiti", "Ise Park"),
    ("Emure-Ekiti", "Emure Park"),
    ("Omuo-Ekiti", "Omuo Park"),
    ("Ijan-Ekiti", "Ijan Park"),
    ("Aisegba-Ekiti", "Aisegba Park"),
    ("Imesi-Ekiti", "Imesi Park"),
    ("Ora-Ekiti", "Ora Park"),
]
for town, park_name in starter_parks:
    cur.execute(
        "INSERT OR IGNORE INTO motor_parks (town, park_name) VALUES (?, ?)",
        (town, park_name),
    )

# Booking notification for customer
cur.execute("""
CREATE TRIGGER IF NOT EXISTS new_booking_notification
AFTER INSERT ON bookings
BEGIN
    INSERT INTO notifications (user_id, booking_id, title, message, status)
    VALUES (
        NEW.user_id,
        NEW.booking_id,
        'Booking Received',
        'Your ride from ' || NEW.pickup_location || ' (' || COALESCE(NEW.pickup_park, 'park not set') || ') to ' || NEW.destination || ' has been booked.',
        COALESCE(NEW.booking_status, 'Pending')
    );
END
""")

cur.execute("""
CREATE TRIGGER IF NOT EXISTS booking_status_notification
AFTER UPDATE OF booking_status ON bookings
WHEN OLD.booking_status IS NOT NEW.booking_status
BEGIN
    INSERT INTO notifications (user_id, booking_id, title, message, status)
    VALUES (
        NEW.user_id,
        NEW.booking_id,
        CASE lower(COALESCE(NEW.booking_status, 'pending'))
            WHEN 'pending' THEN 'Booking Pending'
            WHEN 'accepted' THEN 'Booking Accepted'
            WHEN 'in progress' THEN 'Ride Started'
            WHEN 'completed' THEN 'Ride Completed'
            WHEN 'cancelled' THEN 'Booking Cancelled'
            WHEN 'rejected' THEN 'Booking Rejected'
            ELSE 'Booking Updated'
        END,
        'Your ride from ' || NEW.pickup_location || ' to ' || NEW.destination || ' is now ' || COALESCE(NEW.booking_status, 'Pending') || '.',
        COALESCE(NEW.booking_status, 'Pending')
    );
END
""")

cur.execute("""
CREATE TRIGGER IF NOT EXISTS driver_arrival_notification
AFTER UPDATE OF estimated_arrival ON bookings
WHEN NEW.estimated_arrival IS NOT NULL
AND NEW.estimated_arrival != ''
AND OLD.estimated_arrival IS NOT NEW.estimated_arrival
BEGIN
    INSERT INTO notifications (user_id, booking_id, title, message, status)
    VALUES (
        NEW.user_id,
        NEW.booking_id,
        'Driver Arrival Time Updated',
        'Your driver is expected at ' || COALESCE(NEW.pickup_park, NEW.pickup_location) || ' at ' || NEW.estimated_arrival || '.',
        COALESCE(NEW.booking_status, 'Pending')
    );
END
""")

# Admin
cur.execute("""
    INSERT OR IGNORE INTO users
    (name, username, email, password, gender, address, dob, role)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "System Administrator",
    "john",
    "obamomijohn@gmail.com",
    "ya8nemi@",
    "Other",
    "Admin Office",
    "2007-24-12",
    "admin"
))


con.commit()
