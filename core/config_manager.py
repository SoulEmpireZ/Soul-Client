import json
import os

class ConfigManager:
    def __init__(self, filename="config.json"):
        # Resolve path to AppData/Roaming/SoulClient to avoid Windows UAC permission errors
        appdata_dir = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), "SoulClient")
        os.makedirs(appdata_dir, exist_ok=True)
        self.filename = os.path.join(appdata_dir, filename)

    def load_config(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"username": "", "ram_gb": 4, "accent_color": "#615251", "show_log_on_exit": True}

    def save_config(self, config_data):
        try:
            with open(self.filename, "w") as f:
                json.dump(config_data, f, indent=4)
        except:
            pass