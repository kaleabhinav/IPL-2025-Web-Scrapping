# IPL‑2025‑Web‑Scrapping

A set of Python scripts to scrape comprehensive IPL 2025 data—covering team details, player rosters, and match statistics—and ready the results for upload to your Kaggle dataset.
The output of this repo is stored here : [kaggle](https://www.kaggle.com/datasets/kaleabhinav/ipl-2025-scrapped-data)
##  Overview

This repository streamlines end-to-end data collection for the 18th Indian Premier League (IPL 2025), including:

- Team structure and metadata  
- Player rosters per team  
- Match-by-match statistics  

---

##  File Structure

| File / Directory     | Purpose                                                            |
|----------------------|---------------------------------------------------------------------|
| `config.py`          | Central hub for configuration (base URLs, output paths, etc.)       |
| `team_urls_json/`    | Contains JSON mappings for team-specific endpoints or pages         |
| `team_info.py`       | Scrapes metadata such as team names, home venues, etc.              |
| `team_members.py`    | Collects player rosters and membership data per team                |
| `match_details.py`   | Downloads match logs: scores, outcomes, dates, etc.                 |
| `utils.py`           | Contains helper functions (e.g., HTTP requests, HTML parsing, logging, and file I/O)  |
| `.gitignore`         | Specifies files or patterns to ignore (e.g., logs, notebooks, caches)  |

---

##  Quickstart Guide

1. **Clone & Set Up**
   ```bash
   git clone https://github.com/kaleabhinav/IPL-2025-Web-Scrapping.git
   cd IPL-2025-Web-Scrapping
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Edit `config.py` to update base URLs, output paths, or any relevant settings.
   - Ensure that `team_urls_json/` has correct endpoints or identifiers for each IPL team.

3. **Run Scraping Workflows**
   ```bash
   python team_info.py
   python team_members.py
   python match_details.py
   ```
