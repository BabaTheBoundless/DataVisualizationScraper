import time
import networkx as nx
from scraper import get_team_record
import json

#import and read gml file
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
    time.sleep(2)
    node_dict.append({
        
        "id": node[0],
        #"label": node[1],
        #**node[1], #returns value; don't know if i need it
        "value": conference_dict[str(node[1].get("value"))],
        "wins": record["wins"],
        "losses": record["losses"]

    })
    time.sleep(1)
    

    print(conference_dict["5"])
    #print(node_dict)

#extract the edges
for edge in G.edges(data=True):
    edge_dict.append({
        "source": edge[0],
        "target": edge[1],
        #**edge[2]
    })

#turn to json
output_json = {
    "nodes": node_dict,
    #"edges": edge_dict
}

output = json.dumps(output_json, indent=4)

#print(output)

with open('bargraphdata.json', 'w') as json_file:
    json.dump(output_json, json_file, indent=4)