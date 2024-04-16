# baseball-reference-data-scraper
This repo scrapes data from baseball-reference.com *Note: No data will be scraped from 2024 as the season is still young.*

# Website Structure

## Root
*baseball-reference.com/* is the entrypoint for the website. For scraping purposes, this is irrelevant since we want TEAM data, not current news.

## All Teams
*baseball-reference.com/teams/* is where all the current/former baseball teams live. For this project, the script will pull the 30 active MLB teams from the **Actice Franchises** table.

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