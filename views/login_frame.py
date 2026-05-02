import os
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=("#ffffff", "#1a1a1a"))
        self.app = app

        self.center_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1a1a1a"))
        self.center_frame.pack(expand=True, padx=20, pady=40)

        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo uth.png")
        self.logo_image = ctk.CTkImage(Image.open(logo_path), size=(180, 180))
        ctk.CTkLabel(self.center_frame, image=self.logo_image, text="").pack(pady=(0, 20))

        ctk.CTkLabel(self.center_frame, text="Student Management System", 
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=("#000000", "#ffffff")).pack(pady=20)
        ctk.CTkLabel(self.center_frame, text="Username:",
                     text_color=("#000000", "#ffffff")).pack(pady=(10,0))
        self.username_entry = ctk.CTkEntry(self.center_frame, width=200)
        self.username_entry.pack(pady=5)
        ctk.CTkLabel(self.center_frame, text="Password:",
                     text_color=("#000000", "#ffffff")).pack()
        self.password_entry = ctk.CTkEntry(self.center_frame, width=200, show="*")
        self.password_entry.pack(pady=5)
        self.login_btn = ctk.CTkButton(self.center_frame, text="Login", command=self.login)
        self.login_btn.pack(pady=20)

        self.username_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())

        footer_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#1a1a1a"))
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        ctk.CTkLabel(footer_frame, text="version1.3 project by group 8", 
                     font=ctk.CTkFont(size=10),
                     text_color=("#666666", "#999999")).pack(side="right")

    def login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "admin123":
            self.app.show_main()
        else:
            messagebox.showerror("Error", "Invalid username or password")