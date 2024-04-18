from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

"""
YEARS OF DATA THAT WILL BE GATHERED:
--------------
1990-2023
EXCLUDE 1995
EXCLUDE 2020
"""


"""
"""
def downloadTableFromURL(url, team, year):
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the webpage
    driver.get(url)

    # Wait for JavaScript to load (adjust time as necessary)
    time.sleep(5)  # Increase or decrease based on your network speed and page complexity

    # Extract tables using Pandas
    try:
        tables = pd.read_html(driver.page_source, attrs={'id': 'appearances'})
        if tables:
            df = tables[0]
            print(df)
            # Generate a filename using the team and year
            filename = f"data/{team}_{year}.xlsx"
            df.to_excel(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No table found with the specified ID 'appearances'")
    except Exception as e:
        print(f"An error occurred: {e}")

    driver.quit()

"""
"""
def downloadActiveFranchises(url):
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the webpage
    driver.get(url)

    # Wait for JavaScript to load (adjust time as necessary)
    time.sleep(5)  # Increase or decrease based on your network speed and page complexity

    # Extract tables using Pandas
    tables = pd.read_html(driver.page_source, attrs={'id': 'teams_active'})

    if tables:
        df = tables[0]
        print("Original Data:")
        print(df)

        # Filter rows: remove rows where 'Franchise' column contains "Also played as" or ", see"
        conditions = df['Franchise'].str.contains("Also played as", na=False) | df['Franchise'].str.contains(", see",
                                                                                                             na=False)
        df_cleaned = df[~conditions]
        print("\nCleaned Data:")
        print(df_cleaned)

        # Save the cleaned data to Excel
        df_cleaned.to_excel('data/output_cleaned.xlsx', index=False)
    else:
        print("No table found with the specified ID 'teams_active'")

    driver.quit()


"""
This function will create a URL
for each baseball team of the format
baseball-reference.com/teams/[3 LETTER TEAM (scoreboard) CODE]/yyyy.shtml
"""
def create_urls():
    base_url = "https://www.baseball-reference.com/teams/"
    teams = [
        "ARI", "ATL", "BAL", "BOS", "CHC", "CWS", "CIN", "CLE", "COL", "DET",
        "HOU", "KCR", "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY", "OAK",
        "PHI", "PIT", "SDP", "SFG", "SEA", "STL", "TBR", "TEX", "TOR", "WSN"
    ]
    years = [year for year in range(1990, 2024) if year not in (1995, 2020)]
    urls = []

    for team in teams:
        for year in years:
            url = f"{base_url}{team}/{year}.shtml"
            urls.append((url, team, year))

    return urls


"""
"""
def scrape():
    urls = create_urls()
    print(urls)
    for url, team, year in urls:
        downloadTableFromURL(url, team, year)

scrape()