from core.file_handler import save_tasks_to_file, load_tasks_from_file

    
class TaskManager:
    def __init__(self, data_file = "data/tasks.json"):
        """Initializes the TaskManager object."""
        self.data_file = data_file
        self.tasks = []
        self.load_from_file()

    def add_task(self, task):
        """Adds a task to the task list."""
        self.tasks.append(task)
        self.save_to_file()

    def get_task(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def update_task(self, task_id, **kwargs):
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.save_to_file()
            return True
        return False
    
    def delete_task(self, task_id):
        """Deletes a task from the task list."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_to_file()

    def list_tasks(self, filter_by = None):
        """Lists all the tasks in the task list."""
        if filter_by:
            return [task for task in self.tasks if task.status == filter_by]
        return self.tasks
    
    def load_from_file(self):
        """Loads the tasks from the file."""
        self.tasks = load_tasks_from_file(self.data_file)

    def save_to_file(self):
        """Saves the tasks to the file."""
        save_tasks_to_file(self.tasks, self.data_file)



