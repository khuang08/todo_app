import tkinter as tk
from models.data_manager import DataManager
from views.main_window import MainWindow
from controllers.tab_controller import TabController
from controllers.task_controller import TaskController

def main():
    # Initialize core components
    root = tk.Tk()
    data_manager = DataManager()
    
    # Create main window with data manager
    main_window = MainWindow(root, data_manager)
    
    # Create controllers
    tab_controller = TabController(main_window.tab_view, data_manager)
    task_controller = TaskController(main_window.task_view, data_manager)
    
    # Connect controllers to main window
    main_window.tab_controller = tab_controller
    main_window.task_controller = task_controller
    
    # Initialize tabs
    tabs = data_manager.get_tabs()
    if not tabs:
        tab_controller.create_tab()
    else:
        for tab_name in tabs:
            tab_controller._create_tab_button(tab_name)
        if current_tab := data_manager.get_current_tab() or next(iter(tabs), None):
            tab_controller.switch_tab(current_tab)
    
    root.mainloop()

if __name__ == "__main__":
    main()