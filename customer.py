from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
import sys
import subprocess
import control as connect


user_id = None
if len(sys.argv) > 1:
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        user_id = None

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

# Towns
towns = [
    "Ado-Ekiti",
    "Ifaki-Ekiti",
    "Ido-Ekiti",
    "Ora-Ekiti",
    "Ikole-Ekiti",
    "Oye-Ekiti",
    "Ijero-Ekiti",
    "Ikere-Ekiti",
    "Ilawe-Ekiti",
    "Emure-Ekiti",
    "Iworoko-Ekiti",
    "Igede-Ekiti",
    "Iyin-Ekiti",
    "Igbemo-Ekiti",
    "Itapa-Ekiti",
    "Aramoko-Ekiti",
    "Efon-Alaaye",
    "Okemesi-Ekiti",
    "Ise-Ekiti",
    "Omuo-Ekiti",
    "Ode-Ekiti",
    "Ijan-Ekiti",
    "Aisegba-Ekiti",
    "Imesi-Ekiti",
]

# Distances
town_distances = {
    "Ado-Ekiti": 0,
    "Iworoko-Ekiti": 8,
    "Iyin-Ekiti": 12,
    "Igbemo-Ekiti": 15,
    "Ifaki-Ekiti": 28,
    "Ido-Ekiti": 25,
    "Oye-Ekiti": 35,
    "Itapa-Ekiti": 40,
    "Ikole-Ekiti": 55,
    "Ijero-Ekiti": 30,
    "Aramoko-Ekiti": 30,
    "Efon-Alaaye": 50,
    "Okemesi-Ekiti": 45,
    "Ikere-Ekiti": 25,
    "Ilawe-Ekiti": 35,
    "Ise-Ekiti": 45,
    "Emure-Ekiti": 55,
    "Omuo-Ekiti": 65,
    "Ode-Ekiti": 50,
    "Ijan-Ekiti": 35,
    "Aisegba-Ekiti": 40,
    "Imesi-Ekiti": 40,
    "Igede-Ekiti": 35,
    "Ora-Ekiti": 50,
}
vehicle_rates = {"Economy": 50, "Standard": 70, "SUV": 100, "Luxury": 150}

root = Tk()
root.title("Customer")
root.geometry("1250x750")
root.minsize(1100, 650)
root.configure(bg=BG)
root.resizable(True, True)
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
customer_name_label = Label(
    header_right, text="Customer", font=("Arial", 10, "bold"), bg=WHITE, fg=TEXT
)
customer_name_label.pack(side=LEFT)
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


def get_customer():
    if user_id is None:
        return None
    try:
        connect.cur.execute(
            "SELECT name, username, email, gender, address, dob FROM users WHERE id = ? AND LOWER(role) IN ('customer', 'user')",
            (user_id,),
        )
        return connect.cur.fetchone()
    except Exception:
        return None


def get_unread_count():
    if user_id is None:
        return 0
    try:
        connect.cur.execute(
            "SELECT COUNT(*) FROM notifications WHERE user_id = ? AND COALESCE(is_read, 0) = 0",
            (user_id,),
        )
        return connect.cur.fetchone()[0]
    except Exception:
        return 0


def refresh_header():
    customer = get_customer()
    customer_name_label.config(
        text=(customer[0] if customer and customer[0] else "Customer")
    )
    count = get_unread_count()
    notification_button.config(
        text=f"♧ Notifications ({count})" if count else "♧ Notifications"
    )


def logout():
    if msg.askyesno("Logout", "Are you sure you want to log out?"):
        root.destroy()
        subprocess.Popen([sys.executable, "login.py"])


def calculate_fare(
    pickup, destination, booking_type, passenger_count=1, load_size="Small"
):

    if pickup == destination:
        return None, "Pickup and destination towns must be different"

    if pickup not in town_distances or destination not in town_distances:
        return None, "A distance estimate is not available for this route"

    if pickup == "Ado-Ekiti":
        distance = town_distances[destination]
    elif destination == "Ado-Ekiti":
        distance = town_distances[pickup]
    else:
        distance = town_distances[pickup] + town_distances[destination]

    distance = max(distance, 5)

    # Use the existing Economy rate as the base rate
    base_rate = vehicle_rates.get("Economy", 100)

    passenger_rates = {1: 2.0, 2: 2.5, 3:3, 4: 3.5, 5: 4}

    load_rates = {"Small": 2.0, "Medium": 2.5, "Large": 3.0}

    passenger_count = max(1, min(int(passenger_count), 5))

    if booking_type == "Passenger":
        fare = distance * base_rate * passenger_rates[passenger_count]

    elif booking_type == "Goods":
        fare = distance * base_rate * load_rates[load_size]

    elif booking_type == "Both":
        fare = (
            distance
            * base_rate
            * (passenger_rates[passenger_count] + load_rates[load_size])
        )

    else:
        return None, "Please select a valid booking purpose"

    return fare, None


def get_pending_count():
    connect.cur.execute(
        "SELECT COUNT(*) FROM bookings WHERE user_id = ? AND LOWER(booking_status) = 'pending'",
        (user_id,),
    )
    return connect.cur.fetchone()[0]


def save_booking(
    pickup_town,
    pickup_park,
    destination,
    booking_type,
    passenger_count,
    goods_description,
    load_size,
):
    if user_id is None:
        msg.showerror(
            "Login Required", "Your customer ID was not found. Please log in again."
        )
        return

    if not pickup_town or not pickup_park or not destination:
        msg.showwarning(
            "Prompt",
            "Please select your pickup town, motor park and destination",
        )
        return

    if pickup_town == destination:
        msg.showwarning(
            "Error", "Pickup and destination towns must be different"
        )
        return

    if booking_type not in ["Passenger", "Goods", "Both"]:
        msg.showwarning("prompt", "Please select what you want to transport")
        return

    passenger_count_value = None
    goods_description_value = None
    load_size_value = None

    if booking_type in ["Passenger", "Both"]:
        if not passenger_count:
            msg.showwarning(
                "Missing Details", "Please select the number of passengers."
            )
            return

        passenger_count_value = int(passenger_count)

    if booking_type in ["Goods", "Both"]:
        if not goods_description.strip():
            msg.showwarning(
                "Missing Details", "Please enter a description of the goods"
            )
            return

        if not load_size:
            msg.showwarning("Missing Details", "Please select the load size")
            return

        goods_description_value = goods_description.strip()
        load_size_value = load_size

    try:
        # CHECK THAT THE PICKUP PARK EXISTS
        connect.cur.execute(
            """SELECT park_id FROM motor_parks
            WHERE town = ? AND park_name = ? AND is_active = 1""",
            (pickup_town, pickup_park),
        )

        if connect.cur.fetchone() is None:
            msg.showwarning(
                "Park Not Available",
                "This motor park is no longer available. Please select another",
            )
            return

        # CHECK THE PENDING BOOKING LIMIT
        if get_pending_count() >= 5:
            msg.showwarning(
                "Prompt", "You can have a maximum of 5 pending bookings"
            )
            return

        # CHECK DRIVER AVAILABILITY
        connect.cur.execute("""SELECT COUNT(*) FROM users
            WHERE LOWER(role) = 'driver'
            AND LOWER(COALESCE(availability, 'Unavailable')) = 'available'""")

        if connect.cur.fetchone()[0] == 0:
            msg.showwarning(
                "prompt",
                "There are currently no available drivers. Please try again later",
            )
            return

        # CALCULATE THE FARE
        fare, error = calculate_fare(
            pickup_town,
            destination,
            booking_type,
            passenger_count_value if passenger_count_value is not None else 1,
            load_size_value if load_size_value is not None else "Small",
        )

        if error:
            msg.showwarning("Route Error", error)
            return

        # SAVE THE BOOKING
        connect.cur.execute(
            """INSERT INTO bookings
            (
                user_id,
                pickup_location,
                pickup_park,
                destination,
                vehicle_type,
                fare,
                booking_type,
                passenger_count,
                goods_type,
                load_size
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                pickup_town,
                pickup_park,
                destination,
                booking_type,
                fare,
                booking_type,
                passenger_count_value,
                goods_description_value,
                load_size_value,
            ),
        )

        connect.con.commit()

        msg.showinfo(
            "Booking Successful",
            f"Your booking has been saved.\n\n"
            f"Booking purpose: {booking_type}\n"
            f"Estimated fare: ₦{fare:,.2f}",
        )

        my_rides()

    except Exception as error:
        connect.con.rollback()
        msg.showerror("Booking Error", f"Could not save your booking:\n{error}")


def dashboard():
    clear_page("Dashboard")
    customer = get_customer()
    name = customer[0].split()[0] if customer and customer[0] else "Customer"
    page_heading(
        f"Welcome back, {name}!",
        "View Schedules and book your next Trip instantly here!",
    )
    pending = accepted = completed = 0
    try:
        connect.con
        connect.cur
        
        connect.cur.execute(
            "SELECT COUNT(*) FROM bookings WHERE user_id = ? AND LOWER(booking_status) = 'pending'",
            (user_id,),
        )
        pending = connect.cur.fetchone()[0]
        connect.cur.execute(
            "SELECT COUNT(*) FROM bookings WHERE user_id = ? AND LOWER(booking_status) IN ('accepted', 'in progress')",
            (user_id,),
        )
        accepted = connect.cur.fetchone()[0]
        connect.cur.execute(
            "SELECT COUNT(*) FROM bookings WHERE user_id = ? AND LOWER(booking_status) = 'completed'",
            (user_id,),
        )
        completed = connect.cur.fetchone()[0]
    except Exception as error:
        msg.showerror(
            "Dashboard Error", f"Could not load dashboard statistics:\n{error}"
        )
    stats_frame = Frame(content_frame, bg=BG)
    stats_frame.pack(fill=X, padx=22)
    stats = [
        ("Pending", pending, BLUE, "◷"),
        ("Active", accepted, ORANGE, "↔"),
        ("Completed", completed, GREEN, "✓"),
    ]
    for index, (title, value, color, symbol) in enumerate(stats):
        card = make_card(stats_frame, 16, 15)
        card.grid(row=0, column=index, padx=6, pady=5, sticky="nsew")
        Label(card, text=symbol, font=("Arial", 20, "bold"), bg=WHITE, fg=color).pack(
            anchor="w"
        )
        Label(
            card, text=str(value), font=("Arial", 22, "bold"), bg=WHITE, fg=NAVY
        ).pack(anchor="w", pady=(8, 2))
        Label(card, text=title, font=("Arial", 9), bg=WHITE, fg=MUTED).pack(anchor="w")
        stats_frame.grid_columnconfigure(index, weight=1)
    quick = make_card(content_frame, 18, 18)
    quick.pack(fill=X, padx=28, pady=(22, 15))
    Label(
        quick, text="Get Started", font=("Arial", 15, "bold"), bg=WHITE, fg=NAVY
    ).pack(anchor="w")
    Label(
        quick,
        text="Ready to secure your next journey? Choose your location, destination and book your seat in just few clicks!",
        font=("Arial", 10),
        bg=WHITE,
        fg=MUTED,
        wraplength=760,
        justify=LEFT,
    ).pack(anchor="w", pady=(8, 14))
    styled_button(quick, "Book a Ride", book_ride).pack(anchor="w")
    section = Frame(content_frame, bg=BG)
    section.pack(fill=X, padx=28, pady=(5, 8))
    Label(
        section, text="Recent Rides", font=("Arial", 15, "bold"), bg=BG, fg=NAVY
    ).pack(side=LEFT)
    styled_button(section, "View My Rides", my_rides).pack(side=RIGHT)
    table_card = make_card(content_frame, 10, 10)
    table_card.pack(fill=X, padx=28, pady=(0, 22))
    columns = ("id", "pickup", "park", "destination", "fare", "status")
    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=5)
    headings = {
        "id": "Booking ID",
        "pickup": "Pickup Town",
        "park": "Motor Park",
        "destination": "Destination",
        "fare": "Fare",
        "status": "Status",
    }
    widths = {
        "id": 80,
        "pickup": 130,
        "park": 160,
        "destination": 130,
        "fare": 110,
        "status": 110,
    }
    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], anchor="center")
    tree.pack(fill=X, padx=5, pady=5)
    try:
        connect.cur.execute(
            "SELECT booking_id, pickup_location, pickup_park, destination, fare, booking_status FROM bookings WHERE user_id = ? ORDER BY booking_id DESC LIMIT 5",
            (user_id,),
        )
        for ride in connect.cur.fetchall():
            tree.insert(
                "",
                END,
                values=(
                    ride[0],
                    ride[1],
                    ride[2] or "Not set",
                    ride[3],
                    f"₦{(ride[4] or 0):,.2f}",
                    ride[5],
                ),
            )
    except Exception as error:
        msg.showerror("Rides Error", f"Could not load recent rides:\n{error}")


def book_ride(pickup="", destination=""):

    clear_page("Book a Ride")
    page_heading("Book a Ride", "Choose what you want to transport")

    card = make_card(content_frame, 22, 20)
    card.pack(fill=X, padx=28, pady=(0, 20))

    # PICKUP TOWN
    Label(card, text="Pickup Town", font=("Arial", 10, "bold"), bg=WHITE, fg=TEXT).pack(
        anchor="w", pady=(0, 5)
    )

    pickup_var = StringVar(value=pickup if pickup in towns else "")

    pickup_box = ttk.Combobox(
        card,
        textvariable=pickup_var,
        values=towns,
        state="readonly",
        font=("Arial", 10),
        width=42,
    )
    pickup_box.pack(anchor="w", ipady=4, pady=(0, 14))

    # MOTOR PARK
    Label(
        card,
        text="Registered Motor Park",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT,
    ).pack(anchor="w", pady=(0, 5))

    park_var = StringVar()

    park_box = ttk.Combobox(
        card, textvariable=park_var, state="readonly", font=("Arial", 10), width=42
    )
    park_box.pack(anchor="w", ipady=4, pady=(0, 5))

    park_note = Label(
        card,
        text="Choose a pickup town to load its registered parks",
        font=("Arial", 9),
        bg=WHITE,
        fg=MUTED,
    )
    park_note.pack(anchor="w", pady=(0, 14))

    # DESTINATION TOWN
    Label(
        card, text="Destination Town", font=("Arial", 10, "bold"), bg=WHITE, fg=TEXT
    ).pack(anchor="w", pady=(0, 5))

    destination_var = StringVar(value=destination if destination in towns else "")

    destination_box = ttk.Combobox(
        card,
        textvariable=destination_var,
        values=towns,
        state="readonly",
        font=("Arial", 10),
        width=42,
    )
    destination_box.pack(anchor="w", ipady=4, pady=(0, 14))

    # BOOKING PURPOSE
    Label(
        card,
        text="What do you want to transport?",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT,
    ).pack(anchor="w", pady=(0, 5))

    booking_type_var = StringVar(value="Passenger")

    booking_type_box = ttk.Combobox(
        card,
        textvariable=booking_type_var,
        values=["Passenger", "Goods", "Both"],
        state="readonly",
        font=("Arial", 10),
        width=42,
    )
    booking_type_box.pack(anchor="w", ipady=4, pady=(0, 14))

    # FRAME FOR PASSENGER AND GOODS DETAILS
    details_frame = Frame(card, bg=WHITE)
    details_frame.pack(fill=X)

    # PASSENGER DETAILS
    passenger_frame = Frame(details_frame, bg=WHITE)

    Label(
        passenger_frame,
        text="Number of Passengers",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT,
    ).pack(anchor="w", pady=(0, 5))

    passenger_var = StringVar(value="1")

    passenger_box = ttk.Combobox(
        passenger_frame,
        textvariable=passenger_var,
        values=["1", "2", "3", "4", "5"],
        state="readonly",
        font=("Arial", 10),
        width=42,
    )
    passenger_box.pack(anchor="w", ipady=4, pady=(0, 14))

    # GOODS DETAILS
    goods_frame = Frame(details_frame, bg=WHITE)

    Label(
        goods_frame,
        text="Goods Description",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT,
    ).pack(anchor="w", pady=(0, 5))

    goods_var = StringVar()

    goods_entry = Entry(
        goods_frame, textvariable=goods_var, font=("Arial", 10), width=45
    )
    goods_entry.pack(anchor="w", ipady=4, pady=(0, 14))

    Label(
        goods_frame, text="Load Size", font=("Arial", 10, "bold"), bg=WHITE, fg=TEXT
    ).pack(anchor="w", pady=(0, 5))

    load_size_var = StringVar(value="Small")

    load_size_box = ttk.Combobox(
        goods_frame,
        textvariable=load_size_var,
        values=["Small", "Medium", "Large"],
        state="readonly",
        font=("Arial", 10),
        width=42,
    )
    load_size_box.pack(anchor="w", ipady=4, pady=(0, 14))

    # ESTIMATED FARE
    fare_label = Label(
        card,
        text="Estimated fare: Select your route",
        font=("Arial", 13, "bold"),
        bg=WHITE,
        fg=GREEN,
    )
    fare_label.pack(anchor="w", pady=(2, 15))

    # LOAD REGISTERED PARKS
    def load_parks(event=None):
        town = pickup_var.get()
        park_box.set("")

        if not town:
            park_box["values"] = []
            park_note.config(
                text="Choose a pickup town to load its registered parks.", fg=MUTED
            )
            return

        try:
            connect.cur.execute(
                """SELECT park_name FROM motor_parks
                WHERE town = ? AND is_active = 1
                ORDER BY park_name""",
                (town,),
            )

            parks = [row[0] for row in connect.cur.fetchall()]
            park_box["values"] = parks

            if parks:
                park_note.config(
                    text=f"{len(parks)} registered park(s) available in {town}.",
                    fg=GREEN,
                )
                park_box.current(0)
            else:
                park_note.config(
                    text="No active motor park is registered for this town yet.", fg=RED
                )

        except Exception as error:
            park_note.config(text=f"Could not load parks: {error}", fg=RED)

    # SHOW THE CORRECT DETAILS
    def update_details(event=None):
        booking_type = booking_type_var.get()

        passenger_frame.pack_forget()
        goods_frame.pack_forget()

        if booking_type in ["Passenger", "Both"]:
            passenger_frame.pack(fill=X)

        if booking_type in ["Goods", "Both"]:
            goods_frame.pack(fill=X)

        update_fare()

    # CALCULATE ESTIMATED FARE
    def update_fare(event=None):
        pickup_town = pickup_var.get()
        destination_town = destination_var.get()
        booking_type = booking_type_var.get()

        if not pickup_town or not destination_town:
            fare_label.config(text="Estimated fare: Select your route", fg=GREEN)
            return

        if pickup_town == destination_town:
            fare_label.config(text="Pickup and destination must be different.", fg=RED)
            return

        passenger_count = 1
        load_size = "Small"

        if booking_type in ["Passenger", "Both"]:
            if not passenger_var.get():
                fare_label.config(
                    text="Please select the number of passengers.", fg=RED
                )
                return

            passenger_count = int(passenger_var.get())

        if booking_type in ["Goods", "Both"]:
            if not goods_var.get().strip():
                fare_label.config(text="Enter a description of the goods.", fg=RED)
                return

            if not load_size_var.get():
                fare_label.config(text="Please select the load size.", fg=RED)
                return

            load_size = load_size_var.get()

        fare, error = calculate_fare(
            pickup_town, destination_town, booking_type, passenger_count, load_size
        )

        if error:
            fare_label.config(text=error, fg=RED)
        else:
            fare_label.config(
                text=f"Estimated fare: ₦{fare:,.2f}", fg=GREEN
            )

    # CONNECT THE EVENTS
    pickup_box.bind("<<ComboboxSelected>>", load_parks)
    pickup_box.bind("<<ComboboxSelected>>", update_fare, add="+")
    destination_box.bind("<<ComboboxSelected>>", update_fare)
    booking_type_box.bind("<<ComboboxSelected>>", update_details)
    passenger_box.bind("<<ComboboxSelected>>", update_fare)
    load_size_box.bind("<<ComboboxSelected>>", update_fare)
    goods_entry.bind("<KeyRelease>", update_fare)

    # INITIAL DISPLAY
    if pickup_var.get():
        load_parks()

    update_details()

    # BUTTONS
    buttons = Frame(card, bg=WHITE)
    buttons.pack(fill=X, pady=(5, 0))

    styled_button(
        buttons,
        "Book Ride",
        lambda: save_booking(
            pickup_var.get(),
            park_var.get(),
            destination_var.get(),
            booking_type_var.get(),
            passenger_var.get(),
            goods_var.get(),
            load_size_var.get(),
        ),
        GREEN,
    ).pack(side=LEFT, padx=(0, 8))

    styled_button(buttons, "Clear", lambda: book_ride()).pack(side=LEFT)

    Label(
        content_frame,
        text="Fare note: Distances and fares are estimates not live data",
        font=("Arial", 9),
        bg=BG,
        fg=MUTED,
        wraplength=760,
        justify=LEFT,
    ).pack(anchor="w", padx=30, pady=(0, 20))


def my_rides():
    clear_page("My Rides")

    page_heading(
        "My Rides",
        "Track your bookings, pickup park, goods or passenger details, and driver arrival.",
    )

    if user_id is None:
        Label(
            content_frame,
            text="Customer ID not found. Please log in again.",
            bg=BG,
            fg=RED,
        ).pack(pady=20)
        return

    card = make_card(content_frame, 10, 10)
    card.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    # TABLE COLUMNS
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
        "arrival",
        "status",
        "date",
    )

    tree = ttk.Treeview(card, columns=columns, show="headings", height=18)

    headings = {
        "id": "Booking ID",
        "pickup": "Pickup Town",
        "park": "Motor Park",
        "destination": "Destination",
        "booking_type": "Booking Type",
        "passengers": "Passengers",
        "goods": "Goods Description",
        "load_size": "Load Size",
        "fare": "Estimated Fare",
        "arrival": "Driver Arrival",
        "status": "Status",
        "date": "Booking Date",
    }

    widths = {
        "id": 85,
        "pickup": 130,
        "park": 170,
        "destination": 130,
        "booking_type": 115,
        "passengers": 95,
        "goods": 180,
        "load_size": 95,
        "fare": 120,
        "arrival": 150,
        "status": 110,
        "date": 175,
    }

    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], minwidth=70, anchor="center", stretch=False)

    # VERTICAL SCROLLBAR
    vertical_scroll = ttk.Scrollbar(card, orient=VERTICAL, command=tree.yview)

    # HORIZONTAL SCROLLBAR
    horizontal_scroll = ttk.Scrollbar(card, orient=HORIZONTAL, command=tree.xview)

    tree.configure(
        yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set
    )

    tree.pack(side=TOP, fill=BOTH, expand=True, padx=(4, 0), pady=(4, 0))

    horizontal_scroll.pack(side=BOTTOM, fill=X, padx=4, pady=(0, 4))

    vertical_scroll.pack(side=RIGHT, fill=Y, pady=4)

    # LOAD CUSTOMER BOOKINGS
    def load_rides():
        tree.delete(*tree.get_children())

        try:
            connect.cur.execute(
                """
                SELECT
                    booking_id,
                    pickup_location,
                    pickup_park,
                    destination,
                    booking_type,
                    passenger_count,
                    goods_type,
                    load_size,
                    fare,
                    estimated_arrival,
                    booking_status,
                    booking_date
                FROM bookings
                WHERE user_id = ?
                ORDER BY booking_id DESC
                """,
                (user_id,),
            )

            rides = connect.cur.fetchall()

            for ride in rides:
                booking_type = ride[4] or "Passenger"

                passenger_count = str(ride[5]) if ride[5] is not None else "N/A"

                goods_description = ride[6] or "N/A"
                load_size = ride[7] or "N/A"

                # SHOW ONLY THE DETAILS RELEVANT TO THE BOOKING
                if booking_type == "Passenger":
                    goods_description = "N/A"
                    load_size = "N/A"

                elif booking_type == "Goods":
                    passenger_count = "N/A"

                tree.insert(
                    "",
                    END,
                    values=(
                        ride[0],
                        ride[1],
                        ride[2] or "Not set",
                        ride[3],
                        booking_type,
                        passenger_count,
                        goods_description,
                        load_size,
                        f"₦{(ride[8] or 0):,.2f}",
                        ride[9] or "Not set",
                        ride[10] or "Pending",
                        ride[11] or "Not set",
                    ),
                )

        except Exception as error:
            msg.showerror("Database Error", f"Could not load rides:\n{error}")

    # DELETE A PENDING BOOKING
    def delete_ride():
        selected = tree.selection()

        if not selected:
            msg.showwarning("No Selection", "Please select a ride first.")
            return

        values = tree.item(selected[0], "values")

        booking_id = values[0]

        # STATUS IS NOW COLUMN INDEX 10
        status = values[10].strip().lower()

        if status != "pending":
            msg.showwarning("Cannot Delete", "Only pending rides can be deleted.")
            return

        if not msg.askyesno("Delete Ride", "Delete this pending booking?"):
            return

        try:
            connect.cur.execute(
                """
                DELETE FROM bookings
                WHERE booking_id = ?
                AND user_id = ?
                AND LOWER(booking_status) = 'pending'
                """,
                (booking_id, user_id),
            )

            connect.con.commit()

            msg.showinfo("Ride Deleted", "The pending booking has been deleted.")

            load_rides()

        except Exception as error:
            connect.con.rollback()

            msg.showerror("Delete Error", f"Could not delete ride:\n{error}")

    # PAGE BUTTONS
    buttons = Frame(content_frame, bg=BG)
    buttons.pack(fill=X, padx=28, pady=(5, 20))

    styled_button(buttons, "Refresh", load_rides, BLUE_DARK).pack(
        side=RIGHT, padx=(8, 0)
    )

    styled_button(buttons, "Delete Pending Ride", delete_ride, RED).pack(side=LEFT)

    load_rides()


def notifications_page():
    clear_page("Notifications")
    page_heading("Notifications", "Booking updates and estimated driver arrival times")
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
                (user_id,),
            )
            rows = connect.cur.fetchall()
        except Exception:
            Label(
                list_frame,
                text="Notification records are not available.",
                bg=WHITE,
                fg=MUTED,
            ).pack(anchor="w", pady=10)
            refresh_header()
            return
        if not rows:
            Label(list_frame, text="No notifications yet.", bg=WHITE, fg=MUTED).pack(
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
                wraplength=700,
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
                (nid, user_id),
            )
            connect.con.commit()
            load_notifications()
        except Exception as error:
            connect.con.rollback()
            msg.showerror("Error", str(error))

    load_notifications()


def profile_page():
    clear_page("My Profile")
    page_heading("My Profile", "Manage your personal information")

    customer = get_customer()

    if not customer:
        msg.showerror(
            "Profile Error", "Customer details could not be found. Please log in again."
        )
        return

    # IDENTITY CARD
    identity = make_card(content_frame, 20, 16)
    identity.pack(fill=X, padx=28, pady=(0, 14))

    row = Frame(identity, bg=WHITE)
    row.pack(fill=X)

    initials = "".join(
        word[0] for word in (customer[0] or "Customer").split()[:2]
    ).upper()

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
        text=customer[0] or "Customer",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=NAVY,
    ).pack(anchor="w")

    Label(
        identity_text, text="Customer Account", font=("Arial", 9), bg=WHITE, fg=MUTED
    ).pack(anchor="w", pady=(3, 0))

    # PERSONAL INFORMATION CARD
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

    name_e = make_field("Full Name", customer[0], 0, 0)
    username_e = make_field("Username (cannot be changed)", customer[1], 0, 1, True)
    email_e = make_field("Email Address", customer[2], 1, 0)
    gender_e = make_field("Gender", customer[3], 1, 1)
    address_e = make_field("Home Address", customer[4], 2, 0)
    dob_e = make_field("Date of Birth", customer[5], 2, 1)

    def save_profile():
        name = name_e.get().strip()
        email = email_e.get().strip()
        gender = gender_e.get().strip()
        address = address_e.get().strip()
        dob = dob_e.get().strip()

        if not name or not email:
            msg.showwarning("Prompt", "Name and email are required")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            msg.showwarning("Error", "Please enter a valid email address")
            return

        try:
            connect.cur.execute(
                """UPDATE users
                   SET name = ?, email = ?, gender = ?, address = ?, dob = ?
                   WHERE id = ?
                   AND LOWER(role) IN ('customer', 'user')""",
                (name, email, gender, address, dob, user_id),
            )

            connect.con.commit()

            msg.showinfo("Success", "Your profile has been updated")
            refresh_header()
            profile_page()

        except Exception:
            connect.con.rollback()
            msg.showerror(
                "Failed",
                "Could not save your details. This email may already be registered",
            )

    styled_button(details, "Save Changes", save_profile).pack(anchor="w", pady=(3, 0))

    # CHANGE PASSWORD CARD
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
            password_card, font=("Arial", 10), show="*", relief=SOLID, bd=1, width=30
        )
        entry.pack(anchor="w", ipady=5, pady=(0, 9))

        return entry

    current_e = password_field("Current Password")
    new_e = password_field("New Password")
    confirm_e = password_field("Confirm New Password")

    def save_password():
        current = current_e.get()
        new = new_e.get()
        confirm = confirm_e.get()

        if not current or not new or not confirm:
            msg.showwarning(
                "Missing Information", "Please fill in all password fields."
            )
            return

        if len(new) < 6:
            msg.showwarning(
                "Prompt", "Your new password must contain at least 6 characters."
            )
            return

        if new != confirm:
            msg.showerror("Error", "The new passwords do not match.")
            return

        if current == new:
            msg.showwarning(
                "Error",
                "Your new password must be different from your current password.",
            )
            return

        try:
            connect.cur.execute(
                """SELECT password FROM users
                   WHERE id = ?
                   AND LOWER(role) IN ('customer', 'user')""",
                (user_id,),
            )
            result = connect.cur.fetchone()

            if result is None or result[0] != current:
                msg.showerror(
                    "Error", "Incorrect Password"
                )
                return

            connect.cur.execute(
                """UPDATE users SET password = ?
                   WHERE id = ?
                   AND LOWER(role) IN ('customer', 'user')""",
                (new, user_id),
            )
            connect.con.commit()

            msg.showinfo("Success", "Your password has been updated successfully")

            current_e.delete(0, END)
            new_e.delete(0, END)
            confirm_e.delete(0, END)

        except Exception as error:
            connect.con.rollback()
            msg.showerror("Failed", f"Could not update your password:\n{error}")

    styled_button(password_card, "Update Password", save_password).pack(anchor="w")


# SIDE BAR MENU
Label(
    sidebar, text="TRAVEL", font=("Arial", 16, "bold"), bg=NAVY, fg=WHITE
).pack(anchor="w", padx=20, pady=(28, 3))
Label(
    sidebar, text="CUSTOMER ACCOUNT", font=("Arial", 8, "bold"), bg=NAVY, fg="#9fb7d1"
).pack(anchor="w", padx=21, pady=(0, 25))
menu_items = [
    ("Dashboard", "▦", dashboard),
    ("Book a Ride", "＋", book_ride),
    ("My Rides", "▤", my_rides),
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
