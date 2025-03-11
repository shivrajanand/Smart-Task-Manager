import tkinter as tk
from tkinter import ttk
from datetime import datetime
from core.task import Task

class TaskEditor(tk.Toplevel):
    def __init__(self, master, task=None, on_save=None):
        super().__init__(master)
        self.title("Edit Task" if task else "Add Task")
        self.task = task
        self.on_save = on_save  # callback to main window when saved

        # Form variables
        self.title_var = tk.StringVar(value=task.title if task else "")
        self.description_var = tk.StringVar(value=task.description if task else "")
        self.deadline_var = tk.StringVar(value=task.deadline.strftime('%Y-%m-%d %H:%M') if task else "")
        self.category_var = tk.StringVar(value=task.category if task else "")
        self.status_var = tk.StringVar(value=task.status if task else "NOT_STARTED")
        self.priority_var = tk.StringVar(value=task.priority if task else "Medium")

        self.build_form()
    
    def build_form(self):
        labels = ["Title", "Description", "Deadline (YYYY-MM-DD HH:MM)", "Category", "Status", "Priority"]
        vars = [self.title_var, self.description_var, self.deadline_var, self.category_var, self.status_var, self.priority_var]

        for i, (label, var) in enumerate(zip(labels, vars)):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            if label == "Status":
                options = ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]
                ttk.Combobox(self, textvariable=var, values=options, state="readonly").grid(row=i, column=1, padx=10, pady=5)
            elif label == "Priority":
                options = ["Low", "Medium", "High"]
                ttk.Combobox(self, textvariable=var, values=options, state="readonly").grid(row=i, column=1, padx=10, pady=5)
            else:
                tk.Entry(self, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        tk.Button(self, text="Save", command=self.save_task).grid(row=6, column=0, columnspan=2, pady=10)

    def save_task(self):
        try:
            deadline = datetime.strptime(self.deadline_var.get(), '%Y-%m-%d %H:%M')

            if self.task:
                # Editing existing task
                self.task.title = self.title_var.get()
                self.task.description = self.description_var.get()
                self.task.deadline = deadline
                self.task.category = self.category_var.get()
                self.task.status = self.status_var.get()
                self.task.priority = self.priority_var.get()
            else:
                # Creating new task
                self.task = Task(
                    title=self.title_var.get(),
                    description=self.description_var.get(),
                    deadline=deadline,
                    category=self.category_var.get(),
                    status=self.status_var.get(),
                    priority=self.priority_var.get()
                )

            if self.on_save:
                self.on_save(self.task)

            self.destroy()

        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please check the date format. Use YYYY-MM-DD HH:MM.")
