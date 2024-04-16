from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the webpage
url = 'https://www.baseball-reference.com/teams/ARI/2023.shtml'
driver.get(url)

# Wait for JavaScript to load (adjust time as necessary)
time.sleep(5)  # Increase or decrease based on your network speed and page complexity

# Extract tables using Pandas
tables = pd.read_html(driver.page_source, attrs={'id': 'appearances'})

if tables:
    df = tables[0]
    print(df)
    df.to_excel('output.xlsx', index=False)
else:
    print("No table found with the specified ID 'appearances'")

driver.quit()
