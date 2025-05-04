import json
import os

class DataManager:
    def __init__(self, save_file="todo_data.json"):
        self.save_file = save_file
        self.data = {
            'tabs': {}, 
            'tasks': {},
            'current_tab': None,
            'window_size': {'width': 800, 'height': 600}  # Default size
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Ensure all required keys exist
                    self.data['tabs'] = loaded_data.get('tabs', {})
                    self.data['tasks'] = loaded_data.get('tasks', {})
                    self.data['current_tab'] = loaded_data.get('current_tab')
                    self.data['window_size'] = loaded_data.get('window_size', {'width': 800, 'height': 600})
            except (json.JSONDecodeError, IOError):
                # Keep defaults if loading fails
                pass

    def save_data(self):
        with open(self.save_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_window_size(self):
        try:
            return self.data.get('window_size', {'width': 800, 'height': 600})
        except (KeyError, AttributeError):
            return {'width': 800, 'height': 600}

    def set_window_size(self, width, height):
        self.data['window_size'] = {'width': width, 'height': height}
        self.save_data()

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Migrate old data format
                    if 'window_size' not in loaded_data:
                        loaded_data['window_size'] = {'width': 800, 'height': 600}
                    self.data.update(loaded_data)  # Preserve defaults for missing keys
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data: {e}. Using default values.")
                # Keep the default data we initialized with

    def get_tabs(self):
        return self.data['tabs']

    def get_tasks(self):
        return self.data['tasks']

    def get_current_tab(self):
        return self.data['current_tab']

    def update_tab(self, tab_name, tab_data):
        self.data['tabs'][tab_name] = tab_data
        self.save_data()

    def update_task(self, tab_name, tasks):
        self.data['tasks'][tab_name] = tasks
        self.save_data()

    def set_current_tab(self, tab_name):
        self.data['current_tab'] = tab_name
        self.save_data()

    def delete_tab(self, tab_name):
        if tab_name in self.data['tabs']:
            del self.data['tabs'][tab_name]
        if tab_name in self.data['tasks']:
            del self.data['tasks'][tab_name]
        if self.data['current_tab'] == tab_name:
            self.data['current_tab'] = None
        self.save_data()