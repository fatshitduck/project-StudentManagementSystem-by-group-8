import os
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
from config.themes import get_color
from utils.animations import AnimationUtils, AnimatedButton

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=get_color("bg_primary"))
        self.app = app

        self.center_frame = ctk.CTkFrame(self, fg_color=get_color("bg_primary"))
        self.center_frame.pack(expand=True, padx=20, pady=40)

        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo uth.png")
        self.logo_image = ctk.CTkImage(Image.open(logo_path), size=(180, 180))
        self.logo_label = ctk.CTkLabel(self.center_frame, image=self.logo_image, text="")
        self.logo_label.pack(pady=(0, 20))

        self.title_label = ctk.CTkLabel(self.center_frame, text="Student Management System", 
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=get_color("text_primary"))
        self.title_label.pack(pady=20)
        self.username_label = ctk.CTkLabel(self.center_frame, text="Username:",
                     text_color=get_color("text_primary"))
        self.username_label.pack(pady=(10,0))
        self.username_entry = ctk.CTkEntry(self.center_frame, width=200,
                                          fg_color=get_color("input_bg"),
                                          border_color=get_color("input_border"),
                                          text_color=get_color("text_primary"))
        self.username_entry.pack(pady=5)
        self.password_label = ctk.CTkLabel(self.center_frame, text="Password:",
                     text_color=get_color("text_primary"))
        self.password_label.pack()
        self.password_entry = ctk.CTkEntry(self.center_frame, width=200, show="*",
                                          fg_color=get_color("input_bg"),
                                          border_color=get_color("input_border"),
                                          text_color=get_color("text_primary"))
        self.password_entry.pack(pady=5)
        self.login_btn = AnimatedButton(self.center_frame, text="Login", 
                                      fg_color=get_color("button_primary"),
                                      hover_color=get_color("button_hover"),
                                      border_width=2, border_color=get_color("button_primary"),
                                      corner_radius=8)
        self.login_btn.set_command(self.login)
        self.login_btn.pack(pady=20)

        self.username_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())

        footer_frame = ctk.CTkFrame(self, fg_color=get_color("bg_primary"))
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.footer_label = ctk.CTkLabel(footer_frame, text="version1.3 project by group 8", 
                     font=ctk.CTkFont(size=10),
                     text_color=get_color("text_secondary"))
        self.footer_label.pack(side="right")

        # Start entrance animations
        self.after(100, self._start_entrance_animation)

    def _start_entrance_animation(self):
        """Animate elements entrance"""
        # Logo fade in from below
        AnimationUtils.fade_in_from_bottom(self.logo_label, duration=0.6, distance=40)

        # Title fade in from below
        AnimationUtils.fade_in_from_bottom(self.title_label, duration=0.6, distance=30)

        # Form elements slide in from left
        AnimationUtils.slide_in(self.username_label, "left", 0.4)
        self.after(200, lambda: AnimationUtils.slide_in(self.username_entry, "left", 0.4))
        self.after(400, lambda: AnimationUtils.slide_in(self.password_label, "left", 0.4))
        self.after(600, lambda: AnimationUtils.slide_in(self.password_entry, "left", 0.4))
        self.after(800, lambda: AnimationUtils.fade_in(self.login_btn, 0.5))

    def login(self):
        if self.username_entry.get() == "admin" and self.password_entry.get() == "admin123":
            # Success animation before switching
            AnimationUtils.pulse_button(self.login_btn)
            self.after(300, self.app.show_main)
        else:
            messagebox.showerror("Error", "Invalid username or password")