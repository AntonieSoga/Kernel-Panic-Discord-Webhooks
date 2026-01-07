import json
import os

class StateManager:
    def __init__(self, filepath="state.json"):
        self.filepath = filepath

    def get_last_link(self):
        if not os.path.exists(self.filepath):
            return None
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            return data.get("last_link")

    def update_last_link(self, link: str):
        with open(self.filepath, 'w') as f:
            json.dump({"last_link": link}, f)