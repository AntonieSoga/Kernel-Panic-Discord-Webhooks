import json
import os

class StateManager:
    def __init__(self, filepath="state.json"):
        self.filepath = filepath

    def _load_state(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def get_last_link(self, feed_name: str):
        state = self._load_state()
        return state.get(feed_name)

    def update_last_link(self, feed_name: str, link: str):
        state = self._load_state()
        state[feed_name] = link
        with open(self.filepath, 'w') as f:
            json.dump(state, f, indent=4)