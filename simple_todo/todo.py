import tkinter as tk
from tkinter import messagebox
import json
import threading
import time
import logging

# --- Globals ---
tasks = []  # Stores (chk, var, task, frame) tuples
save_file = "todo_data.json"
autosave_interval = 300  # 5 minutes

# --- Color Scheme (Dark Mode) ---
BG_COLOR = "#2d2d2d"
FG_COLOR = "#e0e0e0"
ENTRY_BG = "#3d3d3d"
BUTTON_BG = "#4d4d4d"
CHECKBOX_BG = BG_COLOR
ACTIVE_BG = "#5d5d5d"
BUTTON_FONT = ("Arial", 8)  # Consistent font for all buttons

# --- Functions ---
def add_task(event=None):
    task = entry.get()
    if task:
        var = tk.BooleanVar(value=False)
        task_frame = tk.Frame(frame, bg=BG_COLOR)
        task_frame.pack(fill=tk.X, pady=2)
        
        chk = tk.Checkbutton(
            task_frame, 
            text=task, 
            variable=var, 
            bg=CHECKBOX_BG,
            fg=FG_COLOR,
            selectcolor="black",
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR
        )
        chk.pack(side=tk.LEFT, anchor="w")
        
        # Delete button (-)
        delete_btn = tk.Button(
            task_frame,
            text="-",
            command=lambda: delete_single_task(tasks.index((chk, var, task, task_frame))),
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            relief=tk.FLAT,
            font=BUTTON_FONT
        )
        delete_btn.pack(side=tk.RIGHT, padx=2)
        
        # Move up button
        move_up = tk.Button(
            task_frame,
            text="↑",
            command=lambda: move_task(tasks.index((chk, var, task, task_frame)), "up"),
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            relief=tk.FLAT,
            font=BUTTON_FONT
        )
        move_up.pack(side=tk.RIGHT, padx=2)
        
        # Move down button
        move_down = tk.Button(
            task_frame,
            text="↓",
            command=lambda: move_task(tasks.index((chk, var, task, task_frame)), "down"),
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            relief=tk.FLAT,
            font=BUTTON_FONT
        )
        move_down.pack(side=tk.RIGHT, padx=2)
        
        tasks.append((chk, var, task, task_frame))
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_single_task(index):
    chk, var, task, task_frame = tasks[index]
    task_frame.destroy()
    tasks.remove((chk, var, task, task_frame))
    save_tasks()

def move_task(index, direction):
    if direction == "up" and index > 0:
        new_index = index - 1
    elif direction == "down" and index < len(tasks) - 1:
        new_index = index + 1
    else:
        return
    
    tasks[index], tasks[new_index] = tasks[new_index], tasks[index]
    refresh_task_display()
    save_tasks()

def refresh_task_display():
    for _, _, _, task_frame in tasks:
        task_frame.pack_forget()
        task_frame.destroy()
    
    new_tasks = []
    for chk, var, task, old_frame in tasks:
        task_frame = tk.Frame(frame, bg=BG_COLOR)
        task_frame.pack(fill=tk.X, pady=2)
        
        new_chk = tk.Checkbutton(
            task_frame, 
            text=task, 
            variable=var, 
            bg=CHECKBOX_BG,
            fg=FG_COLOR,
            selectcolor="black",
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR
        )
        new_chk.pack(side=tk.LEFT, anchor="w")
        
        # Delete button (-)
        delete_btn = tk.Button(
            task_frame,
            text="-",
            command=lambda i=tasks.index((chk, var, task, old_frame)): delete_single_task(i),
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            relief=tk.FLAT,
            font=BUTTON_FONT
        )
        delete_btn.pack(side=tk.RIGHT, padx=2)
        
        # Move up button
        move_up = tk.Button(
            task_frame,
            text="↑",
            command=lambda i=tasks.index((chk, var, task, old_frame)): move_task(i, "up"),
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            relief=tk.FLAT,
            font=BUTTON_FONT
        )
        move_up.pack(side=tk.RIGHT, padx=2)
        
        # Move down button
        move_down = tk.Button(
            task_frame,
            text="↓",
            command=lambda i=tasks.index((chk, var, task, old_frame)): move_task(i, "down"),
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            relief=tk.FLAT,
            font=BUTTON_FONT
        )
        move_down.pack(side=tk.RIGHT, padx=2)
        
        new_tasks.append((new_chk, var, task, task_frame))
    
    tasks[:] = new_tasks

def save_tasks():
    data = [{"text": task, "checked": var.get()} for chk, var, task, _ in tasks]
    with open(save_file, "w") as f:
        json.dump(data, f)

def load_tasks():
    try:
        with open(save_file, "r") as f:
            data = json.load(f)
            for item in data:
                var = tk.BooleanVar(value=item["checked"])
                task_frame = tk.Frame(frame, bg=BG_COLOR)
                task_frame.pack(fill=tk.X, pady=2)
                
                chk = tk.Checkbutton(
                    task_frame, 
                    text=item["text"], 
                    variable=var, 
                    bg=CHECKBOX_BG,
                    fg=FG_COLOR,
                    selectcolor="black",
                    activebackground=ACTIVE_BG,
                    activeforeground=FG_COLOR
                )
                chk.pack(side=tk.LEFT, anchor="w")
                
                # Delete button (-)
                delete_btn = tk.Button(
                    task_frame,
                    text="-",
                    command=lambda i=len(tasks): delete_single_task(i),
                    bg=BUTTON_BG,
                    fg=FG_COLOR,
                    activebackground=ACTIVE_BG,
                    activeforeground=FG_COLOR,
                    relief=tk.FLAT,
                    font=BUTTON_FONT
                )
                delete_btn.pack(side=tk.RIGHT, padx=2)
                
                # Move up button
                move_up = tk.Button(
                    task_frame,
                    text="↑",
                    command=lambda i=len(tasks): move_task(i, "up"),
                    bg=BUTTON_BG,
                    fg=FG_COLOR,
                    activebackground=ACTIVE_BG,
                    activeforeground=FG_COLOR,
                    relief=tk.FLAT,
                    font=BUTTON_FONT
                )
                move_up.pack(side=tk.RIGHT, padx=2)
                
                # Move down button
                move_down = tk.Button(
                    task_frame,
                    text="↓",
                    command=lambda i=len(tasks): move_task(i, "down"),
                    bg=BUTTON_BG,
                    fg=FG_COLOR,
                    activebackground=ACTIVE_BG,
                    activeforeground=FG_COLOR,
                    relief=tk.FLAT,
                    font=BUTTON_FONT
                )
                move_down.pack(side=tk.RIGHT, padx=2)
                
                tasks.append((chk, var, item["text"], task_frame))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def autosave_loop():
    while True:
        time.sleep(autosave_interval)
        save_tasks()

def on_closing():
    save_tasks()
    root.destroy()

# --- Main Window ---
root = tk.Tk()
root.title("To-Do App")
root.geometry("400x500")
root.configure(bg=BG_COLOR)

# Frame (task list container)
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Task Entry (with Enter key binding)
entry = tk.Entry(
    root, 
    width=30, 
    bg=ENTRY_BG, 
    fg=FG_COLOR, 
    insertbackground=FG_COLOR,
    relief=tk.FLAT
)
entry.pack(pady=10, padx=10)
entry.bind("<Return>", add_task)

# Add Task Button
add_btn = tk.Button(
    root, 
    text="Add Task", 
    command=add_task,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=ACTIVE_BG,
    activeforeground=FG_COLOR,
    relief=tk.FLAT,
    font=BUTTON_FONT
)
add_btn.pack(pady=5)

# Load tasks and start autosave
load_tasks()
autosave_thread = threading.Thread(target=autosave_loop, daemon=True)
autosave_thread.start()

# Exit handling
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
