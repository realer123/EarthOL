import json

class Task:
    VALID_CATEGORIES = [
        "School Work",
        "Self-Study-STEM",
        "Self-Study-Humanities",
        "Workout",
        "Combat Training",
        "Looks",
        "Practice Music",
        "Practice Arts",
        "Play Sports",
        "Others"
    ]

    def __init__(self, name, scheduled_time, category, note = "", completed = False):
        self.name = name
        self.scheduled_time = scheduled_time  # string like "2025-10-29 18:00"
        self.category = category
        self.note = note
        self.completed = completed

    def mark_done(self):
        self.completed = not self.completed
        # ticks and unticks

    def to_dict(self):
        return {
            "name": self.name,
            "scheduled_time": self.scheduled_time,
            "category": self.category,
            "note": self.note,
            "completed": self.completed
        }

    @classmethod               # turn dictionary data back to Task
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.name} | {self.category} | {self.scheduled_time} | Note: {self.note}"


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, name, scheduled_time="No time", category="General", note=""):
        self.tasks.append(Task(name, scheduled_time, category, note))
        self.save_tasks()

    def add_task_interactive(self):
        """Prompt the user to fill in all fields for a new task (for console use)."""
        print("📝 Enter new task details:")
        name = input("Task name: ").strip()
        scheduled_time = input("Scheduled time (e.g., 2025-11-05 15:00 or leave blank): ").strip() or "No time"

        for i, cat in enumerate(Task.VALID_CATEGORIES, start=1):
            print(f"{i}. {cat}")

        try:
            choice = int(input(f"Enter number (1-{len(Task.VALID_CATEGORIES)}) or leave blank for 'Others': ").strip())
            if 1 <= choice <= len(Task.VALID_CATEGORIES):
                category = Task.VALID_CATEGORIES[choice - 1]
            else:
                category = "Others"
        except ValueError:
            category = "Others"

        note = input("Note (optional): ").strip()
        self.add_task(name, scheduled_time, category, note)

    def delete_task(self, name):
        new_tasks = []
        for t in self.tasks:
            if t.name != name:
                new_tasks.append(t)

        self.tasks = new_tasks
        self.save_tasks()

    def mark_done(self, name):
        for task in self.tasks:
            if task.name == name:
                task.mark_done()
                break
        self.save_tasks()

    def view_all(self):
        if not self.tasks:
            print("No tasks found.")
            return

        i = 1
        for task in self.tasks:
            print(f"{i}. {task}")
            i += 1  # increase the counter by 1 each loop

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4) #converting Task to dictionary

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]
        except FileNotFoundError:
            self.tasks = []