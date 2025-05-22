from bs4 import BeautifulSoup
import requests
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

def get_teams_information(url):
    try:
        resp = requests.get(url)
        # resp.raise_for_status()
        print("GOT GREEN LIGHT FROM URL!!!")
    except requests.exceptions.RequestException as e:
        print(f"Request Faild : {e}")

    soup = BeautifulSoup(resp.text, "html.parser")
    team_key = url.rstrip("/").split("/")[-1]
    l = []  # Will hold the infomation that is scrapped

    for i in soup.find_all("a", {"data-team_name":True}):
        team_name = i['data-team_name']  
        
        url = i['href']

        abbrevation = i.find('span').text if i.find('span') else None

        trophy_div = i.find('div', class_='trophy-text-align')
        trophy_year =  trophy_div.text if trophy_div else None

        logo_tag = i.find("img")
        logo = logo_tag['src'] if logo_tag else None

        l.append([team_name, abbrevation, trophy_year, logo, url])

    df = pd.DataFrame(l, columns = ["team_name","abbrevation","trophy_year","logo","team_url"])
    df['team_name'] = team_key
    return df


def get_team_players(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        print(f"GOT GREEN LIGHT FROM {url}!!!")
    except requests.exceptions.RequestException as e:
        print(f"Request Failed: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(resp.text, "html.parser")
    players = []

    team_name = url.rstrip("/").split("/")[-1]

    for i in soup.find_all("a", {"data-player_name": True}):
        head_shot_tag = i.find(class_='lazyload')
        head_shot_png = head_shot_tag.get('data-src') if head_shot_tag else None

        player_name = i['data-player_name']

        player_type_tag = i.find(class_='d-block w-100 text-center')
        player_type = player_type_tag.text.strip() if player_type_tag else None

        teams_icon_div = i.find(class_='teams-icon')
        tag = teams_icon_div.find_all("img") if teams_icon_div else []

        player_type_icon = captain_icon = foreign_player_icon = None
        if len(tag) == 1:
            player_type_icon = tag[-1]['src']
        elif len(tag) == 2:
            if "captain" in tag[0]['src']:
                captain_icon = tag[0]['src']
                player_type_icon = tag[1]['src']
            else:
                foreign_player_icon = tag[0]['src']
                player_type_icon = tag[1]['src']
        elif len(tag) >= 3:
            captain_icon = tag[0]['src']
            foreign_player_icon = tag[1]['src']
            player_type_icon = tag[2]['src']

        players.append([
            player_name,
            head_shot_png,
            player_type,
            player_type_icon,
            captain_icon,
            foreign_player_icon
        ])

    df = pd.DataFrame(players, columns=[
        'player_name', 'head_shot_png', 'player_type',
        'player_type_icon', 'captain_icon', 'foreign_player_icon'
    ])
    df['team_name'] = team_name  
    return df

def merge_data_for_team_players(urls):

    dfs = []
    for url in urls:
        df = get_team_players(url)
        dfs.append(df)

    # Merge all data into one DataFrame
    merged_df = pd.concat(dfs).reset_index(drop=True)
    return merged_df

def get_match_soups(url):
    options = Options()
    options.add_argument("--headless")  # Run headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--window-size=1920,1080")  # Optional: helps render full page

    # Pretend to be a real user
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 15)
        inning_tabs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ap-inner-tb-click")))
    except Exception:
        driver.quit()
        raise ValueError("Inning tabs not found or page did not load in time.")

    if len(inning_tabs) < 2:
        driver.quit()
        raise ValueError("Less than two innings tabs found.")

    # First innings
    first_tab = inning_tabs[0]
    first_team = first_tab.text.strip()
    first_tab.click()
    time.sleep(2)
    first_inning_soup = BeautifulSoup(driver.page_source, "html.parser")

    # Second innings
    second_tab = inning_tabs[1]
    second_team = second_tab.text.strip()
    second_tab.click()
    time.sleep(2)
    second_inning_soup = BeautifulSoup(driver.page_source, "html.parser")

    driver.quit()

    return first_inning_soup, second_inning_soup, first_team, second_team

def get_match_metadata(soup):
    """
    The function provides metadata of the match up between two teams.
    Input : Provide the soup of the innings html data.
    Ouput : Gives out a array of [Match Number, Venue, Date, Time].
    """
    l = []
    match_number = soup.find(class_ = "matchOrder mob-hide ng-binding ng-scope").text 
    l.append(match_number)
    
    for i in soup.find(class_ = "ap-match-place col-100 floatLft textCenter re ng-scope").find_all('span'):
        l.append(i.text)

    return l

def get_ball_by_ball_commentary(soup):
    # ball_wrapper = soup.find_all('div', class_ = ['ballWrapper ng-scope','cmdOver mcBall mcBall mcBall mcBall mcBall mcBall'])
    ball_wrapper = soup.select('div.ballWrapper.ng-scope')
    ball_wrapper = ball_wrapper[1:]
    
    # To Store the scrapped data
    l = []

    for i in ball_wrapper:
        if i.p.contents[0].strip() != '':

            # Which ball of the over is this
            ball_number = i.p.contents[0].strip()

            # Event happened on this ball
            event_on_that_ball = i.find('i').text.strip()

            # bowler vs batter info
            bowling_info_tag = i.find('div', class_='commentaryStartText')
            bowling_info = bowling_info_tag.get_text(strip=True) if bowling_info_tag else None

            # detailed commentary
            commentary_tag = i.find('div', class_='commentaryText')
            commentary = commentary_tag.get_text(strip=True) if commentary_tag else None

            l.append({
                'ball': ball_number,
                'event': event_on_that_ball,
                'bowling_info': bowling_info,
                'commentary': commentary,
            })

    df = pd.DataFrame(l)
    return df
    
