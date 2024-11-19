import requests
from bs4 import BeautifulSoup
import json
import re

def get_team_record(team_name):
    
    team_name = re.sub(r'([a-z])([A-Z])', r'\1-\2', team_name).lower()
    team_name.lower()
    if team_name == "kent":
        team_name = "kent-state"
    elif team_name == "miami-florida":
        team_name = "miami-fl"
    elif team_name == "miami-ohio":
        team_name = "miami-oh"
    elif team_name == "texas-a&m":
        team_name = "texas-am"
    
    print(team_name)
    url = f"https://www.sports-reference.com/cfb/schools/{team_name}/2000-schedule.html"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {team_name}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')

  
    record = soup.findAll('p')
   
    for p in record:
        
        if "Record:" in p.text:
            record_text = p.text.split("Record:")[1].strip()
            print(record_text)
            match = re.match(r'(\d+)-(\d+)', record_text)
            wins = int(match.group(1))
            losses = int(match.group(2))
            return {
                'wins': wins,
                'losses': losses,
               
            }
            
print(get_team_record("Oklahoma"))

