import tkinter as tk
from views.tab_view import TabView
from views.task_view import TaskView
from constants import BG_COLOR

class MainWindow:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        
        # Initialize controllers as None (they'll be set later)
        self.tab_controller = None
        self.task_controller = None
        
        # Setup window
        self.root.title("To-Do App")
        self._setup_window()
        self._setup_ui()
        
    def _setup_window(self):
        """Configure main window settings"""
        self.root.configure(bg=BG_COLOR)
        # Set initial size from data manager or use default
        size = self.data_manager.get_window_size()
        self.root.geometry(f"{size['width']}x{size['height']}")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _setup_ui(self):
        """Initialize all UI components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create views
        self.tab_view = TabView(self.main_frame)
        self.task_view = TaskView(self.main_frame)
        
        # Connect views to main window
        self.tab_view.main_window = self
        self.task_view.main_window = self
        
    def _on_close(self):
        """Handle window closing"""
        # Save window size
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.data_manager.set_window_size(width, height)
        self.root.destroy()