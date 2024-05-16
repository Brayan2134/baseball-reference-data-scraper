import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def load_data_from_directory(directory_path):
    """
    Load data from Excel files in the specified directory, parse WAR values, and aggregate data.

    Args:
    directory_path (str): Path to the directory containing the Excel files.

    Returns:
    pandas.DataFrame: DataFrame containing aggregated year, total WAR, wins, losses, and team.
    """
    all_data = pd.DataFrame()

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(directory_path, filename)
            data = pd.read_excel(file_path)
            data['WAR'] = pd.to_numeric(data['WAR'], errors='coerce')
            year = int(filename.split("_")[1][:4])
            team = filename.split("_")[0]
            total_war = data['WAR'].sum()
            wins = data['Wins'].iloc[0]
            losses = data['Losses'].iloc[0]
            new_row = pd.DataFrame(
                {'Year': [year], 'Team': [team], 'Total_WAR': [total_war], 'Wins': [wins], 'Losses': [losses]})
            all_data = pd.concat([all_data, new_row], ignore_index=True)

    return all_data.sort_values(by=["Team", "Year"])


def analyze_and_model(data, team_colors):
    """
    Analyze the data for correlation, build a regression model, and plot with a single overall regression line and a shaded 95% confidence interval.

    Args:
    data (pandas.DataFrame): The input data containing years, total WAR, wins, and team.
    team_colors (dict): Dictionary of team abbreviations to colors.

    Returns:
    LinearRegression: The trained linear regression model.
    """

    plt.figure(figsize=(14, 8))
    unique_teams = data['Team'].unique()

    # Plot each team's scatter points
    for team in unique_teams:
        team_data = data[data['Team'] == team]
        plt.scatter(team_data['Total_WAR'], team_data['Wins'],
                    color=team_colors.get(team, "#000000"), label=team, alpha=0.6)

    # Draw a global regression line with a 95% confidence interval
    sns.regplot(x='Total_WAR', y='Wins', data=data, scatter=False, color='black',
                ci=99, line_kws={"color": "blue", "lw": 2})

    plt.title('Correlation between Total WAR and Wins by Team')
    plt.xlabel('Total WAR')
    plt.ylabel('Wins')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Preparing data for the model
    X = data[['Total_WAR']]
    y = data['Wins']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Building the regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predicting and evaluating the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    model_metrics(y_test, y_pred)

    return model


def predict_future_record(model, future_war):
    """
    Predict future record based on a given WAR value using the trained model.

    Args:
    model (LinearRegression): The trained regression model.
    future_war (float): The WAR value for which to predict the future record.

    Returns:
    float: The predicted number of wins.
    """
    prediction_data = pd.DataFrame({'Total_WAR': [future_war]})
    future_record = model.predict(prediction_data)
    return future_record[0]


# Helper function to categorize the metrics
def categorize_metric(value, metric_name):
    categories = {
        'R2': [(0.85, float('inf'), 'Very Good'),
               (0.75, 0.85, 'Good'),
               (0.6, 0.75, 'Satisfactory'),
               (None, 0.6, 'Not Satisfactory')],
        'NSE': [(0.8, float('inf'), 'Very Good'),
                (0.7, 0.8, 'Good'),
                (0.5, 0.7, 'Satisfactory'),
                (None, 0.5, 'Not Satisfactory')],
        'PBIAS': [(None, 5, 'Very Good'),
                  (5, 10, 'Good'),
                  (10, 15, 'Satisfactory'),
                  (15, float('inf'), 'Not Satisfactory')],
        'ME': [(None, 0.25, 'Very Good'),
               (0.25, 0.5, 'Good'),
               (0.5, 1.0, 'Satisfactory'),
               (1.0, float('inf'), 'Not Satisfactory')],
        'MAE': [(None, 0.5, 'Very Good'),
                (0.5, 0.75, 'Good'),
                (0.75, 1.5, 'Satisfactory'),
                (1.5, float('inf'), 'Not Satisfactory')],
        'RMSE': [(None, 0.75, 'Very Good'),
                 (0.75, 1.0, 'Good'),
                 (1.0, 2.0, 'Satisfactory'),
                 (2.0, float('inf'), 'Not Satisfactory')],
        'RSR': [(None, 0.5, 'Very Good'),
                (0.5, 0.6, 'Good'),
                (0.6, 0.7, 'Satisfactory'),
                (0.7, float('inf'), 'Not Satisfactory')],
    }

    # Adjust for metrics where lower values are better
    lower_is_better = ['PBIAS', 'ME', 'MAE', 'RMSE', 'RSR']
    if metric_name in lower_is_better:
        value = abs(value)

    for lower, upper, category in categories[metric_name]:
        if lower is None:
            lower = -float('inf')
        if upper is None:
            upper = float('inf')
        if lower < value <= upper:
            return category
    return 'Undefined'


def model_metrics(y_true, y_pred):
    """
    Calculate and display statistical metrics.

    Args:
    y_true (array-like): True values for the target variable.
    y_pred (array-like): Predicted values for the target variable.

    Returns:
    dict: Dictionary containing statistical metrics.
    """
    metrics = {}
    metrics['R2'] = r2_score(y_true, y_pred)
    metrics['ME'] = np.mean(y_pred - y_true)
    metrics['MAE'] = mean_absolute_error(y_true, y_pred)
    metrics['RMSE'] = np.sqrt(mean_squared_error(y_true, y_pred))
    metrics['NSE'] = 1 - sum((y_pred - y_true) ** 2) / sum((y_true - np.mean(y_true)) ** 2)
    metrics['PBIAS'] = 100 * sum(y_true - y_pred) / sum(y_true)
    metrics['RSR'] = metrics['RMSE'] / np.std(y_true)

    # Display the metrics with qualitative assessment
    print("\nModel Metrics:")
    for key, value in metrics.items():
        category = categorize_metric(value, key)
        print(f"{key}: {value:.3f} - {category}")
    return metrics


# Main execution
if __name__ == "__main__":
    directory_path = 'data/'

    # Define your team colors here
    team_colors = {
        'ARI': '#A71930',  # Arizona Diamondbacks
        'ATL': '#13274F',  # Atlanta Braves
        'BAL': '#DF4601',  # Baltimore Orioles
        'BOS': '#BD3039',  # Boston Red Sox
        'CWS': '#27251F',  # Chicago White Sox
        'CHC': '#0E3386',  # Chicago Cubs
        'CIN': '#C6011F',  # Cincinnati Reds
        'CLE': '#E31937',  # Cleveland Guardians
        'COL': '#33006F',  # Colorado Rockies
        'DET': '#0C2340',  # Detroit Tigers
        'HOU': '#002D62',  # Houston Astros
        'KCR': '#004687',  # Kansas City Royals
        'LAA': '#BA0021',  # Los Angeles Angels
        'LAD': '#005A9C',  # Los Angeles Dodgers
        'MIA': '#00A3E0',  # Miami Marlins
        'MIL': '#0A2351',  # Milwaukee Brewers
        'MIN': '#002B5C',  # Minnesota Twins
        'NYY': '#0C2340',  # New York Yankees
        'NYM': '#002D72',  # New York Mets
        'OAK': '#003831',  # Oakland Athletics
        'PHI': '#E81828',  # Philadelphia Phillies
        'PIT': '#FDB827',  # Pittsburgh Pirates
        'SDP': '#2F241D',  # San Diego Padres
        'SFG': '#FD5A1E',  # San Francisco Giants
        'SEA': '#0C2C56',  # Seattle Mariners
        'STL': '#C41E3A',  # St. Louis Cardinals
        'TBR': '#092C5C',  # Tampa Bay Rays
        'TEX': '#003278',  # Texas Rangers
        'TOR': '#134A8E',  # Toronto Blue Jays
        'WSN': '#AB0003',  # Washington Nationals
    }
    data = load_data_from_directory(directory_path)
    model = analyze_and_model(data, team_colors)

    # Example prediction for a future WAR value
    future_war = 35  # Example WAR value
    predicted_wins = predict_future_record(model, future_war)
    print(f"Predicted (Wins,Losses) for 2024 based on WAR {future_war}: {predicted_wins}, {162-predicted_wins}")