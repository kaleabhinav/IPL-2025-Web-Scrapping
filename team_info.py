# team_info.py
import pandas as pd
import os
import json

from utils import get_teams_information
from config import StaticConfig

url_info = StaticConfig()

directory = "Scrapped Info/teams_info"
os.makedirs(directory, exist_ok=True)

df = get_teams_information(url_info.website_url)

csv_path = os.path.join(directory, "ipl_teams_data.csv")
df.to_csv(csv_path, index=False)
print(f"Team info data saved to : {csv_path}")

# Save the team URLs to JSON config
urls_path = os.path.join("team_urls_json", "team_urls.json")
os.makedirs("team_urls_json", exist_ok=True)

team_urls = df['team_url'].dropna().unique().tolist()

with open(urls_path, "w") as f:
    json.dump(team_urls, f, indent=2)

print(f"Team URLs saved to {urls_path}")
