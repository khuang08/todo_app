import tkinter as tk
from tkinter import messagebox
from constants import BG_COLOR, FG_COLOR, CHECKBOX_BG, BUTTON_BG, ACTIVE_BG

class TaskController:
    def __init__(self, task_view, data_manager):
        self.view = task_view
        self.model = data_manager
        self.current_frames = []
        
        # Bind events
        self.view.add_btn.config(command=self.add_task)
        self.view.entry.bind("<Return>", lambda e: self.add_task())

    def add_task(self):
        task_text = self.view.entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return

        current_tab = self.model.get_current_tab()
        if not current_tab:
            messagebox.showwarning("Warning", "Please select or create a tab first!")
            return

        # Get current tasks for the tab
        tasks = self.model.get_tasks().get(current_tab, [])
        tasks.append({"text": task_text, "checked": False})
        self.model.update_task(current_tab, tasks)
        
        self.refresh_tasks(current_tab)
        self.view.entry.delete(0, tk.END)

    def refresh_tasks(self, tab_name):
        # Clear current frames
        for frame in self.current_frames:
            frame.destroy()
        self.current_frames = []
        
        # Create new frames for each task
        tasks = self.model.get_tasks().get(tab_name, [])
        for i, task in enumerate(tasks):
            self._create_task_ui(tab_name, i, task["text"], task["checked"])

    def _create_task_ui(self, tab_name, task_index, task_text, is_checked):
        frame = tk.Frame(self.view.task_list_frame, bg=BG_COLOR)
        frame.pack(fill=tk.X, pady=2)
        self.current_frames.append(frame)
        
        # Checkbox
        var = tk.BooleanVar(value=is_checked)
        chk = tk.Checkbutton(
            frame,
            text=task_text,
            variable=var,
            bg=CHECKBOX_BG,
            fg=FG_COLOR,
            command=lambda: self._toggle_task(tab_name, task_index)
        )
        chk.pack(side=tk.LEFT, anchor="w")

        # Action buttons
        buttons_frame = tk.Frame(frame, bg=BG_COLOR)
        buttons_frame.pack(side=tk.RIGHT)

        tk.Button(
            buttons_frame,
            text="↑",
            command=lambda: self._move_task(tab_name, task_index, "up"),
            bg=BUTTON_BG,
            fg=FG_COLOR
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            buttons_frame,
            text="↓",
            command=lambda: self._move_task(tab_name, task_index, "down"),
            bg=BUTTON_BG,
            fg=FG_COLOR
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            buttons_frame,
            text="-",
            command=lambda: self._delete_task(tab_name, task_index),
            bg=BUTTON_BG,
            fg=FG_COLOR
        ).pack(side=tk.LEFT, padx=2)

    def _delete_task(self, tab_name, task_index):
        tasks = self.model.get_tasks().get(tab_name, [])
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            self.model.update_task(tab_name, tasks)
            self.refresh_tasks(tab_name)

    def _toggle_task(self, tab_name, task_index):
        tasks = self.model.get_tasks().get(tab_name, [])
        if 0 <= task_index < len(tasks):
            tasks[task_index]["checked"] = not tasks[task_index]["checked"]
            self.model.update_task(tab_name, tasks)

    def _move_task(self, tab_name, task_index, direction):
        tasks = self.model.get_tasks().get(tab_name, [])
        if 0 <= task_index < len(tasks):
            new_index = task_index - 1 if direction == "up" else task_index + 1
            if 0 <= new_index < len(tasks):
                tasks[task_index], tasks[new_index] = tasks[new_index], tasks[task_index]
                self.model.update_task(tab_name, tasks)
                self.refresh_tasks(tab_name)