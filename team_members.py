import os
import pandas as pd

from config import load_team_urls
from utils import merge_data_for_team_players

team_urls = load_team_urls()

df = merge_data_for_team_players(team_urls)

output_dir = os.path.join("scraped_info", "team_members")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "ipl_team_members.csv")
df.to_csv(output_path, sep='|', index=False)


