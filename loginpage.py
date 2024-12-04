from tkinter import *
from tkinter import messagebox
import hashlib
from database import create_connection

class LoginPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Login")
        self.root.geometry("300x200+500+300")

        self.label_username = Label(root, text="Username")
        self.label_username.pack(pady=10)
        self.entry_username = Entry(root)
        self.entry_username.pack(pady=5)

        self.label_password = Label(root, text="Password")
        self.label_password.pack(pady=10)
        self.entry_password = Entry(root, show="*")
        self.entry_password.pack(pady=5)

        self.login_button = Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        try:
            connection = create_connection()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                    user = cursor.fetchone()

                    if user and self.check_password(password, user[1]):
                        messagebox.showinfo("Success", "Login successful.")
                        self.app.show_main_page()  # Show main app after successful login
                        self.root.withdraw()  # Hide login window
                    else:
                        messagebox.showerror("Login Error", "Invalid username or password.")
            else:
                messagebox.showerror("Database Error", "Could not connect to the database.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection:
                connection.close()

    def check_password(self, entered_password, stored_password):
        """Vérifier si le mot de passe saisi correspond à celui stocké (hashé)."""
        return hashlib.sha256(entered_password.encode()).hexdigest() == stored_password
