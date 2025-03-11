from core.task import Task
import json

def save_tasks_to_file(tasks, filename):
    """
    Saves a list of Task objects to a JSON file.
    Each Task is converted to a dictionary first.
    """

    task_dicts = [task.to_dict() for task in tasks]

    with open(filename, "w") as file:
        json.dump(task_dicts, file, indent=4)
    print(f"{len(tasks)} tasks saved to {filename}")


def load_tasks_from_file(filename):
    """
    Loads a list of Task objects from a JSON file.
    Each dictionary is converted to a Task object first.
    """
    try:
        with open(filename, "r") as file:
            task_dicts = json.load(file)
            return [Task.from_dict(data) for data in task_dicts]
    except FileNotFoundError:
        print(f"⚠️ File {filename} not found. Returning empty task list.")
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON from {filename}. Returning empty task list.")
        return []
    