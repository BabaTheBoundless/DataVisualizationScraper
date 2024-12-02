import json

#file mapping
files = {
    "2000": ("conference_wins2000.json", "conference_teams2000.json"),
    "2005": ("conference_wins2005.json", "conference_teams2005.json"),
    "2010": ("conference_wins2010.json", "conference_teams2010.json"),
}

#load wins and teams data
data = {}
for year, (wins_file, teams_file) in files.items():
    with open(wins_file, 'r') as file:
        wins_data = json.load(file)
    with open(teams_file, 'r') as file:
        teams_data = json.load(file)
    data[year] = {"wins": wins_data, "teams": teams_data}

#calculate average wins per team
average_wins_per_team = {}
for year, year_data in data.items():
    averages = {}
    for conf in year_data["wins"].keys():
        wins = year_data["wins"].get(conf, 0)
        teams = year_data["teams"].get(conf, 1)  #avoid division by zero
        averages[conf] = wins / teams
    average_wins_per_team[year] = averages

#compare averages year-to-year
year_keys = sorted(data.keys())  #ensure the years are ordered
comparisons = {}
for i in range(len(year_keys) - 1):
    year1, year2 = year_keys[i], year_keys[i + 1]
    year_comparison = {}
    for conf in average_wins_per_team[year1].keys():
        avg1 = average_wins_per_team[year1].get(conf, 0)
        avg2 = average_wins_per_team[year2].get(conf, 0)
        year_comparison[conf] = avg2 - avg1  #difference between years
    comparisons[f"{year1} to {year2}"] = year_comparison

#save the comparisons to JSON
with open('yearly_comparisons.json', 'w') as json_file:
    json.dump(comparisons, json_file, indent=4)

#save average wins per team to JSON
with open('yearly_win_differential.json', 'w') as json_file:
    json.dump(average_wins_per_team, json_file, indent=4)

print("Comparisons and averages saved to JSON files.")
