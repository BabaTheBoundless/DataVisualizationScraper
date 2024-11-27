import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import networkx as nx
from scraper import get_team_record
import time



def conference_removal(name):
    name = re.sub(r"\(.*?\)", "", name).strip()
    return name


def scrape_nodes():
    url = "https://www.sports-reference.com/cfb/years/2000-standings.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #locate the schedule table
    table = soup.find('table', {'id': 'standings'})
    if not table:
        print("NO TABLE")
        return []
    
    
    #extract table rows
    
    rows = table.findAll('tr')[1:]
    if len(rows) == 0:
        print("Rows = 0")
    
    #print(rows)

    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            continue

        team = (cols[0].text.strip())
        conference = conference_removal((cols[1].text.strip()))
        print(conference)
        #print(team)
        #print(conference)
        data.append({
            'id': team,
            'value': conference
        })
    team_json_output = json.dumps(data, indent=4)
    #print(team_json_output)
    return data

myOutput_json = scrape_nodes()

with open('scrapeTeams.json', 'w') as json_file:
    json.dump(myOutput_json, json_file, indent=4)
        
        
        

    

    