import json
import tkinter as tk
from tkinter import messagebox

class TodoList:
    def __init__(self, filename='todolist.json'):
        # Initialize TodoList with a default filename for saving tasks
        self.filename = filename
        # Load tasks from the file when creating an instance

    def load_tasks(self):
        # Load tasks from the file or create an empty list if the file doesn't exist or is empty
        try:
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            tasks = []
        return tasks

    def add_task(self, task, deadline=None):
        # Add a new task to the list
        self.tasks.append({'task': task, 'done': False, 'deadline': deadline, 'subtask': []})
        # Save the updated tasks
        self.save_tasks()

    def save_tasks(self):
        # Save tasks to the file
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

    def remove_task(self, index):
        # Remove a task at the specified index
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            # Save the updated tasks
            self.save_tasks()

    def mark_as_down(self, index):
        # Mark a task as done at the specified index

    def add_subtask(self, index, subtask):
        # Mark a task as done at the specified index
        if 0 <= index <= len(self.tasks):
            self.tasks[index]['done'] = True
            # Save the updated tasks

class TodoApp:
    def __init__(self, root):
        # Initialize the TodoApp with a Tkinter root window

    def add_task(self):
        # Add a new task to TodoList and update the task listbox

    def remove_task(self):
        # Remove the selected task from TodoList and update the task listbox
    def mark_as_done(self):
        # Mark the selected task as done in TodoList and update the task listbox
    def add_subtask(self):
        # Add a subtask to the selected task in TodoList and update the task listbox
    def populate_task_listbox(self):
        # Populate the task listbox with tasks from TodoList

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
