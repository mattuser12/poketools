import requests
from bs4 import BeautifulSoup
import time
import threading
from datetime import datetime

# URL of the website to check

"""
vstar_universe = "https://www.pokemoncenter-online.com/?p_cd=4521329331188"
paradigm_trigger = "https://www.pokemoncenter-online.com/?p_cd=4521329331119"
triplet_beat = "https://www.pokemoncenter-online.com/?p_cd=4521329331270"
eevee_heroes = "https://www.pokemoncenter-online.com/?p_cd=4521329314143"
violet = "https://www.pokemoncenter-online.com/?p_cd=4521329331263"
scarlet = "https://www.pokemoncenter-online.com/?p_cd=4521329331256"
incandescent_arcana = "https://www.pokemoncenter-online.com/?p_cd=4521329331096"
clay_burst = "https://www.pokemoncenter-online.com/?p_cd=4521329331294"
snow_hazard = "https://www.pokemoncenter-online.com/?p_cd=4521329331287"


set_url = [vstar_universe, paradigm_trigger, triplet_beat, eevee_heroes, violet, scarlet, incandescent_arcana, clay_burst, snow_hazard]
set_name = ["VSTAR Universe", "Paradigm Trigger", "Triplet Beat", "Eevee Heroes", "Violet", "Scarlet", "Incandescent Arcana", "Clay Burst", "Snow Hazard"]

sets = {}

for set in range(len(set_url)):
    sets[set_name[set]] = set_url[set]
    
"""
val = "https://www.reddit.com/r/ValorantCompetitive/"
tok = "https://www.reddit.com/r/Tokyo/"
pic = "https://www.reddit.com/r/pics/"

sets = {
    "Valorant": val,
    "Tokyo": tok,
    "Pics": pic
}


check_interval = 1

previous_button_text = ""

prev_content = {}


def check_url(url, dicti):
    response = requests.get(url)
    
    content = response.content
    
    if content != dicti[url]:
        key = [k for k, v in dict.items() if v == url]
        if key:
            
            #now = datetime.now()
            #current_time = now.strftime("%H:%M:%S")
            print("Contents have changed for link:", key[0])
            dicti[url] = content
        else:
            print("Error: URL not found in dictionary")
    else:
        print("Contents have not changed for link:", [k for k,v in dict.items() if v == url][0])



# define a function that checks all of the urls in parallel
def check_urls(links, link_contents):
    threads = []
    for name, url in links.items():
        t = threading.Thread(target=check_url, args=(url, link_contents))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# initialize the dictionary of link contents
link_contents = {}
for name, url in sets.items():
    response = requests.get(url)
    content = response.content
    link_contents[url] = content

# continuously check the links for changes
while True:
    check_urls(sets, link_contents)
    time.sleep(60)  # wait for 60 seconds before checking again