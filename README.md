# baseball-reference.com Data Scraper
This repo scrapes data from baseball-reference.com *Note: No data will be scraped from 2024 as the season is still young.*

# Introduction
This repository is my for CS2410 -- Fundamentals of Data Science class -- Capstone (final) project. The goal of this project is to show what my team and I learned throughout the semester. I developed and created the ML model, while my team verified the integrity of the dataset, cleaned, and prepared the data.

## Presentation
The accompanying PPTX presentation for the files can be found under `./presentation`.

# Website Structure

## Root
*baseball-reference.com/* is the entrypoint for the website. For scraping purposes, this is irrelevant since we want TEAM data, not current news.

## All Teams
*baseball-reference.com/teams/* is where all the current/former baseball teams live. For this project, the script will pull the 30 active MLB teams from the **Active Franchises** table.

## Team Specific Pages
*baseball-reference.com/teams/[3 LETTER TEAM (scoreboard) CODE]* is a teams individual page. This includes all seasons (including from previous team names/locations). The code will pull from the **Franchise History** table.

### Season Specific Pages
*baseball-reference.com/teams/[3 LETTER TEAM (scoreboard) CODE]/yyyy.shtml* is a teams individual season page. The Python code will pull from the *Full-Season Roster & Games by Position* table. More specifically, it'll make every player a row entry in the CSV file. A teams record will be at the top of the page, in the format: 
    ```    
    <p><strong>Record:</strong>ww-ll-tt</p>
    ```


# Machine Learning Algorithm
<ol>
    <li>Get teams WAR per year and record.</li>
    <li>Then, create a correlation plot between WAR and team record.</li>
    <li>Finally, predict a teams 2024 record based on said ML model.</li>
</ol>

## Running the program
It's as simple as running the file appropriate to what the developer wishes to get. 
<ul>
    <li>Run *website_scraper.py* to get data. Instructions/customization are found at the top of the file.</li>
    <li>Run *ml_from_data.py* to run the linear regression ML model. Customization is found at the bottom of the file.</li>
</ul>