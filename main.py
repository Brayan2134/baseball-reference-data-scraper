from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os

"""
YEARS OF DATA THAT WILL BE GATHERED:
--------------
1990-2023
EXCLUDE 1995 (because of protests)
EXCLUDE 2020 (because of COVID)
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
    time.sleep(2)  # Increase or decrease based on your network speed and page complexity

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

    # Find the start index for the specific URL
    start_index = next((i for i, (url, team, year) in enumerate(urls) if team == "PHI" and year == 2004), None)
    if start_index is not None:
        print(f"Starting from index {start_index}, URL: {urls[start_index]}")
        urls_to_process = urls[start_index:]  # Create a new list starting from the desired URL
    else:
        print("Specified start URL not found. Processing all URLs.")
        urls_to_process = urls

    # Loop through the filtered list
    for url, team, year in urls_to_process:
        downloadTableFromURL(url, team, year)

    """
    urls = create_urls()
    print(urls)
    for url, team, year in urls:
        downloadTableFromURL(url, team, year)
    """

"""
"""
def parse_record(record_str):
    # Split the string by the dash and convert each part to an integer
    wins, losses, ties = map(int, record_str.split('-'))
    return wins, losses, ties



"""
"""
def fetch_record(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the <strong> tag that contains the text 'Record:'
        record_tag = soup.find('strong', string='Record:')

        # Check if the tag was found
        if record_tag:
            # The next_sibling should contain the record text
            record_data = record_tag.next_sibling.strip()
            # Clean and return the record data
            return record_data.split(',')[0].strip()  # Splits on comma and returns the first part
        else:
            return "Record not found"
    else:
        return f"Failed to retrieve page with status code {response.status_code}"


def generate_urls_from_files(directory):
    # Dictionary to store filenames and their URLs
    file_urls = {}

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") and len(filename.split('_')) == 2:
            # Split the filename to extract the team code and year
            team_code, year_with_extension = filename.split('_')
            year = year_with_extension.split('.')[0]  # Remove the '.xlsx' extension

            # Generate the URL
            url = f"https://www.baseball-reference.com/teams/{team_code}/{year}.shtml"
            file_urls[filename] = url

            # Optionally, read the XLSX file
            # filepath = os.path.join(directory, filename)
            # df = pd.read_excel(filepath)
            # Here you can process df as needed

    return file_urls


"""
"""
def append_to_excel(file_path, data):
    df = pd.read_excel(file_path)
    df['Wins'] = data[0]
    df['Losses'] = data[1]
    df['Ties'] = data[2]
    df.to_excel(file_path, index=False)

"""
"""


# Main function to handle the entire process
def process_files(directory):
    file_count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") and len(filename.split('_')) == 2:
            team_code, year_with_extension = filename.split('_')
            year = year_with_extension.split('.')[0]  # Remove the '.xlsx' extension
            url = f"https://www.baseball-reference.com/teams/{team_code}/{year}.shtml"

            record_str = fetch_record(url)
            if record_str:
                wins, losses, ties = parse_record(record_str)
                if wins is not None and losses is not None and ties is not None:
                    file_path = os.path.join(directory, filename)
                    append_to_excel(file_path, (wins, losses, ties))
                    print(f"Processed {filename} successfully.")
                else:
                    print(f"Error parsing record for {filename}.")
            else:
                print(f"Error fetching record for {filename}.")

            file_count += 1
            if file_count % 10 == 0:
                print("Reached 10 requests, pausing for 60 seconds.")
                time.sleep(60)  # Pause the execution for 60 seconds


directory = "data/"
process_files(directory)

#print(parse_record(fetch_record("https://www.baseball-reference.com/teams/ARI/2018.shtml")))