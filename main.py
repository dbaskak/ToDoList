import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.filedialog as filedialog
from datetime import datetime


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

    def change_deadline(self, index, new_deadline):
        # Add task deadline
        if 0 <= index < len(self.tasks):
            self.tasks[index]['deadline'] = new_deadline
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

    def mark_as_done(self, index, subtask_index=None):
        # Mark a task or subtask as done at the specified index
        if 0 <= index < len(self.tasks):
            if subtask_index is None:
                # Mark the main task as done
                self.tasks[index]['done'] = True
            else:
                # Mark the subtask as done
                subtasks = self.tasks[index].get('subtask', [])
                if 0 <= subtask_index < len(subtasks):
                    subtasks[subtask_index]['done'] = True
            # Save the updated tasks
            self.save_tasks()

    def add_subtask(self, index, subtask):
        # Add a subtask to the task at the specified index
        if 0 <= index < len(self.tasks):
            self.tasks[index]['subtask'].append({'subtask': subtask, 'done': False})
            # Save the updated tasks
            self.save_tasks()

    def remove_subtask(self, index, subtask_index):
        # Remove a subtask from the task at the specified index
        if 0 <= index < len(self.tasks):
            subtasks = self.tasks[index].get('subtask', [])
            if 0 <= subtask_index < len(subtasks):
                del subtasks[subtask_index]
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
        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=50)
        self.task_listbox.pack(pady=10)

        self.remove_button = tk.Button(root, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.done_button = tk.Button(root, text="Mark as Done", command=self.mark_as_done)
        self.done_button.pack(pady=5)

        self.subtask_entry = tk.Entry(root, width=50)
        self.subtask_entry.pack(pady=10)

        self.add_subtask_button = tk.Button(root, text="Add Subtask", command=self.add_subtask)
        self.add_subtask_button.pack(pady=5)

        self.remove_subtask_button = tk.Button(root, text="Remove Subtask", command=self.remove_subtask)
        self.remove_subtask_button.pack(pady=5)

        # Populate the task listbox with existing tasks
        self.populate_task_listbox()

        # Deadline change button
        self.change_deadline_button = tk.Button(root, text="Change Deadline", command=self.change_deadline)
        self.change_deadline_button.pack(pady=5)

        # File select button
        self.select_file_button = tk.Button(root, text="Select Todo List File", command=self.select_file)
        self.select_file_button.pack(pady=5)

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
        # Mark the selected task or subtask as done in TodoList and update the task listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            item_text = self.task_listbox.get(selected_index[0])
            clean_text = item_text.strip()
            indices = [int(index) for index in clean_text.split('.')[0].split('-')[:2] if index.isdigit()]
            if indices:
                main_index, *subtask_index = indices + [0]
                if isinstance(subtask_index, list):
                    subtask_index = subtask_index[0]
                if subtask_index is not None:
                    self.todo.mark_as_done(main_index - 1, subtask_index - 1)
                else:
                    self.todo.mark_as_done(main_index - 1)
                self.populate_task_listbox()

    def add_subtask(self):
        # Add a subtask to the selected task in TodoList and update the task listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            subtask_text = self.subtask_entry.get()
            item_text = self.task_listbox.get(selected_index[0])
            main_index, *subtask_index = map(int, item_text.split('.')[0].split('-')[:2] + [0])
            if isinstance(subtask_index, list) and subtask_index:
                subtask_index = subtask_index[0]
            if 0 <= main_index - 1 < len(self.todo.tasks):
                self.todo.add_subtask(main_index - 1, subtask_text)
                self.populate_task_listbox()
                self.subtask_entry.delete(0, tk.END)

    def get_indices(self, selected_index):
        # Get element index from Listbox
        item_text = self.task_listbox.get(selected_index[0])
        return [int(index) for index in item_text.split('.')[0].split('-') if index.isdigit()]

    def remove_subtask(self):
        # Remove the selected subtask from TodoList and update the task listbox
        selected_index = self.task_listbox.curselection()
        if selected_index:
            item_text = self.task_listbox.get(selected_index[0])
            clean_text = item_text.strip()
            indices = [int(index) for index in clean_text.split('.')[0].split('-') if index.isdigit()]
            if len(indices) == 2:
                main_index, subtask_index = indices
                self.todo.remove_subtask(main_index - 1, subtask_index - 1)
                self.populate_task_listbox()

    def populate_task_listbox(self):
        # Populate the task listbox with tasks from TodoList
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.todo.tasks, start=1):
            status = 'Done' if task['done'] else 'Not Done'

            if isinstance(task['deadline'], str):
                deadline = f" (Deadline: {task['deadline']})"
            elif isinstance(task['deadline'], datetime):
                deadline = f" (Deadline: {task['deadline'].strftime('%Y-%m-%d')})"
            else:
                deadline = ""

            self.task_listbox.insert(tk.END, f"{index}. {task['task']} - {status}{deadline}")

            # Check if there are subtasks and display them
            subtasks = task.get('subtask', [])
            for subtask_index, subtask in enumerate(subtasks, start=1):
                subtask_status = 'Done' if subtask['done'] else 'Not Done'
                self.task_listbox.insert(tk.END, f"     - Subtask: {subtask['subtask']} - {subtask_status}")

    def change_deadline(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            try:
                selected_index = selected_index[0]
                new_deadline = self.get_user_input("Enter new deadline (YYYY-MM-DD):")
                if new_deadline and not self.is_valid_date(new_deadline):
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                    return
                item_text = self.task_listbox.get(selected_index)
                indices = list(map(int, filter(lambda x: x.isdigit(), item_text.split('.')[0].split('-')[:2])))
                if indices:
                    main_index, *_ = indices + [0]
                    if indices[1:]:
                        main_index, *_ = indices + [0]
                        self.todo.change_deadline(main_index - 1, new_deadline)
                    else:
                        self.todo.change_deadline(main_index - 1, new_deadline)
                    self.populate_task_listbox()
            except IndexError:
                messagebox.showerror("Error", "Task not found!")

    def is_valid_date(self, date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def select_file(self):
        # Select task file
        file_path = tk.filedialog.askopenfilename(title="Select Todo List File", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.todo = TodoList(filename=file_path)
            self.populate_task_listbox()

    def get_user_input(self, prompt):
        user_input = simpledialog.askstring("Input", prompt)
        return user_input


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
