from utils import get_match_soups, get_ball_by_ball_commentary, get_match_metadata
import pandas as pd
import os

# Corrected the print statement
print("Please provide a valid URL: ")
url = input()

# Prepare the tasty tasty soup
first_inning_soup, second_inning_soup, whos_first_inning, whos_second_inning = get_match_soups(url)

# Get metadata - [Match Number, Venue, Date, Time]
match_metadata = get_match_metadata(first_inning_soup)

# Extract Ball by Ball Events and commentary (output is dataframe) 
# 1st Inning
df1 = get_ball_by_ball_commentary(first_inning_soup)

# Adding match metadata to df1
columns = ["match_number", "venue", "date", "time"]
for col, val in zip(columns, match_metadata):
    df1[col] = val

df1['batting_team'] = whos_first_inning

# 2nd Inning
df2 = get_ball_by_ball_commentary(second_inning_soup)

# Adding match metadata to df2 (not overwriting df1)
for col, val in zip(columns, match_metadata):
    df2[col] = val

df2['batting_team'] = whos_second_inning

# Merging Both innings vertically (row-wise) using axis=0
result = pd.concat([df1, df2], axis=0, ignore_index=True)

# Making a folder to store the info
os.makedirs("Scrapped Info/match_details", exist_ok=True)

# Save the result to a CSV file
result.to_csv(f"Scrapped Info/match_details/{'_'.join(match_metadata[:3])}.csv", index=False)

