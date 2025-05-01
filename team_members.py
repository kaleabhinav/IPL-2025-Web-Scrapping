import os
import pandas as pd

from config import load_team_urls
from utils import get_team_players, merge_data_for_team_players

team_urls = load_team_urls()

df = merge_data_for_team_players(team_urls)

output_dir = os.path.join("Scrapped Info", "team_members")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "ipl_team_members.csv")
df.to_csv(output_path, sep='|', index=False)

print(f"Player data saved to: {output_path}")
