import json

# Load the JSON files
with open('conference_wins.json') as f:
    wins_data = json.load(f)

with open('conference_teams.json') as f:
    teams_data = json.load(f)


average_wins_per_team = {}

for conference, total_wins in wins_data.items():
    total_teams = teams_data.get(conference, 0)  #get total teams for conference
    if total_teams > 0:  #avoid 0-based division
        average_wins_per_team[conference] = total_wins / total_teams
    else:
        average_wins_per_team[conference] = None 
print(average_wins_per_team) 

with open('average_wins_per_team.json', 'w') as f:
    json.dump(average_wins_per_team, f, indent=4)