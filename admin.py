from tkinter import *
from tkinter import ttk, messagebox as msg
import sys
import os
import control as connect

# GET ADMIN ID
if len(sys.argv) > 1:
    try:
        admin_id = int(sys.argv[1])
    except ValueError:
        admin_id = 0
else:
    admin_id = 0

# MAIN WINDOW
root = Tk()
root.title("Administration")
root.geometry("1250x750")
root.minsize(1100, 650)
root.configure(bg="#f4f7fb")

NAVY = "#12355b"
BLUE = "#2878d0"
WHITE = "#ffffff"
BG = "#f4f7fb"
TEXT = "#26374a"
MUTED = "#7b8794"
GREEN = "#159b72"
ORANGE = "#e99a32"
RED = "#d9534f"
active_button = None

sidebar = Frame(root, bg=NAVY, width=220)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)
main_area = Frame(root, bg=BG)
main_area.pack(side=LEFT, fill=BOTH, expand=True)

top_bar = Frame(main_area, bg=WHITE, height=65)
top_bar.pack(fill=X)
top_bar.pack_propagate(False)
Label(
    top_bar, text="Admin Workspace", font=("Arial", 13, "bold"), fg=TEXT, bg=WHITE
).pack(side=LEFT, padx=25)
notification_button = Button(
    top_bar,
    text="🔔 Notifications",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=NAVY,
    bd=0,
    cursor="hand2",
    activebackground="#e8f1fc",
    command=lambda: show_notifications(),
)
notification_button.pack(side=RIGHT, padx=15, ipady=5)
Label(
    top_bar, text="Administrator", font=("Arial", 10, "bold"), fg=NAVY, bg=WHITE
).pack(side=RIGHT, padx=10)
content_frame = Frame(main_area, bg=BG)
content_frame.pack(fill=BOTH, expand=True, padx=25, pady=20)

style = ttk.Style()
style.configure(
    "Treeview",
    font=("Arial", 9),
    rowheight=30,
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT,
)
style.configure("Treeview.Heading", font=("Arial", 9, "bold"), padding=7)


def clear_page():
    for widget in content_frame.winfo_children():
        widget.destroy()


def page_heading(title, description):
    Label(content_frame, text=title, font=("Arial", 22, "bold"), fg=TEXT, bg=BG).pack(
        anchor="w"
    )
    Label(content_frame, text=description, font=("Arial", 10), fg=MUTED, bg=BG).pack(
        anchor="w", pady=(5, 18)
    )


def get_count(query, params=()):
    try:
        connect.cur.execute(query, params)
        row = connect.cur.fetchone()
        return row[0] if row and row[0] is not None else 0
    except Exception:
        return 0


def make_table(parent, columns, headings, widths=None, height=12):
    frame = Frame(parent, bg=WHITE)
    frame.pack(fill=BOTH, expand=True)

    table = ttk.Treeview(frame, columns=columns, show="headings", height=height)

    for col in columns:
        table.heading(col, text=headings.get(col, col.replace("_", " ").title()))
        table.column(
            col,
            width=(widths or {}).get(col, 120),
            minwidth=80,
            anchor="center",
            stretch=False,
        )

    vertical_scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=table.yview)

    horizontal_scroll = ttk.Scrollbar(frame, orient=HORIZONTAL, command=table.xview)

    table.configure(
        yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set
    )

    table.pack(side=LEFT, fill=BOTH, expand=True)
    vertical_scroll.pack(side=RIGHT, fill=Y)
    horizontal_scroll.pack(side=BOTTOM, fill=X)

    return table


def dashboard():
    clear_page()
    page_heading("Dashboard", "Here is an overview of your system")
    cards = Frame(content_frame, bg=BG)
    cards.pack(fill=X, pady=(0, 20))
    stats = [
        (
            "♙",
            "Total Customers",
            get_count(
                "SELECT COUNT(*) FROM users WHERE LOWER(role) IN ('customer','user')"
            ),
            BLUE,
        ),
        (
            "🚘",
            "Total Drivers",
            get_count("SELECT COUNT(*) FROM users WHERE LOWER(role)='driver'"),
            GREEN,
        ),
        ("▤", "Total Bookings", get_count("SELECT COUNT(*) FROM bookings"), ORANGE),
        (
            "◷",
            "Pending Rides",
            get_count(
                "SELECT COUNT(*) FROM bookings WHERE LOWER(booking_status)='pending'"
            ),
            RED,
        ),
    ]
    for symbol, title, value, color in stats:
        card = Frame(
            cards, bg=WHITE, highlightbackground="#e1e8f0", highlightthickness=1
        )
        card.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        Label(card, text=symbol, font=("Arial", 22, "bold"), fg=color, bg=WHITE).pack(
            anchor="w", padx=13, pady=(12, 4)
        )
        Label(card, text=title, font=("Arial", 9), fg=MUTED, bg=WHITE).pack(
            anchor="w", padx=13
        )
        Label(
            card, text=str(value), font=("Arial", 22, "bold"), fg=TEXT, bg=WHITE
        ).pack(anchor="w", padx=13, pady=(4, 12))
    Label(
        content_frame,
        text="Recent Bookings",
        font=("Arial", 13, "bold"),
        fg=TEXT,
        bg=BG,
    ).pack(anchor="w", pady=(0, 8))
    columns = (
        "booking_id",
        "user_id",
        "pickup",
        "park",
        "destination",
        "booking_type",
        "passengers",
        "goods",
        "load_size",
        "fare",
        "status",
    )

    table = make_table(
        content_frame,
        columns,
        {
            "booking_id": "Booking ID",
            "user_id": "Customer ID",
            "pickup": "Pickup Town",
            "park": "Pickup Park",
            "destination": "Destination",
            "booking_type": "Booking Type",
            "passengers": "Passengers",
            "goods": "Goods Description",
            "load_size": "Load Size",
            "fare": "Fare",
            "status": "Status",
        },
        {
            "booking_id": 85,
            "user_id": 90,
            "pickup": 115,
            "park": 145,
            "destination": 115,
            "booking_type": 105,
            "passengers": 85,
            "goods": 150,
            "load_size": 90,
            "fare": 100,
            "status": 100,
        },
        height=8,
    )

    try:
        connect.cur.execute("""
            SELECT booking_id, user_id, pickup_location,
                   COALESCE(pickup_park, ''),
                   destination,
                   COALESCE(booking_type, vehicle_type, 'Passenger'),
                   COALESCE(passenger_count, 'N/A'),
                   COALESCE(goods_type, 'N/A'),
                   COALESCE(load_size, 'N/A'),
                   fare, booking_status
            FROM bookings
            ORDER BY booking_id DESC
            LIMIT 10
            """)

        for row in connect.cur.fetchall():
            table.insert("", END, values=row)

    except Exception as error:
        msg.showerror(
            "Database Error", "Could not load recent bookings.\n\n" + str(error)
        )


def manage_users():
    clear_page()
    page_heading(
        "Manage Users", "Search, view, and remove registered customers or drivers."
    )
    search_frame = Frame(content_frame, bg=BG)
    search_frame.pack(fill=X, pady=(0, 12))
    search_entry = Entry(search_frame, font=("Arial", 11), relief=SOLID)
    search_entry.pack(side=LEFT, fill=X, expand=True, ipady=7)
    columns = ("id", "name", "username", "email", "role")
    table = make_table(
        content_frame,
        columns,
        {
            "id": "User ID",
            "name": "Name",
            "username": "Username",
            "email": "Email",
            "role": "Role",
        },
    )

    def load_users():
        table.delete(*table.get_children())
        term = "%" + search_entry.get().strip() + "%"
        try:
            connect.cur.execute(
                """SELECT id, name, username, email, role FROM users
                WHERE LOWER(role) IN ('customer','user','driver')
                AND (name LIKE ? OR username LIKE ? OR email LIKE ? OR role LIKE ?) ORDER BY id DESC""",
                (term, term, term, term),
            )
            for row in connect.cur.fetchall():
                table.insert("", END, values=row)
        except Exception as error:
            msg.showerror("Database Error", str(error))

    Button(
        search_frame,
        text="Search",
        bg=BLUE,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=load_users,
    ).pack(side=LEFT, padx=8, ipadx=12, ipady=6)

    def delete_user():
        selected = table.selection()
        if not selected:
            msg.showwarning("No Selection", "Select a user first.")
            return
        user_id = table.item(selected[0], "values")[0]
        if not msg.askyesno(
            "Confirm Delete", "Delete this user? Related bookings may prevent deletion."
        ):
            return
        try:
            connect.cur.execute("DELETE FROM users WHERE id=?", (user_id,))
            connect.con.commit()
            load_users()
            msg.showinfo("Success", "User deleted successfully.")
        except Exception as error:
            connect.con.rollback()
            msg.showerror(
                "Cannot Delete", "This user may have related bookings.\n\n" + str(error)
            )

    Button(
        content_frame,
        text="Delete Selected User",
        bg=RED,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=delete_user,
    ).pack(anchor="e", pady=10, ipadx=12, ipady=7)
    load_users()


def manage_bookings():
    clear_page()
    page_heading(
        "Manage Bookings",
        "Review bookings, view transport details, and update booking status.",
    )

    columns = (
        "booking_id",
        "user_id",
        "pickup",
        "park",
        "destination",
        "booking_type",
        "passengers",
        "goods",
        "load_size",
        "fare",
        "status",
    )

    table = make_table(
        content_frame,
        columns,
        {
            "booking_id": "Booking ID",
            "user_id": "Customer ID",
            "pickup": "Pickup Town",
            "park": "Pickup Park",
            "destination": "Destination",
            "booking_type": "Booking Type",
            "passengers": "Passengers",
            "goods": "Goods Description",
            "load_size": "Load Size",
            "fare": "Fare",
            "status": "Status",
        },
        {
            "booking_id": 85,
            "user_id": 90,
            "pickup": 115,
            "park": 145,
            "destination": 115,
            "booking_type": 105,
            "passengers": 85,
            "goods": 150,
            "load_size": 90,
            "fare": 100,
            "status": 100,
        },
        height=12,
    )

    def load_bookings():
        table.delete(*table.get_children())

        try:
            connect.cur.execute("""
                SELECT booking_id, user_id, pickup_location,
                       COALESCE(pickup_park, ''),
                       destination,
                       COALESCE(booking_type, vehicle_type, 'Passenger'),
                       COALESCE(passenger_count, 'N/A'),
                       COALESCE(goods_type, 'N/A'),
                       COALESCE(load_size, 'N/A'),
                       fare, booking_status
                FROM bookings
                ORDER BY booking_id DESC
                """)

            for row in connect.cur.fetchall():
                table.insert("", END, values=row)

        except Exception as error:
            msg.showerror("Database Error", "Could not load bookings.\n\n" + str(error))

    def update_status():
        selected = table.selection()

        if not selected:
            msg.showwarning("No Selection", "Select a booking first.")
            return

        booking = table.item(selected[0], "values")
        booking_id = booking[0]
        current_status = booking[10]

        win = Toplevel(root)
        win.title("Update Booking Status")
        win.geometry("340x220")
        win.configure(bg=WHITE)
        win.resizable(False, False)

        Label(
            win, text="Select New Status", font=("Arial", 12, "bold"), bg=WHITE, fg=NAVY
        ).pack(pady=(25, 12))

        status_box = ttk.Combobox(
            win,
            values=[
                "Pending",
                "Accepted",
                "In Progress",
                "Completed",
                "Rejected",
            ],
            state="readonly",
        )
        status_box.pack(fill=X, padx=25)
        status_box.set(current_status)

        def save_status():
            new_status = status_box.get()

            if not new_status:
                msg.showwarning("Missing Status", "Choose a booking status.")
                return

            if new_status == "Accepted":
                msg.showwarning(
                    "Driver Assignment",
                    "Changing a booking to Accepted here does not assign a driver. "
                    "Use the driver's Ride Requests page to accept and assign the ride.",
                )
                return

            try:
                connect.cur.execute(
                    """
                    UPDATE bookings
                    SET booking_status = ?
                    WHERE booking_id = ?
                    """,
                    (new_status, booking_id),
                )

                connect.con.commit()
                win.destroy()
                load_bookings()

                msg.showinfo("Success", "Booking status updated successfully.")

            except Exception as error:
                connect.con.rollback()
                msg.showerror("Database Error", str(error))

        Button(
            win,
            text="Save Changes",
            bg=BLUE,
            fg=WHITE,
            bd=0,
            cursor="hand2",
            command=save_status,
        ).pack(pady=18, ipadx=15, ipady=6)

    Button(
        content_frame,
        text="Update Booking Status",
        bg=BLUE,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=update_status,
    ).pack(anchor="e", pady=10, ipadx=12, ipady=7)

    load_bookings()


def manage_drivers():
    clear_page()
    page_heading("Manage Drivers", "View drivers and change their availability.")
    columns = ("id", "name", "username", "email", "availability")
    table = make_table(
        content_frame,
        columns,
        {
            "id": "Driver ID",
            "name": "Name",
            "username": "Username",
            "email": "Email",
            "availability": "Availability",
        },
    )

    def load_drivers():
        table.delete(*table.get_children())
        try:
            connect.cur.execute(
                "SELECT id, name, username, email, COALESCE(availability,'Available') FROM users WHERE LOWER(role)='driver' ORDER BY id DESC"
            )
            for row in connect.cur.fetchall():
                table.insert("", END, values=row)
        except Exception as error:
            msg.showerror(
                "Database Error",
                "Could not load drivers. Check the availability column.\n\n"
                + str(error),
            )

    def change_availability():
        selected = table.selection()
        if not selected:
            msg.showwarning("Prompt", "Select a driver first")
            return
        driver = table.item(selected[0], "values")
        win = Toplevel(root)
        win.title("Driver Availability")
        win.geometry("320x190")
        win.configure(bg=WHITE)
        Label(
            win,
            text="Set Driver Availability",
            font=("Arial", 12, "bold"),
            fg=NAVY,
            bg=WHITE,
        ).pack(pady=(25, 12))
        choice = ttk.Combobox(
            win, values=["Available", "Unavailable"], state="readonly"
        )
        choice.pack(fill=X, padx=25)
        choice.set(driver[4] or "Available")

        def save():
            try:
                connect.cur.execute(
                    "UPDATE users SET availability=? WHERE id=?",
                    (choice.get(), driver[0]),
                )
                connect.con.commit()
                win.destroy()
                load_drivers()
                msg.showinfo("Success", "Driver availability updated")
            except Exception as error:
                connect.con.rollback()
                msg.showerror("Database Error", str(error))

        Button(
            win,
            text="Save Changes",
            bg=BLUE,
            fg=WHITE,
            bd=0,
            cursor="hand2",
            command=save,
        ).pack(pady=18, ipadx=15, ipady=6)

    Button(
        content_frame,
        text="Change Availability",
        bg=BLUE,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=change_availability,
    ).pack(anchor="e", pady=10, ipadx=12, ipady=7)
    load_drivers()


def show_notifications():
    clear_page()
    page_heading("Notifications", "Admin alerts and useful shortcuts")
    alerts = [
        (
            "🔔",
            "Pending bookings",
            "Review rides awaiting confirmation",
            manage_bookings,
        ),
        (
            "🚘",
            "Driver availability",
            "Check which drivers are available",
            manage_drivers,
        ),
        (
            "▤",
            "Registered users",
            "Review registered customers and drivers",
            manage_users,
        ),
    ]
    for symbol, title, description, command in alerts:
        card = Frame(
            content_frame, bg=WHITE, highlightbackground="#e1e8f0", highlightthickness=1
        )
        card.pack(fill=X, pady=7)
        Label(card, text=symbol, font=("Arial", 20), fg=BLUE, bg=WHITE).pack(
            side=LEFT, padx=18, pady=14
        )
        text_frame = Frame(card, bg=WHITE)
        text_frame.pack(side=LEFT, fill=X, expand=True, pady=12)
        Label(
            text_frame, text=title, font=("Arial", 11, "bold"), fg=TEXT, bg=WHITE
        ).pack(anchor="w")
        Label(text_frame, text=description, font=("Arial", 9), fg=MUTED, bg=WHITE).pack(
            anchor="w", pady=(4, 0)
        )
        Button(
            card, text="Open", bg=BLUE, fg=WHITE, bd=0, cursor="hand2", command=command
        ).pack(side=RIGHT, padx=15, ipadx=8, ipady=5)


def logout():
    if msg.askyesno("Logout", "Are you sure you want to log out?"):
        root.destroy()
        os.system(f'"{sys.executable}" admin_login.py')


def sidebar_button(symbol, title, command):
    global active_button
    button = Button(
        sidebar,
        text=symbol + "   " + title,
        font=("Arial", 10, "bold"),
        bg=NAVY,
        fg="#dce8f5",
        activebackground=BLUE,
        activeforeground=WHITE,
        bd=0,
        anchor="w",
        padx=20,
        pady=13,
        cursor="hand2",
        command=lambda: select_page(button, command),
    )
    button.pack(fill=X, padx=10, pady=3)

    def on_enter(event):
        if button != active_button:
            button.configure(bg="#1b4979")

    def on_leave(event):
        if button != active_button:
            button.configure(bg=NAVY)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button


def select_page(button, command):
    global active_button
    if active_button:
        active_button.configure(bg=NAVY, fg="#dce8f5")
    active_button = button
    active_button.configure(bg=BLUE, fg=WHITE)
    command()


Label(
    sidebar, text="🚘 TRAVEL", font=("Arial", 15, "bold"), fg=WHITE, bg=NAVY
).pack(anchor="w", padx=20, pady=(28, 3))
Label(
    sidebar, text="ADMINISTRATION", font=("Arial", 8, "bold"), fg="#a9c6e8", bg=NAVY
).pack(anchor="w", padx=21, pady=(7, 25))
sidebar_button("▦", "Dashboard", dashboard)
sidebar_button("♙", "Manage Users", manage_users)
sidebar_button("▤", "Manage Bookings", manage_bookings)
sidebar_button("🚘", "Manage Drivers", manage_drivers)
# Notifications remains available from the top button, not in the sidebar.
Frame(sidebar, bg=NAVY).pack(fill=BOTH, expand=True)
Label(
    sidebar, text="", font=("Arial", 8), fg="#a9c6e8", bg=NAVY
).pack(pady=(5, 8))
sidebar_button("⇥", "Logout", logout)


dashboard_button = sidebar.winfo_children()[2]
select_page(dashboard_button, dashboard)
root.mainloop()
