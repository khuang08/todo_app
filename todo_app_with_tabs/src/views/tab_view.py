import tkinter as tk
from tkinter import Menu
from constants import TAB_BG, FG_COLOR, BUTTON_BG, ACTIVE_TAB_BG, BG_COLOR

class TabView:
    def __init__(self, parent):
        self.parent = parent
        self.main_window = None  # Will be set by MainWindow
        
        # Main frame with dark theme styling
        self.frame = tk.Frame(
            parent,
            bd=2,
            relief=tk.RAISED,
            bg=TAB_BG,
            width=200
        )
        self.frame.pack_propagate(False)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Tab buttons container
        self.tab_buttons_frame = tk.Frame(
            self.frame,
            bg=TAB_BG
        )
        self.tab_buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tab management buttons
        self.setup_tab_buttons()
    
    def show_context_menu(self, event):
        """Context menu for empty space in tab view"""
        menu = Menu(self.frame, tearoff=0)
        menu.add_command(label="New Tab", command=lambda: self.main_window.tab_controller.create_tab())
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

        # Add this binding in __init__ after creating the frame
#        self.frame.bind("<Button-3>", self.show_context_menu)
                
    def setup_tab_buttons(self):
        button_frame = tk.Frame(self.frame, bg=TAB_BG)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.new_tab_btn = tk.Button(
            button_frame,
            text="+ New Tab",
            width=12,
            bg=BUTTON_BG,
            fg=FG_COLOR,
            relief=tk.RAISED,
            activebackground=ACTIVE_TAB_BG
        )
        self.new_tab_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.delete_tab_btn = tk.Button(
            button_frame,
            text="- Delete Tab",
            width=12,
            bg=BUTTON_BG,
            fg=FG_COLOR,
            relief=tk.RAISED,
            activebackground=ACTIVE_TAB_BG
        )
        self.delete_tab_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Add this line to bind the context menu
        self.frame.bind("<Button-3>", self.show_context_menu)