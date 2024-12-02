import json

# Files for wins and losses by year
files = {
    "2005": ("conference_wins2005.json"),
    "2010": ("conference_wins2010.json"),
}

# To store results
win_rates_data = {}

# Read data for each year
for year, results_file in files.items():
    with open(results_file, 'r') as file:
        team_results = json.load(file)  # Format: {"Conference": {"Team": {"Wins": X, "Losses": Y}}}
    
    conference_rates = {}
    
    # Calculate win rate per conference
    for conference, teams in team_results.items():
        total_win_rate = 0
        total_teams = 0
        
        for team, record in teams.items():
            wins = record["Wins"]
            losses = record["Losses"]
            total_games = wins + losses  # Use wins + losses for total games
            
            if total_games > 0:  # Avoid division by zero
                team_win_rate = wins / total_games
                total_win_rate += team_win_rate
                total_teams += 1

        # Calculate conference-level win rate
        if total_teams > 0:
            conference_rates[conference] = total_win_rate / total_teams
    
    # Store for the year
    win_rates_data[year] = conference_rates

# Compare win rates across years
adjusted_win_rates = {}
years = list(win_rates_data.keys())

for conf in win_rates_data[years[0]].keys():  # Assume same conferences exist in all years
    total_adjusted_rate = 0
    count_years = 0
    
    for year in years:
        if conf in win_rates_data[year]:
            total_adjusted_rate += win_rates_data[year][conf]
            count_years += 1
    
    if count_years > 0:
        adjusted_win_rates[conf] = total_adjusted_rate / count_years

# Save results
with open('adjusted_win_rate_2005-2010.json', 'w') as json_file:
    json.dump(adjusted_win_rates, json_file, indent=4)

print("Adjusted win rates saved to 'adjusted_win_rate_2005-2010.json'.")
