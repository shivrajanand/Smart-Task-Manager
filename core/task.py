import uuid
from datetime import datetime

class Task:
    VALID_PRIORITIES = ["Low", "Medium", "High"]

    def __init__(self, title, description, deadline, category, status, priority = "Medium", created_date=None, task_id=None):
        """Initializes the task object with the given title, description, deadline, category, status, priority and created_date."""
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        if isinstance(deadline, str):
            self.deadline = datetime.fromisoformat(deadline)
        else:
            self.deadline = deadline 
        self.category = category
        self.status = status
        #status = COMPLETED, IN_PROGRESS, NOT_STARTED
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(self.VALID_PRIORITIES)}")
        else: 
            self.priority = priority
        if isinstance(created_date, str):
            self.created_date = datetime.fromisoformat(created_date)
        else:
            self.created_date = created_date or datetime.now()

    def mark_completed(self):
        """Marks the task as completed."""
        self.status = "COMPLETED"

    def mark_in_progress(self):
        """Marks the task as In Progress."""
        self.status = "IN_PROGRESS"

    def is_overdue(self):
        """Checks if the task given is overdue or not by comparing it with now datetime."""
        return datetime.now() > self.deadline
    
    def to_dict(self):
        """Converts the task object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat(),
            "category": self.category,
            "status": self.status,
            "priority": self.priority,
            "created_date": self.created_date.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        """"Converts the dictionary to a task object."""
        return Task(
        task_id = data["id"],
        title = data["title"],
        description = data["description"],
        deadline = data["deadline"],
        category = data["category"],
        status = data["status"],
        priority = data["priority"],
        created_date = data["created_date"])

    def __str__(self):
        """Returns the string representation of the task object."""
        return f"Title: {self.title}\nDeadline: {self.deadline}\nStatus: {self.status}\nPriority: {self.priority}\n Created Date: {self.created_date}"