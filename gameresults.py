import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import networkx as nx
from scraper import get_team_record
import time

def clean_team_name(team_name):
    team_name = re.sub(f'-', '', team_name) #hyphen
    team_name = re.sub(r'\s+', '', team_name) #whitespace
    team_name = re.sub(r'\(\d+\)', '', team_name).strip() #strip ranking
    if team_name == "Miami(FL)":
        team_name = "MiamiFlorida"
    elif team_name == "Miami(OH)":
        team_name = "MiamiOhio"
    elif team_name == "KentState":
        team_name = "Kent"
    elif team_name == "Texas-El Paso":
        team_name = "TexasElPaso"
    elif team_name == "Louisiana": 
        team_name = "LouisianaLafayette"
    elif team_name == "BowlingGreen":
        team_name = "BowlingGreenState"
    
    

    return team_name

with open('2000seasonWithWins', 'r') as myjson:
    football_data = json.load(myjson)

fbs_teams = {node["id"] for node in football_data["nodes"]}
print(fbs_teams)


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
        print(cols[6].text.strip())
        loser_points = clean_team_name(cols[7].text.strip())
        #print(loser_points)

        #get rid of the school's rankings
        formatted_winner = re.sub(r'\(\d+\)', '', winner).strip()
        formatted_loser = re.sub(r'\(\d+\)', '', loser).strip()
        print(formatted_loser)
        #print(formatted_winner)
        #print(formatted_loser)

        #used for checking if the teams are both fbs teams
        if formatted_winner not in fbs_teams or formatted_loser not in fbs_teams:
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
    "0": "Atlantic Coast",
    "1": "Big East",
    "2": "Big Ten",
    "3": "Big Twelve",
    "4": "Conference USA",
    "5": "Independents",
    "6": "Mid-America",
    "7": "Mountain West",
    "8": "Pacific Ten",
    "9": "Southeastern",
    "10": "Sun Belt",
    "11": "Western Athletic"
}

#print(conference_dict["0"])
#extract the nodes
for node in G.nodes(data=True):
    
    #record = get_team_record(node[0])
    #print(f"tam id: {node[0]}") --- PRINTS TEAM NAME
    record = get_team_record(node[0])
    #time.sleep(2)
    node_dict.append({
        "id": node[0],
        #"label": node[1],
        #**node[1], #returns value; don't know if i need it
        "value": conference_dict[str(node[1].get("value"))],
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

with open('2000seasonWithWins', 'w') as json_file:
    json.dump(output_json, json_file, indent=4)


