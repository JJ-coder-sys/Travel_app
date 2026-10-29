
import os
import sqlite3 as sql
import sys
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry

import control as connect


# OPEN LOGIN PAGE
def login():
    root.destroy()
    os.system(f'"{sys.executable}" login.py')


# REGISTER USER
def register():
    name = entn.get().strip()
    username = entu.get().strip()
    email = entem.get().strip()
    password = entp.get()
    gender = entg.get()
    address = enta.get("1.0", "end").strip()
    dob = date_entry.get()
    role = user_role.get()

    if (
        not name
        or not username
        or not email
        or not password
        or not gender
        or not address
        or not role
    ):
        msg.showerror("Error", "Please fill in all fields")
        return

    if "@" not in email:
        msg.showerror("Error", "Email must contain '@'")
        return

    if len(password) < 6:
        msg.showerror(
            "Error",
            "Password must contain at least 6 characters"
        )
        return

    try:
        connect.cur.execute(
            """
            INSERT INTO users
            (name, username, email, password, gender,
             address, dob, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name, username, email, password,
                gender, address, dob, role
            )
        )

        connect.con.commit()

        msg.showinfo(
            "Success",
            "Account created successfully"
        )

    except sql.IntegrityError:
        msg.showerror(
            "Error",
            "Email or Username already exists"
        )


# SHOW AND HIDE PASSWORD
def toggle_password():
    if entp.cget("show") == "*":
        entp.config(show="")
        btn_show.config(text="Hide")
    else:
        entp.config(show="*")
        btn_show.config(text="Show")


# MAIN WINDOW
root = Tk()
root.title("Create Account")
root.geometry("1100x760+100+20")
root.configure(bg="#f4f7fb")
root.resizable(False, False)


# LEFT PANEL
left_panel = Frame(root, bg="#12355b", width=400)
left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)


# LOGO
try:
    logo_image = Image.open("image/logo.jpg")
    logo_image = logo_image.resize((200, 150))
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = Label(
        left_panel,
        image=logo_photo,
        bg="#12355b"
    )
    logo_label.pack(pady=(80, 20))

except Exception:
    Label(
        left_panel,
        text="🚗",
        font=("Arial", 55),
        bg="#12355b",
        fg="white"
    ).pack(pady=(100, 20))


Label(
    left_panel,
    text="TRAVEL",
    font=("Arial", 23, "bold"),
    bg="#12355b",
    fg="white"
).pack(pady=10)

Label(
    left_panel,
    text="Your journey starts here...",
    font=("Arial", 12),
    bg="#12355b",
    fg="#dce7f5"
).pack(pady=5)

Label(
    left_panel,
    text=(
        "\nCreate your account to book rides\n"
        "manage your trips and enjoy\n"
        "a convenient travel experience 🚕"
    ),
    font=("Arial", 11),
    bg="#12355b",
    fg="#dce7f5",
    justify="center"
).pack(pady=25)

Label(
    left_panel,
    text="SAFE  •  SIMPLE  •  RELIABLE",
    font=("Arial", 10, "bold"),
    bg="#12355b",
    fg="white"
).pack(side="bottom", pady=35)


# RIGHT SIDE
right_panel = Frame(root, bg="#f4f7fb")
right_panel.pack(side="right", fill="both", expand=True)


# REGISTRATION CARD
card = Frame(
    right_panel,
    bg="white",
    padx=35,
    pady=22,
    highlightbackground="#e1e7ef",
    highlightthickness=1
)
card.place(relx=0.5, rely=0.5, anchor="center")


# FORM TITLE
Label(
    card,
    text="Create Your Account",
    font=("Arial", 23, "bold"),
    bg="white",
    fg="#12355b"
).grid(row=0, column=0, columnspan=2, sticky="w")

Label(
    card,
    text="Enter your details to get started",
    font=("Arial", 10),
    bg="white",
    fg="#718096"
).grid(
    row=1, column=0, columnspan=2,
    sticky="w", pady=(3, 16)
)


# LABEL STYLE
def field_label(text, row):
    Label(
        card,
        text=text,
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#344054"
    ).grid(
        row=row, column=0,
        sticky="w", pady=6
    )


# ENTRY STYLE
def create_entry(row, show=None):
    entry = Entry(
        card,
        width=32,
        font=("Arial", 10),
        relief="solid",
        bd=1,
        bg="#ffffff",
        fg="#263238",
        insertbackground="#12355b",
        show=show
    )

    entry.grid(
        row=row, column=1,
        sticky="ew", pady=6, ipady=5
    )

    return entry


# FULL NAME
field_label("Full Name", 2)
entn = create_entry(2)


# USERNAME
field_label("Username", 3)
entu = create_entry(3)


# EMAIL
field_label("Email Address", 4)
entem = create_entry(4)


# PASSWORD
field_label("Password", 5)

password_frame = Frame(card, bg="white")
password_frame.grid(
    row=5, column=1,
    sticky="ew", pady=6
)

entp = Entry(
    password_frame,
    width=24,
    font=("Arial", 10),
    relief="solid",
    bd=1,
    bg="white",
    show="*"
)
entp.pack(side="left", ipady=5)

btn_show = Button(
    password_frame,
    text="Show",
    font=("Arial", 9, "bold"),
    bg="white",
    fg="#12355b",
    relief="flat",
    cursor="hand2",
    command=toggle_password
)
btn_show.pack(side="left", padx=5)


# GENDER
field_label("Gender", 6)

entg = ttk.Combobox(
    card,
    width=30,
    values=["Male", "Female"],
    state="readonly",
    font=("Arial", 10)
)
entg.grid(
    row=6, column=1,
    sticky="ew", pady=6, ipady=3
)
entg.current(0)


# ADDRESS
field_label("Home Address", 7)

enta = Text(
    card,
    width=30,
    height=2,
    font=("Arial", 10),
    relief="solid",
    bd=1,
    wrap="word"
)
enta.grid(
    row=7, column=1,
    sticky="ew", pady=5
)


# DATE OF BIRTH
field_label("Date of Birth", 8)

date_entry = DateEntry(
    card,
    width=30,
    borderwidth=1,
    date_pattern="dd/mm/yyyy",
    font=("Arial", 10),
    background="#12355b",
    foreground="white"
)
date_entry.grid(
    row=8, column=1,
    sticky="ew", pady=6, ipady=3
)


# ACCOUNT
field_label("Account", 9)

user_role = ttk.Combobox(
    card,
    width=30,
    values=["Customer", "Driver"],
    state="readonly",
    font=("Arial", 10)
)
user_role.grid(
    row=9, column=1,
    sticky="ew", pady=6, ipady=3
)
user_role.current(0)


# REGISTER BUTTON
btnReg = Button(
    card,
    text="Sign Up",
    font=("Arial", 11),
    bg="#12355b",
    fg="white",
    activebackground="#1e6091",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=register
)
btnReg.grid(
    row=10, column=0, columnspan=2,
    sticky="ew", padx=150, ipady=0
)


# BUTTON HOVER EFFECT
def register_enter(event):
    btnReg.config(bg="#1e6091")


def register_leave(event):
    btnReg.config(bg="#12355b")


btnReg.bind("<Enter>", register_enter)
btnReg.bind("<Leave>", register_leave)


# LOGIN LINK
Label(
    card,
    text="Already have an account?",
    font=("Arial", 10),
    bg="white",
    fg="#718096"
).grid(row=11, column=0, sticky="e", pady=(5, 0))

login_btn = Button(
    card,
    text="Login",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#12355b",
    activebackground="white",
    activeforeground="#1e6091",
    relief="flat",
    cursor="hand2",
    command=login
)
login_btn.grid(
    row=11, column=1,
    sticky="w", padx=5, pady=(5, 0)
)


# ENTER KEY TO REGISTER
root.bind("<Return>", lambda event: register())


root.mainloop()
