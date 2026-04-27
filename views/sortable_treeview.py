from tkinter import ttk

class SortableTreeview(ttk.Treeview):
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, columns=columns, show="headings", **kwargs)
        self.sort_states = {col: None for col in columns}
        self.original_data = []
        for col in columns:
            self.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))

    def set_data(self, data):
        self.original_data = data
        self.refresh()

    def refresh(self):
        for item in self.get_children():
            self.delete(item)
        for row in self.original_data:
            values = [row.get(col, "") for col in self["columns"]]
            self.insert("", "end", values=values)

    def sort_by_column(self, col):
        current = self.sort_states[col]
        if current is None:
            self.sort_states[col] = 'asc'
            reverse = False
        elif current == 'asc':
            self.sort_states[col] = 'desc'
            reverse = True
        else:
            self.sort_states[col] = None
            self.refresh()
            return

        sample = self.original_data[0][col] if self.original_data else ""
        is_numeric = isinstance(sample, (int, float))

        if is_numeric:
            self.original_data.sort(key=lambda x: x[col] if x[col] is not None else 0, reverse=reverse)
        else:
            self.original_data.sort(key=lambda x: str(x[col]).lower(), reverse=reverse)
        self.refresh()