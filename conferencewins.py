import time
import networkx as nx
from scraper import get_team_record
import json

#import and read gml file
gml_path_file = 'football/football.gml'
G = nx.read_gml(gml_path_file)

#dictionaries for nodes and edges




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

node_dict = []
edge_dict = []

wins_dict = {
    "Atlantic Coast": 0,
    "Big East": 0,
    "Big Ten": 0,
    "Big Twelve": 0,
    "Conference USA": 0,
    "Independents": 0,
    "Mid-America": 0,
    "Mountain West": 0,
    "Pacific Ten": 0,
    "Southeastern": 0,
    "Sun Belt": 0,
    "Western Athletic": 0
}

team_dict = {
    "Atlantic Coast": 0,
    "Big East": 0,
    "Big Ten": 0,
    "Big Twelve": 0,
    "Conference USA": 0,
    "Independents": 0,
    "Mid-America": 0,
    "Mountain West": 0,
    "Pacific Ten": 0,
    "Southeastern": 0,
    "Sun Belt": 0,
    "Western Athletic": 0
}



for node in G.nodes(data=True):
    time.sleep(2)
    #print(f"tam id: {node[0]}") --- PRINTS TEAM NAME
    record = get_team_record(node[0])
    
    conference_number = str(node[1].get("value"))
    #print(f"hhhhhhh{conference_number}")
    #print(f"node 1{node[1]}")
    conference_name = conference_dict[conference_number]
    #print(f"wins:{record["wins"]}")
    #print(record["wins"])
    #wins = record["wins"]

    if conference_name:
        team_dict[conference_name] += 1

        print(f"This is the conference name: {conference_name}")
        print(f"TEAM DICTIONARY: {team_dict[conference_name]}")
        print(team_dict)
    else:
        print("NOT ADDED UH OH")
    
 
with open('conference_teams.json', 'w') as json_file:
    json.dump(team_dict, json_file, indent=4)

print("Conference wins have been saved to conference_wins.json.")