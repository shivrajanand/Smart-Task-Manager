import tkinter as tk
from tkinter import ttk, messagebox
from core.task_manager import TaskManager
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Manager")
        self.root.geometry("800x600")

        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#f0f8ff",
                "fg": "#000080",
                "entry_bg": "#ffffff",
                "button_bg": "#dbe9ff",
            },
            "dark": {
                "bg": "#1e1e2f",
                "fg": "#c0d6f0",
                "entry_bg": "#2e2e3d",
                "button_bg": "#3a4a6b",
            }
        }

        self.font = ("Cambria", 11)
        self.task_manager = TaskManager()
        self.visible_tasks = []

        self.setup_ui()

    def setup_ui(self):
        # Heading
        heading = ttk.Label(self.root, text="Smart Task Manager", font=("Cambria", 18, "bold"))
        heading.pack(pady=10)

        # Theme toggle
        ttk.Button(self.root, text="Toggle Theme", command=self.toggle_theme).pack(pady=5)

        # Progress Bar
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="Progress: 0%", font=self.font)
        self.progress_label.pack(side=tk.LEFT, padx=5)

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT)

        # Search
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Search:", font=self.font).pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT)
        search_entry.bind("<KeyRelease>", lambda event: self.refresh_task_list())

        # Sort
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(pady=5)

        ttk.Label(sort_frame, text="Sort by:", font=self.font).pack(side=tk.LEFT)

        self.sort_var = tk.StringVar(value="deadline")
        ttk.Radiobutton(sort_frame, text="Deadline", variable=self.sort_var, value="deadline", command=self.refresh_task_list).pack(side=tk.LEFT)
        ttk.Radiobutton(sort_frame, text="Priority", variable=self.sort_var, value="priority", command=self.refresh_task_list).pack(side=tk.LEFT)

        # Status filter
        status_filter_frame = ttk.Frame(self.root)
        status_filter_frame.pack(pady=5)

        ttk.Label(status_filter_frame, text="Filter by Status:", font=self.font).pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="All")
        status_options = ["All", "NOT_STARTED", "IN_PROGRESS", "COMPLETED"]
        status_menu = ttk.OptionMenu(status_filter_frame, self.status_var, "All", *status_options, command=lambda _: self.refresh_task_list())
        status_menu.pack(side=tk.LEFT)

        # Task List
        self.task_listbox = tk.Listbox(self.root, width=70, height=15, font=self.font)
        self.task_listbox.pack(padx=20, pady=10)
        self.task_listbox.bind("<<ListboxSelect>>", self.show_task_details)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Edit Task", command=self.edit_selected_task)
        self.menu.add_command(label="Delete Task", command=self.delete_selected_task)
        self.task_listbox.bind("<Button-3>", self.show_context_menu)

        # Add Task Button
        ttk.Button(self.root, text="Add Task", command=self.add_task).pack(pady=10)

        self.refresh_task_list()
        self.toggle_theme()  # Apply initial theme

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.list_tasks()
        self.visible_tasks = tasks.copy()

        # Filter by status
        if self.status_var.get() != "All":
            self.visible_tasks = [t for t in self.visible_tasks if t.status == self.status_var.get()]

        # Filter by search
        query = self.search_var.get().lower()
        if query:
            self.visible_tasks = [t for t in self.visible_tasks if query in t.title.lower() or query in t.description.lower()]

        # Sort
        if self.sort_var.get() == "deadline":
            self.visible_tasks.sort(key=lambda t: t.deadline)
        else:
            priority_map = {"High": 1, "Medium": 2, "Low": 3}
            self.visible_tasks.sort(key=lambda t: priority_map.get(t.priority, 4))

        for index, task in enumerate(self.visible_tasks):
            display = f"{task.title} - {task.deadline.strftime('%Y-%m-%d')} ({task.priority})"
            self.task_listbox.insert(tk.END, display)

            color = "black"
            if task.status == "COMPLETED":
                color = "green"
            elif task.status == "IN_PROGRESS":
                color = "orange"
            elif task.deadline < datetime.now():
                color = "red"

            self.task_listbox.itemconfig(index, fg=color)

        # Update progress bar
        total = len(self.visible_tasks)
        completed = len([t for t in self.visible_tasks if t.status == "COMPLETED"])
        percent = int((completed / total) * 100) if total else 0
        self.progress_bar["value"] = percent
        self.progress_label.config(text=f"Progress: {percent}%")

    def show_task_details(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task = self.visible_tasks[index]

            popup = tk.Toplevel(self.root)
            popup.title("Task Details")
            popup.geometry("400x280")

            details = (
                f"Title: {task.title}\n"
                f"Description: {task.description}\n"
                f"Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}\n"
                f"Category: {task.category}\n"
                f"Status: {task.status}\n"
                f"Priority: {task.priority}\n"
                f"Created: {task.created_date.strftime('%Y-%m-%d %H:%M')}"
            )

            ttk.Label(popup, text=details, justify="left", font=self.font, padding=10).pack(expand=True, fill="both")
            ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def show_context_menu(self, event):
        try:
            self.task_listbox.selection_clear(0, tk.END)
            self.task_listbox.selection_set(self.task_listbox.nearest(event.y))
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def edit_selected_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            task = self.visible_tasks[index]
            from gui.task_editor import TaskEditor
            TaskEditor(self.root, task=task, on_save=self.save_edited_task)

    def save_edited_task(self, task):
        self.task_manager.update_task(
            task.id, title=task.title, description=task.description,
            deadline=task.deadline, category=task.category,
            status=task.status, priority=task.priority
        )
        self.refresh_task_list()

    def delete_selected_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            task = self.visible_tasks[index]
            confirm = messagebox.askyesno("Confirm Delete", f"Delete task '{task.title}'?")
            if confirm:
                self.task_manager.delete_task(task.id)
                self.refresh_task_list()
                messagebox.showinfo("Deleted", f"Task '{task.title}' deleted.")

    def add_task(self):
        from gui.task_editor import TaskEditor
        TaskEditor(self.root, on_save=self.save_new_task)

    def save_new_task(self, task):
        self.task_manager.add_task(task)
        self.refresh_task_list()

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        for widget in self.root.winfo_children():
            self.apply_theme(widget, theme)

    def apply_theme(self, widget, theme):
        widget_type = widget.winfo_class()
        try:
            if widget_type in ["Frame", "TFrame"]:
                widget.configure(bg=theme["bg"])
            elif widget_type in ["Label", "Button", "Listbox"]:
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif widget_type == "Entry":
                widget.configure(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
            elif widget_type.startswith("T"):
                style = ttk.Style()
                style.theme_use("clam")
                style.configure(widget_type, background=theme["bg"], foreground=theme["fg"], font=self.font)
            for child in widget.winfo_children():
                self.apply_theme(child, theme)
        except Exception as e:
            print(f"Could not apply theme to {widget}: {e}")
