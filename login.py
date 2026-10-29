import os
import sys
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from PIL import Image, ImageTk
import control as connect

def register():
    root.destroy()
    os.system(f'"{sys.executable}" Register.py')

def login():
    username = ent_user.get().strip()
    password = ent_pass.get()
    role = user_role.get()

    if not username or not password or not role:
        msg.showerror("Error", "Please fill in all fields")
        return

    try:
        connect.cur.execute("""
            SELECT id, name, role
            FROM users
            WHERE (username = ? OR email = ?)
            AND password = ?
            AND LOWER(role) = LOWER(?)
        """, (username, username, password, role))

        user = connect.cur.fetchone()

        if user:
            msg.showinfo(
                "Success",
                f"Welcome back, {user[1]}!"
            )

            if user[2].lower() == "customer":
                root.destroy()
                os.system(
                    f'"{sys.executable}" customer.py {user[0]}'
                )

            elif user[2].lower() == "driver":
                root.destroy()
                os.system(
                    f'"{sys.executable}" driver.py {user[0]}'
                )

        else:
            msg.showerror(
                "Failed",
                "Invalid username or password"
            )

    except Exception as error:
        msg.showerror(
            "Database Error",
            f"An error occurred:\n{error}"
        )
        
# FORGOT PASSWORD FUNCTION
def forgot_password():
    email = ent_user.get().strip()

    if not email or "@" not in email:
        msg.showwarning(
            "Prompt",
            "Enter your Email Address"
        )
        return

    try:
        connect.cur
        connect.con
        
        connect.cur.execute(
            """
            SELECT id FROM users
            WHERE LOWER(email) = LOWER(?)
            AND LOWER(role) IN ('customer', 'user', 'driver')
            """,
            (email,)
        )

        user = connect.cur.fetchone()

        if user is None:
            msg.showerror(
                "Error",
                "Account not found"
            )
            return

        # OPEN A WINDOW TO SET A NEW PASSWORD
        reset_window = Toplevel(root)
        reset_window.title("Reset Password")
        reset_window.geometry("400x300")
        reset_window.resizable(False, False)
        reset_window.configure(bg="#f4f7fb")
        reset_window.transient(root)
        reset_window.grab_set()

        Label(
            reset_window,
            text="Reset Your Password",
            font=("Arial", 17, "bold"),
            bg="#f4f7fb",
            fg=NAVY
        ).pack(pady=(25, 8))

        Label(
            reset_window,
            text="Enter your new password",
            font=("Arial", 10),
            bg="#f4f7fb",
            fg=MUTED
        ).pack(pady=(0, 15))

        Label(
            reset_window,
            text="New Password",
            font=("Arial", 10, "bold"),
            
            bg="#f4f7fb",
            fg=TEXT
        ).pack(anchor="w", padx=35)

        new_password = Entry(
            reset_window,
            font=("Arial", 11),
            show="*",
            width=15,
            relief=SOLID,
            bd=1
        )
        new_password.pack(fill=X, padx=35, pady=(5, 12), ipady=5)

        Label(
            reset_window,
            text="Confirm New Password",
            font=("Arial", 10, "bold"),
            bg="#f4f7fb",
            fg=TEXT
        ).pack(anchor="w", padx=35)

        confirm_password = Entry(
            reset_window,
            font=("Arial", 11),
            show="*",
            width=15,
            relief=SOLID,
            bd=1
        )
        confirm_password.pack(fill=X, padx=35, pady=(5, 15), ipady=5)

        def save_new_password():
            password = new_password.get()
            confirm = confirm_password.get()

            if not password or not confirm:
                msg.showwarning(
                    "Error",
                    "Please fill in both fields",
                    parent=reset_window
                )
                return

            if password != confirm:
                msg.showerror(
                    "Error",
                    "Password Mismatch",
                    parent=reset_window
                )
                return

            if len(password) < 6:
                msg.showwarning(
                    "Prompt",
                    "Your password must contain at least 6 characters",
                    parent=reset_window
                )
                return

            try:
                connect.cur.execute(
                    """
                    UPDATE users
                    SET password = ?
                    WHERE id = ?
                    """,
                    (password, user[0])
                )
                connect.con.commit()

                msg.showinfo(
                    "Success",
                    "Password update successful",
                    parent=reset_window
                )

                reset_window.destroy()
                ent_pass.delete(0, END)

            except Exception as error:
                connect.con.rollback()
                msg.showerror(
                    "Reset Failed",
                    f"Could not change your password:\n{error}",
                    parent=reset_window
                )

        Button(
            reset_window,
            text="Save",
            command=save_new_password,
            font=("Arial", 10, "bold"),
            bg=NAVY,
            fg="white",
            activebackground=BLUE,
            relief=FLAT,
            cursor="hand2"
        ).pack(fill=X, padx=150, ipady=0)

    except Exception as error:
        msg.showerror(
            "Database Error",
            f"Could not process your request:\n{error}"
        )



# SHOW OR HIDE PASSWORD
def toggle_password():
    if ent_pass.cget("show") == "*":
        ent_pass.config(show="")
        show_password_btn.config(text="Hide")
    else:
        ent_pass.config(show="*")
        show_password_btn.config(text="Show")


# MAIN WINDOW
root = Tk()
root.title("Login")
root.geometry("1000x650")
root.resizable(False, False)
root.configure(bg="#f4f7fb")


# COLOURS
NAVY = "#12355b"
BLUE = "#1d568d"
LIGHT_BLUE = "#e8f1fb"
WHITE = "#ffffff"
TEXT = "#263445"
MUTED = "#64748b"


# LEFT BRANDING PANEL
left_panel = Frame(root, bg=NAVY, width=390)
left_panel.pack(side=LEFT, fill=Y)
left_panel.pack_propagate(False)


# LOGO
try:
    logo_image = Image.open("image/logo.jpg")
    logo_image = logo_image.resize((200, 150))
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = Label(
        left_panel,
        image=logo_photo,
        bg=NAVY
    )
    logo_label.image = logo_photo
    logo_label.pack(pady=(65, 25))

except Exception:
    Label(
        left_panel,
        text="🚗\nTRAVEL",
        font=("Arial", 20, "bold"),
        bg=NAVY,
        fg=WHITE
    ).pack(pady=(90, 30))


# BRAND NAME
Label(
    left_panel,
    text="TRAVEL",
    font=("Arial", 22, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(5, 10))


Label(
    left_panel,
    text="Your journey, our priority",
    font=("Arial", 12),
    bg=NAVY,
    fg="#dbeafe"
).pack(pady=(0, 35))


# BRANDING INFORMATION
features_frame = Frame(left_panel, bg=NAVY)
features_frame.pack(fill=X, padx=35)


features = [
    ("✓", "Easy ride booking"),
    ("✓", "Reliable drivers"),
    ("✓", "Safe Drive"),
]

Label(
    left_panel,
    text="SAFE  •  SIMPLE  •  RELIABLE",
    font=("Arial", 10, "bold"),
    bg="#12355b",
    fg="white"
).pack(side="bottom", pady=35)

for symbol, feature in features:
    row = Frame(features_frame, bg=NAVY)
    row.pack(anchor="w", pady=9)

    Label(
        row,
        text=symbol,
        font=("Arial", 13, "bold"),
        bg=NAVY,
        fg="#75d69c"
    ).pack(side=LEFT, padx=(0, 12))

    Label(
        row,
        text=feature,
        font=("Arial", 11),
        bg=NAVY,
        fg=WHITE
    ).pack(side=LEFT)


# RIGHT CONTENT PANEL
right_panel = Frame(root, bg="#f4f7fb")
right_panel.pack(side=LEFT, fill=BOTH, expand=True)


# LOGIN FORM CARD
login_card = Frame(
    right_panel,
    bg=WHITE,
    padx=45,
    pady=35,
    highlightbackground="#e1e8f0",
    highlightthickness=1
)
login_card.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=490
)


# FORM HEADING
Label(
    login_card,
    text="Welcome Back",
    font=("Arial", 25, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")


Label(
    login_card,
    text="Sign in to continue",
    font=("Arial", 11),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(7, 28))


# USERNAME OR EMAIL
Label(
    login_card,
    text="Username or Email",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(0, 7))


ent_user = Entry(
    login_card,
    font=("Arial", 12),
    relief=SOLID,
    bd=1,
    bg="#fbfdff",
    fg=TEXT
)
ent_user.pack(fill=X, ipady=5, pady=(0, 18))


# PASSWORD LABEL
Label(
    login_card,
    text="Password",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(0, 7))


# PASSWORD ENTRY AND SHOW BUTTON
password_frame = Frame(login_card, bg=WHITE)
password_frame.pack(fill=X, pady=(0, 18))

ent_pass = Entry(
    password_frame,
    font=("Arial", 12),
    show="*",
    relief=SOLID,
    bd=1,
    bg="#fbfdff",
    fg=TEXT
)
ent_pass.pack(side=LEFT, fill=X, expand=True, ipady=5)

show_password_btn = Button(
    password_frame,
    text="Show",
    font=("Arial", 9, "bold"),
    bg=WHITE,
    fg=NAVY,
    relief=FLAT,
    cursor="hand2",
    command=toggle_password
)
show_password_btn.pack(side=LEFT, padx=(7, 0), ipady=5, ipadx=5)


# ACCOUNT TYPE
Label(
    login_card,
    text="Login As",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(0, 7))


style = ttk.Style()
style.configure(
    "Login.TCombobox",
    padding=5,
    font=("Arial", 11)
)

user_role = ttk.Combobox(
    login_card,
    values=["Customer", "Driver"],
    state="readonly",
    font=("Arial", 11),
    style="Login.TCombobox"
)
user_role.pack(fill=X, pady=(0, 22))
user_role.set("Customer")


# LOGIN BUTTON
login_btn = Button(
    login_card,
    text="Sign In",
    command=login,
    font=("Arial", 12, "bold"),
    bg=NAVY,
    fg=WHITE,
    activebackground=BLUE,
    activeforeground=WHITE,
    relief=FLAT,
    bd=0,
    cursor="hand2"
)
login_btn.pack(fill=X, ipady=0, padx=150)

# FORGOT PASSWORD LINK
forgot_btn = Button(
    login_card,
    text="Forgot Password?",
    command=forgot_password,
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=BLUE,
    activebackground=WHITE,
    activeforeground=NAVY,
    relief=FLAT,
    bd=0,
    cursor="hand2"
)
forgot_btn.pack(anchor="e", pady=(0, 12))



# BUTTON HOVER EFFECT
def login_hover(event):
    login_btn.config(bg=BLUE)


def login_leave(event):
    login_btn.config(bg=NAVY)


login_btn.bind("<Enter>", login_hover)
login_btn.bind("<Leave>", login_leave)


# REGISTRATION LINK
Label(
    login_card,
    text="Don't have an account?",
    font=("Arial", 10),
    bg=WHITE,
    fg=MUTED
).pack(pady=(3, 2))


register_btn = Button(
    login_card,
    text="Create an Account",
    command=register,
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=BLUE,
    activebackground=WHITE,
    activeforeground=NAVY,
    relief=FLAT,
    bd=0,
    cursor="hand2"
)
register_btn.pack()


# ENTER KEY TO LOGIN
root.bind("<Return>", lambda event: login())

# START APPLICATION
root.mainloop()
