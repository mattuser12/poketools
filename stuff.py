import requests
from bs4 import BeautifulSoup
import time
import threading
from datetime import datetime

# URL of the website to check


vstar_universe = "https://www.pokemoncenter-online.com/?p_cd=4521329331188"
paradigm_trigger = "https://www.pokemoncenter-online.com/?p_cd=4521329331119"
triplet_beat = "https://www.pokemoncenter-online.com/?p_cd=4521329331270"
eevee_heroes = "https://www.pokemoncenter-online.com/?p_cd=4521329314143"
violet = "https://www.pokemoncenter-online.com/?p_cd=4521329331263"
scarlet = "https://www.pokemoncenter-online.com/?p_cd=4521329331256"
incandescent_arcana = "https://www.pokemoncenter-online.com/?p_cd=4521329331096"
clay_burst = "https://www.pokemoncenter-online.com/?p_cd=4521329331294"
snow_hazard = "https://www.pokemoncenter-online.com/?p_cd=4521329331287"
ditto = "https://www.pokemoncenter-online.com/?p_cd=4550213096391"

set_url = [vstar_universe, paradigm_trigger, triplet_beat, eevee_heroes, violet, scarlet, incandescent_arcana, clay_burst, snow_hazard, ditto]
set_name = ["VSTAR Universe", "Paradigm Trigger", "Triplet Beat", "Eevee Heroes", "Violet", "Scarlet", "Incandescent Arcana", "Clay Burst", "Snow Hazard", "Ditto"]

sets = {}

for set in range(len(set_url)):
    sets[set_name[set]] = set_url[set]


"""
val = "https://www.reddit.com/r/ValorantCompetitive/"
tok = "https://www.reddit.com/r/Tokyo/"
pic = "https://www.reddit.com/r/pics/"
jap = "https://www.reddit.com/r/movingtojapan"
die = "https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/foodsearch.aspx"
exa = "http://example.com/"

sets = {
    "Valorant": val,
    "Tokyo": tok,
    "Pics": pic,
    "Moving to Japan": jap,
    "Diet": die,
    "Example": exa
}
"""

check_interval = 1
previous_button_text = ""
prev_content = {}

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0 Chrome/112.0.5615',
    'From': 'hello123@gmail.com'
})

def check_url(name, url):
    global prev_content
    
    while True:
        response = requests.get(url, headers=headers) 
        # Gets website data for singular URL
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Gets button from page
        add_cart_button = soup.find("img", class_ = "add_cart_btn")
        
        current_button_text = add_cart_button.text.strip() if add_cart_button else ""
        
        if url in prev_content and add_cart_button is not None:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f"Content has changed for set {name} ({current_time})")
            
        prev_content[url] = content
        
        time.sleep(1)

"""    
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
"""


# define a function that checks all of the urls in parallel
def check_urls(links):
    threads = []
    for name, url in links.items():
        t = threading.Thread(target=check_url, args=(name, url))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

"""
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
"""

check_urls(sets)