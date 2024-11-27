import requests
from bs4 import BeautifulSoup
import json
import re

def get_team_record(team_name):
    
    #team_name = re.sub(r'([a-z])([A-Z])', r'\1-\2', team_name).lower()
    #team_name.lower()
    team_name = team_name.replace(" ", "-").replace("(", "").replace(")", "").lower()
    if team_name == "pitt":
        team_name = "pittsburgh"
    if team_name == "kent":
        team_name = "kent-state"
    elif team_name == "miami-florida":
        team_name = "miami-fl"
    elif team_name == "miami-ohio":
       team_name = "miami-oh"
    elif team_name == "texas-a&m":
        team_name = "texas-am"
    elif team_name == "uab":
        team_name = "alabama-birmingham"
    elif team_name == "ucf":
        team_name = "central-florida"
    elif team_name == "louisiana":
        team_name = "louisiana-lafayette"
    elif team_name == "usc":
        team_name = "southern-california"
    elif team_name == "lsu":
        team_name = "louisiana-state"
    elif team_name == "ole-miss":
        team_name = "mississippi"
    elif team_name == "tcu":
        team_name = "texas-christian"
    elif team_name == "bowling-green":
        team_name = "bowling-green-state"
    elif team_name == "utep":
         team_name = "texas-el-paso"
    elif team_name == "smu":
        team_name = "southern-methodist"
    elif team_name == "byu":
        team_name = "brigham-young"

    
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
            
#print(get_team_record("Oklahoma"))

