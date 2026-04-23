# views/student_dialog.py
import customtkinter as ctk
from tkinter import messagebox
from models.student import Student

class StudentDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Student", student=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x450")
        self.resizable(False, False)
        self.result = None
        self.student = student

        self.transient(parent)
        self.grab_set()

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_entry = ctk.CTkEntry(frame, width=200)
        self.id_entry.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(frame, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ctk.CTkEntry(frame, width=200)
        self.name_entry.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(frame, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=5)
        self.dob_entry = ctk.CTkEntry(frame, width=200)
        self.dob_entry.grid(row=2, column=1, pady=5)

        ctk.CTkLabel(frame, text="Gender:").grid(row=3, column=0, sticky="w", pady=5)
        self.gender_combo = ctk.CTkComboBox(frame, values=["Nam", "Nu"], width=200)
        self.gender_combo.grid(row=3, column=1, pady=5)

        ctk.CTkLabel(frame, text="Class:").grid(row=4, column=0, sticky="w", pady=5)
        self.class_entry = ctk.CTkEntry(frame, width=200)
        self.class_entry.grid(row=4, column=1, pady=5)

        ctk.CTkLabel(frame, text="Score (0-10):").grid(row=5, column=0, sticky="w", pady=5)
        self.score_entry = ctk.CTkEntry(frame, width=200)
        self.score_entry.grid(row=5, column=1, pady=5)

        if student:
            self.id_entry.insert(0, str(student.id))
            self.id_entry.configure(state="disabled")
            self.name_entry.insert(0, student.name)
            self.dob_entry.insert(0, student.dob)
            self.gender_combo.set(student.gender)
            self.class_entry.insert(0, student.class_name)
            self.score_entry.insert(0, str(student.score))

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        save_btn = ctk.CTkButton(btn_frame, text="Save", command=self.save)
        save_btn.pack(side="left", padx=10)
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", command=self.destroy)
        cancel_btn.pack(side="left", padx=10)

    def save(self):
        try:
            student_id = int(self.id_entry.get()) if self.student is None else self.student.id
            name = self.name_entry.get().strip()
            if not name:
                raise ValueError("Name cannot be empty")
            dob = self.dob_entry.get().strip()
            gender = self.gender_combo.get()
            class_name = self.class_entry.get().strip()
            score = float(self.score_entry.get())
            if score < 0 or score > 10:
                raise ValueError("Score must be between 0 and 10")
            self.result = {
                "id": student_id,
                "name": name,
                "dob": dob,
                "gender": gender,
                "class_name": class_name,
                "score": score
            }
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))