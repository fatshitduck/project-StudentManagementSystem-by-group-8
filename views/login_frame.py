# views/login_frame.py
import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Center frame
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.pack(expand=True)

        ctk.CTkLabel(self.center_frame, text="Student Management System", 
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.center_frame, text="Username:").pack(pady=(10,0))
        self.username_entry = ctk.CTkEntry(self.center_frame, width=200)
        self.username_entry.pack(pady=5)
        ctk.CTkLabel(self.center_frame, text="Password:").pack()
        self.password_entry = ctk.CTkEntry(self.center_frame, width=200, show="*")
        self.password_entry.pack(pady=5)
        self.login_btn = ctk.CTkButton(self.center_frame, text="Login", command=self.login)
        self.login_btn.pack(pady=20)

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())

    def login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "admin123":
            self.app.show_main()
        else:
            messagebox.showerror("Error", "Invalid username or password")