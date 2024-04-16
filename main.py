import pandas as pd

# Specify the path to the HTML file
file_path = 'tests/sample1.html'

# Read the HTML file, specifically targeting the table with the ID 'appearances'
tables = pd.read_html(file_path, attrs={'id': 'appearances'})

# Check if the table was correctly identified and extracted
if tables:
    # Assuming the table is the first (and only) in the list
    df = tables[0]

    # Process the DataFrame, e.g., handling rows that contain 'All Star'
    # Here, you might want to insert any specific processing you need for 'All Star' rows or other data clean-up
    # Example: Remove rows where a specific column (e.g., player name) contains 'All Star'
    # df = df[~df['Player'].str.contains('All Star', na=False)]

    # Save the DataFrame to an Excel file
    df.to_excel('output.xlsx', index=False)
else:
    print("No table found with the specified ID 'appearances'")
