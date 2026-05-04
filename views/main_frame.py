import os
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from views.sortable_treeview import SortableTreeview
from views.student_dialog import StudentDialog
from models.student import Student
from config.themes import get_color
from utils.animations import AnimationUtils, AnimatedButton

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=get_color("bg_secondary"))
        self.app = app
        self.manager = app.manager
        self.current_page = "manage"

        from utils.resources import resource_path
        logo_path = resource_path(os.path.join("assets", "logo uth.png"))
        self.logo_image = ctk.CTkImage(Image.open(logo_path), size=(80, 80))

        main_container = ctk.CTkFrame(self, fg_color=get_color("bg_secondary"))
        main_container.pack(fill="both", expand=True)

        self.sidebar = ctk.CTkFrame(main_container, width=200, fg_color=get_color("bg_sidebar"))
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        header = ctk.CTkFrame(self.sidebar, fg_color=get_color("bg_sidebar"))
        header.pack(fill="x", padx=15, pady=20)
        ctk.CTkLabel(header, image=self.logo_image, text="").pack(pady=(0, 10))
        ctk.CTkLabel(header, text="📊 Student\nManagement", 
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=get_color("text_primary")).pack()

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color=get_color("bg_sidebar"))
        nav_frame.pack(fill="x", padx=10, pady=10)

        self.manage_btn = AnimatedButton(nav_frame, text="👥 Manage Student", 
                                       command=self.show_manage_page, 
                                       fg_color=get_color("button_primary"),
                                       hover_color=get_color("button_hover"),
                                       border_width=2,
                                       border_color=get_color("button_primary"))
        self.manage_btn.pack(fill="x", pady=5)

        self.search_btn = AnimatedButton(nav_frame, text="🔍 Search", 
                                       command=self.show_search_page, 
                                       fg_color=get_color("button_secondary"),
                                       hover_color=get_color("button_hover"),
                                       border_width=2,
                                       border_color=get_color("button_secondary"))
        self.search_btn.pack(fill="x", pady=5)

        self.stats_btn = AnimatedButton(nav_frame, text="📈 Statistics", 
                                      command=self.show_stats_page, 
                                      fg_color=get_color("button_secondary"),
                                      hover_color=get_color("button_hover"),
                                      border_width=2,
                                      border_color=get_color("button_secondary"))
        self.stats_btn.pack(fill="x", pady=5)

        self.import_btn = AnimatedButton(nav_frame, text="📥 Import", 
                                       command=self.show_import_page, 
                                       fg_color=get_color("button_secondary"),
                                       hover_color=get_color("button_hover"),
                                       border_width=2,
                                       border_color=get_color("button_secondary"))
        self.import_btn.pack(fill="x", pady=5)

        sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color=get_color("bg_sidebar"))
        sidebar_footer.pack(side="bottom", fill="x", padx=10, pady=10)

        self.theme_btn = AnimatedButton(sidebar_footer, text="🌙 Dark Mode", width=120, 
                                      command=self.toggle_theme,
                                      fg_color=get_color("button_secondary"),
                                      hover_color=get_color("button_hover"),
                                      border_width=2, border_color=get_color("button_secondary"),
                                      corner_radius=8)
        self.theme_btn.set_command(self.toggle_theme)
        self.theme_btn.pack(fill="x", pady=2)

        logout_btn = AnimatedButton(sidebar_footer, text="🚪 Logout", width=120, 
                     command=self.app.logout,
                     fg_color=get_color("accent_danger"),
                     hover_color=("#c0392b", "#e74c3c"),
                     border_width=2, border_color=get_color("accent_danger"),
                     corner_radius=8)
        logout_btn.set_command(self.app.logout)
        logout_btn.pack(fill="x", pady=2)

        self.content_frame = ctk.CTkFrame(main_container, fg_color=get_color("bg_secondary"))
        self.content_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        top_bar = ctk.CTkFrame(self.content_frame, fg_color=get_color("bg_topbar"), height=60)
        top_bar.pack(fill="x", pady=(0, 15))
        top_bar.pack_propagate(False)

        ctk.CTkLabel(top_bar, text="Student Management System", 
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=get_color("text_primary")).pack(side="left", padx=20, pady=20)

        self.pages_frame = ctk.CTkFrame(self.content_frame, fg_color=get_color("bg_secondary"))
        self.pages_frame.pack(fill="both", expand=True)

        self.setup_manage_page()
        self.setup_search_page()
        self.setup_stats_page()
        self.setup_import_page()

        self.refresh_table()
        self.update_statistics()
        self.show_manage_page()

    def setup_manage_page(self):
        self.manage_page = ctk.CTkFrame(self.pages_frame, fg_color=get_color("bg_secondary"))
        
        toolbar = ctk.CTkFrame(self.manage_page, fg_color=get_color("bg_secondary"))
        toolbar.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(toolbar, text="Search:", text_color=get_color("text_primary")).pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(toolbar, width=200, placeholder_text="Search by name or ID",
                                         fg_color=get_color("input_bg"),
                                         border_color=get_color("input_border"),
                                         text_color=get_color("text_primary"))
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_students)
        search_btn = AnimatedButton(toolbar, text="Search", command=self.search_students, width=80,
                     fg_color=get_color("button_primary"),
                     hover_color=get_color("button_hover"),
                     border_width=2, border_color=get_color("button_primary"),
                     corner_radius=8)
        search_btn.set_command(self.search_students)
        search_btn.pack(side="left", padx=2)

        btn_frame = ctk.CTkFrame(toolbar, fg_color=get_color("bg_secondary"))
        btn_frame.pack(side="right")
        for btn_text, btn_cmd in [("Add", self.add_student), ("Edit", self.edit_student), 
                                   ("Delete", self.delete_student), ("Refresh", self.refresh_table)]:
            fg_color = get_color("accent_danger") if btn_text == "Delete" else get_color("button_primary")
            border_color = fg_color
            ctk.CTkButton(btn_frame, text=btn_text, width=70, command=btn_cmd,
                         fg_color=fg_color, hover_color=get_color("button_hover"),
                         border_width=2, border_color=border_color,
                         corner_radius=8).pack(side="left", padx=2)

        columns = ["ID", "Name", "Date of Birth", "Gender", "Class", "Score"]
        self.tree = SortableTreeview(self.manage_page, columns=columns, height=15)
        self.tree.configure(yscrollcommand=lambda f, l: self.tree_y_scroll.set(f, l),
                            xscrollcommand=lambda f, l: self.tree_x_scroll.set(f, l))
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.tree_y_scroll = ttk.Scrollbar(self.manage_page, orient="vertical", command=self.tree.yview)
        self.tree_y_scroll.pack(side="right", fill="y")
        self.tree_x_scroll = ttk.Scrollbar(self.manage_page, orient="horizontal", command=self.tree.xview)
        self.tree_x_scroll.pack(side="bottom", fill="x")

        column_widths = {
            "ID": 80,
            "Name": 220,
            "Date of Birth": 120,
            "Gender": 80,
            "Class": 100,
            "Score": 80,
        }
        for col in columns:
            self.tree.column(col, width=column_widths[col], minwidth=column_widths[col], anchor="w", stretch=True)

        detail_frame = ctk.CTkFrame(self.manage_page, fg_color=get_color("bg_secondary"))
        detail_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(detail_frame, text="Student Details:", font=ctk.CTkFont(weight="bold"),
                     text_color=get_color("text_primary")).pack(anchor="w")

        self.detail_labels = {}
        for field in columns:
            f = ctk.CTkFrame(detail_frame, fg_color=get_color("bg_secondary"))
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{field}:", width=100, text_color=get_color("text_primary")).pack(side="left")
            self.detail_labels[field] = ctk.CTkLabel(f, text="", anchor="w", text_color=get_color("text_primary"))
            self.detail_labels[field].pack(side="left", padx=10)

    def setup_search_page(self):
        self.search_page = ctk.CTkFrame(self.pages_frame, fg_color=get_color("bg_secondary"))
        
        adv_frame = ctk.CTkFrame(self.search_page, fg_color=get_color("bg_secondary"))
        adv_frame.pack(fill="x", padx=10, pady=10)

        self.adv_name = ctk.CTkEntry(adv_frame, width=150, placeholder_text="Name",
                                     fg_color=get_color("input_bg"),
                                     border_color=get_color("input_border"),
                                     text_color=get_color("text_primary"))
        self.adv_name.grid(row=0, column=0, padx=5, pady=5)
        self.adv_id = ctk.CTkEntry(adv_frame, width=100, placeholder_text="ID",
                                   fg_color=get_color("input_bg"),
                                   border_color=get_color("input_border"),
                                   text_color=get_color("text_primary"))
        self.adv_id.grid(row=0, column=1, padx=5, pady=5)
        self.adv_class = ctk.CTkEntry(adv_frame, width=150, placeholder_text="Class",
                                      fg_color=get_color("input_bg"),
                                      border_color=get_color("input_border"),
                                      text_color=get_color("text_primary"))
        self.adv_class.grid(row=0, column=2, padx=5, pady=5)

        self.adv_gender = ctk.CTkComboBox(adv_frame, values=["All", "Nam", "Nu"], width=100,
                                         fg_color=get_color("input_bg"),
                                         border_color=get_color("input_border"),
                                         text_color=get_color("text_primary"))
        self.adv_gender.grid(row=1, column=0, padx=5, pady=5)
        self.adv_min = ctk.CTkEntry(adv_frame, width=80, placeholder_text="Min Score",
                                    fg_color=get_color("input_bg"),
                                    border_color=get_color("input_border"),
                                    text_color=get_color("text_primary"))
        self.adv_min.grid(row=1, column=1, padx=5, pady=5)
        self.adv_max = ctk.CTkEntry(adv_frame, width=80, placeholder_text="Max Score",
                                    fg_color=get_color("input_bg"),
                                    border_color=get_color("input_border"),
                                    text_color=get_color("text_primary"))
        self.adv_max.grid(row=1, column=2, padx=5, pady=5)
        self.adv_name.bind("<KeyRelease>", self.advanced_search)
        self.adv_id.bind("<KeyRelease>", self.advanced_search)
        self.adv_class.bind("<KeyRelease>", self.advanced_search)
        self.adv_min.bind("<KeyRelease>", self.advanced_search)
        self.adv_max.bind("<KeyRelease>", self.advanced_search)
        adv_search_btn = AnimatedButton(adv_frame, text="Advanced Search", command=self.advanced_search,
                     fg_color=get_color("button_primary"),
                     hover_color=get_color("button_hover"),
                     border_width=2, border_color=get_color("button_primary"),
                     corner_radius=8)
        adv_search_btn.set_command(self.advanced_search)
        adv_search_btn.grid(row=1, column=3, padx=20, pady=5)

        columns = ["ID", "Name", "Date of Birth", "Gender", "Class", "Score"]
        self.adv_tree = SortableTreeview(self.search_page, columns=columns, height=15)
        self.adv_tree.configure(yscrollcommand=lambda f, l: self.adv_tree_y_scroll.set(f, l),
                                xscrollcommand=lambda f, l: self.adv_tree_x_scroll.set(f, l))
        self.adv_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.adv_tree_y_scroll = ttk.Scrollbar(self.search_page, orient="vertical", command=self.adv_tree.yview)
        self.adv_tree_y_scroll.pack(side="right", fill="y")
        self.adv_tree_x_scroll = ttk.Scrollbar(self.search_page, orient="horizontal", command=self.adv_tree.xview)
        self.adv_tree_x_scroll.pack(side="bottom", fill="x")

        column_widths = {
            "ID": 80,
            "Name": 220,
            "Date of Birth": 120,
            "Gender": 80,
            "Class": 100,
            "Score": 80,
        }
        for col in columns:
            self.adv_tree.column(col, width=column_widths[col], minwidth=column_widths[col], anchor="w", stretch=True)

    def setup_stats_page(self):
        self.stats_page = ctk.CTkFrame(self.pages_frame, fg_color=get_color("bg_secondary"))
        self.stat_frame = ctk.CTkFrame(self.stats_page, fg_color=get_color("bg_secondary"))
        self.stat_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_import_page(self):
        self.import_page = ctk.CTkFrame(self.pages_frame, fg_color=get_color("bg_secondary"))
        
        ctk.CTkLabel(self.import_page, text="Import Student Data from File", 
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=get_color("text_primary")).pack(pady=20)
        ctk.CTkLabel(self.import_page, text="Supported formats: CSV, Excel, JSON",
                     text_color=get_color("text_secondary")).pack(pady=10)
        ctk.CTkLabel(self.import_page, text="Required columns: id, name, dob, gender, class_name, score",
                     text_color=get_color("text_secondary")).pack(pady=10)
        import_btn = AnimatedButton(self.import_page, text="Select File to Import", command=self.import_file, 
                     width=200, height=40, fg_color=get_color("button_primary"),
                     hover_color=get_color("button_hover"),
                     border_width=2, border_color=get_color("button_primary"),
                     corner_radius=8)
        import_btn.set_command(self.import_file)
        import_btn.pack(pady=20)

    def show_manage_page(self):
        self._show_page_with_animation(self.manage_page, "manage")

    def show_search_page(self):
        self._show_page_with_animation(self.search_page, "search")

    def show_stats_page(self):
        self._show_page_with_animation(self.stats_page, "stats")
        self.update_statistics()

    def show_import_page(self):
        self._show_page_with_animation(self.import_page, "import")

    def _show_page_with_animation(self, page, page_name):
        """Show a page with fade-in animation"""
        self._hide_all_pages()
        page.pack(fill="both", expand=True)
        page.configure(fg_color=get_color("bg_secondary"))
        self.current_page = page_name
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
                btn.configure(fg_color=get_color("button_primary"), 
                            border_color=get_color("accent_primary"),
                            border_width=3)
            else:
                btn.configure(fg_color=get_color("button_secondary"),
                            border_color=get_color("button_secondary"),
                            border_width=2)

    # ---------- Methods ----------
    def refresh_table(self):
        students = self.manager.get_all()
        data = [{"ID": s.id, "Name": s.name, "Date of Birth": s.dob, "Gender": s.gender, "Class": s.class_name, "Score": s.score} for s in students]
        self.tree.set_data(data)

    def search_students(self, event=None):
        kw = self.search_entry.get()
        results = self.manager.search(kw, partial=True)
        data = [{"ID": s.id, "Name": s.name, "Date of Birth": s.dob, "Gender": s.gender, "Class": s.class_name, "Score": s.score} for s in results]
        self.tree.set_data(data)

    def advanced_search(self, event=None):
        name = self.adv_name.get()
        sid = self.adv_id.get()
        class_name = self.adv_class.get()
        gender = self.adv_gender.get()
        min_s = None
        max_s = None
        try:
            if self.adv_min.get():
                min_s = float(self.adv_min.get())
        except ValueError:
            min_s = None
        try:
            if self.adv_max.get():
                max_s = float(self.adv_max.get())
        except ValueError:
            max_s = None
        results = self.manager.advanced_search(name, sid, class_name, gender, min_s, max_s, partial=True)
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
        summary = ctk.CTkFrame(self.stat_frame, fg_color=get_color("bg_secondary"))
        summary.pack(fill="x", pady=10)
        
        stat1 = ctk.CTkFrame(summary, fg_color=get_color("bg_topbar"))
        stat1.pack(side="left", padx=20)
        ctk.CTkLabel(stat1, text="Total Students", font=ctk.CTkFont(size=12), 
                     text_color=get_color("text_secondary")).pack()
        ctk.CTkLabel(stat1, text=str(total), font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=get_color("accent_primary")).pack()

        stat2 = ctk.CTkFrame(summary, fg_color=get_color("bg_topbar"))
        stat2.pack(side="left", padx=20)
        ctk.CTkLabel(stat2, text="Average Score", font=ctk.CTkFont(size=12),
                     text_color=get_color("text_secondary")).pack()
        ctk.CTkLabel(stat2, text=f"{avg_score:.2f}", font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=get_color("accent_secondary")).pack()

        # Chart
        class_counts = {}
        for s in students:
            class_counts[s.class_name] = class_counts.get(s.class_name, 0) + 1
        
        if class_counts:
            fig, ax = plt.subplots(figsize=(8, 5))
            accent_light, accent_dark = get_color("button_primary")
            chart_color = accent_dark if ctk.get_appearance_mode() == "Dark" else accent_light
            ax.bar(class_counts.keys(), class_counts.values(), color=chart_color)
            ax.set_title("Total Students per Class", fontsize=14, weight="bold")
            ax.set_xlabel("Class")
            ax.set_ylabel("Count")
            fig.patch.set_facecolor("none")
            ax.set_facecolor("none")
            
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
        """Show animated toast notification"""
        toast = ctk.CTkToplevel(self)
        toast.title("")
        toast.geometry("250x50")
        toast.attributes('-topmost', True)
        toast.overrideredirect(True)  # Remove window borders
        
        # Position toast at bottom right
        screen_width = toast.winfo_screenwidth()
        screen_height = toast.winfo_screenheight()
        toast.geometry(f"250x50+{screen_width-270}+{screen_height-80}")
        
        toast_label = ctk.CTkLabel(toast, text=msg, fg_color=get_color("accent_primary"),
                                  text_color=("white", "black"), corner_radius=8)
        toast_label.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Slide in animation
        AnimationUtils.slide_in(toast, "up", 0.3, 50)
        
        # Auto destroy after 3 seconds
        toast.after(3000, lambda: self._fade_out_toast(toast))
    
    def _fade_out_toast(self, toast):
        """Fade out toast before destroying"""
        if toast.winfo_exists():
            AnimationUtils.fade_out(toast, 0.5)
            toast.after(500, toast.destroy)