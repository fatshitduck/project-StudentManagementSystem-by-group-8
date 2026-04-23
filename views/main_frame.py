# views/main_frame.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from views.sortable_treeview import SortableTreeview
from views.student_dialog import StudentDialog
from models.student import Student

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.manager = app.manager

        # Top bar
        top = ctk.CTkFrame(self, height=50)
        top.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(top, text="Student Management System", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=10)
        
        self.theme_btn = ctk.CTkButton(top, text="Dark Mode", width=100, command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=10)
        ctk.CTkButton(top, text="Logout", width=100, command=self.app.logout).pack(side="right", padx=10)

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabview.add("Manage Students")
        self.tabview.add("Advanced Search")
        self.tabview.add("Statistics")
        self.tabview.add("Import File")

        self.setup_manage_tab()
        self.setup_advanced_search_tab()
        self.setup_statistics_tab()
        self.setup_import_tab()

        self.refresh_table()
        self.update_statistics()

    def setup_manage_tab(self):
        manage = self.tabview.tab("Manage Students")
        top_m = ctk.CTkFrame(manage)
        top_m.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(top_m, text="Search:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(top_m, width=200)
        self.search_entry.pack(side="left", padx=5)
        ctk.CTkButton(top_m, text="Search", command=self.search_students).pack(side="left", padx=5)
        
        btn_frame = ctk.CTkFrame(top_m)
        btn_frame.pack(side="right")
        ctk.CTkButton(btn_frame, text="Add", width=80, command=self.add_student).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Edit", width=80, command=self.edit_student).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Delete", width=80, command=self.delete_student).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Refresh", width=80, command=self.refresh_table).pack(side="left", padx=2)

        columns = ["ID", "Name", "Date of Birth", "Gender", "Class", "Score"]
        self.tree = SortableTreeview(manage, columns=columns, height=20)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        detail_frame = ctk.CTkFrame(manage)
        detail_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(detail_frame, text="Student Details:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.detail_labels = {}
        for field in columns:
            f = ctk.CTkFrame(detail_frame)
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{field}:", width=100).pack(side="left")
            self.detail_labels[field] = ctk.CTkLabel(f, text="", anchor="w")
            self.detail_labels[field].pack(side="left", padx=10)

    def setup_advanced_search_tab(self):
        adv = self.tabview.tab("Advanced Search")
        adv_frame = ctk.CTkFrame(adv)
        adv_frame.pack(fill="x", padx=10, pady=10)
        
        self.adv_name = ctk.CTkEntry(adv_frame, width=150, placeholder_text="Name")
        self.adv_name.grid(row=0, column=0, padx=5, pady=5)
        self.adv_id = ctk.CTkEntry(adv_frame, width=100, placeholder_text="ID")
        self.adv_id.grid(row=0, column=1, padx=5, pady=5)
        self.adv_class = ctk.CTkEntry(adv_frame, width=150, placeholder_text="Class")
        self.adv_class.grid(row=0, column=2, padx=5, pady=5)
        self.adv_gender = ctk.CTkComboBox(adv_frame, values=["All", "Nam", "Nu"], width=100)
        self.adv_gender.grid(row=1, column=0, padx=5, pady=5)
        self.adv_min = ctk.CTkEntry(adv_frame, width=80, placeholder_text="Min Score")
        self.adv_min.grid(row=1, column=1, padx=5, pady=5)
        self.adv_max = ctk.CTkEntry(adv_frame, width=80, placeholder_text="Max Score")
        self.adv_max.grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkButton(adv_frame, text="Advanced Search", command=self.advanced_search).grid(row=1, column=3, padx=20, pady=5)

        columns = ["ID", "Name", "Date of Birth", "Gender", "Class", "Score"]
        self.adv_tree = SortableTreeview(adv, columns=columns, height=20)
        self.adv_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_statistics_tab(self):
        stat_tab = self.tabview.tab("Statistics")
        self.stat_frame = ctk.CTkFrame(stat_tab)
        self.stat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_import_tab(self):
        import_tab = self.tabview.tab("Import File")
        ctk.CTkLabel(import_tab, text="Import Student Data from File", font=ctk.CTkFont(size=16)).pack(pady=20)
        ctk.CTkLabel(import_tab, text="Supported formats: CSV, Excel, JSON").pack()
        ctk.CTkLabel(import_tab, text="Required columns: id, name, dob, gender, class_name, score").pack()
        ctk.CTkButton(import_tab, text="Select File to Import", command=self.import_file).pack(pady=20)

    # ---------- Methods ----------
    def refresh_table(self):
        students = self.manager.get_all()
        data = [{"ID": s.id, "Name": s.name, "Date of Birth": s.dob, "Gender": s.gender, "Class": s.class_name, "Score": s.score} for s in students]
        self.tree.set_data(data)

    def search_students(self):
        kw = self.search_entry.get()
        results = self.manager.search(kw)
        data = [{"ID": s.id, "Name": s.name, "Date of Birth": s.dob, "Gender": s.gender, "Class": s.class_name, "Score": s.score} for s in results]
        self.tree.set_data(data)

    def advanced_search(self):
        name = self.adv_name.get()
        sid = self.adv_id.get()
        class_name = self.adv_class.get()
        gender = self.adv_gender.get()
        min_s = float(self.adv_min.get()) if self.adv_min.get() else None
        max_s = float(self.adv_max.get()) if self.adv_max.get() else None
        results = self.manager.advanced_search(name, sid, class_name, gender, min_s, max_s)
        data = [{"ID": s.id, "Name": s.name, "Date of Birth": s.dob, "Gender": s.gender, "Class": s.class_name, "Score": s.score} for s in results]
        self.adv_tree.set_data(data)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            if values:
                fields = ["ID", "Name", "Date of Birth", "Gender", "Class", "Score"]
                for i, f in enumerate(fields):
                    self.detail_labels[f].configure(text=values[i])

    def add_student(self):
        dialog = StudentDialog(self, title="Add Student")
        self.wait_window(dialog)
        if dialog.result:
            self.manager.add_student(Student(**dialog.result))
            self.refresh_table()
            self.update_statistics()
            self.show_toast("Student added!")

    def edit_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student")
            return
        values = self.tree.item(selected[0])['values']
        sid = values[0]
        for s in self.manager.get_all():
            if s.id == sid:
                dialog = StudentDialog(self, title="Edit Student", student=s)
                self.wait_window(dialog)
                if dialog.result:
                    self.manager.update_student(sid, Student(**dialog.result))
                    self.refresh_table()
                    self.update_statistics()
                    self.show_toast("Student updated!")
                break

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student")
            return
        values = self.tree.item(selected[0])['values']
        if messagebox.askyesno("Confirm", f"Delete {values[1]}?"):
            self.manager.delete_student(values[0])
            self.refresh_table()
            self.update_statistics()
            self.show_toast("Student deleted!")

    def update_statistics(self):
        for w in self.stat_frame.winfo_children():
            w.destroy()
        students = self.manager.get_all()
        total = len(students)
        avg_score = sum(s.score for s in students) / total if total > 0 else 0
        summary = ctk.CTkFrame(self.stat_frame)
        summary.pack(fill="x", pady=10)
        ctk.CTkLabel(summary, text=f"Total Students: {total}", font=ctk.CTkFont(size=14)).pack(side="left", padx=20)
        ctk.CTkLabel(summary, text=f"Average Score: {avg_score:.2f}", font=ctk.CTkFont(size=14)).pack(side="left", padx=20)

        class_counts = {}
        for s in students:
            class_counts[s.class_name] = class_counts.get(s.class_name, 0) + 1
        if class_counts:
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.pie(class_counts.values(), labels=class_counts.keys(), autopct='%1.1f%%')
            ax.set_title("Distribution by Class")
            canvas = FigureCanvasTkAgg(fig, master=self.stat_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

    def import_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV/Excel/JSON", "*.csv *.xlsx *.xls *.json")])
        if filename:
            added, errors = self.manager.import_from_file(filename)
            if errors:
                messagebox.showwarning("Import completed with errors", f"Added {added}\nErrors:\n{errors}")
            else:
                messagebox.showinfo("Import successful", f"Added {added} students!")
            self.refresh_table()
            self.update_statistics()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="Light Mode")

    def show_toast(self, msg):
        toast = ctk.CTkToplevel(self)
        toast.title("")
        toast.geometry("250x50")
        toast.attributes('-topmost', True)
        ctk.CTkLabel(toast, text=msg).pack(expand=True, padx=20, pady=10)
        toast.after(2000, toast.destroy)