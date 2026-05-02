import os
from PIL import Image
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
        self.current_page = "manage"

        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo uth.png")
        self.logo_image = ctk.CTkImage(Image.open(logo_path), size=(80, 80))

        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True)

        self.sidebar = ctk.CTkFrame(main_container, width=200, fg_color="#1f1f1f")
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        header = ctk.CTkFrame(self.sidebar, fg_color="#1f1f1f")
        header.pack(fill="x", padx=15, pady=20)
        ctk.CTkLabel(header, image=self.logo_image, text="").pack(pady=(0, 10))
        ctk.CTkLabel(header, text="📊 Student\nManagement", font=ctk.CTkFont(size=14, weight="bold")).pack()

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="#1f1f1f")
        nav_frame.pack(fill="x", padx=10, pady=10)

        self.manage_btn = ctk.CTkButton(nav_frame, text="👥 Manage Student", command=self.show_manage_page, fg_color="#0066ff")
        self.manage_btn.pack(fill="x", pady=5)

        self.search_btn = ctk.CTkButton(nav_frame, text="🔍 Search", command=self.show_search_page, fg_color="#333333")
        self.search_btn.pack(fill="x", pady=5)

        self.stats_btn = ctk.CTkButton(nav_frame, text="📈 Statistics", command=self.show_stats_page, fg_color="#333333")
        self.stats_btn.pack(fill="x", pady=5)

        self.import_btn = ctk.CTkButton(nav_frame, text="📥 Import", command=self.show_import_page, fg_color="#333333")
        self.import_btn.pack(fill="x", pady=5)

        sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color="#1f1f1f")
        sidebar_footer.pack(side="bottom", fill="x", padx=10, pady=10)

        self.theme_btn = ctk.CTkButton(sidebar_footer, text="🌙 Dark Mode", width=120, command=self.toggle_theme)
        self.theme_btn.pack(fill="x", pady=2)

        ctk.CTkButton(sidebar_footer, text="🚪 Logout", width=120, command=self.app.logout).pack(fill="x", pady=2)

        self.content_frame = ctk.CTkFrame(main_container)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        top_bar = ctk.CTkFrame(self.content_frame, fg_color="#2d2d2d", height=60)
        top_bar.pack(fill="x", pady=(0, 15))
        top_bar.pack_propagate(False)

        ctk.CTkLabel(top_bar, text="Student Management System", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=20, pady=20)

        self.pages_frame = ctk.CTkFrame(self.content_frame)
        self.pages_frame.pack(fill="both", expand=True)

        self.setup_manage_page()
        self.setup_search_page()
        self.setup_stats_page()
        self.setup_import_page()

        self.refresh_table()
        self.update_statistics()
        self.show_manage_page()

    def setup_manage_page(self):
        self.manage_page = ctk.CTkFrame(self.pages_frame)
        
        toolbar = ctk.CTkFrame(self.manage_page)
        toolbar.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(toolbar, text="Search:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(toolbar, width=200, placeholder_text="Search by name or ID")
        self.search_entry.pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Search", command=self.search_students, width=80).pack(side="left", padx=2)

        btn_frame = ctk.CTkFrame(toolbar)
        btn_frame.pack(side="right")
        ctk.CTkButton(btn_frame, text="Add", width=70, command=self.add_student).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Edit", width=70, command=self.edit_student).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Delete", width=70, command=self.delete_student).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="Refresh", width=70, command=self.refresh_table).pack(side="left", padx=2)

        columns = ["ID", "Name", "Date of Birth", "Gender", "Class", "Score"]
        self.tree = SortableTreeview(self.manage_page, columns=columns, height=15)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        detail_frame = ctk.CTkFrame(self.manage_page)
        detail_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(detail_frame, text="Student Details:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        self.detail_labels = {}
        for field in columns:
            f = ctk.CTkFrame(detail_frame)
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{field}:", width=100).pack(side="left")
            self.detail_labels[field] = ctk.CTkLabel(f, text="", anchor="w")
            self.detail_labels[field].pack(side="left", padx=10)

    def setup_search_page(self):
        self.search_page = ctk.CTkFrame(self.pages_frame)
        
        adv_frame = ctk.CTkFrame(self.search_page)
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
        self.adv_tree = SortableTreeview(self.search_page, columns=columns, height=15)
        self.adv_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_stats_page(self):
        self.stats_page = ctk.CTkFrame(self.pages_frame)
        self.stat_frame = ctk.CTkFrame(self.stats_page)
        self.stat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_import_page(self):
        self.import_page = ctk.CTkFrame(self.pages_frame)
        
        ctk.CTkLabel(self.import_page, text="Import Student Data from File", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.import_page, text="Supported formats: CSV, Excel, JSON").pack(pady=10)
        ctk.CTkLabel(self.import_page, text="Required columns: id, name, dob, gender, class_name, score").pack(pady=10)
        ctk.CTkButton(self.import_page, text="Select File to Import", command=self.import_file, width=200, height=40).pack(pady=20)

    def show_manage_page(self):
        self._hide_all_pages()
        self.manage_page.pack(fill="both", expand=True)
        self.current_page = "manage"
        self._update_nav_buttons()

    def show_search_page(self):
        self._hide_all_pages()
        self.search_page.pack(fill="both", expand=True)
        self.current_page = "search"
        self._update_nav_buttons()

    def show_stats_page(self):
        self._hide_all_pages()
        self.stats_page.pack(fill="both", expand=True)
        self.current_page = "stats"
        self._update_nav_buttons()
        self.update_statistics()

    def show_import_page(self):
        self._hide_all_pages()
        self.import_page.pack(fill="both", expand=True)
        self.current_page = "import"
        self._update_nav_buttons()

    def _hide_all_pages(self):
        self.manage_page.pack_forget()
        self.search_page.pack_forget()
        self.stats_page.pack_forget()
        self.import_page.pack_forget()

    def _update_nav_buttons(self):
        buttons = {
            "manage": self.manage_btn,
            "search": self.search_btn,
            "stats": self.stats_btn,
            "import": self.import_btn
        }
        for key, btn in buttons.items():
            if key == self.current_page:
                btn.configure(fg_color="#0066ff")
            else:
                btn.configure(fg_color="#333333")

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

        # Summary
        summary = ctk.CTkFrame(self.stat_frame)
        summary.pack(fill="x", pady=10)
        
        stat1 = ctk.CTkFrame(summary)
        stat1.pack(side="left", padx=20)
        ctk.CTkLabel(stat1, text="Total Students", font=ctk.CTkFont(size=12)).pack()
        ctk.CTkLabel(stat1, text=str(total), font=ctk.CTkFont(size=24, weight="bold")).pack()

        stat2 = ctk.CTkFrame(summary)
        stat2.pack(side="left", padx=20)
        ctk.CTkLabel(stat2, text="Average Score", font=ctk.CTkFont(size=12)).pack()
        ctk.CTkLabel(stat2, text=f"{avg_score:.2f}", font=ctk.CTkFont(size=24, weight="bold")).pack()

        # Chart
        class_counts = {}
        for s in students:
            class_counts[s.class_name] = class_counts.get(s.class_name, 0) + 1
        
        if class_counts:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(class_counts.keys(), class_counts.values(), color="#0066ff")
            ax.set_title("Total Students per Class", fontsize=14, weight="bold")
            ax.set_xlabel("Class")
            ax.set_ylabel("Count")
            
            canvas = FigureCanvasTkAgg(fig, master=self.stat_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

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
            self.theme_btn.configure(text="☀️ Light Mode")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="🌙 Dark Mode")

    def show_toast(self, msg):
        toast = ctk.CTkToplevel(self)
        toast.title("")
        toast.geometry("250x50")
        toast.attributes('-topmost', True)
        ctk.CTkLabel(toast, text=msg).pack(expand=True, padx=20, pady=10)
        toast.after(2000, toast.destroy)