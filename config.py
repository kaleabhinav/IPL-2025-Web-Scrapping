from dataclasses import dataclass, field
import json
import os

@dataclass
class StaticConfig:
    website_url: str = "https://www.iplt20.com/teams"

def load_team_urls():
    config_path = os.path.join("config", "team_urls.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return []
