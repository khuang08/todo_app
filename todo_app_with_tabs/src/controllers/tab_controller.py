import tkinter as tk
from tkinter import simpledialog, messagebox
from constants import ACTIVE_TAB_BG, TAB_BG, FG_COLOR, BUTTON_BG

class TabController:
    def __init__(self, tab_view, data_manager):
        self.view = tab_view
        self.model = data_manager
        self.tab_buttons = {}
        
        # Style management buttons
        self.view.new_tab_btn.config(
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_TAB_BG,
            command=self.create_tab
        )
        self.view.delete_tab_btn.config(
            bg=BUTTON_BG,
            fg=FG_COLOR,
            activebackground=ACTIVE_TAB_BG,
            command=self.delete_tab
        )

    def _create_tab_button(self, tab_name):
            tab_btn = tk.Button(
                self.view.tab_buttons_frame,
                text=tab_name,
                command=lambda: self.switch_tab(tab_name),
                bg=TAB_BG,
                fg=FG_COLOR,
                relief=tk.RAISED,
                padx=10,
                pady=5,
                anchor="w",
                activebackground=ACTIVE_TAB_BG
            )
            
            # Bind double-click event
            tab_btn.bind("<Double-Button-1>", lambda e, name=tab_name: self._rename_tab(name))
            
            # Bind right-click event
            tab_btn.bind("<Button-3>", lambda e, name=tab_name: self._show_context_menu(e, name))
            
            tab_btn.pack(fill=tk.X, pady=2, padx=2)
            self.tab_buttons[tab_name] = tab_btn
            return tab_btn

    def _show_context_menu(self, event, tab_name):
        menu = tk.Menu(self.view.tab_buttons_frame, tearoff=0)
        menu.add_command(
            label="Rename Tab",
            command=lambda: self._rename_tab(tab_name)
        )
        menu.add_separator()
        menu.add_command(
            label="Delete Tab",
            command=lambda: self._delete_tab_with_confirmation(tab_name)
        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _delete_tab_with_confirmation(self, tab_name):
        if messagebox.askyesno("Delete Tab", f"Delete tab '{tab_name}' and all its tasks?"):
            self._delete_tab(tab_name)

    def _rename_tab(self, old_name):
        new_name = simpledialog.askstring(
            "Rename Tab",
            "Enter new tab name:",
            initialvalue=old_name,
            parent=self.view.frame
        )
        
        if new_name and new_name != old_name:
            if new_name in self.model.get_tabs():
                messagebox.showerror("Error", f"A tab named '{new_name}' already exists!")
                return
            
            # Update model
            tab_data = self.model.get_tabs().get(old_name, {})
            tasks = self.model.get_tasks().get(old_name, [])
            
            self.model.delete_tab(old_name)
            self.model.update_tab(new_name, tab_data)
            self.model.update_task(new_name, tasks)
            
            # Update current tab if needed
            if self.model.get_current_tab() == old_name:
                self.model.set_current_tab(new_name)
            
            # Update view
            if old_name in self.tab_buttons:
                btn = self.tab_buttons[old_name]
                btn.config(text=new_name)
                btn.bind("<Double-Button-1>", lambda e, name=new_name: self._rename_tab(name))
                btn.bind("<Button-3>", lambda e, name=new_name: self._show_context_menu(e, name))
                
                self.tab_buttons[new_name] = self.tab_buttons.pop(old_name)
            
            # Refresh tasks if needed
            if hasattr(self.view, 'main_window') and hasattr(self.view.main_window, 'task_controller'):
                self.view.main_window.task_controller.refresh_tasks(new_name)

    def _delete_tab(self, tab_name):
        # Don't allow deletion if it's the last tab
        if len(self.model.get_tabs()) <= 1:
            messagebox.showwarning("Warning", "You must have at least one tab")
            return False
        
        # Proceed with deletion
        if tab_name in self.tab_buttons:
            self.tab_buttons[tab_name].destroy()
            del self.tab_buttons[tab_name]
        
        self.model.delete_tab(tab_name)
        
        # Switch to first available tab
        remaining_tabs = self.model.get_tabs()
        if remaining_tabs:
            self.switch_tab(next(iter(remaining_tabs)))
        return True

    def create_tab(self, tab_name=None):
        # Allow empty/blank names by removing the strip() check
        if tab_name is None:
            tab_name = f"Tab {len(self.model.get_tabs()) + 1}"
        
        # Remove the empty name check completely
        if tab_name not in self.model.get_tabs():
            self._create_tab_button(tab_name)
            self.model.update_tab(tab_name, {})
            self.model.update_task(tab_name, [])
            self.switch_tab(tab_name)
            return True
        
        # Handle duplicate names by appending number
        i = 1
        while f"{tab_name} ({i})" in self.model.get_tabs():
            i += 1
        return self.create_tab(f"{tab_name} ({i})")

    def switch_tab(self, tab_name):
        tabs = self.model.get_tabs()
        if tab_name in tabs:
            self.model.set_current_tab(tab_name)
            
            # Update all tab buttons' appearance
            for name, button in self.tab_buttons.items():
                button.config(
                    bg=ACTIVE_TAB_BG if name == tab_name else TAB_BG,
                    relief=tk.SUNKEN if name == tab_name else tk.RAISED
                )
            
            # Refresh tasks
            if hasattr(self.view, 'main_window') and hasattr(self.view.main_window, 'task_controller'):
                self.view.main_window.task_controller.refresh_tasks(tab_name)
            return True
        return False

    def delete_tab(self):
        current_tab = self.model.get_current_tab()
        if not current_tab:
            return
            
        if messagebox.askyesno("Delete Tab", f"Delete tab '{current_tab}' and all its tasks?"):
            # Remove from view
            if current_tab in self.tab_buttons:
                self.tab_buttons[current_tab].destroy()
                del self.tab_buttons[current_tab]
            
            # Remove from model
            self.model.delete_tab(current_tab)
            
            # Handle last tab case
            remaining_tabs = self.model.get_tabs()
            if not remaining_tabs:
                self.create_tab("Default")
            else:
                self.switch_tab(next(iter(remaining_tabs)))