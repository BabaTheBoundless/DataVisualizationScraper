import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import networkx as nx
from scraper import get_team_record
from scrapeNodes import scrape_nodes
import time
from rapidfuzz import process

with open('2000seasonWithWins', 'r') as myjson:
    football_data = json.load(myjson)

with open('scrapeTeams.json', 'r') as nodejson:
    node_data = json.load(nodejson)

fbs_teams = {node["id"] for node in node_data}
mismatched_names = set()



def match_team_names(team, valid_names, threshold = 95):
    match = process.extractOne(team, valid_names)
    if match and match[1] >= threshold: 
        return match[0]
    return None

def clean_team_name(team_name):
    #team_name = re.sub(f'-', '', team_name) #hyphen
    #team_name = re.sub(r'\s+', '', team_name) #whitespace
    team_name = re.sub(r'\(\d+\)', '', team_name).strip() #strip ranking
    if team_name == "Brigham Young":
        team_name = "BYU"
    elif team_name == "Southern Methodist":
        team_name = "SMU"
    elif team_name == "Mississippi":
        team_name = "Ole Miss"
    elif team_name == "Texas-El Paso":
        team_name = "UTEP"
    elif team_name == "Louisiana State":
        team_name = "LSU"
    elif team_name == "Alabama-Birmingham":
        team_name = "UAB"
    elif team_name == "Southern California":
        team_name = "USC"
    elif team_name == "Pittsburgh":
        team_name = "Pitt"
    elif team_name == "Central Florida":
        team_name = "UCF"
    
    matched_name = match_team_names(team_name, fbs_teams)
    return matched_name if matched_name else team_name
    #if team_name == "Miami(FL)":
    #    team_name = "MiamiFlorida"
   # elif team_name == "Miami(OH)":
    #    team_name = "MiamiOhio"
   # elif team_name == "KentState":
   #     team_name = "Kent"
    #elif team_name == "Texas-El Paso":
 #       team_name = "TexasElPaso"
  #  elif team_name == "Louisiana": 
  #      team_name = "LouisianaLafayette"
  #  elif team_name == "BowlingGreen":
   #     team_name = "BowlingGreenState"
    
def scrape_cfb_results():
    url = "https://www.sports-reference.com/cfb/years/2000-schedule.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #locate the schedule table
    table = soup.find('table', {'id': 'schedule'})
    

    #extract table rows
    rows = table.find_all('tr')[1:]  #skip the header row
    #print(rows)
    
    data = []
    for row in rows:
        cols = row.find_all('td')
        #print(cols)
        if not cols:
            continue
        
        #print(cols)

        #extract and clean data
        #print(cols[3].text.strip())
        winner = clean_team_name(cols[3].text.strip())
        winner_points = clean_team_name(cols[4].text.strip())
        loser = clean_team_name(cols[6].text.strip())
        loser_points = clean_team_name(cols[7].text.strip())
        #print(loser_points)

        #get rid of the school's rankings
        formatted_winner = re.sub(r'\(\d+\)', '', winner).strip()
        
        formatted_loser = re.sub(r'\(\d+\)', '', loser).strip()
        
        print(f'Winner: {formatted_winner} - Loser: {formatted_loser}')

        #used for checking if the teams are both fbs teams
        if formatted_winner not in fbs_teams:
            print(f"NO WINNER - {formatted_winner}")
            mismatched_names.add(winner)
            continue

        if formatted_loser not in fbs_teams:
            print(f"NO LOSER - {formatted_loser}")
            mismatched_names.add(loser)
            continue
        #handle missing or invalid data
        if not formatted_winner or not formatted_loser:
            continue

        data.append({
            'source': formatted_winner,
            'target': formatted_loser,
            'win': winner_points,
            'loss': loser_points
        })
    

    with open('mismatched_names.txt', 'w') as f:
        for name in sorted(mismatched_names):
            f.write(name + '\n')

    #convert to JSON
    gamejson_output = json.dumps(data, indent=4)
    return gamejson_output

#get the JSON output
json_results = scrape_cfb_results()
#print(json_results)
parsed_results = json.loads(json_results)
#print(json_results)



gml_path_file = 'football/football.gml'
G = nx.read_gml(gml_path_file)

#dictionaries for nodes and edges

node_dict = []
edge_dict = []
conference_dict = {
    "ACC": "Atlantic Coast",
    "Big East": "Big East",
    "Big Ten": "Big Ten",
    "Big 12": "Big Twelve",
    "CUSA": "Conference USA",
    "IND": "Independents",
    "MAC": "Mid-America",
    "MWC": "Mountain West",
    "PAC-10": "Pacific Ten",
    "SEC": "Southeastern",
    "SBC": "Sun Belt",
    "WAC": "Western Athletic"
}

#print(conference_dict["0"])
#extract the nodes
for node in node_data:
    team = node["id"]
    print(team)
    #record = get_team_record(node[0])
    #print(f"tam id: {node[0]}") --- PRINTS TEAM NAME
    record = get_team_record(team)

    
    #time.sleep(2)
    
    node_dict.append({
        "id": node["id"],
        #"label": node[1],
        #**node[1], #returns value; don't know if i need it
        "value": node["value"],
    
        "wins": record["wins"],
        "losses": record["losses"]

    })
    time.sleep(2)
    

    #print(conference_dict["5"])
    #print(node_dict)

#extract the edges
for scraped_edge in parsed_results:
    edge_dict.append({
        "source": scraped_edge['source'], #winning team
        "target": scraped_edge['target'], #losing team
        "win": scraped_edge['win'], #winning team points
        "loss": scraped_edge['loss'], #losing team points

  
        #**edge[2]
    })
    #print(scraped_edge["source"])
    #print(scraped_edge['target'])

#turn to json
output_json = {
    "nodes": node_dict,
    "edges": edge_dict
}



#print(output)

with open('2000seasonScrapedNodes.json', 'w') as json_file:
    json.dump(output_json, json_file, indent=4)


