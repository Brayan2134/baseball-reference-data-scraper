"""
NAME: BRAYAN QUEVEDO RAMOS
DATE: 04/20/2024

DESCRIPTION: This file uses Selenium to scrape data on baseball-reference.com,
             More specifically, it scrapes the 30 MLB teams data based on user
             defined years. Then, the data will be put into an XLSX file with on sheet being
             table data, and another sheet being Win-Loss-Tie record for the season.
"""
from bs4 import BeautifulSoup
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd

import requests
import time
import os

# Global constants (CAN CHANGE!)
DIRECTORY = "temp/"  # Where to store XLSX Files
START_YEAR = 2010  # What year to start scraping data
END_YEAR = 2020  # What year to end data scraping
SKIP_YEARS = {2013, 2015}  # Any years to be avoided (if any)
TABLE_ID = "appearances"  # The table ID on the website
team_codes = [
    "ARI",  # Arizona Diamondbacks
    "ATL",  # Atlanta Braves
    "BAL",  # Baltimore Orioles
    "BOS",  # Boston Red Sox
    "CHC",  # Chicago Cubs
    "CWS",  # Chicago White Sox
    "CIN",  # Cincinnati Reds
    "CLE",  # Cleveland Guardians, formerly known as Cleveland Indians
    "COL",  # Colorado Rockies
    "DET",  # Detroit Tigers
    "HOU",  # Houston Astros
    "KC",   # Kansas City Royals
    "LAA",  # Los Angeles Angels
    "LAD",  # Los Angeles Dodgers
    "MIA",  # Miami Marlins, formerly known as Florida Marlins
    "MIL",  # Milwaukee Brewers
    "MIN",  # Minnesota Twins
    "NYM",  # New York Mets
    "NYY",  # New York Yankees
    "OAK",  # Oakland Athletics
    "PHI",  # Philadelphia Phillies
    "PIT",  # Pittsburgh Pirates
    "SD",   # San Diego Padres
    "SF",   # San Francisco Giants
    "SEA",  # Seattle Mariners
    "STL",  # St. Louis Cardinals
    "TB",   # Tampa Bay Rays, formerly known as Tampa Bay Devil Rays
    "TEX",  # Texas Rangers
    "TOR",  # Toronto Blue Jays
    "WSH"   # Washington Nationals, formerly known as Montreal Expos
]  # What MLB teams to scrape (all 30 of them)

"""
TABLE IDS ON WEBSITE (If you want to change what table is downloaded!):
-----------------------------------------------------------------------
Team Batting: "team_batting"
Team Pitching: "team_pitching"
Full-Season Roster & Games by Position: "appearances"
Coaching Staff: "coaches"
Team Fielding--Totals: "standard_fielding"
Team Player Value--Batters: "players_value_batting"
Team Player Value--Pitchers: "players_value_pitching"
"""


# Function to create URLs and associated filenames
def create_urls_and_filenames(team_code, start_year, end_year):
    """
    Generates a list of URLs and filenames for each year in the specified range,
    excluding years in SKIP_YEARS.
    """
    urls_filenames = []
    for year in range(start_year, end_year + 1):
        if year not in SKIP_YEARS:
            url = f"https://www.baseball-reference.com/teams/{team_code}/{year}.shtml"
            filename = f"{team_code}_{year}.xlsx"
            urls_filenames.append((url, filename))
    return urls_filenames


# Function to handle HTML table using StringIO
def download_table_from_url(url, table_id):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    # time.sleep(10)  # Adjust time based on your network speed (typically not needed but just in case!)

    try:
        table_html = driver.find_element(By.ID, table_id).get_attribute('outerHTML')
        df_table = pd.read_html(StringIO(table_html))[0]  # Use StringIO here
        driver.quit()
        return df_table
    except Exception as e:
        print(f"No table found with ID {table_id} at {url}: {e}")
        driver.quit()
        return None


# Function to fetch the record from a URL
def fetch_record(url):
    """
    Fetches the record string from the specified URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        record_tag = soup.find('strong', string='Record:')
        if record_tag:
            return record_tag.next_sibling.strip().split(',')[0].strip()
    return None


# Function to parse the record string
def parse_record(record_str):
    """
    Parses the record string into wins, losses, and ties.
    """
    try:
        return map(int, record_str.split('-'))
    except ValueError:
        return None, None, None


# Function to create an Excel file
def create_excel(file_path, data, df_table):
    """
    Creates an Excel file and writes the table and record data to it.
    """
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        if df_table is not None:
            df_table.to_excel(writer, sheet_name='Appearances')
        df = pd.DataFrame({'Wins': [data[0]], 'Losses': [data[1]], 'Ties': [data[2]]})
        df.to_excel(writer, sheet_name='Summary')


# Main function to process the tasks
def process_teams():
    """
    Main function to process each team and year configuration.
    """
    os.makedirs(DIRECTORY, exist_ok=True)  # Ensure the directory exists
    for team_code in team_codes:
        urls_filenames = create_urls_and_filenames(team_code, START_YEAR, END_YEAR)
        for url, filename in urls_filenames:
            df_table = download_table_from_url(url, TABLE_ID)
            record_str = fetch_record(url)
            if record_str:
                wins, losses, ties = parse_record(record_str)
                if wins is not None:
                    file_path = os.path.join(DIRECTORY, filename)
                    create_excel(file_path, (wins, losses, ties), df_table)
                    print(f"Created {filename} successfully with data from {url}")

            time.sleep(6)  # Respect rate limiting (10 requests per minute per website EULA)


if __name__ == "__main__":
    process_teams()
