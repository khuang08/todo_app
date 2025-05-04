import tkinter as tk
from constants import BG_COLOR, FG_COLOR, ENTRY_BG, BUTTON_BG, ACTIVE_BG

class TaskView:
    def __init__(self, parent):
        self.parent = parent
        self.main_window = None  # Will be set by MainWindow
        
        # Main frame with no border
        self.frame = tk.Frame(
            parent,
            bd=0,
            relief=tk.FLAT,
            bg=BG_COLOR
        )
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Task list area
        self.task_list_frame = tk.Frame(
            self.frame,
            bg=BG_COLOR
        )
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bottom controls
        self.bottom_frame = tk.Frame(
            self.frame,
            bg=BG_COLOR
        )
        self.bottom_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM)
        
        self.entry = tk.Entry(
            self.bottom_frame,
            bg=ENTRY_BG,
            fg=FG_COLOR,
            insertbackground=FG_COLOR
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.add_btn = tk.Button(
            self.bottom_frame,
            text="Add Task",
            width=10,
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_BG
        )
        self.add_btn.pack(side=tk.LEFT, padx=2)

    def setup_bottom_controls(self):
        """Legacy method kept for compatibility (now done in __init__)"""
        pass