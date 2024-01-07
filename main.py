import json
import tkinter as tk
from tkinter import messagebox


class TodoList:
    def __init__(self, filename='todolist.json'):
        # Initialize TodoList with a default filename for saving tasks
        self.filename = filename
        # Load tasks from the file when creating an instance
        self.tasks = self.load_tasks()

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

    def mark_as_done(self, index):
        # Mark a task as done at the specified index
        if 0 <= index <= len(self.tasks):
            self.tasks[index]['done'] = True
            # Save the updated tasks
            self.save_tasks()

    def add_subtask(self, index, subtask):
        # Add a subtask to the task at the specified index
        if 0 <= index <= len(self.tasks):
            self.tasks[index]['subtasks'].append({'subtask': subtask, 'done': False})
            # Save the updated tasks
            self.save_tasks()


class TodoApp:
    def __init__(self, root):
        # Initialize the TodoApp with a Tkinter root window
        self.root = root
        self.root.title("ToDo")

        # Create an instance of TodoList
        self.todo = TodoList()

        # Create Tkinter widgets
        self.task_entry = tk.Entry(root, width=20)
        self.task_entry.pack(paddy=10)

        self.add_button = tk.Button(root, text="Task", command=self.add_task)
        self.add_button.pack(paddy=10)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.task_listbox.pack(paddy=10)

        self.remove_button = tk.Button(root, text="REmove", command=self.remove_task)
        self.remove_button.pack(paddy=10)

        self.done_button = tk.Button(root, text="Done", command=self.mark_as_done)
        self.done_button.pack(paddy=10)

        self.subtask_entry = tk.Entry(root, width=20)
        self.subtask_entry.pack(paddy=10)

        self.add_subtask_button = tk.Button(root, text="Subtask", command=self.add_subtask)
        self.add_subtask_button.pack(pady=10)

        # Populate the task listbox with existing tasks
        self.populate_task_listbox()

    def add_task(self):
        # Add a new task to TodoList and update the task listbox
        new_task = self.task_entry.get()
        self.todo.add_task(new_task)
        self.populate_task_listbox()
        self.task_entry.delete(0, tk.END)

    def remove_task(self):
        # Remove the selected task from TodoList and update the task listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.todo.remove_task(selected_index[0])
            self.populate_task_listbox()

    def mark_as_done(self):
        # Mark the selected task as done in TodoList and update the task listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.todo.mark_as_done(selected_index[0])
            self.populate_task_listbox()

    def add_subtask(self):
        # Add a subtask to the selected task in TodoList and update the task listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            subtask_text = self.subtask_entry.get()
            self.todo.add_subtask(selected_index[0], subtask_text)
            self.populate_task_listbox()
            self.subtask_entry.delete(0, tk.END)

    def populate_task_listbox(self):
        # Populate the task listbox with tasks from TodoList
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.todo.tasks, start=1):
            status = 'Done' if task['done'] else 'Not Done'
            deadline = f" (Deadline: {task['deadline']}" if task['deadline'] else ""
            self.task_listbox.insert(tk.END, f"{index}. {task['task']} - {status} {deadline}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
