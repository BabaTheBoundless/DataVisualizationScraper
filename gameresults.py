import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

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
        winner = cols[3].text.strip()
        winner_points = cols[4].text.strip()
        loser = cols[6].text.strip()
        loser_points = cols[7].text.strip()
        #print(loser_points)

        #get rid of the school's rankings
        formatted_winner = re.sub(r'\(\d+\)', '', winner).strip()
        formatted_loser = re.sub(r'\(\d+\)', '', loser).strip()
        #print(formatted_loser)

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
print(json_results)

