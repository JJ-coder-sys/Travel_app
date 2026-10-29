from tkinter import *
from tkinter import messagebox as msg
import os
import sys
import control as connect
from PIL import Image, ImageTk

# MAIN WINDOW
root = Tk()
root.title("Administration")
root.geometry("1000x650+150+40")
root.configure(bg="#f4f7fb")
root.resizable(False, False)


# MAIN FRAME
main_frame = Frame(root, bg="#f4f7fb")
main_frame.pack(fill=BOTH, expand=True)


# LEFT BRANDING PANEL
left_frame = Frame(main_frame, bg="#12355b", width=380)
left_frame.pack(side=LEFT, fill=Y)
left_frame.pack_propagate(False)


logo_image = Image.open("image/logo.jpg")
logo_image = logo_image.resize((200, 150))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = Label(left_frame, image=logo_photo, bg="#12355b")
logo_label.image = logo_photo
logo_label.pack(pady=(65, 25))


Label(
    left_frame, text="TRAVEL", font=("Arial", 23, "bold"), fg="white", bg="#12355b"
).pack(pady=10)


Label(
    left_frame,
    text="ADMINISTRATOR",
    font=("Arial", 12, "bold"),
    fg="#dce8f5",
    bg="#12355b",
).pack(pady=5)


Label(
    left_frame,
    text=("\nManage fleet operations\n" "and oversee scheduling\n\n"),
    font=("Arial", 12),
    fg="#dce8f5",
    bg="#12355b",
    justify=CENTER,
).pack(pady=25)


Label(
    left_frame,
    text="SECURE ADMIN ACCESS",
    font=("Arial", 10, "bold"),
    fg="white",
    bg="#12355b",
).pack(side=BOTTOM, pady=35)


# RIGHT PANEL
right_frame = Frame(main_frame, bg="#f4f7fb")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)


# LOGIN CARD
card = Frame(
    right_frame,
    bg="white",
    padx=40,
    pady=35,
    highlightbackground="#e1e7ef",
    highlightthickness=1,
)
card.place(relx=0.5, rely=0.5, anchor=CENTER)


# CARD HEADING
Label(
    card, text="Welcome Back", font=("Arial", 24, "bold"), bg="white", fg="#12355b"
).pack(anchor="w", pady=(0, 5))


Label(
    card, text="Sign in to your account", font=("Arial", 10), bg="white", fg="#718096"
).pack(anchor="w", pady=(0, 25))


# USERNAME
Label(
    card, text="Username or Email", font=("Arial", 10, "bold"), bg="white", fg="#344054"
).pack(anchor="w")


username_entry = Entry(
    card,
    font=("Arial", 11),
    width=32,
    bd=1,
    relief=SOLID,
    bg="white",
    fg="#263238",
    insertbackground="#12355b",
)
username_entry.pack(pady=(7, 18), ipady=7)


# PASSWORD
Label(card, text="Password", font=("Arial", 10, "bold"), bg="white", fg="#344054").pack(
    anchor="w"
)


password_frame = Frame(card, bg="white")
password_frame.pack(fill=X, pady=(7, 25))


password_entry = Entry(
    password_frame,
    font=("Arial", 11),
    width=25,
    show="*",
    bd=1,
    relief=SOLID,
    bg="white",
    fg="#263238",
    insertbackground="#12355b",
)
password_entry.pack(side=LEFT, ipady=7)


# SHOW/HIDE PASSWORD
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_button.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_button.config(text="Show")


show_button = Button(
    password_frame,
    text="Show",
    font=("Arial", 9, "bold"),
    bg="white",
    fg="#12355b",
    relief=FLAT,
    cursor="hand2",
    command=toggle_password,
)
show_button.pack(side=LEFT, padx=5)


# ADMIN LOGIN
def admin_login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "" or password == "":
        msg.showerror("Error", "Please fill in all fields")
        return

    try:
        connect.con
        connect.cur

        connect.cur.execute(
            """
            SELECT id, name, role
            FROM users
            WHERE (username = ? OR email = ?)
            AND password = ?
            AND LOWER(role) = 'admin'
            """,
            (username, username, password),
        )

        admin = connect.cur.fetchone()

        if admin:
            admin_id = admin[0]

            msg.showinfo("Success", "Login successful")

            root.destroy()

            os.system(f'"{sys.executable}" admin.py {admin_id}')

        else:
            msg.showerror("Login Failed", "Invalid admin username, email or password")

    except Exception as error:
        msg.showerror("Database Error", "Could not log in.\n\n" + str(error))


# LOGIN BUTTON
login_button = Button(
    card,
    text="Login",
    font=("Arial", 11, "bold"),
    bg="#12355b",
    fg="white",
    activebackground="#1d70b8",
    activeforeground="white",
    relief=FLAT,
    cursor="hand2",
    command=admin_login,
)
login_button.pack(fill=X, padx=50, ipady=0)


# BUTTON HOVER EFFECT
def button_enter(event):
    login_button.config(bg="#1d70b8")


def button_leave(event):
    login_button.config(bg="#12355b")


login_button.bind("<Enter>", button_enter)
login_button.bind("<Leave>", button_leave)



root.bind("<Return>", lambda event: admin_login())



root.mainloop()
