# main.py
import customtkinter as ctk
from database.student_manager import StudentManager
from views.login_frame import LoginFrame
from views.main_frame import MainFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x700")
        
        # Khởi tạo student manager
        self.manager = StudentManager()

        # Stacked widget để chuyển giữa login và main
        self.stack = ctk.CTkFrame(self)
        self.stack.pack(fill="both", expand=True)

        self.login_frame = LoginFrame(self.stack, self)
        self.main_frame = None
        self.login_frame.pack(fill="both", expand=True)

    def show_main(self):
        self.login_frame.pack_forget()
        self.main_frame = MainFrame(self.stack, self)
        self.main_frame.pack(fill="both", expand=True)

    def logout(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.login_frame = LoginFrame(self.stack, self)
        self.login_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()