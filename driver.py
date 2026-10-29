from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter.simpledialog import askstring
import sys
import subprocess
import re
import control as connect

# DRIVER ACCOUNT
driver_id = None
if len(sys.argv) > 1:
    try:
        driver_id = int(sys.argv[1])
    except ValueError:
        driver_id = None

BG = "#f4f7fb"
NAVY = "#12355b"
BLUE = "#2878b8"
BLUE_DARK = "#1d568d"
WHITE = "#ffffff"
TEXT = "#1f2937"
MUTED = "#64748b"
BORDER = "#dce4ee"
GREEN = "#238636"
RED = "#c0392b"
ORANGE = "#d97706"

root = Tk()
root.title("Driver")
root.geometry("1100x700")
root.configure(bg=BG)
root.resizable(False, False)
active_page = "Dashboard"
nav_buttons = {}

sidebar = Frame(root, bg=NAVY, width=225)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)
main_area = Frame(root, bg=BG)
main_area.pack(side=LEFT, fill=BOTH, expand=True)
header = Frame(
    main_area, bg=WHITE, height=72, highlightbackground=BORDER, highlightthickness=1
)
header.pack(side=TOP, fill=X)
header.pack_propagate(False)
header_title = Label(
    header, text="Dashboard", font=("Arial", 18, "bold"), bg=WHITE, fg=NAVY
)
header_title.pack(side=LEFT, padx=26)
header_right = Frame(header, bg=WHITE)
header_right.pack(side=RIGHT, padx=22)
notification_button = Button(
    header_right,
    text="♧ Notifications",
    font=("Arial", 10, "bold"),
    bg="#edf4fb",
    fg=NAVY,
    activebackground="#dbeafe",
    relief=FLAT,
    cursor="hand2",
    command=lambda: notifications_page(),
)
notification_button.pack(side=LEFT, padx=(0, 14), ipady=8, ipadx=8)
driver_name_label = Label(
    header_right, text="Driver", font=("Arial", 10, "bold"), bg=WHITE, fg=TEXT
)
driver_name_label.pack(side=LEFT)
content_holder = Frame(main_area, bg=BG)
content_holder.pack(fill=BOTH, expand=True)
page_canvas = Canvas(content_holder, bg=BG, highlightthickness=0)
page_scrollbar = ttk.Scrollbar(
    content_holder, orient=VERTICAL, command=page_canvas.yview
)
page_canvas.configure(yscrollcommand=page_scrollbar.set)
page_scrollbar.pack(side=RIGHT, fill=Y)
page_canvas.pack(side=LEFT, fill=BOTH, expand=True)
content_frame = Frame(page_canvas, bg=BG)
canvas_window = page_canvas.create_window((0, 0), window=content_frame, anchor="nw")


def update_scroll_region(event=None):
    page_canvas.configure(scrollregion=page_canvas.bbox("all"))


def resize_content(event):
    page_canvas.itemconfigure(canvas_window, width=event.width)


content_frame.bind("<Configure>", update_scroll_region)
page_canvas.bind("<Configure>", resize_content)


def scroll_page(event):
    page_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


page_canvas.bind_all("<MouseWheel>", scroll_page)


def clear_page(page_name=None):
    global active_page
    for widget in content_frame.winfo_children():
        widget.destroy()
    if page_name:
        active_page = page_name
        header_title.config(text=page_name)
        set_active_button(page_name)
    page_canvas.yview_moveto(0)


def set_active_button(page_name):
    for name, button in nav_buttons.items():
        button.config(
            bg=BLUE if name == page_name else NAVY,
            fg=WHITE if name == page_name else "#e8eef6",
        )


def page_heading(title, subtitle):
    Label(content_frame, text=title, font=("Arial", 23, "bold"), bg=BG, fg=NAVY).pack(
        anchor="w", padx=28, pady=(25, 4)
    )
    Label(content_frame, text=subtitle, font=("Arial", 10), bg=BG, fg=MUTED).pack(
        anchor="w", padx=28, pady=(0, 20)
    )


def make_card(parent, padx=18, pady=16):
    return Frame(
        parent,
        bg=WHITE,
        padx=padx,
        pady=pady,
        highlightbackground=BORDER,
        highlightthickness=1,
    )


def styled_button(parent, text, command, color=BLUE):
    return Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=BLUE_DARK,
        activeforeground=WHITE,
        relief=FLAT,
        cursor="hand2",
        padx=14,
        pady=8,
    )


def get_driver():
    if driver_id is None:
        return None
    try:
        connect.cur.execute(
            "SELECT name, availability FROM users WHERE id = ? AND LOWER(role) = 'driver'",
            (driver_id,),
        )
        return connect.cur.fetchone()
    except Exception:
        return None


def get_unread_count():
    if driver_id is None:
        return 0
    try:
        connect.cur.execute(
            "SELECT COUNT(*) FROM notifications WHERE user_id = ? AND COALESCE(is_read, 0) = 0",
            (driver_id,),
        )
        return connect.cur.fetchone()[0]
    except Exception:
        return 0


def refresh_header():
    driver = get_driver()
    driver_name_label.config(text=(driver[0] if driver and driver[0] else "Driver"))
    count = get_unread_count()
    notification_button.config(
        text=f"♧ Notifications ({count})" if count else "♧ Notifications"
    )


def logout():
    if msg.askyesno("Logout", "Are you sure you want to log out?"):
        root.destroy()
        subprocess.Popen([sys.executable, "login.py"])


def dashboard():
    clear_page("Dashboard")
    driver = get_driver()
    name = driver[0].split()[0] if driver and driver[0] else "Driver"
    page_heading(
        f"Welcome👋🏽, {name}",
        "Organise your work and improve your performance with us here!",
    )
    pending = active = completed = 0
    earnings_total = 0
    try:
        connect.cur.execute(
            "SELECT COUNT(*) FROM bookings WHERE LOWER(booking_status) = 'pending' AND driver_id IS NULL"
        )
        pending = connect.cur.fetchone()[0]
        connect.cur.execute(
            "SELECT COUNT(*) FROM bookings WHERE driver_id = ? AND LOWER(booking_status) IN ('accepted', 'in progress')",
            (driver_id,),
        )
        active = connect.cur.fetchone()[0]
        connect.cur.execute(
            "SELECT COUNT(*) FROM bookings WHERE driver_id = ? AND LOWER(booking_status) = 'completed'",
            (driver_id,),
        )
        completed = connect.cur.fetchone()[0]
        connect.cur.execute(
            "SELECT COALESCE(SUM(fare), 0) FROM bookings WHERE driver_id = ? AND LOWER(booking_status) = 'completed'",
            (driver_id,),
        )
        earnings_total = connect.cur.fetchone()[0] or 0
    except Exception as error:
        msg.showerror(
            "Dashboard Error", f"Could not load dashboard statistics:\n{error}"
        )
    stats_frame = Frame(content_frame, bg=BG)
    stats_frame.pack(fill=X, padx=22)
    stats = [
        ("Pending Requests", pending, BLUE, "↔"),
        ("Active Trips", active, ORANGE, "◷"),
        ("Completed Trips", completed, GREEN, "✓"),
        ("Total Earnings", f"₦{earnings_total:,.2f}", "#7c3aed", "₦"),
    ]
    for index, (title, value, color, symbol) in enumerate(stats):
        card = make_card(stats_frame, 14, 14)
        card.grid(row=0, column=index, padx=6, pady=5, sticky="nsew")
        Label(card, text=symbol, font=("Arial", 20, "bold"), bg=WHITE, fg=color).pack(
            anchor="w"
        )
        Label(
            card, text=str(value), font=("Arial", 19, "bold"), bg=WHITE, fg=NAVY
        ).pack(anchor="w", pady=(8, 2))
        Label(
            card, text=title, font=("Arial", 9), bg=WHITE, fg=MUTED, wraplength=140
        ).pack(anchor="w")
        stats_frame.grid_columnconfigure(index, weight=1)
    section = Frame(content_frame, bg=BG)
    section.pack(fill=X, padx=28, pady=(24, 8))
    Label(
        section, text="Recent Trips", font=("Arial", 15, "bold"), bg=BG, fg=NAVY
    ).pack(side=LEFT)
    styled_button(section, "View Trips", my_trips).pack(side=RIGHT)
    table_card = make_card(content_frame, 10, 10)
    table_card.pack(fill=X, padx=28, pady=(0, 20))
    columns = ("id", "pickup", "park", "destination", "fare", "status")
    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=5)
    headings = {
        "id": "Booking ID",
        "pickup": "Pickup Town",
        "park": "Pickup Park",
        "destination": "Destination",
        "fare": "Fare",
        "status": "Status",
    }
    widths = {
        "id": 80,
        "pickup": 125,
        "park": 150,
        "destination": 125,
        "fare": 110,
        "status": 120,
    }
    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], anchor="center")
    tree.pack(fill=X, padx=5, pady=5)
    try:
        if driver_id is not None:
            connect.cur.execute(
                "SELECT booking_id, pickup_location, pickup_park, destination, fare, booking_status FROM bookings WHERE driver_id = ? ORDER BY booking_id DESC LIMIT 5",
                (driver_id,),
            )
            for trip in connect.cur.fetchall():
                tree.insert(
                    "",
                    END,
                    values=(
                        trip[0],
                        trip[1],
                        trip[2] or "Not set",
                        trip[3],
                        f"₦{(trip[4] or 0):,.2f}",
                        trip[5],
                    ),
                )
    except Exception as error:
        msg.showerror("Trips Error", f"Could not load recent trips:\n{error}")
    quick = make_card(content_frame, 18, 16)
    quick.pack(fill=X, padx=28, pady=(0, 25))
    Label(
        quick, text="Quick Actions", font=("Arial", 14, "bold"), bg=WHITE, fg=NAVY
    ).pack(anchor="w", pady=(0, 10))
    row = Frame(quick, bg=WHITE)
    row.pack(anchor="w")
    styled_button(row, "View Ride Requests", ride_requests, BLUE).pack(
        side=LEFT, padx=(0, 8)
    )
    styled_button(row, "Change Availability", availability_page, BLUE_DARK).pack(
        side=LEFT
    )


def my_trips():
    clear_page("Trips")
    page_heading(
        "Trips",
        "View booking details, set arrival estimate and update trip progress!",
    )

    if driver_id is None:
        Label(
            content_frame,
            text="Driver ID not found. Please log in again.",
            bg=BG,
            fg=RED,
        ).pack(pady=20)
        return

    card = make_card(content_frame, 8, 8)
    card.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    columns = (
        "id",
        "customer",
        "pickup",
        "park",
        "destination",
        "booking_type",
        "passengers",
        "goods",
        "load_size",
        "fare",
        "arrival",
        "status",
    )

    tree = ttk.Treeview(card, columns=columns, show="headings", height=13)

    headings = {
        "id": "Booking ID",
        "customer": "Customer",
        "pickup": "Pickup Town",
        "park": "Pickup Park",
        "destination": "Destination",
        "booking_type": "Booking Type",
        "passengers": "Passengers",
        "goods": "Goods Description",
        "load_size": "Load Size",
        "fare": "Fare",
        "arrival": "Driver Arrival",
        "status": "Status",
    }

    widths = {
        "id": 85,
        "customer": 130,
        "pickup": 125,
        "park": 165,
        "destination": 125,
        "booking_type": 115,
        "passengers": 95,
        "goods": 180,
        "load_size": 100,
        "fare": 120,
        "arrival": 150,
        "status": 115,
    }

    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], minwidth=70, anchor="center", stretch=False)

    vertical_scroll = ttk.Scrollbar(card, orient=VERTICAL, command=tree.yview)
    horizontal_scroll = ttk.Scrollbar(card, orient=HORIZONTAL, command=tree.xview)

    tree.configure(
        yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set
    )

    tree.pack(side=TOP, fill=BOTH, expand=True, padx=4, pady=(4, 0))
    vertical_scroll.pack(side=RIGHT, fill=Y, pady=4)
    horizontal_scroll.pack(side=BOTTOM, fill=X, padx=4)

    def load_trips():
        tree.delete(*tree.get_children())

        try:
            connect.cur.execute(
                """
                SELECT
                    b.booking_id,
                    u.name,
                    b.pickup_location,
                    b.pickup_park,
                    b.destination,
                    COALESCE(b.booking_type, b.vehicle_type, 'Passenger'),
                    b.passenger_count,
                    b.goods_type,
                    b.load_size,
                    b.fare,
                    b.estimated_arrival,
                    b.booking_status
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                WHERE b.driver_id = ?
                AND LOWER(b.booking_status)
                    IN ('accepted', 'in progress', 'completed')
                ORDER BY b.booking_id DESC
                """,
                (driver_id,),
            )

            for trip in connect.cur.fetchall():
                booking_type = trip[5] or "Passenger"
                passengers = str(trip[6]) if trip[6] is not None else "N/A"
                goods = trip[7] or "N/A"
                load_size = trip[8] or "N/A"

                if booking_type == "Passenger":
                    goods = "N/A"
                    load_size = "N/A"
                elif booking_type == "Goods":
                    passengers = "N/A"

                tree.insert(
                    "",
                    END,
                    values=(
                        trip[0],
                        trip[1],
                        trip[2],
                        trip[3] or "Not set",
                        trip[4],
                        booking_type,
                        passengers,
                        goods,
                        load_size,
                        f"₦{(trip[9] or 0):,.2f}",
                        trip[10] or "Not set",
                        trip[11],
                    ),
                )

        except Exception as error:
            msg.showerror("Database Error", f"Could not load trips:\n{error}")

    def set_arrival_time():
        selected = tree.selection()

        if not selected:
            msg.showwarning("Prompt", "Please select a trip.")
            return

        values = tree.item(selected[0], "values")
        booking_id = values[0]
        current_status = values[11].strip().lower()

        if current_status != "accepted":
            msg.showwarning("Prompt", "Set the arrival time before starting a trip.")
            return

        arrival_time = askstring(
            "Estimated Arrival", "Enter your arrival time at the pickup park:"
        )

        if arrival_time is None:
            return

        arrival_time = arrival_time.strip()

        if not arrival_time:
            msg.showwarning("Prompt", "Please enter an arrival time")
            return

        try:
            connect.cur.execute(
                """
                UPDATE bookings
                SET estimated_arrival = ?
                WHERE booking_id = ?
                AND driver_id = ?
                AND LOWER(booking_status) = 'accepted'
                """,
                (arrival_time, booking_id, driver_id),
            )

            if connect.cur.rowcount == 0:
                connect.con.rollback()
                msg.showwarning("Failed", "Please refresh and try again.")
            else:
                connect.con.commit()
                msg.showinfo("Success", "Estimated arrival time saved.")

            load_trips()

        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", f"Could not save arrival time:\n{error}")

    def update_trip(new_status):
        selected = tree.selection()

        if not selected:
            msg.showwarning("Prompt", "Please select a trip")
            return

        values = tree.item(selected[0], "values")
        booking_id = values[0]
        current_status = values[11].strip().lower()

        if new_status == "In Progress" and current_status != "accepted":
            msg.showwarning("Prompt", "Only accepted trips can be started.")
            return

        if new_status == "Completed" and current_status != "in progress":
            msg.showwarning("Prompt", "Start the trip before completing it.")
            return

        try:
            connect.cur.execute(
                """
                UPDATE bookings
                SET booking_status = ?
                WHERE booking_id = ?
                AND driver_id = ?
                AND LOWER(booking_status) = ?
                """,
                (new_status, booking_id, driver_id, current_status),
            )

            if connect.cur.rowcount == 0:
                connect.con.rollback()
                msg.showwarning("Prompt", "This trip has been changed")
            else:
                connect.con.commit()
                msg.showinfo("Success", f"Trip status changed to {new_status}.")

            load_trips()

        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", f"Could not update trip:\n{error}")

    buttons = Frame(content_frame, bg=BG)
    buttons.pack(fill=X, padx=28, pady=(5, 20))

    styled_button(buttons, "Set Arrival Time", set_arrival_time, ORANGE).pack(
        side=LEFT, padx=(0, 8)
    )

    styled_button(buttons, "Start Trip", lambda: update_trip("In Progress"), BLUE).pack(
        side=LEFT, padx=(0, 8)
    )

    styled_button(
        buttons, "Complete Trip", lambda: update_trip("Completed"), GREEN
    ).pack(side=LEFT, padx=(0, 8))

    styled_button(buttons, "Refresh", load_trips, BLUE_DARK).pack(side=RIGHT)

    load_trips()


def earnings():
    clear_page("Earnings")
    page_heading("Earnings", "Track your income from completed rides")
    if driver_id is None:
        msg.showerror("Error", "Driver account not found")
        return
    try:
        connect.cur.execute(
            "SELECT COUNT(*), COALESCE(SUM(fare), 0) FROM bookings WHERE driver_id = ? AND LOWER(booking_status) = 'completed'",
            (driver_id,),
        )
        result = connect.cur.fetchone()
        completed_count, total_earnings = result[0], result[1] or 0
    except Exception as error:
        msg.showerror("Database Error", str(error))
        return
    cards = Frame(content_frame, bg=BG)
    cards.pack(fill=X, padx=22, pady=(0, 20))
    for index, (title, value, color, note) in enumerate(
        [
            (
                "TOTAL EARNINGS",
                f"₦{total_earnings:,.2f}",
                GREEN,
                "From completed rides",
            ),
            ("COMPLETED TRIPS", str(completed_count), NAVY, "Successfully completed"),
        ]
    ):
        card = make_card(cards, 22, 18)
        card.grid(row=0, column=index, sticky="nsew", padx=6)
        Label(card, text=title, font=("Arial", 9, "bold"), bg=WHITE, fg=MUTED).pack(
            anchor="w"
        )
        Label(card, text=value, font=("Arial", 23, "bold"), bg=WHITE, fg=color).pack(
            anchor="w", pady=(8, 4)
        )
        Label(card, text=note, font=("Arial", 9), bg=WHITE, fg=MUTED).pack(anchor="w")
        cards.grid_columnconfigure(index, weight=1)

    Label(
        content_frame,
        text="Earnings History",
        font=("Arial", 15, "bold"),
        bg=BG,
        fg=NAVY,
    ).pack(anchor="w", padx=28, pady=(0, 10))

    table_card = make_card(content_frame, 8, 8)
    table_card.pack(fill=BOTH, expand=True, padx=20, pady=(0, 25))

    columns = (
        "id",
        "pickup",
        "park",
        "destination",
        "booking_type",
        "passengers",
        "goods",
        "load_size",
        "fare",
        "date",
    )

    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=12)

    headings = {
        "id": "Booking ID",
        "pickup": "Pickup Town",
        "park": "Pickup Park",
        "destination": "Destination",
        "booking_type": "Booking Type",
        "passengers": "Passengers",
        "goods": "Goods Description",
        "load_size": "Load Size",
        "fare": "Fare",
        "date": "Date",
    }

    widths = {
        "id": 85,
        "pickup": 125,
        "park": 165,
        "destination": 125,
        "booking_type": 115,
        "passengers": 95,
        "goods": 180,
        "load_size": 100,
        "fare": 120,
        "date": 175,
    }

    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], minwidth=70, anchor="center", stretch=False)

    vertical_scroll = ttk.Scrollbar(table_card, orient=VERTICAL, command=tree.yview)
    horizontal_scroll = ttk.Scrollbar(table_card, orient=HORIZONTAL, command=tree.xview)

    tree.configure(
        yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set
    )

    tree.pack(side=TOP, fill=BOTH, expand=True, padx=4, pady=(4, 0))
    vertical_scroll.pack(side=RIGHT, fill=Y, pady=4)
    horizontal_scroll.pack(side=BOTTOM, fill=X, padx=4)

    try:
        connect.cur.execute(
            """
            SELECT
                booking_id,
                pickup_location,
                pickup_park,
                destination,
                COALESCE(booking_type, vehicle_type, 'Passenger'),
                passenger_count,
                goods_type,
                load_size,
                fare,
                booking_date
            FROM bookings
            WHERE driver_id = ?
            AND LOWER(booking_status) = 'completed'
            ORDER BY booking_id DESC
            """,
            (driver_id,),
        )

        rides = connect.cur.fetchall()

        for ride in rides:
            booking_type = ride[4] or "Passenger"
            passengers = str(ride[5]) if ride[5] is not None else "N/A"
            goods = ride[6] or "N/A"
            load_size = ride[7] or "N/A"

            if booking_type == "Passenger":
                goods = "N/A"
                load_size = "N/A"
            elif booking_type == "Goods":
                passengers = "N/A"

            tree.insert(
                "",
                END,
                values=(
                    ride[0],
                    ride[1],
                    ride[2] or "Not set",
                    ride[3],
                    booking_type,
                    passengers,
                    goods,
                    load_size,
                    f"₦{(ride[8] or 0):,.2f}",
                    ride[9] or "Not set",
                ),
            )

        if not rides:
            Label(
                content_frame,
                text="No completed rides",
                font=("Arial", 10),
                bg=BG,
                fg=MUTED,
            ).pack(anchor="w", padx=28, pady=(0, 15))

    except Exception as error:
        msg.showerror("Database Error", f"Could not load earnings history:\n{error}")


def availability_page():
    clear_page("Availability")
    page_heading(
        "Driver Availability",
        "Choose whether you are ready to receive new ride requests",
    )
    card = make_card(content_frame, 25, 24)
    card.pack(fill=X, padx=28, pady=(0, 15))
    Label(
        card, text="Current Status", font=("Arial", 9, "bold"), bg=WHITE, fg=MUTED
    ).pack(anchor="w")
    status_label = Label(
        card, text="Loading...", font=("Arial", 22, "bold"), bg=WHITE, fg=MUTED
    )
    status_label.pack(anchor="w", pady=(10, 5))
    description = Label(card, text="", font=("Arial", 10), bg=WHITE, fg=MUTED)
    description.pack(anchor="w")

    def load_availability():
        driver = get_driver()
        if driver is None:
            status_label.config(text="Account Not Found", fg=RED)
            description.config(text="Please log in again")
            return
        status = driver[1] or "Unavailable"
        if status.lower() == "available":
            status_label.config(text="● Available", fg=GREEN)
            description.config(text="You are ready to receive ride requests")
        else:
            status_label.config(text="● Unavailable", fg=RED)
            description.config(text="You will not receive new ride requests")
        refresh_header()

    def set_availability(status):
        if driver_id is None:
            msg.showerror("Error", "Please log in again")
            return
        try:
            connect.cur.execute(
                "UPDATE users SET availability = ? WHERE id = ? AND LOWER(role) = 'driver'",
                (status, driver_id),
            )
            if connect.cur.rowcount == 0:
                connect.con.rollback()
                msg.showerror("Error", "Driver account not found.")
                return
            connect.con.commit()
            load_availability()
            msg.showinfo("Availability Updated", f"You are now {status.lower()}.")
        except Exception as error:
            connect.con.rollback()
            msg.showerror("Database Error", f"Could not update availability:\n{error}")

    Label(
        content_frame,
        text="Change Availability",
        font=("Arial", 1),
        bg=BG,
        fg=NAVY,
    ).pack(anchor="w", padx=28, pady=(10, 10))
    buttons = Frame(content_frame, bg=BG)
    buttons.pack(anchor="w", padx=150, ipady=0)
    styled_button(
        buttons, "✓ Available", lambda: set_availability("Available"), GREEN
    ).pack(side=LEFT, padx=150, ipady=0)
    styled_button(
        buttons, "✕ Unavailable", lambda: set_availability("Unavailable"), RED
    ).pack(side=LEFT)
    info = Frame(content_frame, bg="#e8f1fb", padx=18, pady=14)
    info.pack(fill=X, padx=28, pady=(0, 25))
    Label(
        info, text="Important", font=("Arial", 10, "bold"), bg="#e8f1fb", fg=NAVY
    ).pack(anchor="w")
    Label(
        info,
        text="Only drivers Available can accept new ride requests!",
        font=("Arial", 9),
        bg="#e8f1fb",
        fg=TEXT,
        wraplength=650,
        justify=LEFT,
    ).pack(anchor="w", pady=(5, 0))
    load_availability()


def ride_requests():
    clear_page("Ride Requests")
    page_heading(
        "Ride Requests",
        "Review booking details before accepting or rejecting requests!",
    )

    if driver_id is None:
        Label(
            content_frame,
            text="Driver ID not found. Please log in again.",
            font=("Arial", 12, "bold"),
            bg=BG,
            fg=RED,
        ).pack(pady=25)
        return

    driver = get_driver()

    if driver is None:
        Label(
            content_frame,
            text="Driver account not found.",
            font=("Arial", 12, "bold"),
            bg=BG,
            fg=RED,
        ).pack(pady=25)
        return

    if (driver[1] or "Unavailable").lower() != "available":
        card = make_card(content_frame, 24, 25)
        card.pack(fill=X, padx=28, pady=15)

        Label(
            card,
            text="You are currently unavailable",
            font=("Arial", 17, "bold"),
            bg=WHITE,
            fg=RED,
        ).pack(anchor="w")

        Label(
            card,
            text="You must be available to receive ride requests",
            font=("Arial", 10),
            bg=WHITE,
            fg=MUTED,
        ).pack(anchor="w", pady=(8, 15))

        styled_button(card, "Manage Availability", availability_page).pack(anchor="w")
        return

    card = make_card(content_frame, 8, 8)
    card.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    columns = (
        "id",
        "customer",
        "pickup",
        "park",
        "destination",
        "booking_type",
        "passengers",
        "goods",
        "load_size",
        "fare",
        "date",
    )

    tree = ttk.Treeview(card, columns=columns, show="headings", height=13)

    headings = {
        "id": "Booking ID",
        "customer": "Customer",
        "pickup": "Pickup Town",
        "park": "Pickup Park",
        "destination": "Destination",
        "booking_type": "Booking Type",
        "passengers": "Passengers",
        "goods": "Goods Description",
        "load_size": "Load Size",
        "fare": "Estimated Fare",
        "date": "Booking Date",
    }

    widths = {
        "id": 85,
        "customer": 130,
        "pickup": 125,
        "park": 165,
        "destination": 125,
        "booking_type": 115,
        "passengers": 95,
        "goods": 180,
        "load_size": 100,
        "fare": 120,
        "date": 175,
    }

    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], minwidth=70, anchor="center", stretch=False)

    vertical_scroll = ttk.Scrollbar(card, orient=VERTICAL, command=tree.yview)

    horizontal_scroll = ttk.Scrollbar(card, orient=HORIZONTAL, command=tree.xview)

    tree.configure(
        yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set
    )

    tree.pack(side=TOP, fill=BOTH, expand=True, padx=4, pady=(4, 0))
    vertical_scroll.pack(side=RIGHT, fill=Y, pady=4)
    horizontal_scroll.pack(side=BOTTOM, fill=X, padx=4)

    def load_requests():
        tree.delete(*tree.get_children())

        try:
            connect.cur.execute("""
                SELECT
                    b.booking_id,
                    u.name,
                    b.pickup_location,
                    b.pickup_park,
                    b.destination,
                    COALESCE(b.booking_type, b.vehicle_type, 'Passenger'),
                    b.passenger_count,
                    b.goods_type,
                    b.load_size,
                    b.fare,
                    b.booking_date
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                WHERE LOWER(b.booking_status) = 'pending'
                AND b.driver_id IS NULL
                ORDER BY b.booking_id DESC
                """)

            for ride in connect.cur.fetchall():
                booking_type = ride[5] or "Passenger"
                passengers = str(ride[6]) if ride[6] is not None else "N/A"
                goods = ride[7] or "N/A"
                load_size = ride[8] or "N/A"

                if booking_type == "Passenger":
                    goods = "N/A"
                    load_size = "N/A"
                elif booking_type == "Goods":
                    passengers = "N/A"

                tree.insert(
                    "",
                    END,
                    values=(
                        ride[0],
                        ride[1],
                        ride[2],
                        ride[3] or "Not set",
                        ride[4],
                        booking_type,
                        passengers,
                        goods,
                        load_size,
                        f"₦{(ride[9] or 0):,.2f}",
                        ride[10] or "Not set",
                    ),
                )

        except Exception as error:
            msg.showerror("Error", f"Could not load ride requests:\n{error}")

    def accept_ride():
        selected = tree.selection()

        if not selected:
            msg.showwarning("Prompt", "Please select a ride request")
            return

        booking_id = tree.item(selected[0], "values")[0]

        try:
            connect.cur.execute(
                """
                SELECT availability FROM users
                WHERE id = ? AND LOWER(role) = 'driver'
                """,
                (driver_id,),
            )

            result = connect.cur.fetchone()

            if result is None or (result[0] or "Unavailable").lower() != "available":
                msg.showwarning("Prompt", "You must be Available to accept a ride")
                return

            connect.cur.execute(
                """
                UPDATE bookings
                SET driver_id = ?, booking_status = 'Accepted'
                WHERE booking_id = ?
                AND LOWER(booking_status) = 'pending'
                AND driver_id IS NULL
                """,
                (driver_id, booking_id),
            )

            if connect.cur.rowcount == 0:
                connect.con.rollback()
                msg.showwarning(
                    "Prompt", "This ride has already been updated"
                )
            else:
                connect.con.commit()
                msg.showinfo(
                    "Success",
                    "You accepted this booking",
                )

            ride_requests()

        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", f"Could not accept ride:\n{error}")

    def reject_ride():
        selected = tree.selection()

        if not selected:
            msg.showwarning("Select", "Please select a ride request")
            return

        booking_id = tree.item(selected[0], "values")[0]

        if not msg.askyesno(
            "Reject", "Are you sure you want to reject this request?"
        ):
            return

        try:
            connect.cur.execute(
                """
                UPDATE bookings
                SET booking_status = 'Rejected'
                WHERE booking_id = ?
                AND LOWER(booking_status) = 'pending'
                AND driver_id IS NULL
                """,
                (booking_id,),
            )

            if connect.cur.rowcount == 0:
                connect.con.rollback()
                msg.showwarning(
                    "Prompt", "This request has already been assigned or updated"
                )
            else:
                connect.con.commit()
                msg.showinfo("Prompt", "The request has been rejected.")

            ride_requests()

        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", f"Could not reject ride:\n{error}")

    buttons = Frame(content_frame, bg=BG)
    buttons.pack(fill=X, padx=28, pady=(5, 20))

    styled_button(buttons, "Accept", accept_ride, GREEN).pack(
        side=LEFT, padx=(0, 8)
    )

    styled_button(buttons, "Reject", reject_ride, RED).pack(side=LEFT, padx=(0, 8))

    styled_button(buttons, "Refresh", load_requests, BLUE_DARK).pack(side=RIGHT)

    load_requests()


def profile_page():
    clear_page("My Profile")
    page_heading("My Profile", "Manage your personal information and password")
    if driver_id is None:
        msg.showerror("Error", "Driver account not found")
        return
    try:
        connect.cur.execute(
            "SELECT name, username, email, gender, address, dob, availability, password FROM users WHERE id = ? AND LOWER(role) = 'driver'",
            (driver_id,),
        )
        driver = connect.cur.fetchone()
    except Exception as error:
        msg.showerror("Database Error", str(error))
        return
    if not driver:
        msg.showerror("Error", "Driver details could not be found")
        return
    identity = make_card(content_frame, 20, 16)
    identity.pack(fill=X, padx=28, pady=(0, 14))
    row = Frame(identity, bg=WHITE)
    row.pack(fill=X)
    initials = "".join(word[0] for word in (driver[0] or "Driver").split()[:2]).upper()
    avatar = Frame(row, bg=NAVY, width=58, height=58)
    avatar.pack(side=LEFT, padx=(0, 14))
    avatar.pack_propagate(False)
    Label(avatar, text=initials, font=("Arial", 18, "bold"), bg=NAVY, fg=WHITE).pack(
        expand=True
    )
    identity_text = Frame(row, bg=WHITE)
    identity_text.pack(side=LEFT, fill=X, expand=True)
    Label(
        identity_text,
        text=driver[0] or "Driver",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=NAVY,
    ).pack(anchor="w")
    Label(
        identity_text, text="Driver Account", font=("Arial", 9), bg=WHITE, fg=MUTED
    ).pack(anchor="w", pady=(3, 0))
    status = driver[6] or "Unavailable"
    Label(
        row,
        text=status,
        font=("Arial", 9, "bold"),
        bg="#edf4fb",
        fg=GREEN if status.lower() == "available" else RED,
        padx=12,
        pady=6,
    ).pack(side=RIGHT, anchor="n")
    details = make_card(content_frame, 20, 18)
    details.pack(fill=X, padx=28, pady=(0, 14))
    Label(
        details,
        text="Personal Information",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=NAVY,
    ).pack(anchor="w", pady=(0, 12))
    fields = Frame(details, bg=WHITE)
    fields.pack(fill=X)
    fields.columnconfigure(0, weight=1)
    fields.columnconfigure(1, weight=1)

    def make_field(label, value, r, c, readonly=False):
        wrapper = Frame(fields, bg=WHITE)
        wrapper.grid(
            row=r, column=c, sticky="ew", padx=(0, 16) if c == 0 else 0, pady=(0, 11)
        )
        Label(wrapper, text=label, font=("Arial", 9, "bold"), bg=WHITE, fg=TEXT).pack(
            anchor="w", pady=(0, 5)
        )
        entry = Entry(
            wrapper,
            font=("Arial", 10),
            relief=SOLID,
            bd=1,
            bg="#f8fafc" if readonly else WHITE,
        )
        entry.pack(fill=X, ipady=5)
        entry.insert(0, value or "")
        if readonly:
            entry.config(state="readonly")
        return entry

    name_e = make_field("Full Name", driver[0], 0, 0)
    username_e = make_field("Username (cannot be changed)", driver[1], 0, 1, True)
    email_e = make_field("Email Address", driver[2], 1, 0)
    gender_e = make_field("Gender", driver[3], 1, 1)
    address_e = make_field("Home Address", driver[4], 2, 0)
    dob_e = make_field("Date of Birth", driver[5], 2, 1)

    def update_profile():
        name, email = name_e.get().strip(), email_e.get().strip()
        if not name or not email:
            msg.showwarning("Prompt", "Full name and email address are required")
            return
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            msg.showwarning("Error", "Invalid")
            return
        try:
            connect.cur.execute(
                "UPDATE users SET name = ?, email = ?, gender = ?, address = ?, dob = ? WHERE id = ? AND LOWER(role) = 'driver'",
                (
                    name,
                    email,
                    gender_e.get().strip(),
                    address_e.get().strip(),
                    dob_e.get().strip(),
                    driver_id,
                ),
            )
            connect.con.commit()
            msg.showinfo("Success", "Your profile has been updated")
            refresh_header()
            profile_page()
        except Exception:
            connect.con.rollback()
            msg.showerror(
                "Failed",
                "Could not save your details",
            )

    styled_button(details, "Save Changes", update_profile).pack(anchor="w", pady=(3, 0))
    password_card = make_card(content_frame, 20, 18)
    password_card.pack(fill=X, padx=28, pady=(0, 25))
    Label(
        password_card,
        text="Change Password",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=NAVY,
    ).pack(anchor="w", pady=(0, 12))

    def password_field(label):
        Label(
            password_card, text=label, font=("Arial", 9, "bold"), bg=WHITE, fg=TEXT
        ).pack(anchor="w", pady=(0, 5))
        entry = Entry(
            password_card, font=("Arial", 10), show="*", relief=SOLID, bd=1, width=20
        )
        entry.pack(anchor="w", ipady=5, pady=(0, 9))
        return entry

    current_e = password_field("Current Password")
    new_e = password_field("New Password")
    confirm_e = password_field("Confirm New Password")

    def update_password():
        current, new, confirm = current_e.get(), new_e.get(), confirm_e.get()
        if not current or not new or not confirm:
            msg.showwarning("Prompt", "Please complete all password fields")
            return
        if new != confirm:
            msg.showerror("Prompt", "passwords Mismatch")
            return
        if len(new) < 8:
            msg.showwarning(
                "Prompt", "Your password must contain at least 8 characters."
            )
            return
        try:
            connect.cur.execute(
                "SELECT password FROM users WHERE id = ? AND LOWER(role) = 'driver'",
                (driver_id,),
            )
            result = connect.cur.fetchone()
            if result is None or result[0] != current:
                msg.showerror("Prompt", "Incorrect Password")
                return
            connect.cur.execute(
                "UPDATE users SET password = ? WHERE id = ? AND LOWER(role) = 'driver'",
                (new, driver_id),
            )
            connect.con.commit()
            msg.showinfo("Success", "Password Changed")
            current_e.delete(0, END)
            new_e.delete(0, END)
            confirm_e.delete(0, END)
        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", f"Unable to change password:\n{error}")

    styled_button(password_card, "Update", update_password).pack(anchor="w")


def notifications_page():
    clear_page("Notifications")
    page_heading("Notifications", " View your updates associated with your account")
    card = make_card(content_frame, 14, 14)
    card.pack(fill=X, padx=28, pady=(0, 20))
    list_frame = Frame(card, bg=WHITE)
    list_frame.pack(fill=X)

    def load_notifications():
        for widget in list_frame.winfo_children():
            widget.destroy()
        try:
            connect.cur.execute(
                "SELECT notification_id, title, message, status, is_read, created_at FROM notifications WHERE user_id = ? ORDER BY notification_id DESC",
                (driver_id,),
            )
            rows = connect.cur.fetchall()
        except Exception:
            Label(
                list_frame,
                text="No notification records are available for this account.",
                bg=WHITE,
                fg=MUTED,
            ).pack(anchor="w", pady=10)
            refresh_header()
            return
        if not rows:
            Label(list_frame, text="No new Notification", bg=WHITE, fg=MUTED).pack(
                anchor="w", pady=10
            )
        for row in rows:
            nid, title, message, status, is_read, created = row
            item_bg = "#f8fafc" if is_read else "#edf4fb"
            item = Frame(
                list_frame,
                bg=item_bg,
                padx=12,
                pady=10,
                highlightbackground=BORDER,
                highlightthickness=1,
            )
            item.pack(fill=X, pady=5)
            Label(
                item,
                text=title or "Notification",
                font=("Arial", 11, "bold"),
                bg=item_bg,
                fg=NAVY,
            ).pack(anchor="w")
            Label(
                item,
                text=message or "",
                font=("Arial", 10),
                bg=item_bg,
                fg=TEXT,
                wraplength=650,
                justify=LEFT,
            ).pack(anchor="w", pady=(5, 3))
            Label(
                item,
                text=f"{created or ''}  {status or ''}  {'Read' if is_read else 'Unread'}",
                font=("Arial", 8),
                bg=item_bg,
                fg=MUTED,
            ).pack(anchor="w")
            if not is_read:
                Button(
                    item,
                    text="Mark Read",
                    font=("Arial", 9),
                    bg=WHITE,
                    fg=BLUE,
                    relief=FLAT,
                    cursor="hand2",
                    command=lambda i=nid: mark_read(i),
                ).pack(anchor="e", pady=(4, 0))
        refresh_header()

    def mark_read(nid):
        try:
            connect.cur.execute(
                "UPDATE notifications SET is_read = 1 WHERE notification_id = ? AND user_id = ?",
                (nid, driver_id),
            )
            connect.con.commit()
            load_notifications()
        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", str(error))

    load_notifications()


Label(sidebar, text="TRAVEL", font=("Arial", 16, "bold"), bg=NAVY, fg=WHITE).pack(
    anchor="w", padx=20, pady=(28, 3)
)
Label(sidebar, text="DRIVER ACCOUNT", font=("Arial", 8, "bold"), bg=NAVY, fg="#9fb7d1").pack(
    anchor="w", padx=21, pady=(0, 25)
)
menu_items = [
    ("Dashboard", "▦", dashboard),
    ("Ride Requests", "↔", ride_requests),
    ("Trips", "▤", my_trips),
    ("Availability", "●", availability_page),
    ("Earnings", "₦", earnings),
    ("My Profile", "♙", profile_page),
]
for name, icon, command in menu_items:
    button = Button(
        sidebar,
        text=f"  {icon}    {name}",
        font=("Arial", 10, "bold"),
        bg=NAVY,
        fg="#e8eef6",
        activebackground=BLUE,
        activeforeground=WHITE,
        bd=0,
        anchor="w",
        padx=18,
        height=2,
        cursor="hand2",
        command=command,
    )
    button.pack(fill=X, padx=10, pady=3)
    nav_buttons[name] = button
    button.bind(
        "<Enter>",
        lambda event, b=button, n=name: b.config(
            bg=BLUE_DARK if active_page != n else BLUE
        ),
    )
    button.bind(
        "<Leave>",
        lambda event, b=button, n=name: b.config(bg=BLUE if active_page == n else NAVY),
    )
spacer = Frame(sidebar, bg=NAVY)
spacer.pack(fill=BOTH, expand=True)
logout_button = Button(
    sidebar,
    text="  ⇥    Logout",
    font=("Arial", 10, "bold"),
    bg=NAVY,
    fg="#e8eef6",
    activebackground=RED,
    activeforeground=WHITE,
    bd=0,
    anchor="w",
    padx=18,
    height=2,
    cursor="hand2",
    command=logout,
)
logout_button.pack(fill=X, padx=10, pady=18)
logout_button.bind("<Enter>", lambda event: logout_button.config(bg=RED))
logout_button.bind("<Leave>", lambda event: logout_button.config(bg=NAVY))

refresh_header()
dashboard()
root.mainloop()
